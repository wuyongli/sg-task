---
name: sg-task
description: 森果任务管理工具。帮助管理多仓库开发任务，每个任务是一个独立的工作空间，包含该任务的所有文档。通过 Git 分支自动关联任务，无需手动指定。支持按需创建产品文档、开发计划、接口文档、测试用例等。支持自动 Git 备份，文档变更自动提交到远程仓库。
---

# 森果任务管理工具 (sg-task)

帮助管理森果批发系统的多仓库开发任务。每个任务是一个独立的工作空间，通过 Git 分支自动关联。

## 核心特性

- **任务即工作空间** - 每个任务文件夹包含该任务的所有文档
- **分支自动关联** - 通过当前 Git 分支自动定位任务
- **按需创建文档** - 需要什么文档就创建什么，不被不需要的文档干扰
- **极简起始** - 创建任务只生成 meta.md，其他文档按需创建
- **动态仓库配置** - 首次使用时自动扫描并配置，支持中途添加/删除仓库
- **仓库类型标注** - 明确标注前端/后端、PC/移动端/小程序/原生，快速定位
- **项目启动信息** - 配置各项目的启动命令和端口，方便查询

## 配置文件

**配置文件位置：** `~/.claude/sg-task/config.yaml`

### 配置文件格式

```yaml
repositories:
  - name: 批发后端              # 项目名称
    type: backend               # 类型
    path: /path/to/repo         # 路径
    start_command: cd ... && ... # 启动命令（可选）
    port: 8897                  # 端口（可选）

# Git 自动同步配置（可选）
auto_commit: true
auto_push: true
commit_message_style: emoji
```

### 仓库类型

- `backend` - 后端
- `pc` - PC端前端
- `mobile` - 移动端App
- `mini-program` - 小程序
- `native` - 原生应用
- `other` - 其他类型

## 可用命令

### 创建任务

```bash
/sg-task create <任务名称>
```

创建新任务，自动检测当前 Git 分支。可勾选涉及的仓库，不同仓库可以有不同分支名。

### 查看当前任务

```bash
/sg-task show
```

**通过当前分支自动查找任务并显示信息。**

**流程：**

1. 读取配置文件中的仓库列表（不扫描目录）
2. 批量获取所有仓库的当前分支
3. 在所有任务中查找匹配的分支
4. **如果检测到多个任务，显示列表让用户选择（单选）**
5. 显示选中的任务信息

**注意：**
- **批量获取分支**：使用一条命令获取所有仓库的分支，只需确认一次
  ```bash
  cd repo1 && git rev-parse --abbrev-ref HEAD 2>/dev/null && \
  cd repo2 && git rev-parse --abbrev-ref HEAD 2>/dev/null
  ```
- 使用 `git rev-parse --abbrev-ref HEAD`（兼容所有 git 版本）
- 不要显示"正在读取配置"、"获取分支"等技术细节

**示例（单个任务）：**
```bash
📋 当前任务：优化登录功能

📊 任务信息：
- 任务ID：2024-01-28_优化登录
- 状态：🔄 进行中

📦 涉及仓库：
🔧 批发后端 (pf-backend，backend)
   分支：feature/login-optimization
   路径：../pf-backend

📱 批发移动端 (senguo-pf-easy-mobile，mobile)
   分支：feature/login-optimization
   路径：../senguo-pf-easy-mobile

📄 已创建文档：
- meta.md（任务元数据）
- product.md（产品文档）
- api.md（接口文档）
```

**示例（多个任务 - 交互选择）：**
```bash
⚠️ 检测到多个任务：

[显示单选列表]
○ 优化登录功能 (2024-01-28_优化登录)
  匹配仓库: 批发后端(feature/login-1)

○ 添加购物车 (2024-01-27_添加购物车)
  匹配仓库: 批发移动端(feature/cart-2), 批发PC端(feature/cart-pc)

[用户选择：优化登录功能]

📋 当前任务：优化登录功能
[显示任务详细信息...]
```

### 列出所有任务

```bash
/sg-task list
```

显示所有任务的概览列表。

### 添加仓库到任务

```bash
/sg-task add-repo
```

向当前任务添加新的仓库，自动检测分支。

### 从任务删除仓库

```bash
/sg-task remove-repo
```

从当前任务中移除不需要的仓库。

### 添加仓库配置

```bash
/sg-task add-repo-config
```

向全局配置中添加新的仓库（供所有任务使用）。

### 查看项目启动信息

```bash
/sg-task list-start
```

显示所有项目的启动命令和端口信息。

### 创建文档

```bash
/sg-task doc <文档类型>
```

可用文档类型：
- `product` - 产品需求文档
- `development` - 开发计划与进度
- `api` - 接口文档
- `test` - 测试用例
- `meeting` - 会议记录

### 查看任务进度

```bash
/sg-task progress
```

**通过读取 development.md 计算任务完成百分比。**

**流程：**

1. 通过当前分支定位任务
2. 读取 `development.md` 文件
3. 统计各模块的完成情况
4. 计算整体进度百分比

**示例：**
```bash
📊 任务进度：优化登录功能

## 整体进度：████████░░ 80%

### 🔧 后端开发：██████████ 100%
- [x] 登录接口
- [x] 注册接口
- [x] JWT token 生成

### 📱 移动端开发：██████░░░░ 60%
- [x] 登录页面 UI
- [x] 注册页面 UI
- [ ] 表单验证
- [ ] 记住密码交互

### 🧪 测试：███░░░░░░░ 30%
- [x] 登录功能测试
- [ ] 注册功能测试
- [ ] 异常场景测试

---
📝 统计：
- 总任务：12 个
- 已完成：7 个
- 进行中：0 个
- 未开始：5 个
```

