---
name: sg-task
description: 森果任务管理工具。帮助管理多仓库开发任务，每个任务是一个独立的工作空间，包含该任务的所有文档。通过 Git 分支自动关联任务，无需手动指定。支持按需创建产品文档、开发计划、接口文档、测试用例等。
---

# 森果任务管理工具 (sg-task)

帮助管理森果批发系统的多仓库开发任务。每个任务是一个独立的工作空间，通过 Git 分支自动关联。

## 核心特性

- **任务即工作空间** - 每个任务文件夹包含该任务的所有文档
- **分支自动关联** - 通过当前 Git 分支自动定位任务
- **按需创建文档** - 需要什么文档就创建什么，不被不需要的文档干扰
- **仓库类型标注** - 明确标注前端/后端、PC/移动端，快速定位

## 目录结构

```
[项目根目录]/
├── pf-backend/                        # 后端仓库
├── senguo-pf-easy-mobile/            # 移动端前端仓库
├── senguo-pf-manage-frontend/        # PC端前端仓库
├── .tasks/                            # 任务文档目录
│   ├── 2024-01-28_优化登录/
│   │   ├── meta.md                    # 任务元数据（核心）
│   │   ├── README.md                  # 任务概览
│   │   ├── product.md                 # 产品文档（可选）
│   │   ├── development.md             # 开发计划与进度（可选）
│   │   ├── api.md                     # 接口文档（可选）
│   │   ├── test.md                    # 测试用例（可选）
│   │   └── meeting.md                 # 会议记录（可选）
│   └── 2024-01-27_添加购物车/
│       └── ...
└── .claude/
    └── skills/
        └── sg-task/
            └── SKILL.md
```

## 任务元数据格式 (meta.md)

meta.md 是核心文件，建立任务与分支、仓库的关联。

```yaml
---
task_id: 2024-01-28_优化登录
task_name: 优化登录功能
description: 提升登录体验，增加记住密码功能
status: in_progress
created_at: 2024-01-28

repositories:
  - name: pf-backend
    type: backend
    branch: feature/login-optimization
    path: ../pf-backend

  - name: senguo-pf-easy-mobile
    type: frontend
    platform: mobile
    branch: feature/login-optimization
    path: ../senguo-pf-easy-mobile
---
```

### 仓库类型标注

- **后端仓库**: `type: backend`
- **前端仓库**: `type: frontend` + `platform: pc` 或 `platform: mobile`

示例：
```yaml
# 后端
type: backend

# PC端前端
type: frontend
platform: pc

# 移动端前端
type: frontend
platform: mobile
```

## 可用命令

### 创建任务

```bash
/sg-task create <任务名称>
```

**流程：**

1. 检测当前 Git 分支
2. 询问任务涉及的仓库
3. 收集任务信息（名称、描述等）
4. 创建任务目录：`.tasks/YYYY-MM-DD_任务名称/`
5. 生成 `meta.md`（自动填充分支和仓库信息）
6. 生成 `README.md`（任务概览）
7. 根据仓库类型给出智能建议

**示例：**
```bash
用户：/sg-task create 优化登录功能

Claude：正在创建任务...

✅ 当前分支：feature/login-optimization

请选择涉及仓库：
- [ ] pf-backend（后端）
- [ ] senguo-pf-easy-mobile（移动端前端）
- [ ] senguo-pf-manage-frontend（PC端前端）

[用户选择后]

✅ 已创建任务：2024-01-28_优化登录
   - meta.md（任务元数据）
   - README.md（任务概览）

💡 提示：检测到涉及前后端，建议创建接口文档用于联调
   使用 /sg-task doc api 创建
```

---

### 显示当前任务

```bash
/sg-task show
```

**通过当前分支自动查找任务并显示信息。**

**流程：**

1. 获取当前 Git 分支
2. 在 `.tasks` 中搜索包含该分支的 `meta.md`
3. 显示任务信息

