from selenium import webdriver

from selenium.webdriver.common import by    
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time

class Scrayp:
    targetURL =r"https://ana-slo.com/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/"
    
    def __init__(self,Area:str) -> None:
        self.areaName = Area
        self.star_webdriver()
        
    def star_webdriver(self):
        options = Options()
        options.add_argument('--disable-popup-blocking')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.targetURL)
        print("webdriver start")
    def AD_blocker(self) :
        #js_code = 'document.getElementById("gn_interstitial_close_icon").click()' # サイトによる
        #js_code = code
        
        #ADが出るようなところは更新をしてAD回避
        self.driver.refresh() 
        time.sleep(5)
        Touhoku2 = self.driver.find_element(by.By.LINK_TEXT,self.areaName)
        Touhoku2.click()
    def Start_scrayping(self,startday:str,Endday:str):
        ##とりあえず全部
        Touhoku = self.driver.find_element(by.By.LINK_TEXT,self.areaName)
        
        #######
        Touhoku.click()
        #広告が出るときがある
        ad = '#google_vignette'
        if(ad in self.driver.current_url):
            ##広告が出たら更新
            self.AD_blocker()
        
        
        print("")