import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://localhost:8081/")
print(driver.title) #PrestaShop

time.sleep(5)
driver.quit()