**示例：**
```bash
用户：/sg-task show

Claude：📋 当前任务：优化登录功能

📊 任务信息：
- 任务ID：2024-01-28_优化登录
- 状态：🔄 进行中
- 创建时间：2024-01-28

📦 涉及仓库：
🔧 pf-backend（后端）
   分支：feature/login-optimization
   路径：../pf-backend

📱 senguo-pf-easy-mobile（移动端前端）
   分支：feature/login-optimization
   路径：../senguo-pf-easy-mobile

📄 已创建文档：
- meta.md（任务元数据）
- README.md（任务概览）
- product.md（产品文档）
- api.md（接口文档）

💡 可用命令：
- /sg-task progress - 查看任务进度（需要先创建 development.md）
- /sg-task doc development - 创建开发计划与进度
- /sg-task doc test - 创建测试用例
- /sg-task doc api - 创建接口文档
```

**查找逻辑：**
```python
def find_current_task():
    current_branch = git_branch_show_current()
    for task_dir in glob(".tasks/*/"):
        meta = read_yaml(f"{task_dir}/meta.md")
        for repo in meta['repositories']:
            if repo['branch'] == current_branch:
                return task_dir, meta
    return None, None
```

---

### 列出所有任务

```bash
/sg-task list
```

**示例：**
```bash
用户：/sg-task list

Claude：📋 任务列表

🔄 2024-01-28_优化登录
   分支：feature/login-optimization
   仓库：pf-backend, senguo-pf-easy-mobile

✅ 2024-01-27_添加购物车
   分支：feature/add-cart
   仓库：pf-backend, senguo-pf-easy-mobile

⏸️ 2024-01-26_修复订单bug
   分支：fix/order-bug
   仓库：pf-backend
```

---

### 创建文档

```bash
/sg-task doc <文档类型>
```

**按需创建文档，初始任务只包含 meta.md 和 README.md。**

**可用文档类型：**

| 类型 | 文件名 | 用途 |
|------|--------|------|
| `product` | product.md | 产品需求文档 |
| `development` | development.md | 开发计划与进度（合并） |
| `api` | api.md | 接口文档 |
| `test` | test.md | 测试用例 |
| `meeting` | meeting.md | 会议记录 |

**示例：**
```bash
用户：/sg-task doc api

Claude：正在生成接口文档...
✅ 已创建：api.md

用户：/sg-task doc development test

Claude：正在生成文档...
✅ 已创建：development.md
✅ 已创建：test.md
```

**智能建议：**
```bash
用户：/sg-task doc test

Claude：正在生成测试文档...
✅ 已创建：test.md

💡 提示：检测到该任务涉及前后端，建议也创建：
   - api.md（接口文档）- 前后端联调必备
   要一起创建吗？(y/n)
```

---

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
用户：/sg-task progress

Claude：📊 任务进度：优化登录功能

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

---

### 标记任务完成

```bash
/sg-task complete
```

**流程：**

1. 通过当前分支定位任务
2. 更新 `meta.md` 状态为 `completed`
3. 生成交付总结

**示例：**
```bash
用户：/sg-task complete

Claude：✅ 任务完成！

📦 完成内容：
- [查看产品文档](.tasks/2024-01-28_优化登录/product.md)
- [查看开发计划与进度](.tasks/2024-01-28_优化登录/development.md)
- [查看接口文档](.tasks/2024-01-28_优化登录/api.md)

🔗 待提交分支：
- pf-backend: feature/login-optimization
- senguo-pf-easy-mobile: feature/login-optimization
```

---

## 文档模板

### 产品文档模板 (product.md)

```markdown
# 产品需求文档

## 需求背景


## 功能描述


## 用户故事


## 验收标准


## UI/UX 说明


## 附件
- 原型图：
- 设计稿：
```

---

### 开发计划与进度模板 (development.md)

