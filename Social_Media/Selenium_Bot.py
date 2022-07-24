import tkinter as tk
import tkinter.ttk as ttk
import os
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
import tkinter as tk
import numpy as np
import pandas as pd

data = {'Time':[],
        'Post':[],
        'Caption':[],
        'Likes':[],
        'Hashtags':[]}
#tkinter GUI
class MainApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Frame.__init__(self, self.master)
        self.master = master
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.search = tk.StringVar()
        self.amount = tk.StringVar()
        self.login_widgets()
        self.scrape_widgets()

    def login_widgets(self):
        #Label and Entry box for username
        username_lbl = ttk.Label(self.master, text= 'Username').grid(row =0, column=0, sticky='s')
        username_entry = ttk.Entry(self.master, width = 25, textvariable = self.username).grid(row = 1, column = 0, padx = 5)

        #Label and Entry box for password
        password_lbl = ttk.Label(self.master, text= 'Password').grid(row=2, column=0, sticky='s')
        password_entry = tk.Entry(self.master, width = 25,show ='*', textvariable = self.password).grid(row = 3, column = 0,padx = 5)

        #Submit Button to begin log in function process
        submit = ttk.Button(self.master, text = 'Log In', pad = 5, command= self.log_in).grid(row = 4, column = 0, pady = 5)

    def scrape_widgets(self):
        #Label and Entry box for search
        search_lbl = ttk.Label(self.master, text= 'Search').grid(row=0, column=1, sticky='s')
        search_entry = ttk.Entry(self.master, width = 25, textvariable = self.search).grid(row = 1, column = 1, padx = 5)

        #label and Entry box for amount to scrape
        amount_lbl = ttk.Label(self.master, text= 'Amount of Post').grid(row=2, column=1, sticky='s')
        amount_entry = ttk.Entry(self.master, width = 10, textvariable = self.amount).grid(row = 3, column = 1, padx = 5)

        #Submit Button to begin search/scraping function process
        submit = ttk.Button(self.master, text = 'Scrape', pad = 5, command= self.scrape).grid(row = 4, column = 1, pady = 5)

    # Function for log in buttons
    def log_in(self):
        username = self.username.get()
        password = self.password.get()
        Log_in(username, password)

    # Function for search/scrape process
    def scrape(self):
        search = self.search.get()
        amount = self.amount.get()
        Scrape(driver, search, amount)

#logins in and scrapes data
class Log_in:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        #Options for our driver
        options =webdriver.ChromeOptions()
        options.add_argument('headless')
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
        driver.find_element(By.NAME,'username').send_keys(self.username)
        driver.find_element(By.NAME, 'password').send_keys(self.password)
        driver.find_element(By.XPATH, '//*[contains(text(),"Log In")]').click()

        #Not now notifications
        driver.find_element(By.XPATH, '//*[contains(text(),"Not Now")]').click()
        driver.find_element(By.XPATH, '//*[contains(text(),"Not Now")]').click()

        return driver

#Scrapes information from Website
class Scrape:
    def __init__(self, driver, search, amount):
        self.search = search
        self.amount = amount
        #If search box is None or empty then program will continue scraping only
        if search == '' or None:
            self.scrape_data()
        else:
            self.search_entry()
            self.scrape_data()

    def search_entry(self):
        # clicking in the search bar and filling in with search
        search_element = driver.find_element(By.CSS_SELECTOR,'[aria-label= "Search Input"]')
        search_element.send_keys(self.search)
        time.sleep(1)
        search_element.send_keys(Keys.ENTER)
        search_element.send_keys(Keys.ENTER)
        #clicking on first post
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, value = 'v1Nh3').click()

    def scrape_data(self):
        #Loop for amount of post to be scraped
        for i in range(int(self.amount)):
            #Post URL
            post = driver.current_url
            data['Post'].append(post)
            #Scraping likes in two different locations
            try:
                likes = driver.find_element(By.XPATH, value = '//div[@class="_7UhW9   xLCgt        qyrsm KV-D4               fDxYl    T0kll "]/span')
            except:
                likes = driver.find_element(By.XPATH, value = '//div[@class="_7UhW9   xLCgt        qyrsm KV-D4           uL8Hv        T0kll "]/span')
            finally:
                likes = likes.text
                data['Likes'].append(likes)
            #Scrape Hashtags
            hashtags = driver.find_elements(By.XPATH, value = '//a[@class=" xil3i"]')
            hashtags = [hashtag.text for hashtag in hashtags]
            data['Hashtags'].append(hashtags)
            #Scrape Timestamp
            date_location = driver.find_element(By.TAG_NAME, value = 'time')
            time_attribute = date_location.get_attribute('datetime')
            data['Time'].append(time_attribute)
            #Scrape post caption
            text_box = driver.find_element(By.XPATH, value = '//div[@class="MOdxS "]/span')
            caption = text_box.text
            data['Caption'].append(caption)
            #Clicking Next post and sleeping for (1-3) seconds
            ActionChains(driver).key_down(Keys.ARROW_RIGHT).key_up(Keys.ARROW_RIGHT).perform()
            time.sleep(randint(1,4))

        #Creating dataframe and saving as csv as search_amount.csv
        df = pd.DataFrame.from_dict(data)
        df.to_csv(f'C:/Users/bboul/Desktop/{self.search}_{self.amount}.csv')

if __name__=='__main__':
    root = tk.Tk()
    root.title('InstagramBot')
    myapp = MainApp(root)
    myapp.mainloop()
