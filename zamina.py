from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import config
import time


def save_img():
    driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))

    try:
        driver.get(config.domen)
        time.sleep(2)
        img_url = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[5]/div/div/div[1]/div[1]/div/div/div[1]/div[3]/div/p/img').get_attribute('src')
        driver.get(img_url)
        driver.save_full_page_screenshot('img.png')
    except Exception:
        pass
    finally:
        driver.close()
        driver.quit()
        print('[Driver quit!]')
