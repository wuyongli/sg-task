# sg-task - 森果任务管理工具

一个帮助管理多仓库开发任务的 Claude Code Skill。

## 特性

- **任务即工作空间** - 每个任务文件夹包含该任务的所有文档
- **分支自动关联** - 通过当前 Git 分支自动定位任务
- **按需创建文档** - 需要什么文档就创建什么，不被不需要的文档干扰
- **仓库类型标注** - 明确标注前端/后端、PC/移动端，快速定位

## 适用场景

适用于多仓库的开发项目，特别是：
- 前后端分离的项目
- PC端和移动端并行的项目
- 需要跨仓库追踪任务进度的场景

## 安装

### 方式 1：直接克隆

```bash
# 克隆仓库
git clone https://github.com/你的用户名/sg-task.git

# 复制到 Claude Code 的 skills 目录
cp -r sg-task ~/.claude/skills/
```

### 方式 2：手动下载

1. 下载此仓库的 zip 文件
2. 解压后复制 `sg-task` 目录到 `~/.claude/skills/`

## 使用

```bash
# 创建任务
/sg-task create 优化登录功能

# 显示当前任务
/sg-task show

# 列出所有任务
/sg-task list

# 查看任务进度
/sg-task progress

# 创建文档
/sg-task doc development
/sg-task doc api
/sg-task doc test

# 完成任务
/sg-task complete
```

更多用法请查看 [SKILL.md](SKILL.md)

## 核心设计

1. **极简起步** - 创建任务只生成 meta.md 和 README.md
2. **按需扩展** - 需要什么文档就创建什么
3. **分支驱动** - 通过 Git 分支自动关联任务
4. **类型清晰** - 明确标注仓库类型（前端/后端、PC/移动）
5. **上下文保持** - 新开窗口也能自动识别任务
6. **智能推断** - 通过对话自动更新进度，减少手动操作

## 目录结构

```
sg-task/
├── SKILL.md           # Skill 主文件（必需）
├── README.md          # 本文件
└── references/        # 文档模板
    ├── product.md     # 产品需求文档模板
    ├── development.md # 开发计划与进度模板
    ├── api.md         # 接口文档模板
    ├── test.md        # 测试用例模板
    ├── meeting.md     # 会议记录模板
    └── README.md      # 任务 README 模板
```

## 进度自动更新

本 skill 支持通过对话内容智能推断并更新开发进度：

```bash
用户：登录接口写好了，测试也通过了

Claude：✅ 已自动更新 development.md
      - [x] 登录接口
      📝 已添加到更新日志：2024-01-28 登录接口开发完成
```

## 示例项目结构

```
[项目根目录]/
├── backend/           # 后端仓库
├── mobile/            # 移动端前端仓库
├── pc/                # PC端前端仓库
├── .tasks/            # 任务文档目录
│   └── 2024-01-28_优化登录/
│       ├── meta.md    # 任务元数据（核心）
│       ├── README.md  # 任务概览
│       ├── product.md # 产品文档
│       ├── development.md # 开发计划与进度
│       └── api.md     # 接口文档
└── .claude/
    └── skills/
        └── sg-task/
            └── SKILL.md
```

## 开发者

森果团队

## 许可证

MIT
