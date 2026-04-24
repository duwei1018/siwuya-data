# Skills · 给 Claude Code / Desktop 用户

> 让 Claude Code / Claude Desktop 能直接消费本仓库做价值投资研究的 SKILL.md 文件。

**协议**: CC-BY-SA 4.0

---

## value-investing-research

唯一一份 SKILL,但内容覆盖完整研究工作流。

```
skills/value-investing-research/
├── SKILL.md                          ← 主入口,Claude 触发后读这个
├── reference/
│   ├── moat_types.md                 ← Pat Dorsey 五类护城河详解
│   ├── financial_redflags.md         ← 财务危险信号清单
│   └── integrity_signals.md          ← 管理层诚信信号清单
└── scripts/
    └── load_company.py               ← Claude 调用,输出格式化档案
```

## 怎么用

### Claude Code

```bash
# 仓库根目录直接启动 Claude Code,自动检测 skills/
cd siwuya-data
claude
# 然后问 Claude:"帮我用思无崖框架研究一下小米"
# Claude 会自动加载 SKILL.md,引导你按结构化方式做研究
```

### Claude Desktop

把 `value-investing-research/` 整个目录复制到 Claude Desktop 的 skills 目录(macOS:`~/Library/Application Support/Claude/skills/`),重启 Claude Desktop,在对话中提"价值投资 / value investing"就会触发。

## 核心原则

SKILL.md 强制 Claude 在做价值投资研究时:

1. **结构化** — 用本仓库 [`templates/`](../templates/) 而非自由发挥
2. **署名** — 任何 verdict / 判断必须有 `judged_by`
3. **数据准确** — 任何数字必须 attestable URL
4. **免责** — 每个输出末尾必须带 [DISCLAIMER](../DISCLAIMER.md) 链接
5. **不预测股价** — Claude 不输出"目标价 / 买入卖出建议"

## 与其他 skill 的关系

如果你有自己的 Claude skill,可以在你的 skill 里 `@import skills/value-investing-research/SKILL.md` 拿到本仓库的工作流,但要保留 attribution(CC-BY-SA)。

---

**说明**:Stage 5 by Claude (2026-04-24) · 待 @siwuya 审阅
