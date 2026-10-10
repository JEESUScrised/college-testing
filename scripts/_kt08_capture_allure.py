from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

shots = Path("screenshots/kt08")
report = Path("selenium/artifacts/kt08/allure-report/index.html").resolve().as_uri()
opts = Options()
opts.add_argument("--window-size=1400,1000")
d = webdriver.Chrome(options=opts)
try:
    d.get(report)
    WebDriverWait(d, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)
    p1 = shots / "allure_01_overview.png"
    assert d.save_screenshot(str(p1)) and p1.stat().st_size > 1000
    # Suites nav
    clicked = False
    for sel in ["a[href='#suites']", "[data-tooltip='Suites']", ".side-nav__link"]:
        for el in d.find_elements(By.CSS_SELECTOR, sel):
            try:
                el.click()
                clicked = True
                break
            except Exception:
                continue
        if clicked:
            break
    time.sleep(1.5)
    p2 = shots / "allure_02_suites.png"
    assert d.save_screenshot(str(p2)) and p2.stat().st_size > 1000
    print("OK", p1.stat().st_size, p2.stat().st_size, d.title)
finally:
    d.quit()
