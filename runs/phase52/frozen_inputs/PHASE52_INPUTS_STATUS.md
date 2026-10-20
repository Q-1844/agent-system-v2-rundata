# PHASE52 输入状态（CodeBuddy → WorkBuddy 交接）

导出时间：2026-10-11T18:18:05。基线 commit：`ca02635ac9a932bccd25b02b68e2605e615048d7`（分支 feat/agent-v2-phase-d-golden-run，工程分支 phase52/efficiency）。

## WorkBuddy 现在可以开始的步骤

| 输入 | 状态 | 位置 |
|---|---|---|
| 正式 Skill 主文件 | 已冻结 | `01_skill/builtin_core__full-story-relay-calibration__v1.6.0/SKILL.md` |
| Skill 依赖规则 | 已冻结（7 份 references） | 同上目录 `references/` |
| Skill 绑定清单 | 已冻结（skill.json bindings + required_capabilities） | 同上目录 `skill.json` |
| 修复技能（参考） | 已冻结 | `01_skill/builtin_core__keyframes-bridge-repair__v1.0.0/` |
| 候选技能（非正式，未转正） | 已冻结并标注 | `01_skill/candidate__agnes-production-craft__*` |
| 剧本（五幕） | 已冻结 | `02_project/project.json` story_text |
| 锁定分镜（20 镜） | 已冻结 | `02_project/LOCKED_STORYBOARD.json` |
| 公共意图（角色/船/怪物/声音政策） | 已冻结 | `02_project/COMMON_INTENT.json` |
| 角色 Look 合格参考 | 4/4 已导出 | `03_approved_materials/` |
| 历史 receipts/审查证据 | 已冻结 | `02_project/generation_records.jsonl`、`review_records.jsonl` |
| 六 Agent 工作流定义（W09r6 完成版） | 已冻结 | `02_project/workflow_P50_B_W09r6.json` |

**结论：剧本与锁定分镜存在，WorkBuddy 的视频主测试属于「同分镜冻结输入测试」，不需要自主规划。**

## 缺失与限制（如实记录）

- 注意：ref_87639e9db8d5 本地文件缺失，已从 URL 下载导出；CodeBuddy 已用视觉模型核验通过（无人渔船、右舷 3/4、黄昏海面，与 look 元数据一致）

- 海怪 Look 的 `generation_status=failed` 但存在 1 张已批准参考（ref_9c0ba4bed38c）；以批准参考为准。
- 首帧资产未整包复制（234 个文件约 109MB），仅提供哈希清单 `03_approved_materials/first_frames_index.json`；WorkBuddy 需要具体首帧时可按清单在仓库内定位。
- 本目录为冻结只读副本：不要在此目录内修改；WorkBuddy 的适配副本应在自己的工作区创建。

## 额度与同步约束（重要）

本机 Agnes 为单账号单配额池（视频 500s/天等，见 `04_baseline/config_fingerprint.json`）。WorkBuddy 平台账号与额度由 WorkBuddy 自行核验；在两边的生成额度独立性核实之前，不得同时发起生成请求。本轮 CodeBuddy 不提交新视频（配额不足），仅做真实图片链路与恢复测试。

## 哈希核验

`PHASE52_BASELINE_MANIFEST.json` 的 `files` 数组含每个文件的 SHA-256。收到后先核对哈希再使用。
