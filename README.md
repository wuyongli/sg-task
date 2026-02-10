# sg-task - 森果任务管理工具

一个帮助管理多仓库开发任务的 Claude Code Skill。

## 特性

- **任务即工作空间** - 每个任务文件夹包含该任务的所有文档
- **分支自动关联** - 通过当前 Git 分支自动定位任务
- **手动仓库命名** - 用户自定义仓库名称（如"批发后端"、"商户前端"），灵活直观
- **支持不同分支名** - 各仓库可以使用不同的分支名，自动检测并记录
- **动态仓库配置** - 首次使用时自动扫描并配置，支持中途添加/删除仓库
- **按需创建文档** - 需要什么文档就创建什么，不被不需要的文档干扰
- **仓库类型标注** - 明确标注前端/后端、PC/移动端/小程序/原生，快速定位
- **智能文档联动** - 自动检测文档差异并智能提示，无需手动同步

## 适用场景

适用于多仓库的开发项目，特别是：
- 前后端分离的项目
- PC端、移动端、小程序并行的项目
- 多个子系统的项目（如批发系统、商户中心等）
- 需要跨仓库追踪任务进度的场景
- 仓库数量和组合不固定的项目

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
# 创建任务（首次使用会自动初始化仓库配置）
/sg-task create 优化登录功能

# 显示当前任务
/sg-task show

# 列出所有任务
/sg-task list

# 添加仓库到当前任务
/sg-task add-repo

# 从当前任务删除仓库
/sg-task remove-repo

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
3. **分支驱动** - 通过 Git 分支自动关联任务，各仓库分支名可不同
4. **手动命名** - 用户手动输入仓库名称，灵活自定义（如"批发后端"、"商户前端"）
5. **动态配置** - 首次扫描自动配置到 `~/.claude/sg-task/config.yaml`
6. **类型清晰** - 明确标注仓库类型（backend/pc/mobile/mini-program/native/other）
7. **名称排序** - 所有仓库列表按名称排序展示
8. **上下文保持** - 新开窗口也能自动识别任务
9. **智能推断** - 通过对话自动更新进度，减少手动操作
10. **文档联动** - 自动检测文档差异并智能提示
11. **自动维护** - 自动检测新仓库和缺失仓库，保持配置更新

## 目录结构

```
sg-task/
├── SKILL.md           # Skill 主文件（必需）
├── README.md          # 本文件
└── references/        # 文档模板
    ├── config.yaml.example  # 配置文件示例
    ├── product.md     # 产品需求文档模板
    ├── development.md # 开发计划与进度模板
    ├── api.md         # 接口文档模板
    ├── test.md        # 测试用例模板
    ├── meeting.md     # 会议记录模板
    └── README.md      # 任务 README 模板
```

**配置文件位置：** `~/.claude/sg-task/config.yaml`（首次使用时自动创建）

## 进度自动更新

本 skill 支持通过对话内容智能推断并更新开发进度：

```bash
用户：登录接口写好了，测试也通过了

Claude：✅ 已自动更新 development.md
      - [x] 登录接口
      📝 已添加到更新日志：2024-01-28 登录接口开发完成
```

## 支持不同分支名

在实际开发中，不同仓库可能使用不同的分支命名规范。sg-task 会自动检测每个仓库的当前分支并记录：

```bash
# 用户在各仓库创建不同名称的分支
cd backend && git checkout -b feature/login-v2
cd ../mobile && git checkout -b feature/login
cd ../pc && git checkout -b feature/login-page

# 创建任务时，自动检测各仓库分支
用户：/sg-task create 优化登录

Claude：正在检测各仓库分支...
✅ 批发后端 (pf-backend): feature/login-v2
✅ 批发移动端 (senguo-pf-easy-mobile): feature/login
✅ 批发PC端 (senguo-pf-manage-frontend): feature/login-page

✅ 任务已创建，meta.md 记录了各仓库对应的分支
```

