#!/usr/bin/env python3
"""
dispatch.py — 分配任务给 sub-agent
"""

import argparse
from pathlib import Path
import state

def dispatch(team_dir: Path, role: str, task_id: str, description: str, blocked_by: list = None):
    ts = state.TeamState(team_dir)
    task = ts.add_task(task_id, role, description, blocked_by)
    
    msg = {
        "type": "task",
        "from": "主理人",
        "to": role,
        "task_id": task_id,
        "content": {"description": description}
    }
    ts.add_message(msg)
    
    print(f"任务已分配:")
    print(f"  Task ID: {task_id}")
    print(f"  Role: {role}")
    print(f"  Description: {description}")
    if blocked_by:
        print(f"  Blocked by: {blocked_by}")

def main():
    parser = argparse.ArgumentParser(description="分配任务给 sub-agent")
    parser.add_argument("--team-dir", required=True, type=Path, help="团队目录")
    parser.add_argument("--role", required=True, help="角色名称")
    parser.add_argument("--task-id", required=True, help="任务ID")
    parser.add_argument("--description", required=True, help="任务描述")
    parser.add_argument("--blocked-by", nargs="*", help="依赖的任务ID列表")
    
    args = parser.parse_args()
    dispatch(args.team_dir, args.role, args.task_id, args.description, args.blocked_by)

if __name__ == "__main__":
    main()
