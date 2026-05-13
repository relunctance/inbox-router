#!/usr/bin/env python3
"""
report.py — sub-agent 汇报任务完成
"""

import argparse
from pathlib import Path
import state

def report(team_dir: Path, task_id: str, result: str):
    ts = state.TeamState(team_dir)
    task = ts.update_task_status(task_id, "completed", result)
    
    msg = {
        "type": "report",
        "from": task["assigned_to"],
        "to": "主理人",
        "task_id": task_id,
        "content": {"result": result}
    }
    ts.add_message(msg)
    
    print(f"任务完成汇报:")
    print(f"  Task ID: {task_id}")
    print(f"  Status: completed")
    print(f"  Result: {result}")

def main():
    parser = argparse.ArgumentParser(description="汇报任务完成")
    parser.add_argument("--team-dir", required=True, type=Path, help="团队目录")
    parser.add_argument("--task-id", required=True, help="任务ID")
    parser.add_argument("--result", required=True, help="任务结果")
    
    args = parser.parse_args()
    report(args.team_dir, args.task_id, args.result)

if __name__ == "__main__":
    main()
