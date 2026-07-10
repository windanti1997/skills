# Bad Example: 被简化成 MVP 的软任务

## Task: 实现 Memory Contract Builder MVP

实现一个简单的 memory contract builder，先支持基本流程。后续可以接入 verifier。

## 验收标准

- CLI 可以运行。
- 能生成 contract 文件。
- 基本逻辑可用。
- 后续再完善测试和边界情况。

## 问题

这个任务不合格：

1. 未经授权把完整目标降级成 MVP。
2. “基本流程”“基本逻辑可用”不可判定。
3. 没有说明输入、处理、输出、接入点。
4. 没有边界场景。
5. 测试被后置。
6. verifier 接入被后置，但没有说明是否破坏闭环。
7. 没有反偷懒验收。
8. 没有证据计划。
