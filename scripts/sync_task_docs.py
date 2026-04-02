#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def resolve_git_root(project_root: Path, tasks_dir: Path) -> tuple[Path | None, str | None]:
    tasks_result = run(
        ["git", "-C", str(tasks_dir), "rev-parse", "--show-toplevel"],
        check=False,
    )
    if tasks_result.returncode == 0:
        tasks_root = Path(tasks_result.stdout.strip())
        if tasks_root == tasks_dir:
            return tasks_root, "tasks-repo"

    project_result = run(
        ["git", "-C", str(project_root), "rev-parse", "--show-toplevel"],
        check=False,
    )
    if project_result.returncode == 0:
        return Path(project_result.stdout.strip()), "project-repo"

    if tasks_result.returncode == 0:
        return Path(tasks_result.stdout.strip()), "project-repo"

    return None, None


def build_commit_message(task_name: str | None, task_id: str | None) -> str:
    parts = ["同步任务文档"]
    if task_name:
        parts.append(task_name)
    if task_id:
        parts.append(f"({task_id})")
    return " ".join(parts)


def has_changes(git_root: Path, pathspec: str) -> bool:
    result = run(
        ["git", "-C", str(git_root), "status", "--porcelain", "--", pathspec],
        check=False,
    )
    if result.returncode != 0:
        return False
    return bool(result.stdout.strip())


def sync(project_root: Path, task_name: str | None, task_id: str | None, push: bool, dry_run: bool) -> int:
    tasks_dir = project_root / ".tasks"
    if not tasks_dir.exists():
        print(f"skip: 未找到任务目录 {tasks_dir}")
        return 0

    git_root, repo_type = resolve_git_root(project_root, tasks_dir)
    if git_root is None or repo_type is None:
        print("skip: 未找到可用于同步任务文档的 Git 仓库")
        return 0

    pathspec = "." if repo_type == "tasks-repo" else ".tasks"
    commit_message = build_commit_message(task_name, task_id)

    print(f"git_root: {git_root}")
    print(f"sync_scope: {pathspec}")
    print(f"mode: {repo_type}")

    if not has_changes(git_root, pathspec):
        print("skip: 没有需要同步的任务文档变更")
        return 0

    commands = [
        ["git", "-C", str(git_root), "add", "-A", "--", pathspec],
        ["git", "-C", str(git_root), "commit", "-m", commit_message, "--", pathspec],
    ]
    if push:
        commands.append(["git", "-C", str(git_root), "push"])

    if dry_run:
        for cmd in commands:
            print("dry-run:", " ".join(shlex.quote(part) for part in cmd))
        return 0

    add_result = run(commands[0], check=False)
    if add_result.returncode != 0:
        sys.stderr.write(add_result.stderr)
        return add_result.returncode

    commit_result = run(commands[1], check=False)
    if commit_result.returncode != 0:
        combined = f"{commit_result.stdout}\n{commit_result.stderr}".strip()
        if "nothing to commit" in combined:
            print("skip: 没有新的任务文档变更需要提交")
            return 0
        sys.stderr.write(combined)
        return commit_result.returncode

    sys.stdout.write(commit_result.stdout)

    if push:
        push_result = run(commands[2], check=False)
        if push_result.returncode != 0:
            print("warn: 任务文档已提交到本地，但推送远端失败")
            sys.stderr.write(push_result.stderr)
            return 0
        sys.stdout.write(push_result.stdout)

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="同步 sg-task 的任务文档变更")
    parser.add_argument("--project-root", required=True, help="project_root 配置值")
    parser.add_argument("--task-name", help="任务名称，用于生成提交信息")
    parser.add_argument("--task-id", help="任务 ID，用于生成提交信息")
    parser.add_argument("--push", action="store_true", help="提交后尝试推送远端")
    parser.add_argument("--dry-run", action="store_true", help="仅打印将要执行的命令")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    return sync(
        project_root=project_root,
        task_name=args.task_name,
        task_id=args.task_id,
        push=args.push,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
