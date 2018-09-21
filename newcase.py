#Reflush the SF "Unassigned case queue" in every 20 seconds, if a new case arrives, sing a song.

import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import getpass
from selenium.webdriver.support.select import Select
import winsound

def verificationcode():
##Test if the verification page exists or not
    verification = driver.find_element_by_id("smc")
    key=input("Please input your verfication code:")
    verification.send_keys(key)
    driver.find_element_by_id("save").click()


def newcase():
    while True:
        try:
            ## Title: New cases created Today
            # Select(s).select_by_value("00BC0000008hfCI")
            # print("We are on the new case today page now")

            #Explicitly wait for the page to load
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "select.title[name='fcf'][id$='_listSelect']")))

            ##Locate the select box
            s = driver.find_element_by_id("00BC0000008hfCI_listSelect")
            ##Select the "Unassigned queue"
            Select(s).select_by_value("00BC0000008hqG8")
            time.sleep(1)

            #If any case subject is found
            if driver.find_elements_by_class_name("x-grid3-row-table"):
                print("Case arrives")
                # Play Windows sound.
                winsound.PlaySound(mp3, winsound.SND_FILENAME)
            else:
                print("No case now, page will be refresh by 20 seconds")

            t1=time.time()
            time.sleep(15)
            print("Time to refresh now")

            #Refresh the page
            driver.find_element_by_id("00BC0000008hfCI_refresh").click()
            print(time.time()-t1)
            time.sleep(0.5)

        except TimeoutException:
            print("Wrong! We can't find the element page.")
            break


u = getpass.getuser()
mp3 = input("Please enter your love song: ")
# # initialize Chrome options
chrome_options = Options()
# chrome_options.add_argument('window-size=1920,1080')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--headless')

## Add the user information
chrome_options.add_argument('user-data-dir=C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data' % (u))

## SF Case page
source = "https://na66.salesforce.com/500?fcf=00BC0000008hfCI"
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(source)

##Login page
try:
    driver.find_element_by_id("Login").click()
except NoSuchElementException:
    print("Can't find the login button")

## Verfication Page
if driver.find_elements_by_id("smc"):
    ##If the verification code is not correct(), Re-verify again.
    for i in range(0,4):
        try:
            verificationcode()
            if driver.find_elements_by_id("smc-error"):
                verificationcode()
            else:
                break
        except IOError:
            break
    #############################
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,"00BC0000008hfCI_listSelect")))
    newcase()

#Verfication code failed too much
elif driver.find_elements_by_id("editPage"):
    print("Too much")
    driver.quit()

#Logged in successfully.
else:
    newcase()