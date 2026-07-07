# agent-cli-delegation-partner

一个给 Codex 使用的通用委托型 skill：当任务会消耗大量 Token 或上下文窗口时，让 Codex 不再自己硬扛，而是把长上下文执行工作交给一个可命令行调用的 Agent CLI，自己保留判断、审查和验收责任。

## 这个 skill 解决什么问题

复杂 Coding 任务里，真正消耗上下文的往往不是最终代码，而是过程：读大量文件、理解历史实现、生成任务文档、跑测试、看日志、修失败、再跑测试、review 大 diff。

这个 skill 的目标是让 Codex 形成稳定分工：

- **Codex 负责判断**：澄清需求、控制范围、识别项目工作流、定义验收标准、最终 review。
- **执行 Agent 负责落地**：读文件、写代码、补文档、跑测试、修失败、输出摘要。
- **Codex 最终验收**：不能因为执行 Agent 说“完成了”就直接交付。

## 为什么不叫 mimo-implementation-partner

Mimo 只是一个可用的默认执行器，因为它是 CLI，方便 Codex 调用。

但这个 skill 的核心不是绑定 Mimo，而是抽象出一套通用协议：

```text
Codex 写清楚委托 brief
  ↓
调用 Mimo / MimoCode / 其他 Agent CLI
  ↓
执行 Agent 完成上下文重活
  ↓
Codex review diff、测试、文档和风险
```

所以现在改成通用名字：`agent-cli-delegation-partner`。

## 什么时候使用

适合：

- 多文件实现
- 大量代码阅读
- 大 diff review
- 测试失败循环修复
- 需要维护 Trellis task
- 需要遵循 Superpowers / using-superpowers
- 需要更新 spec / plan / design / task 文档
- 用户明确要求 Codex 调用其他 Agent CLI

不适合：

- 普通问答
- 小范围解释
- 单文件小修
- 不值得委托的低成本任务

## 文件结构

```text
agent-cli-delegation-partner/
├── SKILL.md
├── README.md
├── scripts/
│   ├── delegate-agent.py
│   └── collect-review-context.py
├── prompts/
│   └── executor-output-format.md
├── references/
│   ├── agent-cli-adapter.md
│   ├── delegation-brief-template.md
│   ├── review-checklist.md
│   └── workflow-detection.md
└── examples/
    ├── 01-trellis-feature.md
    ├── 02-superpowers-workflow.md
    ├── 03-spec-plan-workflow.md
    ├── 04-generic-agent-cli.md
    └── 05-test-fix-loop.md
```

## scripts 是干什么的

`scripts/` 里的脚本不是安装脚本，也不是打包脚本。

它们是 Codex 在使用 skill 时可以调用的运行时工具。

### `scripts/delegate-agent.py`

用于把一个委托 brief 交给外部 Agent CLI 执行。

示例：

```text
python scripts/delegate-agent.py \
  --workspace /path/to/project \
  --title "Implement checkout validation" \
  --prompt-file /tmp/delegation-brief.md \
  --agent mimo
```

也可以替换成其他 CLI：

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

## 支持哪些项目工作流

这个 skill 不会强行假设项目一定使用 Trellis。

Codex 应该先识别项目已有规则，包括：

- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/`
- `.windsurfrules`
- `.trellis/`
- Superpowers / using-superpowers
- `spec.md`
- `plan.md`
- `design.md`
- `docs/specs/`
- `docs/plans/`
- `.kiro/specs/`

然后按项目已有工作流委托执行 Agent。

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
- 是否存在安全、迁移、数据兼容、权限或回滚风险

只有经过 Codex review，结果才算可交付。
