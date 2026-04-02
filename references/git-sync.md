# Git 备份策略

`sg-task` 中的 Git 只负责任务文档留痕与备份，不是核心工作流。

## 配置项

```yaml
auto_commit: true
auto_push: true
```

说明：

- `auto_commit: true`：sg-task 写入任务文档后立即尝试同步
- `auto_push: true`：提交后尝试推送

注意：

- 这不是后台定时器，也不是长期守护进程
- 它只覆盖 AI 通过 sg-task 执行的文档写入动作
- 用户手工改文档、别的线程改文档、或之前遗漏的提交，需要再执行 `/sg-task sync`

## 默认行为

当启用了自动提交，且任务文档被 sg-task 写入后：

1. 任务文档发生变更
2. 调用 `python3 scripts/sync_task_docs.py --project-root <project_root>`
3. 只同步 `.tasks`
4. 如果 `auto_push: true`，追加 `--push`

触发点包括：

- `/sg-task create`
- `/sg-task doc product`
- `/sg-task doc development`
- `/sg-task doc api`
- `/sg-task add-repo`
- `/sg-task remove-repo`
- `/sg-task complete`
- 其他任何明确修改任务文档的动作

脚本职责：

- 优先把 `<project_root>/.tasks` 识别为独立 Git 仓库
- 如果 `.tasks` 不是独立仓库，再回退到 `project_root` 所在仓库
- 即使回退到项目仓库，也只允许提交 `.tasks`
- 没有 `.tasks` 变更时直接跳过

## 错误处理

| 场景 | 处理方式 |
| --- | --- |
| 不是 Git 仓库 | 静默跳过 |
| `.tasks` 没有变更 | 静默跳过 |
| 推送失败 | 提示已提交到本地 |
| 网络不可达 | 提示已提交到本地 |

## 手动模式

如果配置为：

```yaml
auto_commit: false
auto_push: false
```

则仍然允许正常更新任务文档，只是不自动提交。需要时使用：

```bash
/sg-task sync
```

等价执行：

```bash
python3 scripts/sync_task_docs.py --project-root <project_root>
```

## 约束

- 不要硬编码 `.tasks` 的绝对路径
- 不要无视 `auto_commit` / `auto_push` 配置
- 不要把 Git 提交作为最高优先级的主流程
- 不要执行 `git add -A` 把整个项目的改动一起提交
- 不要把“自动提交”描述成后台持续运行的能力
