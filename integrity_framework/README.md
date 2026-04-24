# 诚信评分框架 · Integrity Framework

> 一套用于评估上市公司**管理层公开承诺兑现度**的算法 + 方法论。

**版本**: v0.1.0(由 Claude 起草,等 @siwuya 最终署名)
**协议**: 代码 MIT(`src/`)· 文档 + 方法论 CC-BY-SA 4.0(`METHODOLOGY.md` / `docs/` / `examples/`)

---

## 这是什么

一个**纯算法 + 纯方法论**的库:

- **输入**:管理层在公开场合(财报、电话会、媒体)做出的承诺(`Promise`),加上事后某个署名研究者对承诺兑现情况的判定(`Verdict`)
- **输出**:一个 0-100 的整数评分 + 完整可审计的明细(`IntegrityScore`)

它**不是**信用评级,**不是**监管评估,**不构成**投资建议——见 [DISCLAIMER](../DISCLAIMER.md)。

## 这是什么 ≠ 这不是什么

| 是 | 不是 |
|---|---|
| 一套**可被挑战**的方法论 | 权威裁决 |
| 算法 + 数据契约 + 测试覆盖 | 实时评分服务 |
| 任何研究者都能 fork + 改权重 + 重新跑 | 黑盒 |
| 每条 verdict 都强制带 `judged_by` 与 `reasoning` | 匿名打分 |

## 五分钟上手

```python
from datetime import date
from integrity_framework.src import (
    Promise, Verdict,
    compute_integrity_score,
    load_promises_from_company_yaml,
)

# 1. 从公开公司档案读出被追踪的承诺
promises = load_promises_from_company_yaml("companies/_examples/example-company.yaml")

# 2. 由你(署名研究者)给出 verdict
verdicts = [
    Verdict(
        promise_id="fy24-revenue-25pct",
        outcome="broken",
        reasoning="FY24 实际 +18%,低于指引 7pp",
        judged_at=date(2025, 4, 30),
        judged_by="@your-handle",
        evidence_urls=("https://example.com/fy24-results",),
    ),
]

# 3. 算分
score = compute_integrity_score(verdicts, as_of=date(2026, 4, 24))
print(score.score, score.breakdown)
```

完整端到端 walkthrough:[examples/scoring_walkthrough.ipynb](examples/scoring_walkthrough.ipynb)

## 目录

```
integrity_framework/
├── README.md                          ← 你正在读
├── METHODOLOGY.md                     ← 算法方法论(白皮书)
├── src/
│   ├── __init__.py                    ← public API
│   ├── models.py                      ← Promise / Verdict / IntegrityScore
│   ├── scorer.py                      ← compute_integrity_score
│   ├── promise_extractor.py           ← MVP 文本→Promise 提取
│   └── loader.py                      ← YAML ↔ dataclass 适配器
├── tests/                             ← pytest 56 tests · 97% coverage
├── docs/
│   ├── 01_what_is_a_promise.md        ← 什么算承诺、什么不算
│   ├── 02_weighting.md                ← 权重为什么这么设
│   ├── 03_edge_cases.md               ← 边界案例
│   └── 04_known_limitations.md        ← 框架的盲区
└── examples/
    └── scoring_walkthrough.ipynb      ← 端到端跑一遍
```

## 设计原则

1. **结构化承诺** — 算法只消费 schema 中 `integrity_tracking.tracked_promises[*]`,不直接吃自由文本
2. **可解释** — 每条评分有完整 breakdown,任何人 30 秒内能搞清"为什么是这个分"
3. **署名制** — 每个 verdict 强制带 `judged_by`,匿名打分会在构造时直接 `ValueError`
4. **可挑战** — 任何 verdict 可被 GitHub Issue 提出反例,见 [methodology_discussion.yml](../.github/ISSUE_TEMPLATE/methodology_discussion.yml)(Stage 6 上线)
5. **方法论开源,数据闭源** — 算法在本仓库,具体公司当前评分在 [siwuya.org](https://siwuya.org) 主站

## 安装与依赖

仅需 stdlib + PyYAML(用 loader 时):

```bash
pip install pyyaml
```

测试 + 覆盖率:

```bash
pip install pytest pytest-cov
python -m pytest integrity_framework/tests/ --cov=integrity_framework/src
```

## 提出疑问 / 修正

发现某条权重值得讨论,或某个 verdict 你不认同?走这两条:

- **方法论分歧**(动算法/权重/阈值):提 GitHub Issue,标 `methodology` label
- **具体 verdict 异议**(不动方法论,改具体判断):走 `data_correction` issue 模板

详见 [CONTRIBUTING](../CONTRIBUTING.md)。

## 版本

| 版本 | 状态 | 说明 |
|---|---|---|
| v0.1.0 | 当前 | 首版,placeholder 权重待 50 条真实 verdict 后回测 |
| v0.2.0 | 规划 | 接 LLM-backed extractor;加 Node/TS 版镜像实现 |
