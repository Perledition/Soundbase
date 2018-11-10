import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import google_login
import time

# Initialize variables -> outsource to Maintenance class
temp_gate_url = 'http://thehusk.ca/gate.asp?t=518244894'
comment_str = 'Yeah'
gate_insert_mail = 'promo@trackbase.com'


# Define Chrome session options in options object
options = webdriver.ChromeOptions()

# TODO: Headless not running yet
# options.add_argument('headless')

options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--allow-running-insecure-content")
# Also used to deactivate images to speed up script, but some buttons are
# embedded in <img> tags, so images are necessary unfortunately
# OPTIMIZATION -> possible to dynamically change options of Driver Object?
# Then image loading could be turn on only on respective pages.

# Initialize the driver
driver = webdriver.Chrome(options = options)

# Do the google login and get session cookies
google_login.google_login(driver)

# Open new tab with gate link and switch to tab
driver.execute_script("window.open('{}')".format(temp_gate_url))
driver.switch_to.window(driver.window_handles[-1])


# Optionally load cookies (probably not necessary -> temp cookies generated
# through login)
# driver = cookiesaver.load_cookie(driver,
# os.path.dirname(os.path.realpath(__file__)))


# Mandatory sleep time to let page elements initialize
# TODO: Build dynamic function to set sleep time depending on actuall download
# connection speed
time.sleep(1)

# Find and click 'Download' button
driver.find_element_by_id('dlbutton').click()

# Strange combination of commands that work (trial and error but fast!)
driver.find_element_by_id('genre1').click()
driver.execute_script('adjSaveButton();')
driver.find_element_by_id('genre2').click()
driver.find_element_by_id('genre3').click()
driver.find_element_by_id('savechoice').click()

# Find center SoundCloud login button and click it
driver.find_element_by_xpath("//*[@id='step1']/center/img").click()

# Switch to new popup window and let things initialize (important!)
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2)

# When Google login button has initialize, click it and start authentication
# process with local session cookies
WebDriverWait(driver, 120).until( EC.presence_of_element_located((By.XPATH,
"//*[@id='main-wrapper']/div[2]/div[1]/a[2]"))).click()

# Switch back to second tab (gate window)
driver.switch_to.window(driver.window_handles[1])

# Set implicit wait on webdriver (important to make interaction with comment
# field work!)
driver.implicitly_wait(3)

# Find the comment field and send string to it, then click 'Save'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,
'comment'))).send_keys(comment_str)
driver.find_element_by_id('savecomment').click()

# Find the email field and send string to it, then click 'Save'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,
'email'))).send_keys(gate_insert_mail)
driver.find_element_by_id('saveemail').click()

# Additional skip step (TODO: NEED STEP HANDLING WITH EXTRACTOR CLASS HERE!)
driver.find_element_by_id('mailskipbutton').click()

print('Done')
driver.quit()
