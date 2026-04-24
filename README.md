# 思无崖 · 公开数据库

> A public, structured data foundation for value-investing research.

[English](README.en.md) · [免责声明](DISCLAIMER.md) · [贡献指南](CONTRIBUTING.md) · [变更日志](CHANGELOG.md)

---

## 这个仓库是什么

`siwuya-data` 是一个公开的研究基础设施,包含三类内容:

- **公司档案**(YAML)— 中国 / 香港 / 美国上市公司的结构化档案
  涵盖业务模型、护城河、管理层、被追踪的承诺、关键风险等维度。
- **诚信评分框架**(Python + 文档)— 一套用于评估管理层公开承诺兑现度的算法 + 方法论
- **研究模板**(Markdown)— 价值投资研究的可复用模板

**目标用户**:
- PKU-UCLA 价值投资课程的学员(用于做作业、写研究)
- 独立的价值投资研究者(作为研究基础设施)
- 任何想用 Claude Code / Claude Desktop 做公司研究的人(见下方 SKILL.md)

---

## 这个仓库的哲学

**结构开放,数据保留**。

| 在本仓库 | 不在本仓库(在 [siwuya.org](https://siwuya.org) 主站) |
|---|---|
| 公司档案 schema(数据结构) | 实时分析 / 每日 brief |
| 诚信评分算法(方法论) | 当前评分数据(结论) |
| 研究模板 | 用户行为数据 / 订阅信息 |
| 被追踪的承诺**列表**(事实) | 承诺当前**状态**(我们的判断) |

任何涉及 "X 公司今天评分多少" 的具体结论数据,**不在本仓库**。
本仓库只存:**事实(被追踪的承诺)**+ **方法(怎么算分)**,**不存结论**。

---

## 目录结构

```
siwuya-data/
├── README.md / README.en.md         # 你现在看的
├── LICENSE                          # MIT(代码) + CC-BY-SA 4.0(数据) 双协议
├── DISCLAIMER.md                    # 免责声明
├── CONTRIBUTING.md                  # 如何提交公司档案 / 修正
├── CHANGELOG.md                     # 版本变更
├── CITATION.cff                     # 学术引用格式
│
├── companies/                       # 公司档案库
│   ├── _schema/                     # JSON Schema + 校验文档
│   │   ├── company.schema.json
│   │   ├── company.example.yaml
│   │   └── VALIDATION.md
│   ├── _examples/                   # 示例档案(非真实公司,仅作模板)
│   │   └── example-company.yaml
│   ├── us/                          # 美股
│   ├── hk/                          # 港股
│   ├── cn/                          # A股
│   └── INDEX.md                     # 自动生成的全档案索引
│
├── integrity_framework/             # 诚信评分框架(Stage 4 已完工)
│   ├── METHODOLOGY.md               # 方法论(为什么这么打分)
│   ├── README.md                    # 框架使用说明
│   ├── src/                         # 算法实现(MIT)— 56 tests · 97% coverage
│   ├── tests/
│   ├── docs/                        # 4 份辅助文档(承诺定义/权重/边界案例/已知盲区)
│   └── examples/scoring_walkthrough.ipynb
│
├── templates/                       # 研究模板(Stage 5 已完工)
│   ├── company_research_template.md # 公司深度研究 8 段标准结构
│   ├── moat_assessment.md           # Pat Dorsey 五类护城河评估
│   ├── earnings_call_notes.md       # 电话会结构化纪要
│   └── bull_bear_dialectic.md       # 正反辩证(自我 debate)
│
├── skills/                          # 给 Claude Code / Desktop 用户的 SKILL(Stage 5)
│   └── value-investing-research/
│       ├── SKILL.md
│       ├── reference/               # 护城河/财务红旗/诚信信号 三份知识库
│       └── scripts/load_company.py
│
└── scripts/                         # 校验工具
    └── validate_company.py
```

---

## 快速开始

### 给研究者:用模板写一份公司研究

```bash
git clone https://github.com/duwei1018/siwuya-data
cd siwuya-data
cp templates/company_research_template.md research/xiaomi-2026-Q1.md
# 按章节填空,每段开头有填写指南注释
```

### 给 Python 用户:跑一遍诚信评分

```python
from datetime import date
from integrity_framework.src import (
    Verdict, compute_integrity_score, load_promises_from_company_yaml,
)

promises = load_promises_from_company_yaml(
    "companies/_examples/example-company.yaml"
)
verdicts = [
    Verdict(promise_id="fy24-revenue-25pct", outcome="broken",
            reasoning="FY24 实际 +18%,低于指引 7pp",
            judged_at=date(2025, 4, 30), judged_by="@your-handle"),
]
score = compute_integrity_score(verdicts, as_of=date(2026, 4, 24))
print(score.score, score.breakdown)
```

完整 walkthrough:[`integrity_framework/examples/scoring_walkthrough.ipynb`](integrity_framework/examples/scoring_walkthrough.ipynb)

### 给 Claude Code / Desktop 用户

```bash
git clone https://github.com/duwei1018/siwuya-data
cd siwuya-data
claude   # 自动加载 skills/value-investing-research/SKILL.md
# 然后:"帮我用思无崖框架研究一下小米"
```

详见 [`skills/value-investing-research/SKILL.md`](skills/value-investing-research/SKILL.md)。

---

## 谁在维护

`siwuya-data` 由 [思无崖](https://siwuya.org) 团队维护,接受社区贡献。

公司档案的内容由社区贡献(包括 admin、合作研究者、PKU-UCLA 学员等),
每份档案都带 `judged_by` 署名,责任明确。

**想加新公司档案?** 看 [CONTRIBUTING.md](CONTRIBUTING.md)。
**想纠正现有档案?** 直接发 PR,在 PR 描述里写清楚依据。

---

## 法律边界(必读)

诚信评分涉及对上市公司管理层的研究判断。本仓库通过以下设计降低法律风险:

1. **署名制** — 每个判定必须带 `judged_by` 字段
2. **协议分离** — 代码 MIT、数据 CC-BY-SA 4.0
3. **强制 DISCLAIMER** — 每份档案和每个输出都引用免责声明
4. **数据分离** — 具体评分数据**不**在本仓库,只存方法和被追踪的承诺

详见 [DISCLAIMER.md](DISCLAIMER.md)。

任何使用本仓库内容的人,使用即视为已阅读并接受免责声明。

---

## 商业模式

本仓库**永久免费 + 开源**。

[siwuya.org](https://siwuya.org) 主站当前 Beta 期间也免费,
未来如转为订阅制,会提前 30 天邮件通知。
公司档案、研究方法论、诚信框架算法**永远不会**进入付费墙。

---

## 引用

如在学术或公开文章中使用本仓库内容,请按 [CITATION.cff](CITATION.cff) 格式引用。

---

## 协议

- 代码(`integrity_framework/src/*` 等):**MIT** — 见 [LICENSE-MIT.txt](LICENSE-MIT.txt)
- 数据(`companies/*`、`templates/*`):**CC-BY-SA 4.0** — 见 [LICENSE-CC-BY-SA.txt](LICENSE-CC-BY-SA.txt)

详见 [LICENSE](LICENSE)。
