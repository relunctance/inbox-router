#!/usr/bin/env python3
"""
broadcast.py — 广播消息给所有 sub-agents
"""

import argparse
from pathlib import Path
import state

def broadcast(team_dir: Path, message: str):
    ts = state.TeamState(team_dir)
    
    msg = {
        "type": "broadcast",
        "from": "主理人",
        "to": "all",
        "content": {"message": message}
    }
    ts.add_message(msg)
    
    print(f"广播已发送:")
    print(f"  Message: {message}")
    print(f"  Recipients: all roles")

def main():
    parser = argparse.ArgumentParser(description="广播消息给所有 sub-agents")
    parser.add_argument("--team-dir", required=True, type=Path, help="团队目录")
    parser.add_argument("--message", required=True, help="消息内容")
    
    args = parser.parse_args()
    broadcast(args.team_dir, args.message)

if __name__ == "__main__":
    main()
