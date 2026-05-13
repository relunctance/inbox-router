# inbox-router

**sub-agent 协调通信：任务分配、结果汇报、依赖等待。**

## 功能

- dispatch: 分配任务给 sub-agent
- report: sub-agent 汇报任务完成
- wait-for: 等待依赖任务完成
- broadcast: 广播消息给所有 sub-agents
- state.json: 持久化任务状态

## 消息协议

```json
{
  "type": "task" | "report" | "broadcast" | "approval_request",
  "from": "主理人" | "role_name",
  "to": "role_name" | "主理人" | "all",
  "task_id": "task-001",
  "content": {
    "description": "任务描述",
    "files": ["docs/output.md"],
    "deadline": "ISO timestamp"
  },
  "timestamp": "ISO timestamp"
}
```

## 使用方式

```bash
# 分配任务
python scripts/dispatch.py --team-dir <path> --role <name> --task-id <id> --description <text>

# 汇报结果
python scripts/report.py --team-dir <path> --task-id <id> --result <text>

# 等待任务完成
python scripts/wait_for.py --team-dir <path> --task-id <id> [--timeout 300]

# 广播
python scripts/broadcast.py --team-dir <path> --message <text>
```

## 状态文件

任务状态存储在 `<team_dir>/.team/state.json`

## 相关 Skill

- [role-installer](https://github.com/relunctance/role-installer) — 安装团队
- [role-skill-manager](https://github.com/relunctance/role-skill-manager) — 管理 skills
