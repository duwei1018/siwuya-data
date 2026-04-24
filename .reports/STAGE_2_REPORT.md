# siwuya-data · Stage 2 完工报告

**完成日期**: 2026-04-24
**执行者**: Claude Code (Windows Session B,与 Stage 1 同 session)
**实际工时**: ~30 分钟(spec 预估 3-4h)
**状态**: ✅ 本地完成

---

## Stage 2 范围

> Schema 与校验工具(预估 3-4 小时)

## 完成清单

### Schema

- ✅ `companies/_schema/company.schema.json` — JSON Schema Draft 2020-12
  - 11 个顶级字段(meta / identity / classification / segments / business_model / moat / management / integrity_tracking / key_risks / further_reading / disclaimer)
  - 完整字段约束(enum / pattern / format / min/max length)
  - `_example` 字段(boolean,标识非真实档案)
  - 所有"判断性"字段(reasoning_zh / assessment 等)在 schema 中明示需要数据来源
  - 严格 `additionalProperties: false`(防止 typo 漏过)

### 文档

- ✅ `companies/_schema/VALIDATION.md` — 人类可读字段说明
  - 11 节,逐字段解释 + 示例
  - 命名规范段(文件名 / slug 规则)
  - 字段加减历史段(后续 schema 演进时追加)

### 示例

- ✅ `companies/_schema/company.example.yaml` — 跟 schema 同目录,作为模板规范
- ✅ `companies/_examples/example-company.yaml` — 镜像副本,供 loader 测试加载

EXAMPLE 公司 = 虚构 `EXAMPLE.US`,所有字段填示范性内容,顶部 `_example: true`。
按 ADDENDUM_2 决策:**不**写真实公司档案(小米/拼多多/腾讯均推迟到社区贡献)。

### 校验工具

- ✅ `scripts/validate_company.py` — Python validator(Draft202012Validator)
  - 支持 `<file>` / `--all` / `--include-examples` / `--quiet`
  - UTF-8 stdout reconfigure(避免 Windows GBK console emoji 报错)
  - 退出码:0 全过 / 1 有失败 / 2 环境问题
  - 可作为 PR check 接入 GitHub Actions

## 验证

```
$ python scripts/validate_company.py --all --include-examples
✅ companies\_examples\example-company.yaml — schema valid
✅ companies\_schema\company.example.yaml — schema valid

Summary: 2 passed, 0 failed
```

## 未完成 / 推迟

| 项 | 推迟到 | 理由 |
|---|---|---|
| Node/TS 版 validator | v0.2.0 | 主站 Phase 1 内部会用 ajv,这里 Python 已足够 |
| GitHub Actions schema check workflow | Stage 6 | 公开发布前接入 CI |
| `scripts/build_index.py`(自动重建 INDEX.md) | v0.2.0 | 当前 0 真实档案,手维护即可 |

## 与 spec 偏离

按 `UPGRADE_V2_SPEC_ADDENDUM_2.md`:

- **Stage 3 公司档案**:不写小米/拼多多/腾讯,改为 1 份 EXAMPLE 模板(本 Stage 2 已包含)
- 这意味着原 SIWUYA_DATA_BOOTSTRAP.md 的 Stage 3(预估 1-2h)实际工作量并入 Stage 2,
  Stage 3 可视为已包含。

## Stage 启动条件(下一步)

### Stage 3(原计划)→ 已并入 Stage 2

跳过。

### Stage 4 — 诚信评分框架(预估 4-6h)

可立即启动(无前置依赖)。但**建议**先完成 admin 创建 GitHub repo + push,
让仓库可见,然后再做 Stage 4(避免大量代码堆在本地无人看见)。

### Phase 1(主站 vercel-report-proxy)

需:
- ✅ siwuya-data Stage 2 完成(本报告)
- ⏳ admin 创建 GitHub `duwei1018/siwuya-data` 公开仓库 + 本仓库 push 上去
- ⏳ 然后 Phase 1 git submodule add 引用

---

**Stage 2 收工。**