**进度计算逻辑：**
```python
def calculate_progress(section):
    tasks = re.findall(r'- \[([ x])\]', section)
    if not tasks:
        return 0, 0, 0
    completed = tasks.count('x')
    total = len(tasks)
    percentage = (completed / total) * 100 if total > 0 else 0
    return completed, total, percentage

def generate_progress_bar(percentage):
    filled = int(percentage / 10)
    bar = '█' * filled + '░' * (10 - filled)
    return f"{bar} {percentage:.0f}%"
```

### 标记任务完成

```bash
/sg-task complete
```

标记任务为完成状态，生成交付总结。

### 文档自动同步

```bash
/sg-task sync
```

立即同步任务文档到 Git 仓库。

### 查看待提交变更

```bash
/sg-task status
```

查看当前未提交的文档变更。

## Git 自动同步

任务文档支持自动 Git 备份，确保数据永不丢失。

### 配置选项

```yaml
auto_commit: smart          # 提交模式：true/false/smart
auto_push: true             # 是否自动推送
commit_message_style: emoji # 提交信息风格

smart_commit:
  debounce_minutes: 5       # 防抖时间
  immediate_on:
    - task_completed        # 立即提交的场景
    - repository_changed
    - task_created
  max_idle_minutes: 30      # 兜底提交时间
```

### 提交模式说明

- **true** - 每次修改都立即提交
- **false** - 完全手动，使用 `/sg-task sync`
- **smart**（推荐）- 智能组合：
  - 重要操作立即提交（完成任务、添加仓库）
  - 普通编辑防抖合并（5分钟内的修改合并为一次）
  - 超时兜底保护（30分钟未修改自动提交）

### 提交信息风格

- **emoji** - 使用表情符号前缀（推荐）
- **simple** - 简洁文本
- **detail** - 详细变更信息

### 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| 不是 Git 仓库 | 静默跳过，不影响正常功能 |
| 未配置远程仓库 | 仅提交本地，不推送 |
| 推送失败 | 提示错误信息，但不中断任务 |
| 网络不可达 | 仅提交本地，稍后可手动推送 |

### 手动控制

**配置文件切换模式**：
```yaml
# ~/.claude/sg-task/config.yaml

# 完全手动
auto_commit: false
auto_push: false

# 每次修改都立即提交（可能很频繁）
auto_commit: true
auto_push: true

# 智能模式（推荐）⭐
auto_commit: smart
auto_push: true
```

**手动立即同步（适用于 smart 模式）**：
```bash
/sg-task sync

🚀 正在立即同步到 Git...
✅ 已提交 3 个文件更改
✅ 已推送到远程仓库
```

**查看待提交的变更**：
```bash
/sg-task status

📋 当前状态：
📝 待提交的变更：
- M 2026-02-10_对接支付宝转账产品/development.md
- M 2026-02-10_对接支付宝转账产品/product.md

💡 下一次自动提交将在 3 分钟后
    或执行 /sg-task sync 立即提交
```

## 智能特性

### 自动识别仓库类型

根据用户操作自动定位到正确的仓库：

```bash
用户：调整移动端登录页面样式

Claude：📱 正在处理移动端样式调整...
定位到仓库：批发移动端 (senguo-pf-easy-mobile，mobile)
```

### 智能文档建议

根据任务涉及仓库类型给出建议：

```bash
用户：/sg-task create 优化登录

Claude：💡 检测到涉及前后端，建议创建：
   - api.md（接口文档）- 前后端联调必备
```

### 跨窗口自动关联

即使新开对话窗口，也能通过分支信息自动关联到任务：

```bash
# 在任何仓库目录下打开新窗口
用户：这个任务的接口是什么

Claude：通过当前分支 feature/login-optimization 找到任务「优化登录功能」
[显示接口文档]
```

### 自动更新进度

通过对话内容智能推断并更新开发进度：

```bash
# 用户提到完成某项工作
用户：登录接口开发完成了，测试也通过了

Claude：✅ 已自动更新 development.md
      在「后端开发-接口开发」中找到相关任务
      - [x] 登录接口

      📝 已添加到更新日志：
      ### 2024-01-28
      - ✅ 登录接口开发完成（已通过测试）
```

**自动更新逻辑：**
1. 检测用户提到完成某项工作
2. 在 `development.md` 中查找对应任务
3. 将 `- [ ]` 改为 `- [x]`
4. 在更新日志中添加记录
5. 提供友好确认消息

### 文档智能联动

自动检测产品文档与开发计划的差异，智能提示更新

## 图标规范

- 🔄 进行中
- ✅ 已完成
- ⏸️ 暂停
- 🔧 后端
- 💻 PC端前端
- 📱 移动端前端
- 📦 小程序
- 🏗️ 原生应用
- 📄 文档

## 核心设计原则

1. **极简起步** - 创建任务只生成 meta.md，其他文档按需创建
2. **按需扩展** - 需要什么文档就创建什么
3. **分支驱动** - 通过 Git 分支自动关联任务，各仓库分支名可不同
4. **一次配置** - 首次使用扫描配置，后续不再扫描
5. **类型清晰** - 明确标注仓库类型（backend/pc/mobile/mini-program/native/other）
6. **上下文保持** - 新开窗口也能自动识别任务
7. **智能推断** - 通过对话自动更新进度，减少手动操作
8. **快速响应** - 不重复扫描，批量获取 Git 分支，命令执行速度快
9. **智能备份** - 防抖合并 + 重要立即提交 + 超时兜底，确保数据安全
