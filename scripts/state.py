#!/usr/bin/env python3
"""
state.py — 任务状态管理
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional


class TeamState:
    """团队状态管理"""

    def __init__(self, team_dir: Path):
        self.team_dir = team_dir
        self.team_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.team_dir / ".team" / "state.json"
        self._ensure_state()

    def _ensure_state(self):
        """确保状态文件存在"""
        state_dir = self.team_dir / ".team"
        state_dir.mkdir(exist_ok=True)

        if not self.state_file.exists():
            initial_state = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "tasks": {},
                "roles": {},
                "messages": []
            }
            self._save(initial_state)

    def _load(self) -> dict:
        """加载状态"""
        return json.loads(self.state_file.read_text())

    def _save(self, state: dict):
        """保存状态"""
        self.state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))

    def add_task(self, task_id: str, role: str, description: str, blocked_by: list = None) -> dict:
        """添加任务"""
        state = self._load()

        task = {
            "id": task_id,
            "assigned_to": role,
            "description": description,
            "status": "pending",
            "blocked_by": blocked_by or [],
            "result": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        state["tasks"][task_id] = task
        state["roles"].setdefault(role, {"inbox_port": None, "status": "idle"})
        self._save(state)

        return task

    def get_task(self, task_id: str) -> Optional[dict]:
        """获取任务"""
        state = self._load()
        return state["tasks"].get(task_id)

    def update_task_status(self, task_id: str, status: str, result: str = None) -> dict:
        """更新任务状态"""
        state = self._load()

        if task_id not in state["tasks"]:
            raise ValueError(f"Task not found: {task_id}")

        task = state["tasks"][task_id]
        task["status"] = status
        task["updated_at"] = datetime.now().isoformat()

        if result is not None:
            task["result"] = result

        self._save(state)
        return task

    def list_tasks(self, role: str = None, status: str = None) -> list:
        """列出任务"""
        state = self._load()
        tasks = list(state["tasks"].values())

        if role:
            tasks = [t for t in tasks if t["assigned_to"] == role]
        if status:
            tasks = [t for t in tasks if t["status"] == status]

        return tasks

    def wait_for_task(self, task_id: str, timeout: int = 300) -> dict:
        """等待任务完成"""
        start = time.time()

        while time.time() - start < timeout:
            task = self.get_task(task_id)
            if task and task["status"] == "completed":
                return task
            time.sleep(1)

        raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")

    def add_message(self, msg: dict):
        """添加消息"""
        state = self._load()
        msg["timestamp"] = datetime.now().isoformat()
        state["messages"].append(msg)
        self._save(state)

    def get_messages(self, role: str = None, since: str = None) -> list:
        """获取消息"""
        state = self._load()
        messages = state["messages"]

        if role:
            messages = [m for m in messages if m.get("to") == role or m.get("from") == role]
        if since:
            messages = [m for m in messages if m["timestamp"] > since]

        return messages
