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

## 示例命令

```text
python scripts/delegate-agent.py \
  --workspace /path/to/project \
  --title "Implement checkout validation" \
  --prompt-file /tmp/delegation-brief.md \
  --command-template "agentx run --cwd {workspace} --task-file {prompt_file}"
```

## 原则

Mimo 不是必需品。

只要目标 CLI 满足适配条件：能接收清晰 prompt、在目标 workspace 执行、读写项目文件、运行验证并返回结构化结果，就可以替换。
