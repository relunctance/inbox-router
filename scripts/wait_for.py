#!/usr/bin/env python3
"""
wait_for.py — 等待依赖任务完成
"""

import argparse
from pathlib import Path
import state

def wait_for(team_dir: Path, task_id: str, timeout: int = 300):
    ts = state.TeamState(team_dir)
    task = ts.wait_for_task(task_id, timeout)
    print(f"任务完成: {task_id}")
    print(f"  Result: {task.get('result', 'N/A')}")

def main():
    parser = argparse.ArgumentParser(description="等待依赖任务完成")
    parser.add_argument("--team-dir", required=True, type=Path, help="团队目录")
    parser.add_argument("--task-id", required=True, help="任务ID")
    parser.add_argument("--timeout", type=int, default=300, help="超时秒数")
    
    args = parser.parse_args()
    wait_for(args.team_dir, args.task_id, args.timeout)

if __name__ == "__main__":
    main()
