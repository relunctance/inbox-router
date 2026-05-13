#!/usr/bin/env python3
"""
inbox_server.py — 轻量级 HTTP inbox 服务器
每个 sub-agent 运行一个，用于接收主理人的任务分配

用法:
  python inbox_server.py --port 3001 --role architect --team-dir ~/expert-teams/ProductStrategyTeam
"""

import argparse
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import state

class InboxHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        role = self.server.role
        ts = state.TeamState(self.server.team_dir)
        messages = ts.get_messages(role=role)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(messages, indent=2, ensure_ascii=False).encode())
        
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        msg = json.loads(body.decode())
        
        ts = state.TeamState(self.server.team_dir)
        ts.add_message(msg)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
        
    def log_message(self, format, *args):
        print(f"[{self.server.role}] {format % args}")

class InboxServer(HTTPServer):
    def __init__(self, *args, role=None, team_dir=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role
        self.team_dir = team_dir

def main():
    parser = argparse.ArgumentParser(description="启动 inbox HTTP 服务器")
    parser.add_argument("--port", type=int, required=True, help="监听端口")
    parser.add_argument("--role", required=True, help="角色名称")
    parser.add_argument("--team-dir", required=True, type=Path, help="团队目录")
    
    args = parser.parse_args()
    
    server = InboxServer(("localhost", args.port), InboxHandler, role=args.role, team_dir=args.team_dir)
    print(f"启动 inbox 服务器: {args.role} @ localhost:{args.port}")
    print(f"Team dir: {args.team_dir}")
    server.serve_forever()

if __name__ == "__main__":
    main()
