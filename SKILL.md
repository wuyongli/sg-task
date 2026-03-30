---
name: sg-task
description: 任务中心的 AI 多仓库上下文管理技能。用于需求任务、工作空间、开发计划、任务进度、产品文档、接口文档、多仓库联动以及新会话恢复上下文等场景。特别适用于一个需求对应多个仓库分支，需要 AI 通过当前仓库和分支快速识别当前任务、读取关键文档区块并持续推进工作的情况。
---

# sg-task

将一个需求固定成一个任务工作空间，让 AI 在多仓库开发中稳定识别“当前任务是什么、涉及哪些仓库和分支、现在应该继续做什么”。

## 核心模型

- 一个需求就是一个任务
- 一个任务可以关联多个仓库
- 每个关联仓库必须同时绑定一个具体分支
- 任务是主实体，分支只是反查任务的索引
- 一个仓库分支最多命中一个任务；命中多个任务时视为异常数据

## 设计原则

- 任务优先：先创建任务，再绑定仓库与分支
- 低摩擦：默认只维护最小文档集
- 源文档唯一：业务正文只写在源文档，不在 `meta.md` 重复保存
- 选择性加载：`show --load` 用于恢复工作态，不默认加载整份文档
- Git 从属：Git 是文档留痕和备份策略，不是主流程
- 仓库命名前置：仓库显示名只在全局配置阶段维护，建任务时直接复用

## 最小文档集

- `meta.md`：任务主档，必须有
- `product.md`：需求、范围、验收标准，建议有
- `development.md`：开发进度、阻塞、测试记录，必须有
- `api.md`：按需创建，仅在接口联调明显时使用

不要默认维护：

- `test.md`
- `meeting.md`
- 任务级 `README.md`

模板位于：

- [references/meta.md](references/meta.md)
- [references/product.md](references/product.md)
- [references/development.md](references/development.md)
- [references/api.md](references/api.md)

## 关键文件

### 全局配置

读取：

```text
~/.claude/sg-task/config.yaml
```

示例见：

- [references/config.yaml.example](references/config.yaml.example)

配置里的仓库字段职责：

- `name`：业务显示名，例如“批发后端”
- `key`：稳定标识，通常等于目录名，例如 `pf-backend`
- `type`：仓库类型
- `path`：仓库真实路径，通常使用用户机器上的绝对路径

路径规则：

- skill 仓库内部文档引用使用相对路径
- `repositories[].path` 属于运行时仓库配置，不属于 skill 包内部引用
- `repositories[].path` 通常使用绝对路径，指向用户机器上的真实仓库位置

仓库命名时机只有两种：

1. 第一次使用技能，初始化全局仓库配置时
2. 使用 `/sg-task add-repo-config` 给整个项目新增全局仓库时

后续创建任务时：

- 直接读取已配置仓库
- 不再重复询问仓库名称
- 只需要选择这个任务涉及哪些仓库

### 任务主档 `meta.md`

`meta.md` 是任务唯一入口，负责：

- 记录任务基础信息
- 记录仓库与分支映射
- 记录文档文件名
- 可选记录新线程恢复上下文时默认加载的短事实
- 可选记录按需深读时使用的关键区块引用

要求：

- `repositories[]` 中一旦挂上仓库，就必须带上 `branch`
- 如果仓库处于 detached HEAD，不能直接绑定到任务
- `always_load` 是可选字段，用于新线程恢复上下文，内容必须短且只包含已确认事实
- `context_refs` 是可选字段，只在需要按标题精确深读时使用
- `context_refs` 只保存稳定引用，不保存重复正文

完整模板见：

- [references/meta.md](references/meta.md)

## 命令工作流

### 主流程命令

- `/sg-task create <任务名称>`
- `/sg-task show`
- `/sg-task show --load`
- `/sg-task doc product`
- `/sg-task doc development`
- `/sg-task doc api`
- `/sg-task add-repo`
- `/sg-task remove-repo`
- `/sg-task progress`
- `/sg-task complete`

### 次级命令

- `/sg-task list`
- `/sg-task add-repo-config`
- `/sg-task sync`

命令语义：

- `/sg-task add-repo-config`：给整个项目新增全局仓库配置
- `/sg-task add-repo`：给当前任务补挂一个已经存在于全局配置中的仓库

详细命令规则见：

- [references/command-workflow.md](references/command-workflow.md)

## `show --load` 规则

`show --load` 的目标是用尽量低的上下文成本恢复任务定位，不是全文阅读。

默认顺序：

1. 先通过当前仓库和当前分支定位任务
2. 读取全局配置，确定 `project_root`
3. 只在 `<project_root>/.tasks` 下定位任务
4. 只读取命中的 `meta.md`
5. 默认只恢复：
   - 任务名称
   - 任务状态
   - 仓库与分支映射
   - 已存在的文档列表
   - `meta.md` 中已有的简短 `summary`（如果存在）
   - `meta.md` 中 `always_load` 里的短事实（如果存在）
6. 不默认读取 `product.md`、`development.md`、`api.md`
7. 只有用户明确要求“继续看需求 / 看进度 / 看阻塞 / 看下一步”时，才按需深读对应文档或区块

不要：

- 默认读取整份 `product.md`
- 默认读取整份 `development.md`
- 默认根据 `context_refs` 深读区块
- 为了定位任务去扫描整个用户目录
- 同时尝试多个历史 `.tasks` 目录
- 报告 `pwd`、`find`、`已浏览几个文件` 之类的中间过程
- 在 `always_load` 中塞入大段正文
- 在 `meta.md` 维护第二份摘要正文

详细加载规则见：

- [references/loading-strategy.md](references/loading-strategy.md)

## Git 备份策略

Git 是文档留痕与备份层，不是使用 sg-task 的主流程。

详细规则见：

- [references/git-sync.md](references/git-sync.md)

## 推荐输出格式

展示仓库时统一使用：

```text
业务名 (key, type)
```

例如：

- `批发后端 (pf-backend, backend)`
- `批发移动端 (senguo-pf-easy-mobile, mobile)`

## 异常处理

- 当前仓库分支没有绑定任务：提示当前分支未绑定任务
- 一个分支命中多个任务：提示数据异常并列出候选项
- 任务缺少关键文档区块：返回“未记录”或提示补全文档结构，不要自行发明缺失区块内容
- 推送失败：只提示已提交到本地，不中断任务流程
- 只有在定位失败时，才说明查找过程中的关键信息

## 最终目标

在任意相关仓库的新会话中执行：

```bash
/sg-task show --load
```

AI 应该能用尽量少的上下文，快速知道：

- 当前任务是什么
- 涉及哪些仓库和分支
- `meta.md` 中明确记录的任务目标和当前上下文
- 有哪些文档可继续深读
- 是否已经有简短任务摘要
