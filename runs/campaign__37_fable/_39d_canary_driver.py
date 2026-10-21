# -*- coding: utf-8 -*-
# _37_fable/_39d_canary_driver.py
# Phase 39D——Crane_Lake_P39D 干净重建 Canary 驱动（复用 39C 驱动器模式）。
#
# 纪律（沿用用户 Canary Gate 定版）：
#   - 全程走 Producer 正式 REST 流式入口（thinking=true），zcode 不替用户批准任何 major；
#   - 每 turn 完整 transcript 存档 _37_fable/_39d_canary/。
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

import httpx

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8000"
PROJ = "Crane_Lake_P39D"
OUT_DIR = ROOT / "_37_fable" / "_39d_canary"


def ensure_producer_session() -> str:
    r = httpx.post(f"{BASE}/api/project/{PROJ}/agents/sessions",
                   json={"agent_id": "producer", "scope_type": "project",
                         "scope_id": ""}, timeout=30)
    r.raise_for_status()
    d = r.json()
    return d.get("session_id") or d.get("id") or d["session"]["session_id"]


def stream_turn(session_id: str, content: str, timeout_s: float = 3600.0) -> dict:
    """流式 producer turn（thinking=true），返回完整事件流 + 终态 result。"""
    events = []
    result = None
    with httpx.stream(
        "POST",
        f"{BASE}/api/project/{PROJ}/agents/sessions/{session_id}/turn/stream",
        json={"content": content, "thinking": True}, timeout=timeout_s,
    ) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line.startswith("data: "):
                continue
            try:
                ev = json.loads(line[6:])
            except Exception:
                continue
            events.append(ev)
            t = ev.get("type")
            if t == "tool.completed":
                print(f"  [tool] {ev.get('name')}", flush=True)
            elif t == "tool.progress":
                print(f"  [progress] {(ev.get('message') or '')[:90]}", flush=True)
            elif t == "turn.completed":
                result = ev.get("result") or {}
                break
            elif t == "turn.failed":
                raise RuntimeError(f"turn.failed: {ev.get('error')}")
    if result is None:
        raise RuntimeError("流结束但无 turn.completed")
    return {"events": events, "result": result}


def save_transcript(name: str, data: dict) -> pathlib.Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / f"{name}.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def cmd_turn(name: str, content: str):
    sid = ensure_producer_session()
    print(f"[producer session] {sid}")
    t0 = time.time()
    data = stream_turn(sid, content)
    data["meta"] = {"turn": name, "latency_s": round(time.time() - t0, 1),
                    "project": PROJ, "thinking": True}
    p = save_transcript(name, data)
    r = data["result"]
    msg = r.get("assistant_message") or ""
    receipts = [x.get("operation") for x in (r.get("receipts") or [])
                if isinstance(x, dict)]
    print(f"\n[done] {name} latency={data['meta']['latency_s']}s ops={receipts}")
    print(f"[transcript] {p}")
    print(f"\n[assistant_message]\n{msg[:3000]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--content-file", required=True)
    a = ap.parse_args()
    cmd_turn(a.name, pathlib.Path(a.content_file).read_text(encoding="utf-8"))
