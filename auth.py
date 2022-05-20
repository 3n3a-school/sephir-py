import requests as r
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

class Auth:
  def __init__(self):
    self.baseUrl = "https://sephir.ch/ICT/user/lernendenportal"

  def get(self):
    res = r.get(f"{self.baseUrl}"
    
