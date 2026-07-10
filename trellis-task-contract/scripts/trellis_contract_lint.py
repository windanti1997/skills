#!/usr/bin/env python3
"""Lightweight linter for Trellis task contract markdown files.

This script is intentionally conservative. It does not replace an Agent reviewer;
it catches common contract omissions and laziness signals.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "背景与真实目标",
    "为什么不能简化成普通 MVP",
    "本次最小完整闭环",
    "非目标",
    "禁止降级项",
    "实现范围",
    "边界场景",
    "验收标准",
    "反偷懒验收",
    "证据计划",
    "Checkpoints",
    "Review 打回条件",
]

SOFT_ACCEPTANCE_PATTERNS = [
    r"基本可用",
    r"功能正常",
    r"正常展示",
    r"逻辑完善",
    r"后续优化",
    r"后续再补",
    r"应该可以",
    r"理论上",
]

LAZINESS_PATTERNS = [
    r"TODO",
    r"placeholder",
    r"mock",
    r"stub",
    r"先做 MVP",
    r"简单实现",
    r"暂不考虑",
]

EVIDENCE_KEYWORDS = [
    "测试", "运行命令", "命令输出", "修改文件", "日志", "截图", "产物路径", "手动验证"
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: trellis_contract_lint.py <task-contract.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            issues.append(f"Missing required section: {heading}")

    for pattern in SOFT_ACCEPTANCE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append(f"Soft acceptance / escape phrase found: {pattern}")

    for pattern in LAZINESS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append(f"Potential laziness marker found: {pattern}")

    evidence_hits = sum(1 for kw in EVIDENCE_KEYWORDS if kw in text)
    if evidence_hits < 3:
        issues.append("Evidence plan appears weak: fewer than 3 evidence keywords found")

    checkbox_count = len(re.findall(r"- \[ \]", text))
    if checkbox_count < 5:
        issues.append("Too few checkbox acceptance items; contract may be underspecified")

    boundary_keywords = ["缺失输入", "非法输入", "空数据", "重复执行", "错误恢复"]
    boundary_hits = sum(1 for kw in boundary_keywords if kw in text)
    if boundary_hits < 3:
        issues.append("Boundary scenarios appear weak: fewer than 3 standard boundary cases found")

    if issues:
        print("FAIL: Trellis task contract lint found issues:\n")
        for i, issue in enumerate(issues, start=1):
            print(f"{i}. {issue}")
        return 1

    print("PASS: Basic Trellis task contract lint checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
