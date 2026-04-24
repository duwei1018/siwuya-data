# siwuya-data v0.1.0 — 思无崖 siwuya-data 首次公开

> 价值投资研究者的公共数据基础设施 · Public data infrastructure for value investing research

发布日期: 2026-04-24

---

## 这次发布有什么

`siwuya-data` 是一个公开的研究基础设施,首版交付三块:

### 📂 公司档案库(JSON Schema + 校验工具)

- 完整的公司档案 JSON Schema(11 顶级字段:meta / identity / classification / segments / business_model / moat / management / integrity_tracking / key_risks / further_reading / disclaimer)
- 包含一份 EXAMPLE 公司虚构档案(`companies/_examples/example-company.yaml`)用于格式参考
- Python 校验工具(`scripts/validate_company.py`)
- 真实公司档案由社区贡献(走 GitHub PR 流程,详见 [CONTRIBUTING](CONTRIBUTING.md))

### ⚖️ 诚信评分框架(算法 + 方法论)

- 一套用于评估**管理层公开承诺兑现度**的算法 + 完整方法论文档
- 三个核心数据结构:`Promise`(被追踪的承诺,基于事实)、`Verdict`(署名研究者的判定)、`IntegrityScore`(0-100 + 完整 breakdown)
- 算法 v0.1.0:基础权重(broken -15 / partial -5)+ 时间衰减(3 年半权重)+ 严重性放大(financial_misconduct 等 -30)
- **强制 audit trail**:每个 Verdict 必须有 `judged_by`(拒绝匿名)+ `reasoning`(拒绝空)
- 56 个单元测试 · 97% 行覆盖率
- 完整 [METHODOLOGY.md](integrity_framework/METHODOLOGY.md)(2400+ 字白皮书,含已知盲区)+ 4 份辅助文档(承诺定义 / 权重背书 / 边界案例 / 已知盲区)
- 端到端 [scoring_walkthrough.ipynb](integrity_framework/examples/scoring_walkthrough.ipynb)

### 📝 研究模板 + Claude Skill

4 份 Markdown 研究模板(均为可填空表单 + Markdown 灵活):

- `company_research_template.md` — 公司深度研究 8 段标准结构(6000-8000 字篇幅)
- `moat_assessment.md` — Pat Dorsey 五类护城河完整评估表
- `earnings_call_notes.md` — 单次电话会结构化纪要(可直接喂给诚信框架)
- `bull_bear_dialectic.md` — 强制正反辩证(避免 anchor bias)

一份 `skills/value-investing-research/SKILL.md` 给 Claude Code / Claude Desktop 用户开箱即用,加载 3 份 reference 知识库(护城河类型 / 财务危险信号 / 诚信信号)。

---

## 这次发布**不**有什么

为了清楚预期,刻意**不**包含:

- ❌ 任何"某公司当前评分多少"的具体数据(数据在 [siwuya.org](https://siwuya.org) 主站)
- ❌ 实时财务数据(股价 / 市值 / 每日 brief)
- ❌ 任何"买入 / 卖出 / 持有"建议(本仓库不提供投资建议)
- ❌ 真实公司档案(等社区 PR 贡献,详见 CONTRIBUTING)
- ❌ 外部 API 调用(本仓库零依赖网络,纯方法论库)

---

## 怎么用(三种入口)

**给研究者**:

```bash
git clone https://github.com/duwei1018/siwuya-data
cp templates/company_research_template.md research/your-target.md
# 按章节填空,每段开头有填写指南注释
```

**给 Python 用户**:

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
            reasoning="FY24 +18%, missed by 7pp",
            judged_at=date(2025, 4, 30), judged_by="@your-handle"),
]
score = compute_integrity_score(verdicts)
print(score.score, score.breakdown)
```

**给 Claude Code / Desktop 用户**:

```bash
git clone https://github.com/duwei1018/siwuya-data && cd siwuya-data
claude   # 自动加载 skills/value-investing-research/SKILL.md
# 然后提问:"帮我用思无崖框架研究一下小米"
```

---

## 路线图

| 版本 | 计划 |
|---|---|
| v0.1.0 | ✅ 当前 |
| v0.2.0 | LLM-backed promise extractor(下游集成接口);Node/TS 镜像;真实 50+ verdict backtest 后调整算法权重 |
| v0.3.0 | 跨市场(中港美)算法差异化;methodology v0.2(基于实证调整) |

---

## 协议

- **代码**(`integrity_framework/src/` / `scripts/` / `skills/.../scripts/`):**MIT License**
- **数据 + 文档**(`companies/` / `templates/` / METHODOLOGY / docs / SKILL.md):**CC-BY-SA 4.0**

详见 [LICENSE](LICENSE) 与 [DISCLAIMER](DISCLAIMER.md)。

---

## 致谢

- Pat Dorsey, *The Little Book That Builds Wealth* (2008) — 五类护城河框架
- PKU-UCLA 价值投资课程的学员社区,本仓库的预期主要用户
- 所有提 GitHub Issue / PR 提出意见的研究者

---

## 贡献

任何人都可以贡献:

- **新增公司档案**:走 GitHub Issue → fork → PR(详见 [CONTRIBUTING](CONTRIBUTING.md))
- **修正 / 数据纠错**:`data_correction` issue 模板
- **方法论讨论**:`methodology_discussion` issue 模板

每份贡献都带 `judged_by` 署名,责任明确。

---

## 联系

- GitHub Issues: 任何问题、bug、建议
- Email: 见 [CITATION.cff](CITATION.cff) 维护者邮箱

---

**重要声明**:本仓库不提供投资建议。所有内容仅用于教育与研究目的。
请在使用任何内容前阅读 [DISCLAIMER.md](DISCLAIMER.md)。
