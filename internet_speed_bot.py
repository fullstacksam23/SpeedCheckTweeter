from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
ISP = "ACT Fibernet"
ISP_HANDLES_LIST = ["@ACTFibernet", "@ACTFibernetHYD"]


class InternetSpeedTwitterBot:

    def __init__(self, up, down):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.down = 0
        self.up = 0
        self.msg = ""
        self.minUp = up
        self.minDown = down

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_cookies = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            accept_cookies.click()
        except:
            print("No cookie found to interact with")

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "start-text")))
        start_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        start_button.click()
        try:
            result_element = WebDriverWait(self.driver, 180).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "result-data"))
            )

        except Exception as e:
            print(f"Error: {e}")
            self.driver.quit()
            return -1

        self.down = float(self.driver.find_element(By.CLASS_NAME, "download-speed").text)
        self.up = float(self.driver.find_element(By.CLASS_NAME, "upload-speed").text)
        print(self.down)
        print(self.up)


    def tweet_at_provider(self):
        self.driver.get("https://x.com/home")
        email_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, "text")))
        email_input.send_keys(TWITTER_EMAIL)
        button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
        button.click()

        try:
            username_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "text")))
            username_input.send_keys(TWITTER_USERNAME)
            next_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button')
            next_button.click()
        except:
            print("No unusual activity detected continuing with login")

        password_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input.send_keys(TWITTER_PASSWORD)
        login_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button')
        login_button.click()


        post_area = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div')))
        msg = f"Hey {ISP}, why is my internet speed {self.down}down/{self.up}up when i pay for {self.minDown}down/{self.minUp}up\n"
        for handle in ISP_HANDLES_LIST:
            msg += handle+" "
        self.msg = msg
        post_area.send_keys(msg)
        post_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')
        post_button.click()