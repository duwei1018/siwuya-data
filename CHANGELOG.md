# Changelog

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/),
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 计划中
- Stage 6: GitHub public 化 + v0.1.0 tag(admin 操作)
- v0.2.0: LLM-backed promise extractor(下游集成)+ Node/TS 镜像

## [0.1.0] - 2026-04-24

### Added
- Stage 4: 诚信评分框架(`integrity_framework/`)
  - `src/models.py` — Promise / Verdict / IntegrityScore / ScoreBreakdown 数据类(`@dataclass(frozen=True)`,zero deps)
  - `src/scorer.py` — `compute_integrity_score(verdicts, as_of=None)` 算法(基础权重 + 时间衰减 + 严重性放大 + clamp)
  - `src/promise_extractor.py` — MVP 文本 → Promise 模板匹配版(中英关键词 + 4 类 verification_type 推断)
  - `src/loader.py` — YAML ↔ dataclass 适配器
  - `tests/` — pytest 56 tests · 97% line coverage
  - `METHODOLOGY.md` — 9 节白皮书,标注权重 placeholder + 50 verdict 后回测节点
  - `docs/01-04` — 承诺定义 / 权重背书 / 12 边界案例 / 4 类已知盲区
  - `examples/scoring_walkthrough.ipynb` — 6-step 端到端 notebook(15 cells)
- Stage 5: 研究模板 + SKILL(`templates/` + `skills/`)
  - `templates/company_research_template.md` — 公司深度研究 8 段标准结构
  - `templates/moat_assessment.md` — Pat Dorsey 五类护城河完整评估表
  - `templates/earnings_call_notes.md` — 单次电话会结构化纪要
  - `templates/bull_bear_dialectic.md` — 正反辩证强制结构(自我 debate)
  - `skills/value-investing-research/SKILL.md` — Claude Code / Desktop 主入口 SKILL
  - `skills/.../reference/{moat_types,financial_redflags,integrity_signals}.md` — 三份知识库
  - `skills/.../scripts/load_company.py` — 公司档案 pretty-printer

### Notes
- v0.1.0 是首版正式发布,标志 siwuya-data 从仓库骨架(v0.0.x)进入"可用研究基础设施"阶段
- 算法权重均为 placeholder,等积累 50+ 真实 verdict 后做实证回测调整(标注于 `scorer.py` 注释 + `docs/02_weighting.md`)
- `METHODOLOGY.md` 末尾署名为 "Drafted by Claude · finalize by @siwuya",待 admin review 后改正式署名

## [0.0.2] - 2026-04-24

### Added
- Stage 2: `companies/_schema/company.schema.json`(JSON Schema 公司档案规格)
- Stage 2: `companies/_schema/company.example.yaml`(随附示例,用于 schema 测试)
- Stage 2: `companies/_schema/VALIDATION.md`(每个字段的人类可读说明)
- Stage 2: `companies/_examples/example-company.yaml`(完整示例档案,虚构 EXAMPLE.US,标 `_example: true`)
- Stage 2: `scripts/validate_company.py`(本地校验工具)

## [0.0.1] - 2026-04-24

### Added
- Stage 1: 仓库骨架与法律文档
- README.md / README.en.md(中英文入口)
- LICENSE(双协议:MIT 代码 + CC-BY-SA 4.0 数据)
- LICENSE-MIT.txt / LICENSE-CC-BY-SA.txt(全文)
- DISCLAIMER.md(中英双语免责声明)
- CONTRIBUTING.md(贡献指南)
- CITATION.cff(学术引用格式)
- 完整目录骨架(companies/ integrity_framework/ templates/ skills/)

### Notes
- 本仓库由思无崖团队维护,接受社区贡献
- v2 战略决策:**永久免费 + 开源**(见 README.md "商业模式" 段)
- Phase 0(主站) 同期独立化为 [github.com/duwei1018/vercel-report-proxy](https://github.com/duwei1018/vercel-report-proxy)
