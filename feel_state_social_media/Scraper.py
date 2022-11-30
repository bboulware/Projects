#Libraries needed 
import numpy as np
import time as tm
import pandas as pd
import regex as re
import os
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth

# Dictionary to hold data before saving as a csv.
data = {'Time':[],'Post':[],'Image':[],'Caption':[],'Likes':[],'Hashtags':[]}

class Insta_Bot:
    #Options for our driver
    options =webdriver.ChromeOptions()
    options.add_argument('--disable-blink-feature=AutomationControlled')
    options.add_argument('--flags#enable-new-usb-backend')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    def __init__(self, search, amount):
        self.search  = search
        self.amount = amount
        self.log_in()
        self.scrape_data()
        self.save_data()

    def log_in(self):
        __username = 'notarobot8591'
        __password = 'Lucille1515'

        #Options for our driver
        options =webdriver.ChromeOptions()

        #options.add_argument('headless')
        options.add_argument('--disable-blink-feature=AutomationControlled')
        options.add_argument('--flags#enable-new-usb-backend')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        #Creating our driver object
        global driver
        driver = webdriver.Chrome(options = options, service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(5)
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        #Opens browser and logins in
        driver.get('http://www.instagram.com')

        #Login information entered into text boxes
        driver.find_element(By.NAME,'username').send_keys(__username)
        driver.find_element(By.NAME, 'password').send_keys(__password)
        tm.sleep(1)
        driver.find_element(By.XPATH,'//div[contains(text(),"Log in")]').click()

        #Not now notifications
        driver.find_element(By.XPATH, '//*[contains(text(),"Not Now")]').click()
        driver.find_element(By.XPATH, '//*[contains(text(),"Not Now")]').click()
    
    def scrape_data(self):

        #Looks for search box and inserts search from args 
        driver.find_element(By.XPATH,'//div[contains(text(),"Search")]').click()
        ActionChains(driver).send_keys(self.search).perform()
        tm.sleep(1)
        ActionChains(driver).send_keys(Keys.ENTER).perform()

        #Loop for the amount of specified post
        for i in range(self.amount):
            #Image containers
            img_box = driver.find_elements(By.XPATH, value = '//div[@class="_aagv"]/img')
            img=[img.get_attribute('alt') for img in img_box]

            # Code tries to look for next arrow for gallery of photos on post
            try:
                #scrapes description for first two photos in gallery 
                driver.find_element(By.XPATH, value = '//div[@class="_9zm2"]')
                if any("Photo by" in s for s in img):
                    data['Image'].append(img[-2:])
                else:
                    data['Image'].append('Video')

            # Code when no gallery detected scrapes description for single image
            except NoSuchElementException:
                if any("Photo by" in s for s in img):
                    data['Image'].append(img[-1])
                else:
                    data['Image'].append('Video')
            
            #Scrapes post url 
            post = driver.current_url
            data['Post'].append(post)
            
            #Verifies XPATH location for likes and scrapes data
            try:
                likes = driver.find_element(By.XPATH, value = '//div[@class="_aacl _aaco _aacw _aacx _aada _aade"]/span')
                likes = likes.text
            except NoSuchElementException:
                likes = driver.find_elements(By.XPATH, value = '//div[@class="_aacl _aaco _aacw _aacx _aad6 _aade"]')[-1].click()
        
            except NoSuchElementException:
                likes = driver.find_element(By.XPATH, value = '//div[@class="_aauu"]/span')
                likes = likes.text
            except NoSuchElementException:
                likes = 'Not Displayed'
            finally: 
                data['Likes'].append(likes) 
        
            #Scrapes Hashtags BY XPATH location
            hashtags = driver.find_elements(By.XPATH, value = '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz  _aa9_ _a6hd"]')
            hashtags = [hashtag.text for hashtag in hashtags]
            data['Hashtags'].append(hashtags)
            
            #Scrapes dat/time by XPATH 
            date_location = driver.find_element(By.TAG_NAME, value = 'time')
            time_attribute = date_location.get_attribute('datetime')
            data['Time'].append(time_attribute)
            
            #Scrape post caption by XPATH if available
            try:
                text_box = driver.find_element(By.XPATH, value = '//div[@class="_a9zs"]/span')
                caption = text_box.text
                data['Caption'].append(caption)
            except NoSuchElementException:
                pass

            #Clicking Next post and sleeping for (1-3) seconds
            tm.sleep(randint(1,3)) 
            ActionChains(driver).key_down(Keys.ARROW_RIGHT).key_up(Keys.ARROW_RIGHT).perform()
            
    # Function for saving temporary dictionary to csv. 
    def save_data(self):
        dataframe = pd.DataFrame.from_dict(self.data)
        dataframe.to_csv(f'C:/Users/bboul/OneDrive/Documents/feel_state_data/{self.search}_'f'{self.amount}.csv', index=False)
        print('Post Scrapped: '+str(len(dataframe.index)))
