---
name: trellis-task-contract
description: 中文优先的 Trellis 任务契约生成与审查 skill。用于防止 agent 在生成 Trellis 任务、PRD、实施计划或验收标准时偷懒简化成未授权 MVP，强制执行 Anti-MVP Preflight、最小完整闭环、禁止降级项、反偷懒验收、证据计划、checkpoint 回填和 Task Contract Review。
---
# Trellis Task Contract Skill

## 名称

trellis-task-contract

## 目的

当用户要求你生成 Trellis 任务、拆解长任务、写 PRD、写 implement plan、制定验收标准或推进复杂项目时，使用本 Skill。

本 Skill 的目标不是“把需求写成任务”，而是把需求转成一个**不可逃逸的任务契约**，防止 Agent 在长任务中偷懒、目标衰减、默认 MVP 化、验收放水、TODO 化、happy path 化和假完成。

## 什么时候必须使用

只要出现以下任一情况，必须使用本 Skill：

- 用户说“生成 Trellis 任务 / 建 Trellis task / 写 task / 写 implement plan / 写 PRD”。
- 用户要求一个长任务、复杂项目、多阶段实现或多个 Agent 协作。
- 用户担心 Agent 偷懒、简化成 MVP、验收不严格、只做短任务能做好。
- 用户说“不要偷懒”“不要只做 MVP”“任务要严格验收”。
- 用户让你为 Codex、Trae、Mimo、Claude Code 等 coding agent 写执行计划。
- 任务如果失败会表现为：写了壳子、没接真实调用链、没测试、只做 happy path、TODO 很多。

## 核心原则

### 1. MVP 必须是产品决策，不是 Agent 的逃生通道

不要默认把完整目标简化成 MVP。只有用户明确要求 MVP，或你能证明完整目标需要拆分且本次交付仍是完整薄片时，才允许使用 MVP 表述。

### 2. 任务可以小，但不能残

正确拆任务是拆成“完整薄片”：每个子任务都有输入、处理、输出、接入点、测试和证据。

错误拆任务是拆成“残缺阶段”：先搭壳、后补逻辑、后补测试、后补文档。这会制造假进展。

### 3. 验收必须有证据

不能只写“功能正常”“基本可用”“完成实现”。每个验收项必须能通过至少一种证据验证：测试、命令输出、截图、diff、日志、文件路径、手动验证步骤。

### 4. 先审查任务，再进入实现

生成 Trellis 任务后，必须先进行 Task Contract Review。不通过就重写任务；不得一边写软任务一边直接 implement。

### 5. 长任务必须 checkpoint 化

长任务不能等最后才验收。必须设计中间 checkpoint，每个 checkpoint 都回填证据。

## 标准流程

### Step 1: Task Contract Preflight

先不要生成任务，先回答：

1. 用户真实目标是什么？
2. 如果 Agent 偷懒，会把它简化成什么 MVP？
3. 这个 MVP 为什么不满足真实目标？
4. 本次最小完整闭环是什么？
5. 哪些必须交付？
6. 哪些允许后置？
7. 哪些禁止降级？
8. 哪些不能用 TODO / placeholder / mock 代替？
9. 哪些必须接入真实调用链？
10. 哪些必须有测试或证据？

使用：`references/03_anti_mvp_preflight.md`

### Step 2: 生成 Trellis Task Contract

任务文档必须包含：

1. 背景与真实目标
2. 为什么不能简化成普通 MVP
3. 本次最小完整闭环
4. 非目标
5. 禁止降级项
6. 实现范围
7. 接入范围
8. 边界场景
9. 验收标准
10. 反偷懒验收
11. 证据计划
12. Checkpoints
13. Review 打回条件

使用：`references/02_task_contract_template.md`

### Step 3: Task Contract Review

用 reviewer 检查任务是否可执行、可验收、不可逃逸。

必须输出：

```text
PASS
```

或：

```text
FAIL
失败机制：...
必须修改：...
重写后的关键字段：...
```

使用：`references/05_review_rubric.md` 和 `prompts/trellis_task_contract_reviewer.md`

### Step 4: Implement with Checkpoints

长任务必须按 checkpoint 实施，每个 checkpoint 回填证据：

- 修改文件
- 新增/更新测试
- 运行命令
- 命令结果
- 未覆盖风险
- 下一 checkpoint 进入条件

使用：`references/06_checkpoint_workflow.md`

### Step 5: Final Evidence Report

最终输出必须包含：

- 完成了什么
- 没有做什么，为什么合理
- 修改文件列表
- 新增/更新测试
- 运行命令和结果
- 已覆盖边界场景
- 未覆盖风险
- 是否存在 TODO / placeholder / mock
- 是否满足禁止降级项

## 输出要求

你生成 Trellis 任务时，不要只写摘要，不要只写标题列表，不要用“后续优化”逃避核心任务。

如果用户的需求太大，不要直接缩成 MVP；先拆成多个完整薄片，并说明每个薄片如何独立验收。

如果用户的需求本身不清楚，先做合理假设并标明；只有关键分叉会改变任务契约时才追问。

## 和其他 Skill 的配合

若存在 `anti-overfit-collaboration`：先用它判断用户输入是否是例子、锚点、质疑或边界，不要误读需求。

若存在 `anti-overfit-reviewer`：在 Task Contract Review 后再做一次反过拟合审查，检查是否讨好用户当前判断、把例子当边界、假完成。

## 快速引用

- 第一性原理：`references/01_first_principles.md`
- 任务模板：`references/02_task_contract_template.md`
- 反 MVP preflight：`references/03_anti_mvp_preflight.md`
- 验收与证据：`references/04_acceptance_and_evidence.md`
- 审查 Rubric：`references/05_review_rubric.md`
- Checkpoint 工作流：`references/06_checkpoint_workflow.md`
- 评测样例：`references/08_eval_cases.md`
