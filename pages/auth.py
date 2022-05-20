import requests as r
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class Auth:
    def __init__(self):
        self.baseUrl = "https://sephir.ch/ICT/user/lernendenportal"

    def get_tokens(self):
        res = r.get(f"{self.baseUrl}")
        html = res.text
        self.__parse_tokens__(html)
        print(f"{res.status_code} Get Tokens")

    def __parse_tokens__(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        token_url = urlparse(
            soup.find(id="mainFrame").get('src')
        )
        query_params = parse_qs(token_url.query)
        self.cfid = query_params.get('cfid')[0]
        self.cftoken = query_params.get('cftoken')[0]

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        res = r.post(f"{self.baseUrl}/login_action.cfm?cfid{self.cfid}&cftoken={self.cftoken}",
                     {'email': username, 'passwort': password})
        print(f"{res.status_code} Do Login")

    def __get_logged_in_url__(self):
        return f"{self.baseUrl}/10_start/frameset_start.cfm?cfid={self.cfid}&cftoken={self.cftoken}"

    def get_home(self):
        res = r.get(self.__get_logged_in_url__())
        print(res.text)