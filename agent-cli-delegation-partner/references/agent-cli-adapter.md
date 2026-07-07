# Agent CLI 适配说明

这个 skill 不绑定某一个执行 Agent。Mimo / MimoCode 只是常见 preset。

## 适配条件

一个可替换的 Agent CLI 至少要支持：

- 能在指定 workspace 内执行，或能接收 workspace 参数。
- 能接收任务 prompt，优先支持从文件读取。
- 在授权范围内能读写项目文件。
- 在授权范围内能运行测试、构建、静态检查等验证命令。
- 结束时能输出结构化结果：变更摘要、文件列表、验证结果、风险。

## 命令模板占位符

`scripts/delegate-agent.py` 支持这些占位符：

- `{workspace}`：项目目录
- `{title}`：任务标题
- `{prompt_file}`：委托 brief 文件路径
- `{prompt}`：委托 brief 正文

优先使用 `{prompt_file}`，因为长 prompt 通过命令行 inline 传递容易遇到转义和长度问题。

## Windows 兼容要求

Windows 上很多 Node/npm/yarn/pnpm 安装的 CLI 实际入口是 `.cmd` 或 `.bat`。

`delegate-agent.py` 会先用 `shutil.which()` 解析 argv[0]，如果发现是 `.cmd` / `.bat`，会通过 Windows shell 执行，避免直接启动失败。

如果自定义 wrapper 仍失败，优先检查：

- CLI 是否在 PATH 上。
- 实际入口是不是 `.cmd`。
- prompt 是否太长，是否应该改用 `{prompt_file}`。
- 当前 shell 和路径风格是否写进了 brief。

## 长任务支持

前台模式会实时输出并写日志，避免长任务完全静默。

后台模式：

```text
python scripts/delegate-agent.py \
  --workspace /path/to/project \
  --title "Long implementation" \
  --prompt-file /tmp/delegation-brief.md \
  --agent mimo \
  --background
```

脚本会返回 PID、log 文件和 status JSON。

查询状态：

```text
python scripts/delegate-agent.py --status /path/to/status.json
```

## 示例

Mimo：

```text
mimo run --dir {workspace} --title {title} {prompt}
```

通用文件输入型 Agent：

```text
agentx run --cwd {workspace} --task-file {prompt_file}
```

只支持 inline prompt 的 Agent：

```text
agentx "{prompt}"
```

inline 模式只适合短任务。复杂任务优先选择 prompt file。

## yargs / array 参数注意事项

有些 CLI 使用 yargs、commander 或类似参数解析库。对 `-f` 这类 array/repeatable 选项，如果后面还有位置参数，可能会被错误吞进数组里。

建议：

- 把位置参数放在 `-f` 等 array 参数之前；或
- 用 `--` 明确分隔 CLI options 和 task positional arguments；或
- 优先用 `--task-file {prompt_file}` 这种显式参数，不混用模糊位置参数。
