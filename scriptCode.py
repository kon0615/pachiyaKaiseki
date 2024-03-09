from selenium import webdriver
from selenium.webdriver.remote  import webelement
from selenium.webdriver.common import by    
from selenium.webdriver.chrome.options import Options
#macOSの場合はchromedriver_binaryはコメントアウト
#import chromedriver_binary
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
    def AD_blocker(self) :
        #js_code = 'document.getElementById("gn_interstitial_close_icon").click()' # サイトによる
        #js_code = code
        
        #ADが出るようなところは更新をしてAD回避

        self.driver.refresh() 
        
        Touhoku2 = self.driver.find_elements(by.By.CLASS_NAME,'simple_square_btn')
        
        while(self.driver.current_url ==self.ad):
            self.driver.refresh()
            self.SearchForAreaButton(Touhoku2)
        
        
    def Start_scrayping(self,startday:str,Endday:str):
        ##とりあえず全部
        MainMenu = self.driver.find_elements(by.By.CLASS_NAME,'simple_square_btn')
        self.driver.get(self.targetURL + self.areaName)
        #地域の店舗URLを取得
        
        #######
        time.sleep(5)

        #広告が出るときがある
        

    def SearchForAreaButton(self,listBt:list[webelement.WebElement]):
        #メインメニューから指定エリアのボタンを探してクリック
        for item in  listBt:
            if item.text == self.areaName:
                print('catch')
                
                item.click()
                return
        
        