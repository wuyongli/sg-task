---
task_id: {{task_id}}
task_name: {{task_name}}
status: in_progress
created_at: {{created_at}}
updated_at: {{updated_at}}

summary: {{summary}}

repositories:
  - name: {{repo_name}}
    key: {{repo_key}}
    type: {{repo_type}}
    path: {{repo_path}}
    branch: {{repo_branch}}

documents:
  product: product.md
  development: development.md
  api: api.md

context_refs:
  goal: product.md#目标与成功指标
  scope: product.md#改动范围
  acceptance: product.md#验收标准
  progress: development.md#当前状态
  in_progress: development.md#进行中
  blockers: development.md#阻塞问题
  next_steps: development.md#下一步计划
---

# 说明

- 本文件是任务主档，不重复保存产品或开发正文
- `repositories[]` 中一旦加入仓库，必须同时记录 `branch`
- `context_refs` 只保存稳定引用，供 `show --load` 精确读取
