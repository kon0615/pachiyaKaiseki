from selenium import webdriver
from selenium.webdriver.remote  import webelement
from selenium.webdriver.common import by    
from selenium.webdriver.chrome.options import Options
#macOSの場合はchromedriver_binaryはコメントアウト
import chromedriver_binary
import time 

class Scrayp:
    targetURL =r"https://ana-slo.com/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/"
    ad = '#google_vignette'
    def __init__(self,Area:str) -> None:
        self.areaName = Area
        self.start_webdriver()
        
    def start_webdriver(self):
        options = Options()
        options.add_argument('--disable-popup-blocking')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.targetURL)
        print("webdriver start")
    def AD_blocker(self,driver:webdriver.Chrome) :
        #js_code = 'document.getElementById("gn_interstitial_close_icon").click()' # サイトによる
        #js_code = code
        
        #ADが出るようなところは更新をしてAD回避

        driver.refresh() 
        
        
        while(driver.current_url ==self.ad):
            self.driver.refresh()
            if driver.current_url !=self.ad:
                return
        
        
    def Start_scrayping(self,startday:str,Endday:str):
        
        #MainMenu = self.driver.find_elements(by.By.CLASS_NAME,'simple_square_btn')
        self.driver.get(self.targetURL + self.areaName)
        #地域の店舗URLを取得
        holeList = self .driver.find_elements(by.By.CLASS_NAME,"table-row")
        for hole in holeList:
            if hole.text =='ホール名\n市区郡':
                continue
            time.sleep(2)
            holeURL=  hole.find_element(by.By.TAG_NAME,"a").get_attribute('href')
            insertQuery = self.GetHoleData(holeURL,hole.text)
            print("")
        #######
        print("driver END")
    
    #ホールデータを取得して文字列に
    def GetHoleData(self,HoleURL:str,HoleName) -> str:
        options = Options()
        options.add_argument('--disable-popup-blocking')
        NewDriver= webdriver.Chrome(options=options)
        NewDriver.get(HoleURL)
        self.AD_blocker(NewDriver)
        print(f'{HoleName} access')
        
        