```markdown
# 开发计划与进度

## 📊 整体进度：🔄 进行中 | ✅ 已完成 | ⏸️ 暂停

---

## 🔧 后端开发

### 接口开发
- [ ] 任务 1
- [ ] 任务 2

### 数据库
- [ ] 任务 1

---

## 📱 移动端开发

### 页面开发
- [ ] 任务 1

### 状态管理
- [ ] 任务 1

---

## 💻 PC端开发

### 页面开发
- [ ] 任务 1

---

## 🧪 测试

- [ ] 功能测试
- [ ] 边界测试

---

## 📝 更新日志

### {{date}}
- ✅ 完成的任务
- 🔄 正在进行的任务

---

## 🚧 阻塞问题


---

## 📅 下一步计划
```

**说明：**
- 使用 `- [ ]` 表示未完成的任务
- 使用 `- [x]` 表示已完成的任务
- 在更新日志中记录重要的进度节点

---

### 接口文档模板 (api.md)

```markdown
# 接口文档

## 后端接口

### 1. <接口名称>
**接口路径：**
**请求方式：**
**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
|        |      |      |      |

**返回参数：**
| 参数名 | 类型 | 说明 |
|--------|------|------|
|        |      |      |

**示例：**
\`\`\`json

\`\`\`

---

## 前端接口

### 1. <组件/页面名称>
**组件路径：**
**Props：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
|        |      |      |      |

**Events：**
\`\`\`typescript

\`\`\`
```

---

### 测试用例模板 (test.md)

```markdown
# 测试用例

## 功能测试

### 用例 1：<用例名称>
**前置条件：**
**测试步骤：**
1.
2.

**预期结果：**


### 用例 2：
**前置条件：**
**测试步骤：**
1.

**预期结果：**


## 边界测试


## 异常测试


## 性能测试
```

---

### 会议记录模板 (meeting.md)

```markdown
# 会议记录

## 会议信息
- **时间：**
- **参与人：**
- **主题：**

## 讨论内容


## 决策事项


## 待办事项
- [ ]
- [ ]


## 下次会议
```

---

## README.md 自动生成格式

```markdown
# <任务名称>

## 📊 任务概览
- **任务ID：** YYYY-MM-DD_<任务名称>
- **状态：** 🔄 进行中 | ✅ 已完成 | ⏸️ 暂停
- **创建时间：** YYYY-MM-DD

## 📦 涉及仓库

### 🔧 后端
- **pf-backend** (`<分支名>`)
  - 路径：`../pf-backend`

### 📱 移动端
- **senguo-pf-easy-mobile** (`<分支名>`)
  - 路径：`../senguo-pf-easy-mobile`

### 💻 PC端
- **senguo-pf-manage-frontend** (`<分支名>`)
  - 路径：`../senguo-pf-manage-frontend`

## 📄 文档列表
- [产品文档](product.md)
- [开发计划与进度](development.md)
- [接口文档](api.md)
- [测试用例](test.md)

## 🔗 快速链接
- [切换到移动端目录](../senguo-pf-easy-mobile)
- [切换到PC端目录](../senguo-pf-manage-frontend)
- [切换到后端目录](../pf-backend)
```

---

## 工作流程示例

### 1. 开始新任务

```bash
# 1. 用户在各仓库中手动创建分支
cd pf-backend && git checkout -b feature/login-optimization
cd ../senguo-pf-easy-mobile && git checkout -b feature/login-optimization

# 2. 创建任务
用户：/sg-task create 优化登录功能

# 3. skill 自动检测分支并创建任务
Claude：✅ 已创建任务：2024-01-28_优化登录
```

### 2. 按需创建文档

```bash
用户：/sg-task doc product
用户：/sg-task doc api
```

### 3. 开发中自动关联

```bash
# 新开窗口，自动识别任务
用户：查看接口文档

Claude：📋 找到任务「优化登录功能」（通过分支 feature/login-optimization）
[显示 api.md 内容]
```

### 4. 自动更新进度（智能推断）

```bash
# 用户在对话中提到完成某事
用户：登录接口写好了，测试也通过了

Claude：✅ 已自动更新 development.md
      - [x] 登录接口
      📝 已添加到更新日志：2024-01-28 登录接口开发完成
```

### 5. 查看任务进度

