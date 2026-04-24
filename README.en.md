# siwuya-data

> A public, structured data foundation for value-investing research.

[中文](README.md) · [Disclaimer](DISCLAIMER.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

---

## What is this

`siwuya-data` is a public research-infrastructure repository containing:

- **Company profiles** (YAML) — structured profiles of CN / HK / US listed companies,
  covering business model, moat, management, tracked promises, key risks
- **Integrity-scoring framework** (Python + docs) — algorithm + methodology for
  evaluating how well management keeps their public promises over time
- **Research templates** (Markdown) — reusable templates for value-investing research

**Target users**:
- Students of the PKU-UCLA Value Investing program
- Independent value-investing researchers
- Anyone using Claude Code / Claude Desktop for company research (see SKILL.md below)

---

## Philosophy

**Open structure, retained data.**

| In this repo | NOT in this repo (lives at [siwuya.org](https://siwuya.org)) |
|---|---|
| Schema for company profiles (data shape) | Real-time analysis / daily briefs |
| Integrity-scoring algorithm (methodology) | Current scoring data (conclusions) |
| Research templates | User behavior / subscription data |
| **List** of tracked management promises (facts) | **Status** of promises (our judgment) |

Any data answering "what is company X's score today" lives at the main site,
not here. This repo holds **facts** (tracked promises) and **methods** (how to score),
**not conclusions**.

---

## Layout

```
siwuya-data/
├── README.md / README.en.md         # this file
├── LICENSE                          # MIT (code) + CC-BY-SA 4.0 (data) dual license
├── DISCLAIMER.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CITATION.cff                     # Academic citation
│
├── companies/                       # Company profile library
│   ├── _schema/                     # JSON Schema + validation docs
│   ├── _examples/                   # Synthetic example (NOT a real company)
│   ├── us/ / hk/ / cn/              # Markets
│   └── INDEX.md                     # Auto-generated index
│
├── integrity_framework/             # Integrity-scoring framework
│   ├── METHODOLOGY.md
│   ├── README.md
│   └── src/                         # Algorithm (MIT)
│
├── templates/                       # Research templates
└── skills/                          # SKILL.md for Claude Code / Desktop users
```

---

## Maintenance

`siwuya-data` is maintained by the [siwuya](https://siwuya.org) team, with community contributions.

Company-profile content comes from contributors (the admin, collaborating researchers,
PKU-UCLA students, etc.). Every profile carries a `judged_by` byline so authorship
is unambiguous.

**Want to add a company profile?** See [CONTRIBUTING.md](CONTRIBUTING.md).
**Found an error?** Open a PR with the source for the correction.

---

## Legal note (please read)

Integrity scoring involves research judgments about management of listed companies.
This repository reduces legal risk through:

1. **Bylines** — every judgment carries a `judged_by` field
2. **License separation** — code MIT, data CC-BY-SA 4.0
3. **Mandatory DISCLAIMER** — every profile and output references the disclaimer
4. **Data separation** — concrete scoring data is NOT here, only methodology and tracked promises

See [DISCLAIMER.md](DISCLAIMER.md). Use of this repository constitutes acceptance.

---

## Commercial model

This repository is **permanently free and open source**.

The [siwuya.org](https://siwuya.org) main site is also free during Beta. If it ever
becomes a paid subscription, users will be notified 30 days in advance. Company profiles,
research methodology, and the integrity framework will **never** sit behind a paywall.

---

## Citation

For academic or public-article use, please cite per [CITATION.cff](CITATION.cff).

---

## License

- Code (`integrity_framework/src/*` etc.): **MIT** — see [LICENSE-MIT.txt](LICENSE-MIT.txt)
- Data (`companies/*`, `templates/*`): **CC-BY-SA 4.0** — see [LICENSE-CC-BY-SA.txt](LICENSE-CC-BY-SA.txt)

See [LICENSE](LICENSE) for details.
