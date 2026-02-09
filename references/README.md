# {{task_name}}

## 📊 任务概览
- **任务ID：** {{task_id}}
- **状态：** 🔄 进行中 | ✅ 已完成 | ⏸️ 暂停
- **创建时间：** {{created_at}}

## 📦 涉及仓库

### 🔧 后端
{{#backend_repositories}}
- **{{name}}** (`{{branch}}`)
  - 路径：`{{path}}`
{{/backend_repositories}}

### 📱 移动端
{{#mobile_repositories}}
- **{{name}}** (`{{branch}}`)
  - 路径：`{{path}}`
{{/mobile_repositories}}

### 💻 PC端
{{#pc_repositories}}
- **{{name}}** (`{{branch}}`)
  - 路径：`{{path}}`
{{/pc_repositories}}

## 📄 文档列表
{{#documents}}
- [{{name}}]({{file}})
{{/documents}}

## 🔗 快速链接
{{#quick_links}}
- [{{name}}]({{path}})
{{/quick_links}}
