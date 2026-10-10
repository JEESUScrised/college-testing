# KT10 — Browser × viewport matrix

Прогон remediation: **6 passed in 42.73s** (один session на профиль; 36 строк evidence).

Файл: `selenium/artifacts/kt10/responsive_matrix.jsonl`  
Скриншоты: `screenshots/kt10/responsive/{browser}_{profile}_r0N_*.png` (36 PNG).

Фактический viewport может отличаться от target из‑за chrome UI (пример desktop Chrome: target 1440×900 → innerWidth≈1424). Это ожидаемо; в JSONL пишутся `viewport` и `window` отдельно.

CDP Chrome tablet/phone = **browser device emulation**, не физическое Android-устройство.
