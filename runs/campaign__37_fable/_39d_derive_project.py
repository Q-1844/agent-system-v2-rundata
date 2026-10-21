# -*- coding: utf-8 -*-
# _37_fable/_39d_derive_project.py
# Phase 39D 项目派生脚手架（用户 2026-09-26 裁定：新建项目重来，旧 P39C 留作事故证据档）。
#
# 属纪律 #5 的「建项目脚手架」豁免（一次性派生新项目初始 canonical，非 live mutation）；
# 派生完成后的一切生产动作走 Agent 正式入口。
#
# 保留：style/native_av/story_text/characters（project.json）、resources.json+
#       output/resources/（鹤 approved Look + 参考图像）、scene_system.json +
#       scene_system/（2 Location + 6 Instance + 6 approved SIV）、project_profile.json、
#       output/characters/（Look 分段图）。
# 剥离：旧 6×1 分镜（scenes=[]、next_scene_seq=1）、shot_production_bindings、
#       视频/帧/分镜图产物、calibration_runs、agents 会话任务历史、cache、review 归档。
# 实例预映射（新 2 段×3 镜；重建时 Scene Agent 正式核验 SIV fresh）：
#       scin_c96eeacc7（破晓云端滑翔，天空与森林上空） s01→s01 active
#       scin_db53fec84（俯冲接近水面，湖泊）           s04→s02 active
#       其余 4 instance → archived（不可绑定；SIV 随实例原样保留）
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "projects" / "Crane_Lake_P39C"
DST = ROOT / "projects" / "Crane_Lake_P39D"

KEEP_ACTIVE = {
    # instance_id: (旧 story_scene_id, 新 story_scene_id, 语义)
    "scin_c96eeacc7": ("s01", "s01", "破晓云端滑翔 → 新 s01 天空与森林上空段"),
    "scin_db53fec84": ("s04", "s02", "俯冲接近水面 → 新 s02 湖泊段"),
}


def main() -> None:
    assert SRC.exists(), f"源项目不存在: {SRC}"
    assert not DST.exists(), f"目标已存在（幂等保护，不覆盖）: {DST}"

    shutil.copytree(SRC, DST)
    print(f"[copy] {SRC.name} -> {DST.name}")

    # 1) project.json：改名 + 清分镜结构（保留 style/native_av/story_text/characters）
    pj_path = DST / "output" / "project.json"
    pj = json.loads(pj_path.read_text(encoding="utf-8"))
    old_scenes = len(pj.get("scenes") or [])
    pj["name"] = DST.name
    pj["scenes"] = []
    pj["next_scene_seq"] = 1
    pj["updated_at"] = time.time()
    pj_path.write_text(json.dumps(pj, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    print(f"[project.json] name={DST.name} scenes {old_scenes}->0 "
          f"next_scene_seq=1（story_text/characters/style 保留）")

    # 2) scene_system.json：实例预映射 + 其余归档
    ss_path = DST / "output" / "scene_system.json"
    ss = json.loads(ss_path.read_text(encoding="utf-8"))
    remapped, archived = [], []
    for iid, inst in (ss.get("scene_instances") or {}).items():
        head = iid[:14]
        if head in KEEP_ACTIVE:
            old_sid, new_sid, why = KEEP_ACTIVE[head]
            assert inst.get("story_scene_id") == old_sid, \
                f"{iid}: 预映射前提变化（{inst.get('story_scene_id')} != {old_sid}）"
            inst["story_scene_id"] = new_sid
            inst["updated_at"] = time.time()
            remapped.append(f"{head}: {old_sid}->{new_sid}（{why}）")
        else:
            inst["status"] = "archived"
            inst["updated_at"] = time.time()
            archived.append(f"{head}（原 story={inst.get('story_scene_id')}）")
    ss_path.write_text(json.dumps(ss, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    for r in remapped:
        print(f"[instance] remap {r}")
    for a in archived:
        print(f"[instance] archived {a}")

    # 3) 生产绑定清空（schema_version 保留）
    sb_path = DST / "output" / "shot_production_bindings.json"
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    n_bindings = len(sb.get("bindings") or {})
    sb["bindings"] = {}
    sb_path.write_text(json.dumps(sb, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    print(f"[bindings] {n_bindings}->0")

    # 4) 剥离旧产物与历史（目录整个删除，运行时按需重建）
    for rel in ("output/videos", "output/frames", "output/storyboards",
                "output/experiments", "output/agents", "output/_p39c_review",
                "output/audio", "output/subtitles", "cache",
                "output/experiments/calibration_runs"):
        p = DST / rel
        if p.exists():
            shutil.rmtree(p)
            print(f"[strip] {rel}/")
    (DST / "input").mkdir(exist_ok=True)

    # 5) 自验
    pj2 = json.loads(pj_path.read_text(encoding="utf-8"))
    ss2 = json.loads(ss_path.read_text(encoding="utf-8"))
    sb2 = json.loads(sb_path.read_text(encoding="utf-8"))
    actives = [(i[:14], v.get("story_scene_id"))
               for i, v in (ss2.get("scene_instances") or {}).items()
               if v.get("status") == "active"]
    print("\n[verify] scenes:", len(pj2.get("scenes") or []),
          "| next_scene_seq:", pj2.get("next_scene_seq"),
          "| bindings:", len(sb2.get("bindings") or {}))
    print("[verify] active instances:", actives)
    print("[verify] SIV approved:",
          sum(1 for v in (ss2.get("scene_instance_views") or {}).values()
              if v.get("approval_status") == "approved"))
    print("[verify] resources.json 大鹤 looks:",
          sum(1 for v in (json.loads(
              (DST / "output" / "resources.json").read_text(encoding="utf-8")
          ).get("looks") or {}).values()))
    print("\n[DONE] Crane_Lake_P39D 派生完成")


if __name__ == "__main__":
    main()
