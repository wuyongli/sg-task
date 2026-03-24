# Git 备份策略

`sg-task` 中的 Git 只负责任务文档留痕与备份，不是核心工作流。

## 配置项

```yaml
auto_commit: true
auto_push: true
```

说明：

- `auto_commit: true`：任务文档变更后自动提交
- `auto_push: true`：提交后尝试推送

## 默认行为

当 `.tasks` 是 Git 仓库，且启用了自动提交：

1. 任务文档发生变更
2. 执行 `git add -A`
3. 执行 `git commit`
4. 如果 `auto_push: true`，再尝试 `git push`

## 错误处理

| 场景 | 处理方式 |
| --- | --- |
| 不是 Git 仓库 | 静默跳过 |
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

## 约束

- 不要硬编码 `.tasks` 的绝对路径
- 不要无视 `auto_commit` / `auto_push` 配置
- 不要把 Git 提交作为最高优先级的主流程
