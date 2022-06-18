from argparse import Action
import os
from xvfbwrapper import Xvfb
from time import sleep
from urllib.parse import urlparse
from dotenv import dotenv_values, load_dotenv
from selenium import webdriver
from selenium.webdriver import FirefoxOptions, Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
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
        
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        options.set_preference("browser.download.dir", "C:\\Users\\enea\\Downloads\\")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("print.always_print_silent", True)
        options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
        options.set_preference("print_printer", "Mozilla Save to PDF")
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)

        self.wait2 = WebDriverWait(self.driver, 2)
        self.wait = WebDriverWait(self.driver, 10)

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
        self.wait.until(EC.presence_of_element_located((By.XPATH, uk_table_path)))
        uk_table = self.driver.find_element(By.XPATH, uk_table_path)
        uk_list = uk_table.find_elements(By.CLASS_NAME, "dsicon")
        uk_urls = []
        for uk in uk_list:
            a = uk.find_element(By.TAG_NAME, "a")
            uk_urls.append(a.get_attribute("href"))
        
        self.uk_urls = uk_urls

    def savePage(self, name):
        # save image
        self.driver.maximize_window()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("-").perform()
        body = self.driver.find_element(By.TAG_NAME, "body")
        with open(f"{name}.png", "wb") as f:
            f.write(body.screenshot_as_png)
            f.close()

    def getUKMarks(self):
        marks=[]
        counter = 0
        for url in self.uk_urls:
            counter += 1
            self.driver.get(url)

            bewertung = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/table/tbody/tr/td[4]")
            bewertung.click()

            kurs_bewertung = self.driver.find_elements(By.LINK_TEXT, "Kursbewertung öffnen")

            if len(kurs_bewertung) == 2:
                kurs_bewertung[1].click()
            else:
                # Exit loop
                print(f"ÜK {counter} - No Mark")
                break

            self.wait.until(EC.number_of_windows_to_be(2))

            new_window_handle = self.driver.window_handles[1]
            self.driver.switch_to.window(new_window_handle)

            # handle unexpected alerts
            try:
                self.wait2.until(EC.alert_is_present())
                self.driver.switch_to.alert.accept()
                self.savePage(f"uk_{counter}")
            except NoAlertPresentException:
                self.savePage(f"uk_{counter}")
            except TimeoutException:
                self.savePage(f"uk_{counter}")

            mark = self.driver.find_element(By.XPATH, "/html/body/table[1]/tbody/tr[9]/td/table[4]/tbody/tr[4]/td[3]/div/b")
            marks.append({"uk": counter, "mark": mark.get_attribute("value")})
        print(marks)
                

    def close(self):
        self.driver.quit()

def main(app):
    vdi = Xvfb()
    vdi.start()

    app.openLogin()
    app.fillLoginForm()
    app.getTokens()
    app.openUKPage()
    app.getUKList()
    app.getUKMarks()
    app.close()

    vdi.stop()

if __name__=="__main__":
    main(
        App()
    )