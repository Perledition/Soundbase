import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import pickle
import credentials


def google_login(driver):


    google_login_url = ('https://accounts.google.com/signin/v2/identifier?f'
                        'lowName=GlifWebSignIn&flowEntry=ServiceLogin')


    try:
        driver.get(google_login_url)
        driver.save_screenshot("screenshot.png")

        driver.find_element_by_id("identifierId").send_keys(
        credentials.serve_credentials('user'))
        driver.find_element_by_id("identifierNext").click()
        password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password')))
        password.send_keys(credentials.serve_credentials('pwd'))
        driver.find_element_by_class_name("CwaK9").click()

        # save_cookie(driver, os.path.dirname(os.path.realpath(__file__)))

    except ElementNotVisibleException as err:
        print(err)
        google_login(driver)

    except NoSuchElementException as err:
        print(err)
        google_login(driver)


def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver
