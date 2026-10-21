# Phase39B Shadow Replay 对照（replay=cal_20260925_170235_d911 vs gold=cal_20260925_004933_6b30）

| 决策点 | gold(lvl/act) | agent(lvl/act) | 判定 |
|---|---|---|---|
| M1 | minor/continue | minor/continue | MATCH |
| M1_a1 | major/retry_generation | none/continue | MISMATCH |
| M2 | minor/continue | major/add_transition | MISMATCH |
| M3 | minor/continue | minor/continue | MATCH |
| M3_a1 | major/retry_generation | minor/continue | MISMATCH |
| M3B | none/continue | none/continue | MATCH |
| M4 | none/continue | none/continue | MATCH |
| M4_a1 | minor/continue | minor/continue | MATCH |
| M4_a2 | major/retry_generation | major/retry_generation | MATCH |
| M4_a3 | major/retry_generation | major/add_transition | MISMATCH |
| M5 | minor/continue | major/retry_generation | MISMATCH |
| M5_a1 | major/retry_generation | major/retry_generation | MATCH |
| M5_a2 | minor/continue | minor/continue | MATCH |
| M5_a3 | minor/continue | minor/continue | MATCH |
| M5_a4 | major/retry_generation | major/retry_generation | MATCH |
| M5B | none/continue | minor/continue | MISMATCH |
| M5B_a1 | major/retry_generation | minor/continue | MISMATCH |
| M6 | minor/continue | minor/continue | MATCH |
| M7 | none/continue | none/continue | MATCH |
| M8 | minor/continue | minor/continue | MATCH |
| M9 | minor/continue | none/continue | MISMATCH |
| SCENARIO_M3_M4_HARDCUT | major/add_transition | major/add_transition | MATCH |
| SCENARIO_M5_M6_SEAM_BREAK | major/add_transition | minor/other | MISMATCH |

## 失败分类计数
- false_none: 2
- unnecessary_retry: 1
- missed_major: 4
- missed_bridge: 1
- unnecessary_bridge: 2
- ownership_violation: 0
- skipped_cascade: 0
- no_verdict: 0
- match: 14
- total: 23