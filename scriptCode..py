from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

class Scrayp:
    targetURL =r"https://ana-slo.com/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/"
    
    def __init__(self,AreaArgs:str) -> None:
        self.areaName = AreaArgs
    def star_webdriver(self):
        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get(self.targetURL)
        print("webdriver start")
        