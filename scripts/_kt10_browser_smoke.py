"""Quick Chrome + Firefox WebDriver smoke for KT10 diagnose."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

c = webdriver.Chrome(options=ChromeOptions())
print("chrome_ok", c.capabilities.get("browserName"), c.capabilities.get("browserVersion"))
c.quit()

f = webdriver.Firefox(options=FirefoxOptions())
print("firefox_ok", f.capabilities.get("browserName"), f.capabilities.get("browserVersion"))
f.quit()

print("DIAGNOSE_PASS")
