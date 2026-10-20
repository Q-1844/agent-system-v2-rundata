# Agent System V2 — 运行数据/产物仓（B）

> 冻结批次的运行数据与产物归档。配套：A [`agent-system-v2`](https://github.com/Q-1844/agent-system-v2)（主代码）· C [`agent-system-v2-archive`](https://github.com/Q-1844/agent-system-v2-archive)（档案）· D `agnes-frame-host`（图床）。

## 铁律

1. **运行中 SQLite / 活数据库永不进仓**（可变二进制：Git 存储会滚雪球且有写坏风险）——只进冻结导出/快照
2. 单文件 >100MB 不进仓
3. 每批次必须带 `manifests/sha256-index.csv`（逐文件 SHA256+字节数）与批次 `manifest.json`（含来源与审批记录）
4. 批次与 A 仓 commit 通过 `source_commit_note` 关联，不形成运行时依赖

## 当前批次

| 批次 | 内容 | 文件数 |
|---|---|---|
| `runs/phase52/` | Phase52 效率战役：账本（生图 2 + 视频 45 条目、时间线 701 行）、冻结输入 44 文件（skill 包/项目状态/核准素材/基线指纹）、人评图片 2 张 | 49 |
| `runs/scene_multiview_20260917/` | 场景模块多视角生图样张（2026-09-17） | 3 |

元数据：`manifests/manifest.json`（批次总纲）+ `manifests/sha256-index.csv`（逐文件哈希，52 项）。

## 新增批次流程

1. 运行/战役结束 → 从活目录导出冻结副本到 `runs/<batch>/`
2. 生成该批次 sha256-index 行（沿用现有 CSV 表头 `sha256,bytes,relative_path`）
3. 追加 `manifest.json` 条目 → 分类提交：`data(<batch>)` 结构化数据 / `assets(<batch>)` 图片资产 / `manifest(<batch>)` 哈希索引

## Pages

本站由 `docs/` 目录发布（GitHub Pages）：https://q-1844.github.io/agent-system-v2-rundata/
