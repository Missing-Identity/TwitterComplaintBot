import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

class TwitterComplaintBot():

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.up = 10
        self.down = 150

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(5)
        go = self.driver.find_element(By.CSS_SELECTOR, ".js-start-test .start-text")
        go.click()
        time.sleep(60)
        down = self.driver.find_element(By.CSS_SELECTOR, ".result-data .download-speed").text
        up = self.driver.find_element(By.CSS_SELECTOR, ".result-data .upload-speed").text
        self.down = float(down)
        self.up = float(up)
        print(f"Download Speed: {self.down} Mbps")
        print(f"Upload Speed: {self.up} Mbps")

    def tweet(self):
        self.driver.get("https://twitter.com/login")
        time.sleep(8)
        load_dotenv()
        username = self.driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
        username.send_keys(os.getenv("TWITTER_EMAIL"))
        username.send_keys(Keys.TAB)
        username.send_keys(Keys.ENTER)
        time.sleep(5)
        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys(os.getenv("TWITTER_PASSWORD"))
        password.send_keys(Keys.TAB)
        password.send_keys(Keys.ENTER)
        time.sleep(8)
        tweet = self.driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        tweet.send_keys(f"Hey!, why is my internet speed {self.down}down/{self.up}up when I pay for 150down/10up?")
        time.sleep(5)
        tweet_button = self.driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
        tweet_button.click()

bot = TwitterComplaintBot()
bot.get_internet_speed()
if bot.down < 150 or bot.up < 10:
    bot.tweet()
