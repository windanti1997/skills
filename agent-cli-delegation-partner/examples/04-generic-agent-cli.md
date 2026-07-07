# 示例：把默认执行器换成其他 Agent CLI

## 场景

用户说：

```text
Use agentx instead of Mimo.
```

## Codex 应该怎么做

1. 把 `agentx` 当成执行 CLI。
2. 构造 command template，把 workspace 和 prompt file 传进去。
3. 通过 `scripts/delegate-agent.py --command-template` 调用。
4. 如果 CLI 使用 yargs/commander 这类解析器，注意 array 参数和位置参数顺序。

## 示例命令

```text
python scripts/delegate-agent.py \
  --workspace /path/to/project \
  --title "Implement checkout validation" \
  --prompt-file /tmp/delegation-brief.md \
  --command-template "agentx run --cwd {workspace} --task-file {prompt_file}"
```

## yargs 注意事项

对 `-f` 这类 array/repeatable 选项，位置参数放前，或用 `--` 分隔：

```text
agentx run task-name -f a -f b
```

或：

```text
agentx run -f a -f b -- task-name
```

## 原则

Mimo 不是必需品。

只要目标 CLI 满足适配条件：能接收清晰 prompt、在目标 workspace 执行、读写项目文件、运行验证并返回结构化结果，就可以替换。
