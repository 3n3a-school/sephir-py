import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()

class App:
    def __init__(self):
        self.user = {
            "email": os.getenv("USERNAME"),
            "password": os.getenv("PASSWORD")
        }
        self.url = "https://sephir.ch/ict/user/lernendenportal"
        
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)
    
    def openLogin(self):
        self.driver.get(f"{self.url}/login.cfm")

    def fillLoginForm(self):
        email = self.driver.find_element(By.NAME, "email")
        password = self.driver.find_element(By.NAME, "passwort")
        submitBtn = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        email.send_keys(self.user.get("email"))
        password.send_keys(self.user.get("password"))
        submitBtn.click()

    def close(self):
        self.driver.quit()

def main(app):
    app.openLogin()
    app.fillLoginForm()

if __name__=="__main__":
    main(
        App()
    )