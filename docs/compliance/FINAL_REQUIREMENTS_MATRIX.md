# FINAL REQUIREMENTS MATRIX — KT01–KT12

Date: **2026-10-11** | Remote Jira verification: **DONE** (KAN-4/5/6)

Status values: PASS | PARTIAL | FAIL | BLOCKED | NOT RUN | PENDING

| KT | Req ID | Teacher requirement | Implemented | Source | Execution evidence | Report | Status | Remaining |
|---|---|---|---|---|---|---|---|---|
| 01 | R01-01 | Selenium Chrome opens ya.ru | yes | `selenium/tests/test_kt01_ya_ru.py` | historical PASS | KT01.docx | PASS | Fill personal title-page fields |
| 02 | R02-01 | Public website | Sauce Demo | `test_kt02_sauce_public.py` | 11 PASS / 49.34s | KT02.docx | PASS | — |
| 02 | R02-02 | Positive / negative / boundary | yes | same | same | KT02.docx | PASS | — |
| 02 | R02-03 | Windows / iframe / cookies | local+public | windows/iframe + public | hist 6 PASS + public | KT02.docx | PASS | — |
| 02 | R02-04 | Test report | yes | docs/kt02 + DOCX | — | KT02.docx | PASS | — |
| 03 | R03-01 | Public website PO | Sauce PO | `pages/sauce/`, `test_kt03_sauce_po.py` | 5 PASS / 21.11s | KT03.docx | PASS | — |
| 03 | R03-02 | ≥2 major functions | login/inventory/cart/checkout | same | same | KT03.docx | PASS | — |
| 04 | R04-01 | Real Jira project | yes | collegeqakt04 / KAN | REST+UI 2026-10-11 | KT04.docx | PASS | Key is KAN not QAKT04 |
| 04 | R04-02 | Defect reports | yes | KAN-4/5/6 + bug-reports | descriptions + screenshots | KT04.docx | PASS | — |
| 04 | R04-03 | Workflow transitions | yes | changelog KAN-4 | Open→IP→RFT→Done | KT04.docx | PASS | Localized status names |
| 04 | R04-04 | Assignment / comments | yes | JEESUS + 3 comments/issue | REST verified | KT04.docx | PASS | Single-account educational roles |
| 04 | R04-05 | Fixes + retests | lifecycle copy | `kt04_lifecycle/` | **3 PASS / 8.74s** | KT04.docx | PASS | Seeded suite kept 2P/3F |
| 04 | R04-06 | Native Components | labels only | jira-project.md | `components=[]` | KT04.docx | **PARTIAL** | Propose native comps; need approval |
| 04 | R04-07 | Jira statistics/reports | filter+summary+dashboard | filter 10002; dash 10001 | screenshots/kt04/jira/final/ | KT04.docx | **PARTIAL** | Gadgets need UI filter; board Reports 404 |
| 05 | R05-01 | Choose/justify website | VDNH | website-selection.md | — | KT05.docx | PASS | — |
| 05 | R05-02 | Black/gray/white strategy | documented | test-plan.md | — | KT05.docx | PASS | White-box N/A backend |
| 05 | R05-03 | Scope + entry/exit | yes | test-plan.md | — | KT05.docx | PASS | — |
| 05 | R05-04 | Functional scenarios | 10 tests | test_kt05_vdnh_news.py | Hist 9P/1F; remediation **10 PASS / 50.63s** | KT05.docx | PASS | — |
| 05 | R05-05 | Defect analysis | yes | defect-analysis.md | no product bug confirmed | KT05.docx | PASS | — |
| 05 | R05-06 | Recommendations | yes | recommendations.md | — | KT05.docx | PASS | — |
| 06 | R06-01 | Choose mobile app | ApiDemos | kt06-test-plan.md | — | KT06.docx | PASS | N/A payments/auth |
| 06 | R06-02 | Platform characteristics | API 36 emulator | plan + environment-report | — | KT06.docx | PASS | Real device NOT RUN |
| 06 | R06-03 | Strategy / test types | yes | plan/report | — | KT06.docx | PASS | — |
| 06 | R06-04 | Scenarios + execution | 10 tests | test_kt06_appium.py | Hist 7 PASS; remediation **10 PASS / 67.70s** | KT06.docx | PASS | — |
| 06 | R06-05 | Defects + analysis | INC-06-01 test-only | defect-analysis.md | no app bugs | KT06.docx | PASS | — |
| 07 | R07-01 | Multi-node Grid | Hub+2 Nodes | start_hub_multi_node.ps1 | nodes=2 | KT07.docx | PASS | Not multi-machine |
| 07 | R07-02 | Different browsers | Chrome+Firefox | test_kt07_multi_node.py | 4 PASS / 7.72s | KT07.docx | PASS | — |
| 07 | R07-03 | Parallel overlap | yes | run_kt07_parallel_proof.py | overlap=true | KT07.docx | PASS | — |
| 08 | R08-01 | Public site screenshots | Sauce + Allure | test_kt08_public_allure.py | 9 PASS / 34.64s | KT08.docx | PASS | — |
| 08 | R08-02 | Allure HTML attachments | yes | allure-report artifacts | — | KT08.docx | PASS | — |
| 09 | R09-01 | BASIC multi-OS public web (auto) | Win+Android | xp + DOM W01–W10 | Win 2P; Android DOM **11 PASS / 36.91s** | KT09.docx | PASS | Auto only |
| 09 | R09-02 | Manual testing | checklist + guide | kt09-manual-*.md | — | KT09.docx | **PENDING** | Human verification required |
| 09 | R09-03 | Screenshots + comparison | auto yes / manual no | platform-comparison.md | DOM screenshots | KT09.docx | PARTIAL | Manual screenshots empty |
| 09 | R09-04 | Gestures (suppl.) | Android | test_kt09_gestures.py | 5 PASS / 54.93s | KT09.docx | PASS | — |
| 10 | R10-01 | Responsive multi-browser | Sauce matrix | test_kt10_responsive.py | 6 PASS / 42.73s | KT10.docx | PASS | — |
| 10 | R10-02 | Desktop/tablet/phone | yes | 36 rows | overflow none | KT10.docx | PASS | — |
| 11 | R11-01 | ≥10 Robot cases | 10 | robot/tests/kt11.robot | 10 PASS / 28.39s | KT11.docx | PASS | — |
| 12 | R12-01 | ≥10 gRPC cases | 10 | grpc/tests/test_kt12_grpc.py | 10 PASS / 2.34s | KT12.docx | PASS | — |

## Prominent open items

1. **KT09 manual** — `PENDING HUMAN VERIFICATION` (`mobile/docs/kt09-manual-execution-guide.md`).
2. **KT04 Components** — **PARTIAL** (labels substitute on team-managed project; native Components not created without approval).
3. **KT04 dashboard gadgets** — dashboard exists; charts need UI filter selection.
4. **Personal DOCX fields** — fill `reports/report_metadata.json` (do not invent).
5. **KT09 iOS** — NOT RUN.
6. **KT07** — multi-node on one host (not multi-machine).

## Title-page personal metadata

Shared config: `reports/report_metadata.json` (+ `reports/report_title.py`).  
Empty fields render as underscore placeholders. **Do not invent** student/group/teacher.
