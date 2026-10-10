# KT07 — Hub + multi-node + parallel (remediation)

## Архитектура

- Hub `127.0.0.1:4444`
- Node A `127.0.0.1:5556`
- Node B `127.0.0.1:5557`
- Event Bus: `tcp://127.0.0.1:4442` / `4443`

## Запуск

```powershell
.\selenium\grid\stop_grid.ps1
.\selenium\grid\start_hub_multi_node.ps1
.\scripts\run_kt07_multi.ps1 -SkipStart
.\selenium\grid\stop_grid.ps1
```

## Результаты (2026-10-10)

- Grid status: **ready=true, nodes=2**
- Multi-browser pytest: **4 passed in 7.72s** (Chrome + Firefox × 2 tests)
- Parallel overlap proof: **parallel_overlap=true** (`parallel_overlap_evidence.json`)
  - Chrome session `9917fa0b…` hold 17:30:21–17:30:25Z
  - Firefox session `94648f25…` hold 17:30:23–17:30:27Z (пересечение есть)

## Исторический слой

Standalone / Hub+1 Node Chrome suite **5 PASS / 4.88 с** сохранён (`test_kt07_grid.py`).
