# 免责声明 · Disclaimer

**最后更新**: 2026-04-24
**适用范围**: `siwuya-data` 仓库内全部内容,以及任何下游使用本仓库数据的产品(包括 [siwuya.org](https://siwuya.org))

> **English version below.**

---

## 1. 研究性质

`siwuya-data` 包含的所有公司档案、承诺追踪、诚信评分算法、研究模板,
均为我们对**公开信息**进行**结构化整理与判断**的研究成果,
目的是为价值投资研究者提供可反复回看的长期参考底稿。

任何内容的呈现形式(YAML 字段、JSON Schema、文档段落等)都是
"研究记录" 而非 "权威结论"。

## 2. 不构成投资建议

本仓库任何内容都**不构成**对任何证券、衍生品或其他金融产品的购买、持有、
出售建议,也不构成任何形式的财务、税务、法律意见。

投资决策应当基于读者**自身的判断**与**具备资质的专业人士提供的建议**。

## 3. 数据局限

本仓库使用的所有数据均来自公开渠道(交易所披露、公司财报、监管文件、
公开报道等)。我们尽力保证数据的及时性与准确性,但**不对其完整性、
无错性、无遗漏**作任何承诺。

数据具有**时效性**:档案最后审阅日期(`meta.last_reviewed`)之后,
公司情况可能已发生变化。

如发现错误,欢迎通过 GitHub Issue 或 PR 指正。

## 4. 判断的边界

诚信评分、承诺兑现度评估等判断性内容均带有作者署名(`judged_by`)与
推理过程(`reasoning_zh` / `reasoning_en`),欢迎挑战与讨论。

我们**不主张**这些判断是终局结论,而是将其作为**可被反驳的工作假设**呈现。

下游使用者(包括 siwuya.org 主站)在展示这些判断时,**必须**:
- 保留 `judged_by` 字段不被截断
- 在显著位置链接回本免责声明
- 不得将研究判断重写为"投资建议"性质的措辞

## 5. 立场披露

本仓库的贡献者及其关联方可能持有或交易所讨论公司的证券。这种持仓不会
改变研究判断,但读者应当知晓这一可能性。

任何具体公司档案中如有重大持仓披露,会在该档案的 `disclaimer` 字段中明示。

## 6. 责任限制

在任何情况下,本仓库的维护者、贡献者及其关联方,均**不对**任何使用本仓库
内容(直接或间接)所导致的损失承担任何责任,包括但不限于投资损失、
名誉损失、机会成本损失等。

使用本仓库,即表示使用者同意承担所有相关风险。

## 7. 第三方数据来源

本仓库引用的第三方资料(财报、公告、监管文件、媒体报道等)的著作权属于
原始权利人。本仓库的引用属于**合理使用**(以研究、评论、教育为目的),
但下游使用者在二次引用时,需自行判断合理使用边界。

## 8. 协议关系

本免责声明是本仓库 [LICENSE](LICENSE)(MIT + CC-BY-SA 4.0)的**补充约束**。
当协议许可的使用方式与本声明产生冲突时,**以本声明为准**。

## 9. 变更

本声明可能随仓库演进而更新,以本文件最新版本为准。
重大变更会在 [CHANGELOG.md](CHANGELOG.md) 中记录。

---

# Disclaimer (English)

**Last updated**: 2026-04-24
**Applies to**: all content in the `siwuya-data` repository, and any downstream
product that uses this data (including [siwuya.org](https://siwuya.org)).

## 1. Research nature

All content in `siwuya-data` — company profiles, promise tracking, integrity-scoring
algorithms, research templates — represents **structured records and judgments** we
have made based on **publicly available information**. Its purpose is to provide
value-investing researchers with a long-term, reviewable working notebook.

The presentation format (YAML fields, JSON Schema, documentation prose) is
"research record", not "authoritative conclusion".

## 2. Not investment advice

Nothing in this repository constitutes a recommendation to buy, hold, or sell any
security, derivative, or other financial product. It does not constitute financial,
tax, or legal advice in any form.

Investment decisions must be based on the reader's **own judgment** and advice from
**qualified professionals**.

## 3. Data limitations

All data used here is from public sources. We make best efforts on timeliness and
accuracy but make **no guarantees** of completeness, correctness, or absence of
omissions.

Data has a time horizon: after a profile's `meta.last_reviewed` date, the company's
situation may have changed.

Corrections welcome via GitHub Issue or PR.

## 4. Boundaries of judgment

Judgment-laden content (integrity scores, promise-fulfillment assessments) carries
an author byline (`judged_by`) and reasoning (`reasoning_zh` / `reasoning_en`), and
is open to challenge.

We do not claim these are final conclusions; they are **falsifiable working
hypotheses**.

Downstream users (including the siwuya.org main site) **must**, when displaying
these judgments:
- preserve the `judged_by` field
- prominently link back to this disclaimer
- not re-render research judgments as "investment recommendation" language

## 5. Position disclosure

Contributors and their affiliates may hold or trade securities of discussed companies.
This does not change research judgments, but readers should be aware. Material position
disclosures, if any, will be in the `disclaimer` field of the relevant profile.

## 6. Limitation of liability

Under no circumstances shall the maintainers, contributors, or affiliates be liable
for any loss arising from use of this repository's content, including but not limited
to investment losses, reputational losses, or opportunity costs.

Use of this repository constitutes acceptance of all related risks.

## 7. Third-party material

Third-party material cited (financial reports, filings, regulatory documents, media
reports) belongs to the original rights holders. Citation here is for research,
commentary, and educational purposes (fair use), but downstream users must judge
fair-use boundaries themselves when re-citing.

## 8. Relationship to license

This disclaimer is a **supplemental constraint** to the [LICENSE](LICENSE)
(MIT + CC-BY-SA 4.0). Where license permissions conflict with this disclaimer,
**this disclaimer prevails**.

## 9. Changes

This disclaimer may be updated as the repository evolves. The latest version of
this file is authoritative. Significant changes will be recorded in
[CHANGELOG.md](CHANGELOG.md).
