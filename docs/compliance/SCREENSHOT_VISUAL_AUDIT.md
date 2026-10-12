# Screenshot visual audit (KT01–KT12, excluding KT09)

Date: 2026-10-12

KT09 excluded — separate remediation commit `cb50cf1`.

## Summary

| Quality | Count |
|---|---:|
| GOOD | 170 |
| DEFECTIVE | 0 |
| NEEDS_REVIEW | 0 |
| INTENTIONAL_BLANK | 3 |

**Total audited (excl. KT09):** 173

## Confirmed root causes

1. **Premature screenshot** before fonts/images painted → SauceDemo UI without text (KT02/03/08/10). Minimal repro: `wait_visually_ready()` yields readable Chrome captures.
2. **Allure opened via `file://`** → Overview `Loading...`, Suites `404`. Fixed by HTTP static server + wait for widgets.
3. **KT05 Chrome `imagesEnabled=false`** under `page-load-strategy=none` → broken carousel/event images. Recaptured with images enabled; CDN failures documented, not painted in.
4. **KT07 blank session PNGs** are intentional empty remote sessions.

## Remediation actions taken

- Added `selenium/screenshot_ready.py` (`wait_visually_ready`, Chrome screenshot args).
- Wired settle wait into `save_screenshot` fixture and KT10 responsive `_shot`.
- Recaptured SauceDemo public evidence (KT02/03/08), KT10 responsive matrix, KT05 VDNH, Allure overview/suites.
- Contact sheets: `screenshots/_audit_contact_sheets/`.

## Per-file inventory

