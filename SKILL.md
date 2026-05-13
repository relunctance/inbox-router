---
name: inbox-router
description: Sub-Agent 协调器 — 任务分配、结果汇报、依赖等待，通过 state.json 持久化任务状态
triggers:
  - 分配任务给 sub-agent
  - 协调 sub-agent
  - sub-agent 通信
  - assign task
  - dispatch to sub-agent
category: Infrastructure
author: relunctance
created: 2026-05-13
updated: 2026-05-13
version: "1.0.0"
tags:
  - coordination
  - sub-agent
  - inbox
  - task-management
  - expert-team
platforms:
  openclaw: true
  claude_code: true
  codex: true
  hermes: true
---

# inbox-router

> Sub-Agent 协调器 — 任务分配、结果汇报、依赖等待

## 概述

sub-agent 协调通信：任务分配、结果汇报、依赖等待。

## 核心组件

| 脚本 | 功能 |
|------|------|
| `dispatch.py` | 分配任务给 sub-agent |
| `report.py` | sub-agent 汇报任务完成 |
| `wait_for.py` | 等待依赖任务完成 |
| `broadcast.py` | 广播消息给所有 sub-agents |
| `state.py` | 任务状态持久化（TeamState 类） |
| `inbox_server.py` | 每个 sub-agent 的 HTTP inbox 服务器 |

## 使用方式

```bash
# 分配任务
python scripts/dispatch.py \
  --team-dir <path> \
  --role <name> \
  --task-id <id> \
  --description <text> \
  [--blocked-by <task-id>...]

# 汇报结果
python scripts/report.py \
  --team-dir <path> \
  --task-id <id> \
  --result <text>

# 等待任务完成
python scripts/wait_for.py \
  --team-dir <path> \
  --task-id <id> \
  [--timeout 300]

# 广播消息
python scripts/broadcast.py \
  --team-dir <path> \
  --message <text>
```

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

## 状态文件

任务状态存储在 `<team_dir>/.team/state.json`

```json
{
  "version": "1.0",
  "tasks": {
    "task-001": {
      "id": "task-001",
      "assigned_to": "architect",
      "description": "设计登录系统",
      "status": "completed",
      "blocked_by": [],
      "result": "输出在 docs/login-arch.md",
      "created_at": "ISO timestamp",
      "updated_at": "ISO timestamp"
    }
  },
  "roles": {},
  "messages": []
}
```

## 工作流程

```
1. 主理人启动 inbox 服务器
2. 各 sub-agent 启动自己的 inbox 服务器
3. 主理人用 dispatch.py 分配任务
4. sub-agent 完成，用 report.py 汇报
5. 主理人收到汇报，决定下一步
```

## 示例

```bash
# 分配任务
python scripts/dispatch.py \
  --team-dir ~/expert-teams/ProductStrategyTeam \
  --role architect \
  --task-id task-001 \
  --description "设计用户登录系统"

# 分配有依赖的任务
python scripts/dispatch.py \
  --team-dir ~/expert-teams/ProductStrategyTeam \
  --role engineer \
  --task-id task-002 \
  --description "实现用户登录" \
  --blocked-by task-001

# 等待完成
python scripts/wait_for.py \
  --team-dir ~/expert-teams/ProductStrategyTeam \
  --task-id task-001 \
  --timeout 600
```

## 相关 Skill

| Skill | 说明 |
|-------|------|
| [role-installer](https://github.com/relunctance/role-installer) | 安装团队 |
| [role-skill-manager](https://github.com/relunctance/role-skill-manager) | 管理 skills |
