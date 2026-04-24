# 公司档案 Schema 字段说明

> 本文件是 [`company.schema.json`](company.schema.json) 的人类可读版本。
> 想新增/修改公司档案前必读。

---

## 顶层字段

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `_example` | 否 | bool | 仅 EXAMPLE 用,为 `true` 时主站列表会过滤掉。**真实公司档案不要加这个字段。** |
| `meta` | ✅ | object | 元数据(版本、审阅者、时效) |
| `identity` | ✅ | object | 身份(代码、名称、上市信息) |
| `classification` | ✅ | object | 行业归类 + 一句话商业模式 |
| `segments` | 否 | array | 业务分部(可省略,小公司可能没有) |
| `business_model` | ✅ | object | 营收引擎、成本结构、单位经济性 |
| `moat` | ✅ | object | 护城河评估(Pat Dorsey 框架) |
| `management` | ✅ | object | 管理层 + 治理 |
| `integrity_tracking` | ✅ | object | 被追踪的承诺列表 + scoring 数据指针 |
| `key_risks` | ✅ | array | 关键风险(至少 1 项) |
| `further_reading` | ✅ | object | 一手 + 三方资料 |
| `disclaimer` | ✅ | string | 免责声明(通常引用顶级 DISCLAIMER.md) |

---

## meta — 元数据

| 字段 | 必填 | 格式 | 例 |
|---|---|---|---|
| `schema_version` | ✅ | SemVer | `"0.1.0"` |
| `last_reviewed` | ✅ | YYYY-MM-DD | `"2026-04-24"` |
| `reviewer` | ✅ | string | `"alice"` 或 `"alice + bob"` |
| `data_freshness_note` | ✅ | string | `"FY2024 年报 + 2025 Q1 季报"` |

---

## identity — 身份

| 字段 | 必填 | 格式 | 例 |
|---|---|---|---|
| `primary_ticker` | ✅ | string | `"AAPL.US"` `"0700.HK"` `"600519.SH"` |
| `aliases` | ✅ | string[] | `["AAPL", "Apple", "苹果公司"]` |
| `name_zh` | ✅ | string | `"苹果"` `"腾讯"` |
| `name_zh_full` | 否 | string | `"苹果公司"` |
| `name_en` | ✅ | string | `"Apple Inc."` |
| `slug` | ✅ | URL slug | `"apple"` `"kweichow-moutai"` |
| `exchange` | ✅ | enum | `NASDAQ`/`NYSE`/`HKEX`/`SSE`/`SZSE`/... |
| `listing_date` | ✅ | YYYY-MM-DD | `"1980-12-12"` |
| `fiscal_year_end` | ✅ | MM-DD | `"12-31"` `"09-30"` `"03-31"` |
| `reporting_currency` | ✅ | ISO 4217 | `"USD"` `"HKD"` `"CNY"` |
| `hq_country` | ✅ | ISO 3166-1 α-2 | `"US"` `"CN"` `"HK"` |
| `hq_city` | ✅ | string | `"Cupertino"` `"深圳"` |
| `website` | ✅ | URL | `"https://apple.com"` |
| `ir_website` | 否 | URL | `"https://investor.apple.com"` |

`slug` 规则:小写字母+数字+连字符,首尾必须是字母或数字,**一旦定下不要改**(主站 URL 依赖)。

---

## classification — 分类

| 字段 | 必填 | 长度 | 例 |
|---|---|---|---|
| `gics_sector` | ✅ | - | `"Information Technology"`(GICS 11 大类之一) |
| `gics_industry_group` | ✅ | - | `"Software & Services"`(GICS 24 个之一) |
| `primary_business_zh` | ✅ | - | `"消费电子 + 服务订阅"` |
| `business_one_liner_zh` | ✅ | ≤60 字 | 中文电梯演讲(主站列表页直接用这个) |
| `business_one_liner_en` | ✅ | ≤120 字符 | 英文 elevator pitch |

GICS 分类参考:https://www.msci.com/our-solutions/indexes/gics

---

## segments — 业务分部(可选)

每个分部:

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 分部名 |
| `revenue_share_fy2024` | 否 | 0.0~1.0 之间的浮点数(占比),所有 segments 合计 ≈ 1.0 |
| `margin_profile` | 否 | 文字描述毛利/利润率(如 "高毛利低增长") |
| `note` | 否 | 其他备注 |

---

