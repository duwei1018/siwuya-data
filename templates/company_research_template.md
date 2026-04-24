<!--
模板:公司深度研究 · v0.1.0 · siwuya-data templates · CC-BY-SA 4.0

填写指南
- 8 段标准结构,顺序固定
- 每段开头的 HTML 注释是给填写者的指南,Markdown 渲染时不显示
- 所有判断性结论必须带 `reasoning_zh:` 字段(中文一两句话说明依据)
- 所有数据必须有 `source:` URL
- 末尾 Disclaimer 段不能删
-->

# {公司中文名} 公司深度研究

**ticker**: {US/HK/CN ticker}
**研究者**: {你的 GitHub handle 或公开身份}
**起草日期**: {YYYY-MM-DD}
**最后更新**: {YYYY-MM-DD}
**版本**: 0.1
**模板**: siwuya-data company_research_template v0.1.0

---

## 0. TL;DR · 一段摘要

<!--
填写指南:
- 不超过 200 字
- 必须包含:这家公司是做什么的(1 句)、它的核心护城河(1 句)、当前你最大的疑问/担忧(1 句)、你的当前结论(1 句)
- 不要在这段里给"买入/卖出"建议(本仓库不提供投资建议)
- 这段是写给"只看 30 秒"的人,后面所有内容是给"愿意看 30 分钟"的人
-->

(在此填写 200 字内 TL;DR)

---

## 1. 业务全景 · What Does This Company Do

<!--
填写指南:
- 用人话讲一遍:这家公司怎么赚钱?谁是客户?最近一份财报披露的业务分部 + 收入占比?
- 给一张分部表(中文 markdown table)
- 不要复制公司官网的 marketing copy,要用自己的话
-->

### 1.1 业务分部 · Segments

| 分部 | 收入占比 | 主要客户 | source |
|---|---|---|---|
| {分部 A} | {%} | {B2B / B2C / 政企} | {URL} |
| {分部 B} | {%} | ... | ... |

### 1.2 主营业务一句话总结

(reasoning_zh: 这家公司的核心业务是 ...)

---

## 2. 护城河 · Moat

<!--
填写指南:
- 这段可以引用 `templates/moat_assessment.md` 的完整评估
- 至少要回答:这家公司的护城河是 Pat Dorsey 五类的哪一类(网络效应 / 转换成本 / 品牌 / 成本优势 / 政府许可),还是没有?
- 给出"如果护城河被攻击,信号会是什么"——这是判断未来护城河走势的 leading indicator
-->

### 2.1 当前护城河类型

(选一类或多类:network_effect / switching_cost / brand / cost_advantage / regulatory_moat / none)

reasoning_zh: ...

### 2.2 护城河强度(主观 1-10)

(给一个数字 + 理由)

reasoning_zh: ...

### 2.3 护城河被攻击的早期信号

- ...
- ...

---

## 3. 财务画像 · Financial Profile

<!--
填写指南:
- 选 5 个最相关的财务指标(不要堆 50 个),每个给 3-5 年序列
- 必须包含:营收增速 / 毛利率 / 营业利润率 / 自由现金流 / ROIC(若可算)
- 都要附 source URL(招股书 / 财报 / 年报)
- 不要复制粘贴整张利润表,选你认为重要的几个数
-->

### 3.1 关键指标 5 年序列

| 指标 | FY{Y-4} | FY{Y-3} | FY{Y-2} | FY{Y-1} | FY{Y} | source |
|---|---|---|---|---|---|---|
| 营收(亿元) | | | | | | |
| 营收同比增长 | | | | | | |
| 毛利率 | | | | | | |
| 营业利润率 | | | | | | |
| 自由现金流 | | | | | | |

### 3.2 一段话财务总结

(reasoning_zh: 这家公司的财务画像是 ...)

---

## 4. 管理层 · Management

