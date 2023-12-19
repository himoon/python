from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import events

driver = webdriver.Chrome()

# https://chromedevtools.github.io/devtools-protocol/
# driver.execute_cdp_cmd()

driver.get("https://youtube.com")
driver.execute_cdp_cmd("Network.enable", {})
# driver.execute_cdp_cmd('Network.getResponseBody', {})
driver.execute_cdp_cmd("Network.dataReceived", {})


title = driver.title

driver.implicitly_wait(0.5)

# text_box = driver.find_element(by=By.NAME, value="my-text")
# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# text_box.send_keys("Selenium")
# submit_button.click()

# message = driver.find_element(by=By.ID, value="message")
# text = message.text

# driver.quit()
