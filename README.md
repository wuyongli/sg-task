# sg-task

面向 AI 的多仓库任务上下文管理 skill。

这个仓库的目标不是做通用任务管理平台，而是把“一个需求”固定成一个任务工作空间，让 AI 在多仓库开发中稳定识别当前任务、按需加载关键文档区块，并围绕同一个任务持续推进工作。

## 解决的问题

- 一个需求会跨多个仓库，AI 容易丢失上下文
- 新开会话或切换仓库后，AI 不容易知道当前分支对应哪个任务
- 产品、开发、接口信息散落在不同文档里，缺少统一入口
- 任务文档需要 Git 留痕，但 Git 只是备份层，不应该压过主流程

## 核心模型

- 一个需求就是一个任务
- 一个任务可以关联多个仓库
- 每个关联仓库必须同时绑定一个具体分支
- 任务是主实体，分支是反查任务的索引
- 一个仓库分支最多命中一个任务

## 目录结构

```text
sg-task/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── sync_task_docs.py
├── references/
│   ├── meta.md
│   ├── product.md
│   ├── development.md
│   ├── api.md
│   ├── config.yaml.example
│   ├── command-workflow.md
│   ├── loading-strategy.md
│   └── git-sync.md
└── evals/
    └── evals.json
```

## 最小文档集

每个任务目录默认只维护：

- `meta.md`：任务主档，必须有
- `product.md`：需求、范围、验收标准，建议有
- `development.md`：开发进度、阻塞、测试记录，必须有
- `api.md`：按需创建

不再默认维护：

- `test.md`
- `meeting.md`
- 任务级 `README.md`

## 关键设计

### 1. 仓库命名前置

仓库显示名只在两种情况下维护：

1. 第一次使用 skill，初始化全局仓库配置时
2. 使用 `/sg-task add-repo-config` 新增全局仓库时

后续建任务时，直接读取全局配置中的 `name / key / type / path`，不再重复询问仓库名称。

### 2. `meta.md` 是任务主档

`meta.md` 负责：

- 任务基础信息
- 仓库与分支映射
- 文档文件名
- `show --load` 默认加载的短事实
- 按需深读时使用的链接或区块引用

### 3. `show --load` 做选择性加载

`show --load` 的目标是先恢复任务定位，不是全文阅读。

默认读取顺序：

1. 当前仓库路径和当前分支
2. 全局配置里的 `project_root`
3. `<project_root>/.tasks` 下命中的 `meta.md`

默认只返回：

- 任务名称
- 状态
- 仓库与分支映射
- 已存在的文档列表
- `meta.md` 中已有的简短 `summary`
- `meta.md` 中 `always_load` 记录的短事实

需要看需求、进度、阻塞时，再按需深读对应文档。
如果历史文档没有对应区块，应视为“未记录”，不能由 AI 自行补全或推断。

推荐做法：

- `summary` 只写一句任务概述
- `always_load` 只写 1 到 3 条有助于跨线程续做的已确认事实
- `always_load` 最好包含：一句目标、一句当前需求点、几条事实
- 其他文档继续通过链接或区块引用做导航，不默认展开
- 恢复成功时直接给任务快照，不要播报扫描过程

## 主要命令

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
- `/sg-task add-repo-config`
- `/sg-task sync`

详细规则见：

- [SKILL.md](SKILL.md)
- [references/command-workflow.md](references/command-workflow.md)
- [references/loading-strategy.md](references/loading-strategy.md)

## 配置示例

见：

- [references/config.yaml.example](references/config.yaml.example)

## Git 备份策略

Git 在这套 skill 中的定位是任务文档留痕和备份。

- `auto_commit: true` 不是后台定时器，而是在任务文档写入命令结束后立即尝试同步
- `auto_push: true` 时提交后尝试推送
- 推送失败时只提示“已提交到本地”
- `auto_commit: false` 时可通过 `/sg-task sync` 手动备份
- 同步范围只应包含 `.tasks`，不能顺手提交整个项目的其他改动

详细规则见：

- [references/git-sync.md](references/git-sync.md)

## 评测

评测定义位于：

- [evals/evals.json](evals/evals.json)

覆盖重点包括：

- 首次初始化仓库命名
- 创建任务并绑定仓库分支
- 当前分支反查任务
- `show --load` 的轻量加载与按需深读
- 手动备份模式
- 自动同步不是后台守护进程