<!--
填写指南:
- 列核心 3-5 位管理层(CEO / CFO / 关键创始人或核心高管)
- 每人:加入年份 + 此前主要经历 + 关键决策(他/她任内做过的最关键 2-3 个决策)
- 不要写"履历表",要写"过去 5 年他/她做了什么、说了什么"
- 引用必须是公开来源(财报 / 媒体 / 公开演讲)
-->

### 4.1 核心管理层

| 姓名 | 角色 | 加入年份 | 此前经历 | source |
|---|---|---|---|---|
| {姓名} | CEO | | | |
| {姓名} | CFO | | | |

### 4.2 关键决策追踪

- {决策 1}: {做了什么} · reasoning_zh: 我认为这个决策的意义是 ...
- {决策 2}: ...

---

## 5. 管理层诚信追踪 · Integrity Tracking

<!--
填写指南:
- 这段是 siwuya-data 仓库的特色——把管理层公开承诺与兑现情况结构化记录
- 至少列 3-5 条最近 2 年的可考证承诺(招股书 / 财报指引 / 电话会 / 公开声明)
- 每条承诺独立记一次 verdict
- verdict 必须带 reasoning(为什么是 fulfilled/partial/broken)+ source URL
- 算分用 integrity_framework: `from integrity_framework.src import compute_integrity_score`
-->

### 5.1 被追踪的承诺(最近 2 年)

| ID | 承诺(摘要) | 来源 | 到期 | Verdict | reasoning_zh |
|---|---|---|---|---|---|
| {slug-1} | | | | fulfilled / partial / broken / pending / unverifiable | |
| {slug-2} | | | | | |

### 5.2 总体诚信评分(可选)

如果你想算个分:

```python
from datetime import date
from integrity_framework.src import Verdict, compute_integrity_score
verdicts = [Verdict(promise_id="...", outcome="...", reasoning="...", judged_at=date(...), judged_by="@you"), ...]
score = compute_integrity_score(verdicts)
print(score.score, score.breakdown)
```

reasoning_zh: 我对这家管理层诚信的总体看法是 ...

---

## 6. 关键风险 · Key Risks

<!--
填写指南:
- 至少 3 条,排序按你认为的严重性
- 每条:风险描述 + 触发场景 + 你的对冲思路(如果有)
- 不要列"经济周期下行"这种通用风险——要 company-specific
-->

### 6.1 风险列表

| # | 风险描述 | 触发场景 | reasoning_zh |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## 7. 估值思路 · Valuation Approach

<!--
填写指南:
- 这段不是"算估值",而是"我用什么思路判断当前估值"
- 列 2-3 种你考虑的估值锚(P/E peer / DCF assumption / SOTP / EV/Sales)
- 关键不是数字,是"我的关键 assumption 是什么"
- 不要给"目标价"——本仓库不提供投资建议
-->

### 7.1 估值锚

- {锚 1}: 用什么方法 + 关键 assumption · reasoning_zh: ...
- {锚 2}: ...

### 7.2 我最不确定的输入

(reasoning_zh: 上面所有 assumption 中,我最没把握的是 ... 因为 ...)

---

## 8. 进一步阅读 · Further Reading

- [{招股书 / 关键年报}]({URL})
- [{核心媒体报道}]({URL})
- [{管理层关键演讲}]({URL})

---

## Reasoning Trail

<!--
填写指南:
- 这段是给读者审计你的判断用的
- 列出你做这份研究最依赖的 3-5 个 source
- 列出你曾经持有但又放弃的判断(为什么放弃)
- 这是诚实的研究者标志
-->

- 我最依赖的 sources:
  - ...
- 我曾经判断过但后来改变想法的:
  - ...

---

## Disclaimer

本研究为研究者(`{@your-handle}`)的个人研究判断,**不构成投资建议**。所有内容基于截至 `{研究日期}` 的公开信息,可能已过时。读者应独立验证所有内容并形成自己的结论。

详见仓库 [DISCLAIMER.md](../DISCLAIMER.md)。

---

**模板**: [`siwuya-data templates/company_research_template.md v0.1.0`](https://github.com/duwei1018/siwuya-data) · CC-BY-SA 4.0