| KT | Path | Scenario | Size | WxH | Quality | Problem | Action |
|---|---|---|---:|---|---|---|---|
| kt01 | `screenshots/kt01/ya_ru_opened.png` | ya_ru_opened | 264786 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/01_main_window_before_open.png` | 01_main_window_before_open | 12852 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/02_after_open_still_on_main.png` | 02_after_open_still_on_main | 13173 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/03_switched_to_new_window.png` | 03_switched_to_new_window | 13271 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/04_new_window_content_verified.png` | 04_new_window_content_verified | 13271 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/05_before_close_secondary.png` | 05_before_close_secondary | 13271 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/06_returned_to_main_window.png` | 06_returned_to_main_window | 13173 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/07_iframe_host_before_switch.png` | 07_iframe_host_before_switch | 21339 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/08_iframe_interaction_result.png` | 08_iframe_interaction_result | 21832 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/09_inside_iframe_before_default_content.png` | 09_inside_iframe_before_default_content | 21339 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/10_back_to_default_content.png` | 10_back_to_default_content | 21339 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt02 | `screenshots/kt02/public/bound_01_empty_zip.png` | bound_01_empty_zip | 33813 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/bound_02_min_zip.png` | bound_02_min_zip | 31431 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/neg_01_empty_username.png` | neg_01_empty_username | 31186 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/neg_02_empty_password.png` | neg_02_empty_password | 31800 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/neg_03_bad_credentials.png` | neg_03_bad_credentials | 32166 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/neg_04_checkout_required.png` | neg_04_checkout_required | 33813 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/pos_01_inventory.png` | pos_01_inventory | 264878 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/pos_02_cart.png` | pos_02_cart | 40826 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/pos_03_checkout_complete.png` | pos_03_checkout_complete | 39278 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/tech_01_locators.png` | tech_01_locators | 264878 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/tech_02_cookies.png` | tech_02_cookies | 264878 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt02 | `screenshots/kt02/public/tech_03_secondary_tab.png` | tech_03_secondary_tab | 266616 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt03 | `screenshots/kt03/01_po_main_before_open.png` | 01_po_main_before_open | 12852 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/02_po_after_open_on_main.png` | 02_po_after_open_on_main | 13173 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/03_po_switched_to_secondary.png` | 03_po_switched_to_secondary | 13271 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/04_po_secondary_content_verified.png` | 04_po_secondary_content_verified | 13271 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/05_po_before_close_secondary.png` | 05_po_before_close_secondary | 13271 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/06_po_returned_to_main.png` | 06_po_returned_to_main | 13173 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/07_po_iframe_host.png` | 07_po_iframe_host | 21339 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/08_po_iframe_interaction.png` | 08_po_iframe_interaction | 22708 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/09_po_back_to_default_content.png` | 09_po_back_to_default_content | 22708 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt03 | `screenshots/kt03/public/po_01_login_form.png` | po_01_login_form | 28290 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt03 | `screenshots/kt03/public/po_02_inventory_via_po.png` | po_02_inventory_via_po | 264878 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt03 | `screenshots/kt03/public/po_03_product_details.png` | po_03_product_details | 113654 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt03 | `screenshots/kt03/public/po_04_cart.png` | po_04_cart | 40826 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt03 | `screenshots/kt03/public/po_05_checkout_complete.png` | po_05_checkout_complete | 39278 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt03 | `screenshots/kt03/public/po_06_logout.png` | po_06_logout | 28290 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt04 | `screenshots/kt04/jira/01_board_college_qa.png` | 01_board_college_qa | 79244 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/02_issue_KAN-4.png` | 02_issue_KAN-4 | 133485 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/03_filter_bugs_done.png` | 03_filter_bugs_done | 97544 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/final/02_KAN-4_issue_comments.png` | 02_KAN-4_issue_comments | 133461 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/final/03_KAN-4_history.png` | 03_KAN-4_history | 133661 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/final/04_project_summary.png` | 04_project_summary | 115521 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/final/05_dashboard_kt04_reports.png` | 05_dashboard_kt04_reports | 87185 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/final/06_board_done_bugs.png` | 06_board_done_bugs | 97284 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/final/07_saved_filter_bugs_done.png` | 07_saved_filter_bugs_done | 102271 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/jira/final/08_dashboard_configured_stats.png` | 08_dashboard_configured_stats | 110158 | 1265x602 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/lifecycle/retest_seed001_empty_password.png` | retest_seed001_empty_password | 21429 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/lifecycle/retest_seed002_invalid_email.png` | retest_seed002_invalid_email | 15053 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/lifecycle/retest_seed003_zero_quantity.png` | retest_seed003_zero_quantity | 19946 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/tc01_valid_login.png` | tc01_valid_login | 16743 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/tc02_seed001_empty_password.png` | tc02_seed001_empty_password | 16743 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/tc03_seed002_invalid_email.png` | tc03_seed002_invalid_email | 14169 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/tc04_seed003_zero_quantity.png` | tc04_seed003_zero_quantity | 19194 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt04 | `screenshots/kt04/tc05_valid_order.png` | tc05_valid_order | 19165 | 1264x749 | GOOD | spot-check OK / local fixture / portal | keep |
| kt05 | `screenshots/kt05/01_home_opened.png` | 01_home_opened | 621511 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/02_news_section_loaded.png` | 02_news_section_loaded | 674146 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/03_news_heading.png` | 03_news_heading | 672746 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/04_news_cards.png` | 04_news_cards | 673484 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/05_news_card_links.png` | 05_news_card_links | 671051 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/06_article_opened.png` | 06_article_opened | 789476 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/07_article_heading.png` | 07_article_heading | 787999 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/08_back_to_news.png` | 08_back_to_news | 697112 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/09_before_show_more.png` | 09_before_show_more | 698528 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/10_after_show_more.png` | 10_after_show_more | 703115 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/11_news_to_home_logo.png` | 11_news_to_home_logo | 675239 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt05 | `screenshots/kt05/12_home_to_news_menu.png` | 12_home_to_news_menu | 674331 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt06 | `screenshots/kt06/01_app_home.png` | 01_app_home | 70697 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/02_app_menu.png` | 02_app_menu | 93473 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/03_alert_dialogs.png` | 03_alert_dialogs | 129987 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/04_list_dialog.png` | 04_list_dialog | 124337 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/05_text_entry_dialog.png` | 05_text_entry_dialog | 129769 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/06_back_to_app_menu.png` | 06_back_to_app_menu | 93473 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/07_back_to_home.png` | 07_back_to_home | 70697 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/08_textfields.png` | 08_textfields | 37256 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/09_dialog_before_cancel.png` | 09_dialog_before_cancel | 128999 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/10_dialog_after_cancel.png` | 10_dialog_after_cancel | 129921 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/11_textfields_cleared.png` | 11_textfields_cleared | 32480 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt06 | `screenshots/kt06/12_home_a11y.png` | 12_home_a11y | 70630 | 1080x2400 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/01_remote_session_blank.png` | 01_remote_session_blank | 5208 | 1384x849 | INTENTIONAL_BLANK | empty initial Grid session | keep as blank-session evidence |
| kt07 | `screenshots/kt07/02_navigate_title.png` | 02_navigate_title | 19057 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/03_dom_interaction.png` | 03_dom_interaction | 19223 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/04_windows_main.png` | 04_windows_main | 13638 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/05_windows_secondary.png` | 05_windows_secondary | 14041 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/06_windows_back_main.png` | 06_windows_back_main | 13956 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/07_iframe_host.png` | 07_iframe_host | 22125 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/08_iframe_inside.png` | 08_iframe_inside | 22930 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/09_iframe_default_content.png` | 09_iframe_default_content | 23754 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/multi/chrome_01_session.png` | chrome_01_session | 5208 | 1384x849 | INTENTIONAL_BLANK | empty initial Grid session | keep as blank-session evidence |
| kt07 | `screenshots/kt07/multi/chrome_02_landing.png` | chrome_02_landing | 19057 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/multi/firefox_01_session.png` | firefox_01_session | 6901 | 1384x907 | INTENTIONAL_BLANK | empty initial Grid session | keep as blank-session evidence |
| kt07 | `screenshots/kt07/multi/firefox_02_landing.png` | firefox_02_landing | 18108 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/multi/parallel_chrome_overlap.png` | parallel_chrome_overlap | 19057 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt07 | `screenshots/kt07/multi/parallel_firefox_overlap.png` | parallel_firefox_overlap | 17337 | 1280x851 | GOOD | spot-check OK / local fixture / portal | keep |
| kt08 | `screenshots/kt08/01_home_actual.png` | 01_home_actual | 19142 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt08 | `screenshots/kt08/02_text_color_actual.png` | 02_text_color_actual | 19274 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt08 | `screenshots/kt08/03_layout_shift_actual.png` | 03_layout_shift_actual | 19083 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt08 | `screenshots/kt08/04_significant_actual.png` | 04_significant_actual | 18309 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt08 | `screenshots/kt08/05_dimension_mismatch_actual.png` | 05_dimension_mismatch_actual | 16061 | 884x549 | GOOD | spot-check OK / local fixture / portal | keep |
| kt08 | `screenshots/kt08/allure_01_overview.png` | allure_01_overview | 56155 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt08 | `screenshots/kt08/allure_02_suites.png` | allure_02_suites | 25813 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt08 | `screenshots/kt08/public_01_login_page.png` | public_01_login_page | 28290 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt08 | `screenshots/kt08/public_02_inventory.png` | public_02_inventory | 264878 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt08 | `screenshots/kt08/public_03_sort_dropdown.png` | public_03_sort_dropdown | 267962 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt08 | `screenshots/kt08/public_04_add_to_cart.png` | public_04_add_to_cart | 113421 | 1384x849 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/chrome_01_home_title.png` | chrome_01_home_title | 23143 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/chrome_02_dom_click.png` | chrome_02_dom_click | 23002 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/chrome_03_form_invalid.png` | chrome_03_form_invalid | 23579 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/chrome_04_form_valid.png` | chrome_04_form_valid | 25061 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/chrome_05_secondary_window.png` | chrome_05_secondary_window | 14041 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/chrome_06_back_main_window.png` | chrome_06_back_main_window | 13956 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/chrome_07_inside_iframe.png` | chrome_07_inside_iframe | 22476 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/chrome_08_default_content.png` | chrome_08_default_content | 22476 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/FAIL_chrome_test_intentional_failure_for_screenshot_hook[chrome].png` | FAIL_chrome_test_intentional_failure_for_screenshot_hook[chrome] | 23143 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_01_home_title.png` | firefox_01_home_title | 21496 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_02_dom_click.png` | firefox_02_dom_click | 21506 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_03_form_invalid.png` | firefox_03_form_invalid | 21842 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_04_form_valid.png` | firefox_04_form_valid | 23025 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_05_secondary_window.png` | firefox_05_secondary_window | 13690 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_06_back_main_window.png` | firefox_06_back_main_window | 13437 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_07_inside_iframe.png` | firefox_07_inside_iframe | 21187 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/firefox_08_default_content.png` | firefox_08_default_content | 21187 | 1384x907 | GOOD | spot-check OK / local fixture / portal | keep |
| kt10 | `screenshots/kt10/responsive/chrome_desktop_r01_layout.png` | chrome_desktop_r01_layout | 27852 | 1424x749 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_desktop_r02_login_form.png` | chrome_desktop_r02_login_form | 27852 | 1424x749 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_desktop_r03_inventory.png` | chrome_desktop_r03_inventory | 226084 | 1424x749 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_desktop_r04_menu_open.png` | chrome_desktop_r04_menu_open | 195770 | 1424x749 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_desktop_r05_cart.png` | chrome_desktop_r05_cart | 40127 | 1424x749 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_desktop_r06_checkout.png` | chrome_desktop_r06_checkout | 26445 | 1424x749 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_phone_r01_layout.png` | chrome_phone_r01_layout | 56101 | 780x1688 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_phone_r02_login_form.png` | chrome_phone_r02_login_form | 56101 | 780x1688 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_phone_r03_inventory.png` | chrome_phone_r03_inventory | 138937 | 780x1688 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_phone_r04_menu_open.png` | chrome_phone_r04_menu_open | 24153 | 780x1688 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_phone_r05_cart.png` | chrome_phone_r05_cart | 93682 | 780x1688 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_phone_r06_checkout.png` | chrome_phone_r06_checkout | 72082 | 780x1688 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_tablet_r01_layout.png` | chrome_tablet_r01_layout | 62094 | 1536x2048 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_tablet_r02_login_form.png` | chrome_tablet_r02_login_form | 62094 | 1536x2048 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_tablet_r03_inventory.png` | chrome_tablet_r03_inventory | 451150 | 1536x2048 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_tablet_r04_menu_open.png` | chrome_tablet_r04_menu_open | 162973 | 1536x2048 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_tablet_r05_cart.png` | chrome_tablet_r05_cart | 100468 | 1536x2048 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/chrome_tablet_r06_checkout.png` | chrome_tablet_r06_checkout | 79624 | 1536x2048 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_desktop_r01_layout.png` | firefox_desktop_r01_layout | 26872 | 1424x807 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_desktop_r02_login_form.png` | firefox_desktop_r02_login_form | 26872 | 1424x807 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_desktop_r03_inventory.png` | firefox_desktop_r03_inventory | 308610 | 1424x807 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_desktop_r04_menu_open.png` | firefox_desktop_r04_menu_open | 308196 | 1424x807 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_desktop_r05_cart.png` | firefox_desktop_r05_cart | 37382 | 1424x807 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_desktop_r06_checkout.png` | firefox_desktop_r06_checkout | 30258 | 1424x807 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_phone_r01_layout.png` | firefox_phone_r01_layout | 21932 | 500x751 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_phone_r02_login_form.png` | firefox_phone_r02_login_form | 21932 | 500x751 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_phone_r03_inventory.png` | firefox_phone_r03_inventory | 113002 | 500x751 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_phone_r04_menu_open.png` | firefox_phone_r04_menu_open | 26070 | 500x751 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_phone_r05_cart.png` | firefox_phone_r05_cart | 28647 | 500x751 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_phone_r06_checkout.png` | firefox_phone_r06_checkout | 26056 | 500x751 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_tablet_r01_layout.png` | firefox_tablet_r01_layout | 24109 | 752x931 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_tablet_r02_login_form.png` | firefox_tablet_r02_login_form | 24109 | 752x931 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_tablet_r03_inventory.png` | firefox_tablet_r03_inventory | 159358 | 752x931 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_tablet_r04_menu_open.png` | firefox_tablet_r04_menu_open | 132186 | 752x931 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_tablet_r05_cart.png` | firefox_tablet_r05_cart | 34915 | 752x931 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt10 | `screenshots/kt10/responsive/firefox_tablet_r06_checkout.png` | firefox_tablet_r06_checkout | 28873 | 752x931 | GOOD | recaptured/verified 2026-10-12 | keep |
| kt11 | `screenshots/kt11/01_home_title.png` | 01_home_title | 22507 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/02_navigation_register.png` | 02_navigation_register | 14590 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/03_form_valid.png` | 03_form_valid | 18599 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/04_form_invalid.png` | 04_form_invalid | 15600 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/05_checkbox.png` | 05_checkbox | 21642 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/06_radio.png` | 06_radio | 22105 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/07_dropdown.png` | 07_dropdown | 21726 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/08_iframe.png` | 08_iframe | 22617 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/09_back_main.png` | 09_back_main | 23118 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/09_secondary_tab.png` | 09_secondary_tab | 14556 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/10_dynamic_update.png` | 10_dynamic_update | 22772 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/11_robot_report.png` | 11_robot_report | 63982 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt11 | `screenshots/kt11/12_robot_log.png` | 12_robot_log | 83897 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
| kt12 | `screenshots/kt12/01_pytest_html_report.png` | 01_pytest_html_report | 67353 | 1384x849 | GOOD | spot-check OK / local fixture / portal | keep |
