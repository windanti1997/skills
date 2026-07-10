# Good Example: Trellis Task Contract

# Task: Memory Contract Builder + CLI 最小完整闭环

## 1. 背景与真实目标

用户真正想解决的问题是：让 active memories 能被转换成 verifier 可消费的 memory contract，从而让后续任务系统不只是“召回记忆”，而是能生成明确 obligations 供执行与验收使用。

本任务的真实价值是：建立 active memories → memory contract → verifier obligations 的可验证数据闭环。

不是：只写一个 schema，或只做一个 CLI 壳子。

## 2. 为什么不能简化成普通 MVP

如果 Agent 偷懒，可能会把任务简化成：只定义 JSON schema，CLI 输出一个示例文件，测试后续再补。

这个简化为什么不满足目标：它没有真实 builder，没有输入校验，没有 obligations 生成逻辑，也无法证明 verifier 能消费。

MVP 是否是用户明确要求：否。

如果本任务是最小版本，它为什么仍然是完整闭环，而不是残缺壳子：本任务包含输入 active memories、builder 转换、schema 校验、CLI 调用、产物输出、测试验证。可以暂不接入完整 verifier 运行时，但必须输出 verifier 可消费的 contract 文件，并用测试验证字段。

## 3. 本次最小完整闭环

- 输入：active memories JSON 文件。
- 处理：builder 校验输入并生成 obligations。
- 输出：memory contract JSON 文件。
- 接入点：CLI 命令 `aeb contract build --input ... --output ...`。
- 可验证结果：输出文件通过 schema 校验，包含 obligations/source_memories/scope/created_at。
- 用户/调用方能获得的真实价值：后续 verifier 可以读取 contract 并执行 obligation 检查。

## 4. 非目标

本任务明确不做：完整 verifier 执行引擎。

这些不做不会破坏本次闭环，因为：本任务仍然输出 verifier 可消费 artifact，并通过测试验证 contract 结构和 obligations 字段。

## 5. 允许后置项

允许后置：verifier runtime 的完整执行与 UI 展示。

后置原因：这属于下游消费，不影响本任务生成 contract 的完整闭环。

后置后不会破坏当前设计的证据：contract schema 和 builder 测试会固定下游接口字段。

## 6. 禁止降级项

不得：

- 用 TODO 代替 builder 核心逻辑。
- 用 placeholder contract 代替真实输入转换。
- 用 mock active memories 作为唯一实现路径。
- 只做 happy path。
- 只写 schema 不实现 CLI。
- 只写 CLI 不接 builder。
- 把完整目标改成未经授权的 MVP。

## 7. 实现范围

必须新增/修改的模块：

- `src/contracts/schema.ts`
- `src/contracts/builder.ts`
- `src/cli/contract.ts`
- `tests/contracts/builder.test.ts`
- `docs/memory-contract.md`

必须接入的真实调用链：CLI 调用 builder，builder 读取 active memories，输出 contract 文件。

必须保留的现有行为：现有 memory recall 命令不被破坏。

可能影响的旧逻辑：CLI command registry。

## 8. 边界场景

至少覆盖：

1. 正常场景：多个 active memories 生成多个 obligations。
2. 缺失输入：input 文件不存在时返回错误。
3. 非法输入：active memories 缺少 id/content 时返回 schema error。
4. 空数据：空 active memories 输出空 obligations 且 warning。
5. 旧数据兼容：缺少 optional metadata 时仍可生成。
6. 重复执行：同输入重复执行输出稳定。
7. 错误恢复：输出路径不可写时返回非 0 状态。

## 9. 验收标准

### 功能验收

- [ ] CLI 能从真实 input 文件生成 contract output 文件。
- [ ] Builder 生成 obligations，不是输出固定示例。
- [ ] Contract 包含 obligations/source_memories/scope/created_at。

### 测试验收

- [ ] 新增 builder 单元测试覆盖正常、空数据、非法输入、重复执行。
- [ ] 新增 CLI 测试覆盖缺失输入和输出路径错误。
- [ ] 运行测试命令通过。

### 文档验收

- [ ] 文档说明 contract 字段和 CLI 用法。

### 兼容性验收

- [ ] 现有 recall 命令测试仍通过。

## 10. 反偷懒验收

- [ ] 没有把完整目标降级成未经授权的 MVP。
- [ ] 没有用 TODO / placeholder / mock 冒充完成。
- [ ] 没有只实现 happy path。
- [ ] 没有只写接口而不接入真实调用链。
- [ ] 每个验收项都有证据来源。

## 11. 证据计划

完成后必须提供：

- 修改文件列表。
- 新增/更新测试。
- 运行命令：`npm test -- contracts` 与 CLI smoke test。
- 命令输出摘要。
- 手动验证步骤：给定 sample active memories，运行 CLI，查看 contract。
- 产物路径：sample contract output。
- 未覆盖风险。

## 12. Checkpoints

### Checkpoint 1: Schema 与类型

完成条件：schema 和类型定义完成，单元测试验证 required 字段。

证据：测试文件和测试输出。

不得进入下一步的阻塞条件：schema 字段不稳定或缺少 obligations。

### Checkpoint 2: Builder 核心逻辑

完成条件：builder 从 active memories 生成 obligations。

证据：builder 测试通过。

不得进入下一步的阻塞条件：builder 只返回固定 mock。

### Checkpoint 3: CLI 接入

完成条件：CLI 调用 builder 读取 input 并写 output。

证据：CLI smoke test 通过。

不得进入下一步的阻塞条件：CLI 未接真实 builder。

### Checkpoint 4: 文档与最终证据

完成条件：文档、测试、最终 evidence report 完成。

证据：文档路径、测试输出、sample output。

## 13. Review 打回条件

出现以下任一情况必须打回：

- 只写 schema。
- CLI 只输出固定示例。
- Builder 没有测试。
- 没有错误场景。
- verifier 可消费字段缺失。
- 使用 TODO / placeholder 冒充完成。
