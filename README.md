# inbox-router

> ⚠️ **已废弃** — 请使用 [ClawTeam-OpenClaw](https://github.com/win4r/ClawTeam-OpenClaw) 替代。
>
> 迁移指南：ClawTeam-OpenClaw 提供完整的 inbox、task dependencies、git worktree 隔离，且由社区维护，升级只需 `git pull`。

**sub-agent 协调通信：任务分配、结果汇报、依赖等待。**

## 核心组件

| 脚本 | 功能 |
|------|------|
| `dispatch.py` | 分配任务给 sub-agent |
| `report.py` | sub-agent 汇报任务完成 |
| `wait_for.py` | 等待依赖任务完成 |
| `broadcast.py` | 广播消息给所有 sub-agents |
| `state.py` | 任务状态持久化 |
| `inbox_server.py` | 每个 sub-agent 的 HTTP inbox 服务器 |

## 状态文件

```
<team_dir>/.team/state.json
```

## 使用流程

1. 主理人启动 inbox 服务器
2. 各 sub-agent 启动自己的 inbox 服务器
3. 主理人用 `dispatch.py` 分配任务
4. sub-agent 完成，用 `report.py` 汇报
5. 主理人收到汇报，决定下一步

## 消息协议

```json
{
  "type": "task",
  "from": "主理人",
  "to": "architect",
  "task_id": "task-001",
  "content": {"description": "设计登录系统"}
}
```

## 相关

- [role-installer](https://github.com/relunctance/role-installer)
- [role-skill-manager](https://github.com/relunctance/role-skill-manager)
