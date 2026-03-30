---
task_id: {{task_id}}
task_name: {{task_name}}
status: in_progress
created_at: {{created_at}}
updated_at: {{updated_at}}

summary: {{summary}}

# 可选：新线程默认加载的短事实，只写已确认内容
# always_load:
#   goal: {{one_sentence_goal}}
#   current_context: {{current_context}}
#   notes:
#     - {{fact_1}}
#     - {{fact_2}}
#     - {{fact_3}}

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

# 可选：仅在需要按标题精确深读时再维护
# deep_links:
#   product: product.md
#   development: development.md
#   api: api.md
#
# context_refs:
#   goal: product.md#目标与成功指标
#   scope: product.md#改动范围
#   acceptance: product.md#验收标准
#   progress: development.md#当前状态
#   in_progress: development.md#进行中
#   blockers: development.md#阻塞问题
#   next_steps: development.md#下一步计划
---

# 说明

- 本文件是任务主档，不重复保存产品或开发正文
- `repositories[]` 中一旦加入仓库，必须同时记录 `branch`
- `always_load` 是默认加载层，只保留新线程继续工作的短事实
- `deep_links` 和 `context_refs` 是按需深读导航，不是默认加载内容

## `always_load` 推荐写法

推荐结构：

```yaml
always_load:
  goal: 优化登录体验，统一多端登录流程
  current_context: 当前在同一任务下继续处理“记住密码”这个需求点
  notes:
    - 登录接口和 token 逻辑已经完成
    - 当前任务涉及批发后端和移动端
    - 如需细看需求，去读 product.md
```

推荐只写：

- 任务目标的一句话版本
- 当前这个线程为什么开出来
- 1 到 3 条已确认的工作事实

不要写：

- 大段需求背景
- 冗长更新日志
- 猜测性的进度、阻塞、下一步
- 需要 AI 自己再总结一遍的大段正文

判断标准：

- 新线程读完 10 秒内能知道“这个任务是什么、我现在要接着处理哪个点”
- 总长度尽量控制在 3 到 6 行