```bash
用户：/sg-task progress

Claude：📊 任务进度：优化登录功能

## 整体进度：████████░░ 80%

### 🔧 后端开发：██████████ 100%
- [x] 登录接口
- [x] 注册接口

### 📱 移动端开发：██████░░░░ 60%
- [x] 登录页面 UI
- [ ] 表单验证

---
📝 统计：总任务 12 个，已完成 7 个
```

### 6. 完成任务

```bash
用户：/sg-task complete
```

---

## 智能特性

### 自动识别仓库类型

根据用户操作自动定位到正确的仓库：

```bash
用户：调整移动端登录页面样式

Claude：📱 正在处理移动端样式调整...
定位到仓库：senguo-pf-easy-mobile（移动端前端）
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

**友好提示模式：**
```bash
用户：运行测试

Claude：测试通过！💡 要更新任务进度吗？
   检测到相关任务：「功能测试」
   要标记为完成吗？(y/n)
```

### 文档智能联动

自动检测产品文档与开发计划的差异，智能提示更新：

**触发场景 1：修改产品文档**
```bash
用户：在 product.md 中添加"记住密码"功能需求

Claude：✅ 已更新产品文档

💡 智能提示：
检测到新增功能「记住密码」

development.md 中可能需要添加：
- 后端：记住密码接口、token 延长逻辑
- 移动端：记住密码选项、自动登录

需要我现在帮你更新开发计划吗？
（稍后也可以说"更新开发计划"）
```

**触发场景 2：查看开发计划时**
```bash
用户：查看开发计划

Claude：正在读取 development.md...

⚠️ 发现差异：

product.md 中有这些功能，但开发计划中缺失：
- 记住密码功能（新增）
- 找回密码功能（新增）

💡 要不要帮你补充到开发计划？
回复"添加"自动补全，或说"不用"跳过
```

**触发场景 3：完成开发任务**
```bash
用户：登录接口开发完成了

Claude：✅ 已自动更新 development.md
      - [x] 登录接口

💡 检查产品文档时发现：
product.md 中的「记住密码」功能还没有对应的开发任务

要不要现在添加到开发计划？
（这是一个遗漏的功能点）
```

**智能对比逻辑：**
```python
def smart_document_sync():
    """智能文档联动（自动执行）"""

    # 当 product.md 被编辑时
    if product_modified:
        missing = compare_product_to_dev()
        if missing:
            show_friendly_tip(
                f"检测到 {len(missing)} 个新功能需要添加到开发计划",
                auto_generate=True  # 自动生成任务建议
            )

    # 当 development.md 被查看时
    if development_viewed:
        orphans = find_missing_features()
        if orphans:
            show_friendly_tip(
                f"产品文档中有 {len(orphans)} 个功能未添加到开发计划",
                suggestions=generate_tasks(orphans)
            )

    # 提示风格：友好、可跳过
    # 不强制、不打断、不记命令
```

**核心特性：**
- 🤖 **全自动** - 无需用户执行命令，自动检测
- 💡 **智能提示** - 只在需要时提醒，不打扰
- 🎯 **上下文感知** - 根据当前操作判断是否提示
- ✅ **可跳过** - 用户可选择忽略或稍后处理
- 🔄 **双向同步** - 产品文档→开发计划，开发计划→产品文档

---

## 图标规范

- 🔄 进行中
- ✅ 已完成
- ⏸️ 暂停
- 🔧 后端
- 💻 PC端前端
- 📱 移动端前端
- 📋 任务
- 📦 仓库
- 📄 文档

---

## 核心设计原则

1. **极简起步** - 创建任务只生成 meta.md 和 README.md
2. **按需扩展** - 需要什么文档就创建什么
3. **分支驱动** - 通过 Git 分支自动关联任务
4. **类型清晰** - 明确标注仓库类型（前端/后端、PC/移动）
5. **上下文保持** - 新开窗口也能自动识别任务
6. **智能推断** - 通过对话自动更新进度，减少手动操作
7. **文档联动** - 自动检测文档差异并智能提示，无需手动同步
