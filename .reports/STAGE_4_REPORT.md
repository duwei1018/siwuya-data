# siwuya-data · Stage 4 完工报告

**完成日期**: 2026-04-24
**执行者**: Claude (Windows new session — Stage 4-5 接力指南触发)
**实际工时**: ~1.5h(spec 预估 4-6h)
**状态**: ✅ 本地完成,等 commit + push

---

## Stage 4 范围(SIWUYA_DATA_BOOTSTRAP.md L507-654)

> 诚信评分框架(预估 4-6 小时)

## 完成清单

### 算法核心 — `integrity_framework/src/`(MIT)

- ✅ `__init__.py` — public API 出口
- ✅ `models.py` — `Promise` / `Verdict` / `IntegrityScore` / `ScoreBreakdown` 数据类 + 强制 invariant
- ✅ `scorer.py` — `compute_integrity_score(verdicts, as_of=None)` 实现:基础权重 + 时间衰减 + 严重性放大 + clamping
- ✅ `promise_extractor.py` — MVP 模板匹配版,中英文关键词 + 4 类 verification_type 推断
- ✅ `loader.py` — YAML ↔ dataclass 适配器(从 company yaml 读 promise + sidecar verdicts yaml)

### 测试 — `integrity_framework/tests/`(MIT)

- ✅ `test_models.py` — 21 个 case(Promise/Verdict/IntegrityScore 全字段验证)
- ✅ `test_scorer.py` — 14 个 case(权重 / 衰减 / 放大 / 跳过 / 截断 / breakdown)
- ✅ `test_promise_extractor.py` — 12 个 case(中英关键词 / 类型推断 / 边界)
- ✅ `test_loader.py` — 9 个 case(EXAMPLE 加载 / 异常输入 / 日期 coerce / 匿名拒绝)
- ✅ `conftest.py` — sys.path 接入,无需 pip install

**总计**:**56 tests · 56 passed · 97% line coverage**(目标 ≥ 80% 远超达标)

```
Name                                           Stmts   Miss  Cover
-----------------------------------------------------------------
integrity_framework\src\__init__.py                5      0   100%
integrity_framework\src\loader.py                 60      7    88%
integrity_framework\src\models.py                 73      0   100%
integrity_framework\src\promise_extractor.py      47      0   100%
integrity_framework\src\scorer.py                 42      0   100%
TOTAL                                            227      7    97%
```

### 文档 — `integrity_framework/`(CC-BY-SA)

- ✅ `METHODOLOGY.md` — 9 节白皮书(2400+ 字),含
  - §2 What This Framework Is NOT(法律边界)
  - §4 算法 + 默认权重(标注 placeholder + 50 verdict 后回测节点)
  - §5 Authorship and Accountability(强制 judged_by)
  - §6 How to Challenge a Verdict(GitHub issue 流程)
  - §7 Known Limitations(诚实列出盲区)
  - 末尾 "Drafted by Claude · finalize by @siwuya" 占位

- ✅ `docs/01_what_is_a_promise.md` — 边界规则 + 4 类承诺示例 + 12 类不接受的"承诺"
- ✅ `docs/02_weighting.md` — 每个权重的"为什么不是另一个数字" + 替代选择讨论
- ✅ `docs/03_edge_cases.md` — 12 个真实边界案例 + 推荐处理(分拆/撤回/翻译歧义/跨年度等)
- ✅ `docs/04_known_limitations.md` — A/B/C/D 四类盲区诚实展开

- ✅ `examples/scoring_walkthrough.ipynb` — 6-step 端到端 notebook(15 cells)
  - 加载 EXAMPLE 公司 promise → 写 verdict → 算分 → 显示 breakdown → severity 演示 → JSON 序列化
  - 已验证 notebook 算法逻辑端到端正确(score=80, severity demo=55)

- ✅ `README.md` 重写 — 五分钟上手 + 目录 + 设计原则 + 安装 + 版本路线图

## 与 spec 的偏离(必须记录)

### 偏离 1:模块拆分

接力指南 (`2026-04-24_思无崖v2_Stage4-5_接力指南.md`) 提到 `src/{promise_extractor, fulfillment_tracker, scorer, types}.py`,但 SIWUYA_DATA_BOOTSTRAP.md L514-543 明确是 `models.py + scorer.py + promise_extractor.py`。

**决策**:走 spec 版本(权威)。`Verdict.outcome` 已含 fulfillment 全部语义,不需独立 `fulfillment_tracker.py` 模块。

**额外加**:`loader.py` 作为 YAML ↔ dataclass 的小适配器(spec L596 隐含但未单独命名),清晰对称于 `promise_extractor.py`(text → Promise)。

