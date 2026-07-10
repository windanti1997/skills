# Review Report Example

# Task Contract Review

结论：FAIL

## 失败机制

任务把“Memory Contract Builder + CLI 完整闭环”降级成了“先做 schema 和 CLI 示例”的 MVP。该 MVP 没有真实 builder、没有 obligations 生成逻辑、没有边界测试，也没有证明 verifier 可消费。

## 具体问题

1. 验收标准写成“基本可用”，不可判定。
2. 没有禁止降级项。
3. 测试被写成后续优化。
4. CLI 是否接入真实 builder 未说明。
5. 缺少非法输入、空数据、重复执行、输出路径错误等边界场景。

## 必须修改

1. 增加“本次最小完整闭环”。
2. 明确禁止只写 schema、只写 CLI 壳子、输出 placeholder contract。
3. 增加 builder 与 CLI 测试要求。
4. 增加 evidence plan。
5. 增加 checkpoint。

## 是否允许进入 implement

不允许。
