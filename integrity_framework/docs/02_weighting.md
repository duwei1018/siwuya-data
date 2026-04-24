# 02 · 权重为什么这么设 · Why These Weights

> 这是 [METHODOLOGY.md §4.1](../METHODOLOGY.md#41-默认权重v010) 的扩展讨论。任何对权重的修改必须更新 METHODOLOGY 的 Version History 与本文。

---

## v0.1.0 默认权重

| outcome | weight | 含义 |
|---|---|---|
| `fulfilled` | `0` | 不奖励 |
| `partial` | `-5` | 轻扣 |
| `broken` | `-15` | 重扣(3× partial) |
| `pending` | 跳过 | 不计入 |
| `unverifiable` | 跳过 | 不计入 |

```
base = 100
fulfilled : 0 → 一家全兑现公司 = 100 分(基线)
1 partial : -5 → 95
1 broken : -15 → 85
3 partial = 1 broken(粗略对应)
```

## 为什么 fulfilled = 0?

**兑现是基线**,不是加分项。

替代选择:`fulfilled = +5`(每条兑现承诺加 5 分,封顶 100)。

为什么不采用这个替代:
- 鼓励"高频低质承诺"——管理层故意做大量低门槛承诺刷分
- 公司间承诺数量本来就不可比(有些公司每季度给指引,有些只年度给一次)
- "兑现是应该做的事"作为基础假设更符合诚信框架的法律谨慎

未来可能加 `consistency_bonus`(连续 N 季度全兑现的小幅加分),但需要更多数据支持。

## 为什么 partial = -5,broken = -15?

3:1 的比例。

替代选择:
- 2:1(`partial = -7.5`)
- 5:1(`partial = -3`)

为什么是 3:1:
- 部分完成在公司沟通中频繁出现(战略落地的常态),不应该跟"完全违背"相同惩罚
- 但"部分"的定义有主观性,不能 0 扣分(否则会鼓励所有 broken 被柔化为 partial)
- 3:1 让 3 条 partial 等价于 1 条 broken,在直觉上对得上"3 次 50% 完成 vs 1 次完全违背"

**这个比例是 placeholder**,等积累 50+ 真实 verdict 后会回测调整。

## 为什么 pending / unverifiable 跳过?

不进算分,但在 `IntegrityScore.skipped_verdicts` 中**可见**。

理由:
- `pending` = 还没到时间,惩罚就是错的
- `unverifiable` = 没证据,惩罚等于 punishing the analyst's data gap

但**不**隐藏掉 — 看分数的人需要知道"这个分是基于多少条已结案 verdict",不能让 100 分的公司其实只有 1 条已结案 + 99 条 pending。

读分时的常识:**`counted_verdicts < 5` 时分数没什么意义**,样本量太小。

## 时间衰减:为什么是 3 年?

`DECAY_YEARS = 3`,3 年前的 verdict 半权重。

替代选择:
- 5 年(更宽容,适合产业周期长的行业)
- 1 年(更激进,只看近 1 年)

为什么 3 年:
- 一个公司管理层任期通常 3-5 年,3 年前的承诺与现在是不同管理层的事
- 战略 cycle 通常 2-4 年(半导体扩产、出海、产品代际),3 年外的承诺背景已经显著不同
- 同时仍保留**部分**权重(`× 0.5`,而不是 `× 0`),因为重大违背(如造假)的影响应该长期存在

**这个参数也是 placeholder**,可能根据实证调整或按行业差异化(比如制药行业用 5 年)。

## 严重性放大:只放在 broken 上?

是的。`partial / pending / unverifiable / fulfilled` 即使带 `severity_tag` 也不放大。

理由:严重性 = "不只是没做到,还触碰了红线"。如果一个 partial 触碰了红线,应该提级为 broken,而不是 partial + 红线 tag。

放大集合(白名单):
- `financial_misconduct`(财务造假/重大错报)
- `audit_qualification`(审计被出具保留意见)
- `fraud_admission`(自认欺诈)

**为什么起步只有这 3 个**:
- 都是**客观可考证**的(SEC 公告 / 审计报告 / 法庭文书)
- 不依赖主观判断
- 错误使用的成本足够高(法律风险)

扩充必须走 GitHub `methodology_discussion` issue,不能 maintainer 单方面加。

## 不在权重之外的几个重要东西

### 不区分 "金额大小"

承诺"营收增长 1pp" 和 "营收增长 25pp" 在框架里是同等的。

理由:
- 跨公司不可比(1pp 对小公司可能是巨变,对大公司可能是噪音)
- 鼓励管理层"承诺小目标"刷分会扭曲

可能的未来扩展:加 `materiality` 字段(none/medium/high),但需要严格定义防滥用。

### 不区分 "管理层个人 vs 公司层面"

CEO 个人承诺 与 公司新闻稿里的承诺,在框架中权重相同。

理由:公司新闻稿也是公司治理结构通过的对外承诺,法律意义上同等约束力。

### 不奖励 "主动披露"

公司主动披露未达标 vs 被外部发现,在 outcome 上都是 `broken`。

理由:
- 主动披露是法律义务(重大事项必须及时披露),不是美德
- 把"主动 vs 被动"放进算分会鼓励披露包装而非诚信本身
- 但 reasoning 应该写明这一区别,作为定性信息留存

---

**Last reviewed**: 2026-04-24 by Claude · finalize by @siwuya
