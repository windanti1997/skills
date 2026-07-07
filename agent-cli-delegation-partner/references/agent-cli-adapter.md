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
