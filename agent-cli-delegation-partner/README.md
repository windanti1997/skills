# agent-cli-delegation-partner

一个给 Codex 使用的通用委托型 skill：当任务会消耗大量 Token 或上下文窗口时，让 Codex 不再自己硬扛，而是把长上下文执行工作交给一个可命令行调用的 Agent CLI，自己保留判断、审查和验收责任。

## 这次修复了什么

这版针对真实试用暴露的问题做了强化：

- **Trellis 不再只写“按约定执行”**：必须明确 task.py、task.json、implement.md、状态流转和执行记录分工。
- **禁止执行 Agent 用自己的内部 task 系统替代项目工作流**：Mimo 可以有自己的内部 task，但不能代替 Trellis task。
- **brief 模板增加 Detected Environment**：要求写明 OS / shell，避免 delegated agent 用错 shell 命令。
- **delegate-agent.py 修 Windows**：会先解析 argv[0]，Windows 上 `.cmd` / `.bat` 走 shell 启动。
- **增加实时输出和后台模式**：长任务不再完全静默，也支持 `--background` 后台执行和 `--status` 查询。
- **adapter 补 yargs 注意事项**：对 `-f` 这类 array 参数，建议位置参数放前或使用 `--` 分隔。

## 这个 skill 解决什么问题

复杂 Coding 任务里，真正消耗上下文的往往不是最终代码，而是过程：读大量文件、理解历史实现、生成任务文档、跑测试、看日志、修失败、再跑测试、review 大 diff。

这个 skill 的目标是让 Codex 形成稳定分工：

- **Codex 负责判断**：澄清需求、控制范围、识别项目工作流、定义验收标准、最终 review。
- **执行 Agent 负责落地**：读文件、写代码、补文档、跑测试、修失败、输出摘要。
- **Codex 最终验收**：不能因为执行 Agent 说“完成了”就直接交付。

## 最重要的原则

```text
Codex 可以委托执行，但不能委托责任。
```

执行 Agent 做完后，Codex 必须自己检查：

- 是否满足用户真实需求
- 是否越界改动
- 是否遵守项目工作流
- 是否乱改无关文件
- 是否真的运行验证
- 文档和代码是否一致
- Trellis 状态、执行记录和代码是否一致
- 是否存在安全、迁移、数据兼容、权限或回滚风险

只有经过 Codex review，结果才算可交付。

## scripts 是干什么的

`scripts/` 里的脚本不是安装脚本，也不是打包脚本。

它们是 Codex 在使用 skill 时可以调用的运行时工具。

### `scripts/delegate-agent.py`

用于把一个委托 brief 交给外部 Agent CLI 执行。

前台执行：

```text
python scripts/delegate-agent.py \
  --workspace /path/to/project \
  --title "Implement checkout validation" \
  --prompt-file /tmp/delegation-brief.md \
  --agent mimo
```

后台执行：

```text
python scripts/delegate-agent.py \
  --workspace /path/to/project \
  --title "Long implementation" \
  --prompt-file /tmp/delegation-brief.md \
  --agent mimo \
  --background
```

查询后台状态：

```text
python scripts/delegate-agent.py --status /path/to/status.json
```

替换成其他 CLI：

```text
python scripts/delegate-agent.py \
  --workspace /path/to/project \
  --title "Implement checkout validation" \
  --prompt-file /tmp/delegation-brief.md \
  --command-template "agentx run --cwd {workspace} --task-file {prompt_file}"
```

### `scripts/collect-review-context.py`

用于执行 Agent 完成后，帮 Codex 收集 review 所需的简洁上下文：

- `git status`
- changed files
- diff stat
- recent commits
- 可选 capped diff

它的目标是减少上下文噪音，而不是把完整 diff 全塞回主对话。

## Trellis 特别注意

如果项目使用 Trellis，brief 不能只写“按 Trellis 约定”。必须明确：

- 具体 Trellis task 路径
- 是否允许执行 Agent 调用 `.trellis/scripts/task.py start/finish/archive`
- `task.json` 状态由 Codex 还是执行 Agent 负责
- `implement.md` 或等价执行记录由谁更新
- 明确禁止执行 Agent 用自己的内部 task 系统替代 Trellis

默认建议：Codex 控制状态流转，执行 Agent 至少更新 `implement.md` 执行记录。
