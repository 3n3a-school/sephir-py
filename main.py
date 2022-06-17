import os
from urllib.parse import urlparse
from dotenv import dotenv_values, load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()
config = dotenv_values(".env")

class App:
    def __init__(self):
        self.user = {
            "email": config.get("USERNAME"),
            "password": config.get("PASSWORD")
        }
        self.url = "https://sephir.ch/ict/user/lernendenportal"
        
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)

    def _get_query(self, url):
        url = urlparse(url)
        query_pairs = url.query.split("&")
        query = {}
        for pair in query_pairs:
            pair = pair.split("=")
            query[pair[0]] = pair[1]
        return query
    
    def openLogin(self):
        self.driver.get(f"{self.url}/login.cfm")

    def fillLoginForm(self):
        email = self.driver.find_element(By.NAME, "email")
        password = self.driver.find_element(By.NAME, "passwort")
        submitBtn = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        email.send_keys(self.user.get("email"))
        self.driver.implicitly_wait(1)
        password.send_keys(self.user.get("password"))
        self.driver.implicitly_wait(1)
        submitBtn.click()
        self.driver.implicitly_wait(5)

    def getTokens(self):
        query = self._get_query(self.driver.current_url)
        self.cfid = query.get("cfid")
        self.cftoken = query.get("cftoken")

    def openUKPage(self):
        url = "https://sephir.ch/ict/user/lernendenportal/30_uk/ausschreibung.cfm"
        self.driver.get(f"{url}?cfid={self.cfid}&cftoken={self.cftoken}")
        self.driver.implicitly_wait(1)

    def getUKList(self):
        uk_table_path = "/html/body/table[2]"
        uk_table = self.driver.find_element(By.XPATH, uk_table_path)
        uk_list = uk_table.find_elements(By.CLASS_NAME, "dsicon")
        print(uk_list)
        for uk in uk_list:
            uk.click()
            self.driver.implicitly_wait

    def close(self):
        self.driver.quit()

def main(app):
    app.openLogin()
    app.fillLoginForm()
    app.getTokens()
    app.openUKPage()
    app.getUKList()

if __name__=="__main__":
    main(
        App()
    )