### 偏离 2:Promise 字段对齐 Stage 2 schema(而非 spec L519)

spec L519 沿用早期设计:`Promise(id, text, source_type, source_url, made_at, made_by, subject_ticker, verification_type, maturity_date)`,verification_type enum 是 `financial|operational|qualitative`。

但 Stage 2 已实施的 YAML schema 用了不同字段集:`id, promise_zh, promise_en, source, made_on, due_by, verification_type` 且 enum 是 `financial_metric|product_launch|strategic_initiative|ESG_target|other`。

**决策**:Promise dataclass 与 **Stage 2 已发布的 YAML schema** 对齐(YAML 是 shipped data 的 single source of truth;dataclass 必须能从 YAML 直接 round-trip)。

变更对比:

| spec L519 字段 | 我用的字段 | 说明 |
|---|---|---|
| `text` | `promise_zh` | 加 `text` 作为 `@property` 别名指向 `promise_zh`,保持 spec API 兼容 |
| `source_url + source_type` | `source` | 简化为单 URL 字段(source_type 可从 URL 推断/在 reasoning 中说) |
| `made_at` | `made_on` | 字段名差异,语义同 |
| `maturity_date` | `due_by` | 字段名差异,语义同 |
| verification_type enum | 对齐 schema 5 项 enum | 按 Stage 2 YAML 已发布 |

**没有 breaking impact**:这是首版,spec 是设计意图,Stage 2 实施先落地了 schema,Stage 4 dataclass 必须服从 schema 决定。

### 偏离 3:Notebook 不下载 / 不 fetch

spec L644 说 notebook 必须用虚构 EXAMPLE_CORP — 已严格遵守。所有数据 inline 在 notebook 内,无任何网络 / 文件依赖(除读 EXAMPLE YAML 这唯一一次)。

## 验收清单

- [x] models.py 定义完整,可被导入
- [x] scorer.py 的 compute_integrity_score 可正常调用
- [x] 所有单元测试通过(56/56)
- [x] coverage ≥ 80%(实际 97%)
- [x] METHODOLOGY.md 完整,等 @siwuya 最终署名
- [x] docs/ 下 4 份辅助文档完整
- [x] scoring_walkthrough.ipynb 可完整跑通(端到端 score=80 + severity demo=55 验证)

## 设计选择背书(给将来读代码的人)

### 为什么 Promise / Verdict 用 `@dataclass(frozen=True)` 而不是 Pydantic

- spec L520 说 "@dataclass 或 Pydantic 均可"
- 选 dataclass:零依赖(本仓库主张依赖最小化,只加 PyYAML)
- frozen=True 让 Verdict 可 hash + 不可变,跨线程安全 + 防止意外修改 audit trail

### 为什么 `judged_by` 黑名单包含 "anonymous / unknown / n/a / none"

- 不只是检查空字符串 — 真实滥用是写 "anonymous"、"unknown" 等占位词
- 大小写不敏感(`anonymous == Anonymous == ANONYMOUS`)
- 在 Verdict.__post_init__ 直接 ValueError,不允许构造完后再发现

### 为什么 SCORE 在 [0, 100] 截断而不允许负数

- 心理学:负数评分会被解读为"债务"或"不能信任的极端",法律风险高
- 实用:0 已经足够极端,负数无信息增益
- 守住 0-100 区间让分数始终具备直觉解释

### 为什么时间衰减只是 binary(全权 vs 半权),不是 smooth decay

- v0.1.0 简单优先,可被 5 行 code 解释
- smooth decay (e^-x) 引入不必要的参数
- 等真实数据足够时,v0.2.0 可换 smooth

## 未完成 / 推迟

| 项 | 推迟到 | 理由 |
|---|---|---|
| GitHub Actions tests workflow | Stage 6 | 公开发布前接入 CI |
| LLM-backed promise_extractor | v0.2.0 | 本仓库不引外部 API key,留接口给下游 |
| Node/TS 镜像实现 | v0.2.0 | 主站 Phase 1 用 ajv 已能验,Python 已足够 |
| 真实 50 verdict backtest 调权重 | 等数据积累 | placeholder 权重在 docs/02 已标注 |

## Stage 启动条件(下一步)

### Stage 5 — 研究模板 + SKILL.md

✅ **本 session 已并行完成**(详见 STAGE_5_REPORT.md)。

### Stage 6 — GitHub public 化

需要:
- ✅ Stage 1-5 全完工(本报告确认 Stage 4)
- ⏳ admin 在 GitHub Settings → Change repository visibility → Make public(7-step checklist 见 admin handoff)
- ⏳ 本 session 已起草 `RELEASE_NOTES_v0.1.0.md`,admin Publish Release 时直接 copy

---

**Stage 4 收工。**