任务元数据示例：
```yaml
repositories:
  - name: 批发后端
    branch: feature/login-v2    # 后端分支名
  - name: 批发移动端
    branch: feature/login       # 移动端分支名
  - name: 批发PC端
    branch: feature/login-page  # PC端分支名
```

## 仓库配置

sg-task 使用配置文件来管理项目仓库信息：

**配置文件位置：** `~/.claude/sg-task/config.yaml`

**首次使用时自动创建**，扫描项目目录下的所有 Git 仓库并询问配置信息。

### 配置示例

```yaml
repositories:
  # 后端仓库
  - name: 批发后端              # 手动输入的名称
    type: backend
    path: /Users/wuyongli/Documents/sg-project/pf-backend

  # 移动端App
  - name: 批发移动端            # 手动输入的名称
    type: mobile
    path: /Users/wuyongli/Documents/sg-project/senguo-pf-easy-mobile

  # PC端前端
  - name: 批发PC端              # 手动输入的名称
    type: pc
    path: /Users/wuyongli/Documents/sg-project/senguo-pf-manage-frontend

  # 商户后端
  - name: 商户后端              # 手动输入的名称
    type: backend
    path: /Users/wuyongli/Documents/sg-project/senguo-merchantcenter-backend
```

**展示格式：** 在选择和显示仓库时，使用 `手动名称 (目录名, 类型)` 的格式，例如：
- `批发后端 (pf-backend, backend)`
- `批发移动端 (senguo-pf-easy-mobile, mobile)`
- `批发PC端 (senguo-pf-manage-frontend, pc)`

### 首次使用流程

```bash
用户：/sg-task create 优化登录

Claude：🔍 首次使用，正在初始化仓库配置...

扫描到以下 Git 仓库（共 3 个）：

1. ./pf-backend
2. ./senguo-pf-easy-mobile
3. ./senguo-pf-manage-frontend

现在需要为每个仓库配置名称和类型：

**1. ./pf-backend**
这个仓库叫什么名字？（输入名称，如"批发后端"）
> 批发后端

是什么类型？
> backend

**2. ./senguo-pf-easy-mobile**
这个仓库叫什么名字？
> 批发移动端

是什么类型？
> mobile

**3. ./senguo-pf-manage-frontend**
这个仓库叫什么名字？
> 批发PC端

是什么类型？
> pc

✅ 配置完成！已保存到 ~/.claude/sg-task/config.yaml

已配置的仓库（按名称排序）：
- 批发PC端（senguo-pf-manage-frontend，pc）
- 批发后端（pf-backend，backend）
- 批发移动端（senguo-pf-easy-mobile，mobile）
```

### 按名称排序选择仓库

创建任务时，仓库按名称排序显示，格式为：`手动名称 (目录名, 类型)`

**勾选交互方式：**
- 显示带序号的复选框列表
- 支持多种输入方式：序号、名称、混合输入
- 支持多选

```bash
用户：/sg-task create 优化登录

请勾选涉及仓库（可多选，输入序号或名称）：

- [ ] 1. 批发PC端（senguo-pf-manage-frontend，pc）
- [ ] 2. 批发后端（pf-backend，backend）
- [ ] 3. 批发移动端（senguo-pf-easy-mobile，mobile）
- [ ] 4. 商户后端（senguo-merchantcenter-backend，backend）

> 2, 3
或
> 后端、移动端
```

### 中途添加/删除仓库

任务开发过程中，可以动态添加或删除仓库：

```bash
# 添加仓库
用户：/sg-task add-repo

Claude：当前任务：2024-01-28_优化登录
当前涉及的仓库：
- 批发后端（pf-backend，backend）
- 批发移动端（senguo-pf-easy-mobile，mobile）

请勾选要添加的仓库（可多选）：
- [ ] 1. 批发PC端（senguo-pf-manage-frontend，pc）
- [ ] 2. 商户后端（senguo-merchantcenter-backend，backend）

> 1
或
> 批发PC端

✅ 已添加

# 删除仓库
用户：/sg-task remove-repo
✅ 已从任务中移除
```

---

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