## business_model — 商业模式

| 字段 | 必填 | 说明 |
|---|---|---|
| `revenue_engines` | ✅ | string[] 至少 1 项,营收引擎(如 "硬件销售"/"广告"/"订阅") |
| `cost_structure_notes` | ✅ | 成本结构关键点 |
| `unit_economics_highlights` | ✅ | string[] 至少 1 项,单位经济性要点(LTV/CAC、ARPU、Take Rate 等) |

---

## moat — 护城河

`assessment`: `narrow` / `wide` / `none` / `unclear`

`types`(至少 1 项):
- `type`: `network_effects` / `switching_costs` / `intangible_assets` / `cost_advantage` / `efficient_scale` / `other`
- `strength`: `weak` / `moderate` / `strong`
- `reasoning_zh`: 中文推理,**必须附数据来源**

`pat_dorsey_framework`: 自由 key-value 对,通常包含 5 维:
- `intangible_assets`
- `switching_costs`
- `network_effects`
- `cost_advantage`
- `efficient_scale`

---

## management — 管理层

`chairman_ceo`(主席/CEO):
| 字段 | 必填 | 例 |
|---|---|---|
| `name_zh` | ✅ | `"蒂姆·库克"` |
| `name_en` | ✅ | `"Tim Cook"` |
| `tenure_since` | ✅ | `"2011-08-24"` |
| `background_brief` | ✅ | 履历要点 |

`key_executives`: 数组,每项至少有 `name_zh` + `role`,可选 `name_en`。

`governance_notes`: 公司治理关键点(双层股权、独立董事比例、关联交易、审计委员会等)。

---

## integrity_tracking — 承诺追踪(本仓库的核心创新)

`tracked_promises`(数组),每条:

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | 稳定 slug,如 `"fy24-revenue-25pct"`(一旦定下**不要改**) |
| `promise_zh` | ✅ | 承诺中文整理 |
| `promise_en` | 否 | 承诺英文原文 |
| `source` | ✅ | URL,数据来源(财报/公告/transcript) |
| `made_on` | 否 | YYYY-MM-DD,承诺做出日期 |
| `due_by` | 否 | YYYY-MM-DD,承诺到期日 |
| `verification_type` | ✅ | `financial_metric` / `product_launch` / `strategic_initiative` / `ESG_target` / `other` |

`scoring_data_location`: URL,指向主站(siwuya.org)展示当前评分的页面。

**重要**:本仓库**只记录承诺事实**,不记录"承诺是否兑现"的判断。判断在 siwuya.org 主站。

---

## key_risks — 关键风险

至少 1 项,每项:

| 字段 | 必填 | 说明 |
|---|---|---|
| `category` | ✅ | `regulatory` / `competitive` / `technology` / `macro` / `geopolitical` / `execution` / `governance` / `ESG` / `financial` / `other` |
| `risk_zh` | ✅ | 中文风险描述 |

---

## further_reading — 延伸阅读

`primary_sources`(一手资料):
- `title` ✅
- `url` ✅(必须是稳定 URL,不要短链)

`third_party_research`(三方研究):
- `title` ✅
- `url` ✅
- `note`(可选,推荐理由)

---

## disclaimer

每份档案的 `disclaimer` 字段最少要包含:

> 本档案是研究记录,不构成投资建议。详见 [DISCLAIMER.md](../../DISCLAIMER.md)。

可补充档案特定情况(如档案作者持仓披露)。

---

## 校验

提交前必须本地跑校验:

```bash
python scripts/validate_company.py companies/us/AAPL.yaml
```

期望输出:
```
✅ companies/us/AAPL.yaml — schema valid
```

如有错误,会列出每个 violation 的字段路径 + 期望/实际值。

---

## 命名规范

- 文件名 = ticker(小写字母,去掉国别后缀):`AAPL.yaml` 不是 `AAPL.US.yaml`
- 港股带交易所前缀 + 0:`0700.yaml`(腾讯)`9988.yaml`(阿里港股)
- A 股完整代码:`600519.yaml`(茅台)`000333.yaml`(美的)
- 美股纯 ticker:`AAPL.yaml` `MSFT.yaml`
- ADR / 双重上市 / 中概股:用主代码,在 aliases 列出其他

---

## 字段加减历史

> 当 schema 演进时,新增/移除字段在此追加记录。

- `0.1.0`(2026-04-24)— 初版
