# 研究模板 · Research Templates

> 价值投资研究的可复用 Markdown 模板。给学员、给独立研究者、给任何想用结构化方式做公司研究的人。

**协议**: CC-BY-SA 4.0 · 用即标 attribution

---

## 4 份模板

| 文件 | 用途 | 大致字数 |
|---|---|---|
| [`company_research_template.md`](company_research_template.md) | 完整公司深度研究(8 段标准结构) | 6,000-8,000 字 |
| [`moat_assessment.md`](moat_assessment.md) | Pat Dorsey 五类护城河评估表 | 1,500-3,000 字 |
| [`earnings_call_notes.md`](earnings_call_notes.md) | 单次电话会议结构化纪要 | 800-1,500 字 |
| [`bull_bear_dialectic.md`](bull_bear_dialectic.md) | 同一公司正反辩证(自己和自己 debate) | 2,000-4,000 字 |

## 怎么用

```bash
# 1. 复制模板
cp templates/company_research_template.md research/xiaomi-2026-Q1.md

# 2. 按章节填空(模板里每段顶部有 <!-- 填写指南 --> 注释)

# 3. 走完最后两段:Disclaimer 占位 + Reasoning Trail
#    所有判断性结论必须有 reasoning_zh

# 4. 如要发布,引用本仓库:
#    <!-- 引自 siwuya-data templates v0.1.0 (CC-BY-SA 4.0) -->
```

## 设计原则

1. **可填空** — 每段开头有 `<!-- 填写指南: ... -->` 隐藏注释,Markdown 渲染不显示
2. **强制 reasoning** — 所有判断必须带 `reasoning_zh:` 字段
3. **强制 source** — 所有数据必须引用 URL
4. **强制 disclaimer** — 末尾不能去掉免责声明
5. **结构稳定** — 章节 heading 不要改,这样用工具批量提取数据时一致

## 与诚信框架的关系

`company_research_template.md` 末尾有"管理层诚信追踪"段,可以引用本仓库的 [integrity_framework](../integrity_framework/) 做评分。但**模板本身不强制**——你可以只写定性评价不算分。

## 给 Claude Code 用户

如果你用 Claude Code,直接 `Skill` 系统会自动加载本仓库的 [`skills/value-investing-research/SKILL.md`](../skills/value-investing-research/SKILL.md),它会引用这些模板。模板本身可以单独用,无需 Claude。

---

**说明**:Stage 5 by Claude (2026-04-24) · 待 @siwuya 审阅
