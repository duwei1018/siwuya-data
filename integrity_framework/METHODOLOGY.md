# Integrity Framework Methodology · 诚信评分方法论

**版本**: v0.1.0
**起草**: Claude (Windows session, 2026-04-24)
**最终署名**: 待 @siwuya review 后定稿

> 这是一份**白皮书**,不是 marketing。结构是:这是什么、不是什么、怎么算、谁负责、怎么挑战、它哪里不行。简洁比全面重要。

---

## 1. What This Framework Is · 这套框架是什么

一套把**管理层在公开场合做出的承诺,与该承诺事后是否被兑现**这件事,**结构化、可度量、可审计地**记录下来的方法论。

输入:
- `Promise` — 一条承诺(谁、什么时候、对谁、说了什么、可量化在什么时候到期)
- `Verdict` — 一条事后的兑现判定(谁判的、什么时候判的、判定结果、推理)

输出:
- `IntegrityScore` — 0-100 的整数 + 完整 per-verdict breakdown

每个数字都能被回溯到"谁说了什么、谁判了什么、为什么"。

## 2. What This Framework Is NOT · 这套框架不是什么

> 这一节是法律边界,不是修辞。任何使用本框架的人都需要清楚下列**不是**。

- **不是投资建议**。本框架不输出"买入/卖出/持有"。任何使用本框架的人对自己的投资决策负全责。
- **不是信用评级**。本框架不是、也不试图替代任何监管批准的信用评级机构(S&P / Moody's / Fitch / 中诚信 / 大公等)。
- **不是权威裁决**。每个 `Verdict` 是**署名研究者的研究观点**,不是事实陈述,可以被任何人挑战。
- **不是道德裁判**。本框架只评估**承诺与事实之间的差距**,不对管理层的人格、动机、品德下判断。
- **不预测未来**。一个公司过去诚信记录良好,**不**意味着未来会继续如此;反之亦然。

详细见 [../DISCLAIMER.md](../DISCLAIMER.md)。

## 3. Core Concepts · 核心概念

### 3.1 Promise · 承诺

一条承诺至少必须满足:

- **公开性**:承诺被做在公开场合(招股书、财报、电话会议、官方声明、社交账号实名发言)
- **可识别说话人**:能追溯到具体人(CEO / CFO / 某指定发言人)
- **可量化或可观察的结果**:"我们会努力" 不算;"FY24 营收同比增长 25%" 算
- **可追溯的源**:必须有一个 URL、文档名、或可考证的引用

边界讨论见 [docs/01_what_is_a_promise.md](docs/01_what_is_a_promise.md)。

### 3.2 Verdict · 兑现判定

一条 verdict 必须满足:

- **署名**:`judged_by` 字段必填,不能是 `anonymous` / 空 / `unknown`(框架在构造时直接 `ValueError`)
- **解释**:`reasoning` 字段必填(任何无解释的判定无法被挑战 = 黑盒,不允许)
- **证据**:`evidence_urls` 鼓励但不强制(有些证据是私下沟通,无法公开链接)
- **判定时间**:`judged_at` 必填,用于时间衰减计算

5 种合法 outcome:

| outcome | 含义 |
|---|---|
| `fulfilled` | 承诺如期或提前完成 |
| `partial` | 部分完成 / 重大改变但非完全违背 |
| `broken` | 明显违背 / 未达标 |
| `pending` | 还未到验证窗口,无法判定 |
| `unverifiable` | 信息不足,无法形成判定 |

### 3.3 Integrity Score · 整体评分

一组 verdicts 经过算法,得到 0-100 的整数。**它不是一个公司的"诚信分",而是一个公司的"被记录承诺的兑现情况摘要"**。一份评分必须始终标注它对应的 verdict 集合 + `methodology_version`,否则数字本身没有意义。

## 4. Scoring Algorithm · 算法

```
base = 100
for each verdict:
    raw_delta = WEIGHTS[outcome]              # 见下表
    decay     = 0.5  if verdict 老于 DECAY_YEARS 年, else 1.0
    severity  = -SEVERITY_AMPLIFICATION
                if outcome == "broken" and severity_tag in 严重性放大集合, else 0.0
    final_delta = (raw_delta + severity) * decay
    score      += final_delta
score = clamp(score, 0, 100)
```

### 4.1 默认权重(v0.1.0)

| outcome | weight | 说明 |
|---|---|---|
| `fulfilled` | `0` | 兑现是基线,不奖励 |
| `partial` | `-5` | 轻微扣分 |
| `broken` | `-15` | 重扣 |
| `pending` | 跳过 | 不计入,但在 `skipped_verdicts` 中可见 |
| `unverifiable` | 跳过 | 同上 |

权重选择的理由 + 其他可能的选择 → [docs/02_weighting.md](docs/02_weighting.md)。

### 4.2 时间衰减

`DECAY_YEARS = 3`。3 年前的 verdict 半权重(`× 0.5`)。理由:管理层换、战略换、市场环境换;近期行为更有预测力。

### 4.3 严重性放大

只在 `outcome == "broken"` 且 `severity_tag` 在以下白名单时,额外扣 30 分:

- `financial_misconduct`
- `audit_qualification`
- `fraud_admission`

放大集合**故意起步狭窄**(只有这 3 个客观可考证的标签),避免方法论被当成主观情绪发泄工具。扩充走 GitHub `methodology_discussion` issue 流程。

### 4.4 截断

最终 `score` clamp 到 `[0, 100]`。一个公司无论破多少承诺,分数最低 0;无论兑现多漂亮,基线 100,不奖励。

## 5. Authorship and Accountability · 署名与责任

每个 `Verdict` 必须 `judged_by`,框架在构造时强制。`judged_by` 应该是:

- GitHub handle:`@duwei1018`
- 学术 ORCID:`0000-0001-2345-6789`
- 研究者公开身份的稳定标识

不接受:`anonymous` / `unknown` / 空字符串 / 其他无法追溯的占位。

**理由**:研究判断必须由某个具体可被反驳的人承担。匿名判断不可挑战 = 不应存在。

## 6. How to Challenge a Verdict · 怎么挑战一条 verdict

任何人对任何 verdict 持异议,走 GitHub `data_correction` issue 模板:

1. 引用具体的 `promise_id` 与原 verdict 的 `judged_by`
2. 给出反例证据(URL / 引用)
3. 说明你建议的新 outcome 与 reasoning
4. Maintainer + 原判定者会被 ping 进讨论

我们**不**保证每个反对意见都被采纳——有时分歧本身是有价值的信号。但每个反对意见都会有 maintainer review 决定是否更新。

## 7. Known Limitations · 已知盲区

> 写一份只列优点的方法论是 marketing。这份方法论必须诚实列出它的弱点。

### 7.1 承诺识别的语义模糊

"我们将努力推动 X" 算不算承诺?目前框架不接受这种,但 grey area 很多。MVP `promise_extractor` 是基于关键词的,大量真实承诺会被漏掉。

### 7.2 时间衰减参数的主观性

`DECAY_YEARS = 3` 是直觉,不是实证。等到积累 50+ 真实 verdict 后会回测调整。

### 7.3 跨文化与跨市场差异

中国 A 股、港股、美股的"指引文化"不同——美国有强 SOX/Reg FD 约束、A 股是自愿性指引、港股两者之间。同一种"未达预期"在三地的语义、合规含义都不同,本框架当前**不**对此做区分。

### 7.4 正面信号缺失

框架只惩罚违背、不奖励兑现。这意味着一个"低承诺低兑现"和"高承诺高兑现"的公司分数相同(都是 100)。这是**故意**的,但也意味着分数对"高质量沟通的公司"的区分度不足。

### 7.5 单一指标风险

把一个公司的"诚信"压缩成一个 0-100 的数字本身就是有损压缩。任何使用者都应该把分数当作**入口**,而不是**结论**——下钻到 `breakdown` 看具体每条 verdict 才有意义。

更多边界讨论 → [docs/03_edge_cases.md](docs/03_edge_cases.md) 与 [docs/04_known_limitations.md](docs/04_known_limitations.md)。

## 8. Version History · 版本演进

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1.0 | 2026-04-24 | 首版。Promise / Verdict / IntegrityScore 数据契约,基础权重 + 时间衰减 + 严重性放大。Placeholder 权重待 50 真实 verdict 回测后调整。 |

## 9. Citation · 引用

如在学术写作中引用本方法论,请使用:

```
思无崖. (2026). siwuya-data Integrity Framework, v0.1.0.
GitHub: https://github.com/duwei1018/siwuya-data
```

完整 BibTeX 见 [../CITATION.cff](../CITATION.cff)。

---

**Author**: Drafted by Claude (Windows session, 2026-04-24), to be finalized and endorsed by @siwuya on review.
