# 与反过拟合协作协议集成

如果项目中有 anti-overfit-collaboration / anti-overfit-reviewer，本 Skill 应与它们形成流水线。

## 推荐流水线

```text
用户需求
→ anti-overfit-collaboration：判断输入类型，不把例子当边界
→ trellis-task-contract：生成不可逃逸任务契约
→ trellis-task-contract-reviewer：审查任务契约
→ implement
→ checkpoint verifier
→ anti-overfit-reviewer：最终检查是否假完成/讨好/过拟合
```

## 关键衔接点

### 1. 用户说“其他 / 类似 / 比如”

先由 anti-overfit 判断：这是开放集合，不是封闭边界。

再由 trellis-task-contract 抽象成任务类别和完整闭环。

### 2. 用户说“继续”

不能直接 implement。先检查当前任务契约是否仍然有效，是否有目标衰减。

### 3. 用户说“不要只做 MVP”

触发 anti-MVP preflight，必须定义本次最小完整闭环和禁止降级项。

### 4. 用户局部批评任务不严格

不要只加几条验收项。必须重审任务契约机制：目标、范围、证据、打回条件是否都弱。

## 共享失败模式

- 例子当边界
- 质疑当结论
- 继续当无条件执行
- 不要 X 走向反面极端
- 局部修补替代系统修复
- MVP 化
- 壳子化
- TODO 化
- 自证化
- 软验收
