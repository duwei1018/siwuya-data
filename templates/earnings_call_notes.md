<!--
模板:电话会议结构化纪要 · v0.1.0 · siwuya-data templates · CC-BY-SA 4.0

填写指南
- 一次电话会一份纪要
- 重点不是"全文转录",而是"提取信号"
- 必须把所有量化承诺/指引拎出来,可直接喂给 integrity_framework 做 promise tracking
-->

# {公司中文名} {YYYY} Q{N} 电话会纪要

**ticker**: {ticker}
**会议日期**: {YYYY-MM-DD}
**研究者**: {@your-handle}
**transcript 来源**: {URL}
**模板**: siwuya-data earnings_call_notes v0.1.0

---

## 0. 一段话总结

<!--
填写指南:
- 不超过 100 字
- 必须包括:管理层情绪 / 最重要的一个数字 / 最重要的一个新承诺(如果有)
-->

(总结)

---

## 1. 数据回顾(管理层口径)

<!--
填写指南:
- 列管理层在开场白中强调的 3-5 个数字
- 必须有 source(transcript 段落 / slide page),便于回查
-->

| 指标 | 本季度 | 同比 | 管理层评论 | source |
|---|---|---|---|---|
| 营收 | | | | |
| 利润 | | | | |
| 自由现金流 | | | | |

---

## 2. 量化承诺 / 指引(★ 关键 — 喂 integrity_framework)

<!--
填写指南:
- 每条承诺独立列,提取为可入 schema 的字段
- 这些会成为 companies/<market>/<slug>.yaml 的 tracked_promises[]
-->

| ID | 承诺(中文) | promise_en | source | made_on | due_by | verification_type |
|---|---|---|---|---|---|---|
| {slug-1} | | | | | | financial_metric / product_launch / ... |
| {slug-2} | | | | | | |

---

## 3. 战略 / 业务讨论亮点

<!--
填写指南:
- 不要 paraphrase 整段,挑你认为重要的 3-5 个 quote
- 每个 quote 给说话人 + 一句话评论(为什么你认为重要)
-->

### 3.1 {主题 1}

> "{quote}" — {speaker name + role}

reasoning_zh: 我认为这段重要因为 ...

### 3.2 {主题 2}

> "{quote}" — {speaker name + role}

reasoning_zh: ...

---

## 4. Q&A 精选

<!--
填写指南:
- Q&A 是电话会最有信息量的部分(因为非脚本)
- 挑 2-4 个最尖锐的问题
- 不只是 paraphrase 答案,要看"管理层有没有正面回答"
-->

### Q1: {分析师姓名 / 机构} — {问题摘要}

**A**: {管理层回答摘要}

reasoning_zh: 管理层是否正面回答了?信号是 ...(直球 / 太极 / 转移话题)

### Q2: ...

---

## 5. 管理层情绪 / 沟通质量

<!--
填写指南:
- 主观判断,但要有依据
- 不仅是"乐观/悲观",还要看"是否承认弱点 / 是否给具体数字 / 是否避谈"
-->

| 维度 | 评估 |
|---|---|
| 整体情绪 | 乐观 / 中性 / 谨慎 / 防守 |
| 是否承认弱点? | 主动 / 被问到才承认 / 回避 |
| 是否给具体数字? | 详细 / 一般 / 模糊 |
| 主导发言人 | CEO / CFO / 其他 |

reasoning_zh: 这次电话会沟通质量是 ...

---

## 6. 我的 takeaways

<!--
填写指南:
- 3-5 条
- 每条:这个 takeaway 改变了你之前对这家公司的什么判断(或没改变)
-->

- ...
- ...

---

## 7. 待跟踪事项

<!--
填写指南:
- 下次电话会(Q+1)要重点关注什么
- 哪些承诺到期需要 verdict
-->

- 下季度关注:
  - ...
- 到期 promise 待 verdict:
  - {promise_id} - 到期 {YYYY-MM-DD}

---

## Disclaimer

本纪要为研究者(`{@your-handle}`)的个人记录与判断,**不构成投资建议**。所有引用均出自 `{transcript 来源}`,引用准确性由研究者负责。

详见仓库 [DISCLAIMER.md](../DISCLAIMER.md)。

---

**模板**: [`siwuya-data templates/earnings_call_notes v0.1.0`](https://github.com/duwei1018/siwuya-data) · CC-BY-SA 4.0
