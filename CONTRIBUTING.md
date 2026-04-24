# 贡献指南 · Contributing

欢迎贡献!本仓库以社区驱动的方式建设公司档案库与诚信评分基础设施。

> **English version below.**

---

## 1. 你可以贡献什么

| 类型 | 路径 | 难度 |
|---|---|---|
| 新公司档案 | `companies/{us,hk,cn}/<ticker>.yaml` | ⭐⭐ |
| 修正现有档案错误 | 同上 | ⭐ |
| 改进 schema(增字段、调约束) | `companies/_schema/company.schema.json` | ⭐⭐⭐ |
| 改进诚信评分算法 | `integrity_framework/src/**` | ⭐⭐⭐⭐ |
| 写诚信方法论文档 | `integrity_framework/METHODOLOGY.md` | ⭐⭐⭐ |
| 添加研究模板 | `templates/**` | ⭐⭐ |
| 写 SKILL.md(给 Claude Code 用) | `skills/**` | ⭐⭐ |
| 修文档错别字、改翻译 | 任何 `*.md` | ⭐ |

---

## 2. 提交新公司档案

### Step 1 — 确认这家公司还没有

```bash
ls companies/{us,hk,cn}/<ticker>.yaml
```

如果文件已存在,改用"修正"流程(下一节)。

### Step 2 — 复制 EXAMPLE 起步

```bash
cp companies/_examples/example-company.yaml companies/us/AAPL.yaml
```

### Step 3 — 填写所有必填字段

打开 [companies/_schema/VALIDATION.md](companies/_schema/VALIDATION.md) 看每个字段的含义。

**特别注意**:
- 所有判断性字段(`reasoning_zh`、`assessment` 等)必须**附数据来源**
- `meta.reviewer` 填你的 GitHub 用户名 / 邮箱
- `integrity_tracking.tracked_promises` 列出你能找到的管理层公开承诺
  (财报会议纪要、公司公告、CEO 公开访谈等),每条带 source URL

### Step 4 — 本地校验

```bash
# Python
python scripts/validate_company.py companies/us/AAPL.yaml

# 或 Node
node scripts/validate_company.js companies/us/AAPL.yaml
```

校验通过才能提交 PR。

### Step 5 — 发 PR

PR 描述模板:

```markdown
**新公司档案**: AAPL (Apple Inc., 苹果公司)

**数据来源**:
- FY2024 10-K: https://...
- Q4 2024 earnings call: https://...
- 维基百科: https://...

**追踪承诺**: 收录了 N 条 management 公开承诺(见 yaml integrity_tracking)

**自查**:
- [ ] schema 校验通过
- [ ] 所有 reasoning_zh 都有数据来源
- [ ] 没有"投资建议"性质措辞(详见 DISCLAIMER.md §4)
- [ ] meta.reviewer 已填我的 GitHub 用户名
```

---

## 3. 修正现有档案

如果你发现现有档案有事实错误 / 数据过期 / 推理瑕疵:

1. 直接编辑对应的 yaml 文件
2. 更新 `meta.last_reviewed` 为今天
3. 在 `meta.reviewer` 后面加你的名字(用 ` + ` 连接,保留原作者历史)
4. 在 PR 描述里写清楚:**改了什么字段** + **依据是什么**

---

## 4. Review 流程

每个 PR 至少需要 1 位 maintainer 通过才能 merge。

Review 关注点:
- ✅ 数据来源真实可查
- ✅ 推理符合事实,没有"投资建议"措辞
- ✅ schema 校验通过
- ✅ `judged_by` 署名正确
- ✅ 不违反 [DISCLAIMER.md](DISCLAIMER.md)

---

## 5. 不接受的内容

- 任何"建议买/卖/持有"性质的措辞
- 没有数据来源的"判断"
- 抄袭其他付费研究报告(可以引用,不能搬运)
- 含有未公开内幕信息的内容
- 涉嫌诽谤、仇恨、骚扰的内容
- AI 生成且未经人工审核的批量档案

---

## 6. 风格约定

- 中文优先(主目标用户群),英文字段(`name_en` 等)按需填
- 字段值是**事实陈述**,不是判断;判断写在 `reasoning_zh` / `reasoning_en` 里
- 数字字段用阿拉伯数字 + 中文单位(如 `revenue_share_fy2024: 0.42`,不写"四成二")
- 链接必须是稳定 URL(避免短链、临时分享链)

---

## 7. 行为准则

我们采用 [Contributor Covenant 2.1](https://www.contributor-covenant.org/zh-cn/version/2/1/code_of_conduct/) 作为社区行为准则。

简言之:**专业、尊重、欢迎不同观点**。维护者保留对不当行为采取适当措施的权利。

---

## 8. 法律 / 版权

提交 PR 即表示你同意:

1. 你的贡献按本仓库的双协议(MIT 代码 + CC-BY-SA 数据)发布
2. 你拥有所贡献内容的版权,或你贡献的内容是合理使用的公开信息
3. 你已阅读并接受 [DISCLAIMER.md](DISCLAIMER.md)

---

# Contributing (English)

Welcome! This repository builds a community-driven company-profile library and
integrity-scoring infrastructure.

## What you can contribute

| Type | Path | Difficulty |
|---|---|---|
| New company profile | `companies/{us,hk,cn}/<ticker>.yaml` | ⭐⭐ |
| Fix existing profile | same | ⭐ |
| Improve schema | `companies/_schema/company.schema.json` | ⭐⭐⭐ |
| Improve scoring algorithm | `integrity_framework/src/**` | ⭐⭐⭐⭐ |
| Write methodology doc | `integrity_framework/METHODOLOGY.md` | ⭐⭐⭐ |
| Add research template | `templates/**` | ⭐⭐ |
| Write SKILL.md (for Claude Code) | `skills/**` | ⭐⭐ |
| Fix docs typo / translation | any `*.md` | ⭐ |

## Submitting a new company profile

1. Confirm the company doesn't already have a file
2. Copy `companies/_examples/example-company.yaml` as starting point
3. Fill in all required fields (see `companies/_schema/VALIDATION.md`)
4. Validate locally: `python scripts/validate_company.py path/to/file.yaml`
5. Open a PR with sources for every judgment-laden field

## Review

Each PR needs at least 1 maintainer approval. Reviewers check:
- ✅ Sources are real and verifiable
- ✅ Reasoning is fact-based, no "investment advice" language
- ✅ Schema validation passes
- ✅ `judged_by` byline is correct
- ✅ Does not violate [DISCLAIMER.md](DISCLAIMER.md)

## What we don't accept

- "Buy/sell/hold" language
- Judgments without sources
- Copy-paste from paid research reports
- Content with undisclosed insider information
- Defamatory / harassing content
- AI-generated profiles without human review

## Code of conduct

We follow [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
Be professional, respectful, welcoming to differing viewpoints.

## Legal

By opening a PR, you agree:

1. Your contribution is released under our dual license (MIT code + CC-BY-SA data)
2. You own the copyright, or it is fair-use public information
3. You have read and accept [DISCLAIMER.md](DISCLAIMER.md)
