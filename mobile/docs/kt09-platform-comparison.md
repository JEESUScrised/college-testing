# KT09 — Windows vs Android comparison matrix

App: https://www.saucedemo.com/

| Scenario | Windows Chrome | Windows Firefox | Android Chrome | Difference | Conclusion |
|---|---|---|---|---|---|
| Load login | PASS | PASS | PASS (W01) | Desktop wider layout | Compatible |
| Login form | PASS | PASS | PASS (W02) | Touch vs mouse | Compatible |
| Auth → inventory | PASS | PASS | PASS (W03/W04) | Mobile single column | Compatible |
| Product details | PASS (KT02/03) | — | PASS (W05) | Same DOM | Compatible |
| Add to cart | PASS | — | PASS (W06) | Same badge UX | Compatible |
| Cart | PASS | — | PASS (W07) | Same cart.html | Compatible |
| Checkout required | PASS (KT02) | — | PASS (W08) | Same validation | Compatible |
| Menu | PASS (KT10) | PASS (KT10) | PASS (W09) | Burger more critical on phone | Compatible |
| Overflow | none (KT10) | none | none (W10) | — | **No defect** |

**Functional defects:** none confirmed.  
**Usability:** Chrome onboarding promos may appear on Android before the page; dismissed via chromeOptions / FRE flags where possible.  
**Manual human comparison:** PENDING HUMAN VERIFICATION.
