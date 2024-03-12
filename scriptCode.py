from math import e
from operator import indexOf
from os import replace
from socket import timeout
import time

from selenium import webdriver
from selenium.webdriver.remote  import webelement
from selenium.webdriver.common.by import By    
from selenium.webdriver.chrome.options import Options
#macOSの場合はchromedriver_binaryはコメントアウト
#import chromedriver_binary
from time import sleep
from datetime import datetime as dt
import datetime

class Scrayp:
    targetURL =r"https://ana-slo.com/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/"
    ad = '#google_vignette'
    todayDatetime =  datetime.datetime.today() 

    profilePath =r'C:\\Users\\server\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
    userName = 'ユーザー1'
    def __init__(self,Area:str) -> None:
        self.areaName = Area
        self.date =f'{self.todayDatetime.year}/{self.todayDatetime.month}/{self.todayDatetime.day}' 
        self.start_webdriver()
        
    def start_webdriver(self):
        options = Options()
        
        #options.add_argument(f"--profile-directory={self.userName}")
        options.add_extension(r"C:\\Users\\server\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\cfhdojbkjhnklbpkdaibdccddilifddb\\3.25_0.crx")
       # options.add_argument(r"--user-data-dir=./profile")       
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--enable-sync-extensions')
       # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

        self.driver.get(self.targetURL)
        self.driver.refresh()
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
        self.startDay = startday
        self.ENDday = Endday
        
        #MainMenu = self.driver.find_elements(by.By.CLASS_NAME,'simple_square_btn')
        self.driver.get(self.targetURL + self.areaName)
        
        self.reflashError(self.driver)
        holeList = self .driver.find_elements(By.CLASS_NAME,"table-row")
            
       
        #地域の店舗URLを取得
        
        #insert = DB()
        for hole in holeList:
            
            if hole.text =='ホール名\n市区郡':#カラムも拾っちゃうから除外
                continue
            
            #ホールのURL
            holeURL=  hole.find_element(By.TAG_NAME,"a").get_attribute('href')
            self.SETHoleData(holeURL,hole.text)
           
           
            print("")
        
        #######
        
        print("driver END")
    
    #ホールデータを取得して文字列に
    def SETHoleData(self,HoleURL:str,HoleName:str) :
        options = Options()
        #options.add_argument(fr"--user-data-dir={self.profilePath}")
        #options.add_argument(f"--profile-directory={self.userName}")
        options.add_extension(r"C:\\Users\\server\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\cfhdojbkjhnklbpkdaibdccddilifddb\\3.25_0.crx")
        #options.add_argument('--headless')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--enable-sync-extensions')
        NewDriver= webdriver.Chrome(options=options)
        NewDriver.get(HoleURL)
       
        Hole = HoleName.replace("\n",'/地域名:')
        self.reflashError(NewDriver)
        self.AD_blocker(NewDriver)
        print(f'{Hole} access')
        
        dataCells = NewDriver.find_elements(By.CLASS_NAME,'table-data-cell')

       
        
        queryHeader = 'Insert into アナスロ元データ([年月日],[店舗名] ,[地域名],[機種名],[台番号],[G数],[差枚],[BB],[RB],[合成確率],[BB確率],[RB確率],[データ作成年月日],[ART],[ART確率]) VALUES'
        innerQuery =''
        #日ごとにループ
        insert = DB()
        for cell in dataCells:
            innerQuery =''
            try:
                if cell.text =="–"  or '/' not in cell.text or '%' in cell.text:
                    continue
            except:
                print('Holedata error')
                NewDriver.close()
                #つながるまで繰り返す
                self.SETHoleData(HoleURL,HoleName)
                return
            
            dayTxt = cell.text #日付
            #指定した日付だけ対応
            daytxt2 = dayTxt[0:10] #曜日排除
            
            if not(dt.strptime(daytxt2,'%Y/%m/%d') >= dt.strptime(self.startDay,'%Y/%m/%d')    and dt.strptime(daytxt2,'%Y/%m/%d')  <= dt.strptime(self.ENDday,'%Y/%m/%d')) :
                continue
            print(dayTxt)
            try:
                DaiDataURL = cell.find_element(By.TAG_NAME,'a').get_attribute('href')
            except:
                continue
            
            #クエリ作成　
            
            try:
                innerQuery += self.GetDaiData(DaiDataURL,daytxt2,HoleName)
                insert.InsertToDB(queryHeader + innerQuery)
            except  Exception as e :
                print('[error]' +cell.text )
                print(e)
                continue
        #リソース開放
        NewDriver.quit()
        
    def GetDaiData(self,URL:str,day:str,TenpoName:str) -> str:
        retStr =''
        tenpo = TenpoName[0:indexOf(TenpoName,'\n')]
        chiiki =self.areaName + TenpoName.replace(tenpo,'').replace('\n','')
        options = Options()
        #options.add_argument(fr"--user-data-dir={self.profilePath}")
        #options.add_argument(f"--profile-directory={self.userName}")
        options.add_extension(r"C:\\Users\\server\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\cfhdojbkjhnklbpkdaibdccddilifddb\\3.25_0.crx")
        #options.add_argument('--headless')
        options.add_argument('--enable-popup-blocking')
        options.add_argument('--enable-sync-extensions')
        daiDriver  = webdriver.Chrome(options=options)
        daiDriver.get(URL)
        
        ##self.AD_blocker(daiDriver)
        ##daiDriver.get(daiDriver.current_url.replace(self.ad,''))
        self.reflashError(daiDriver)
        #グラフ表示ボタンクリック
        daiDriver.find_element(By.XPATH,'//*[@id="all_data_btn"]').click()

        #カラムにARTを含むか調べる
        DaiCols =  daiDriver.find_element(By.XPATH,'//*[@id="all_data_table"]/thead/tr/th[1]')
        InART = self.isART(DaiCols)

        daiTBL =daiDriver.find_element(By.XPATH,'//*[@id="all_data_table"]/tbody')
        DaiRow = daiTBL.find_elements(By.TAG_NAME,'tr')
        print('catch')
        for row in DaiRow:

            Title = row.find_element(By.CLASS_NAME,'fixed01').get_attribute("textContent").replace(' ','')
            if Title == '':
                return
            if len(retStr) > 0:
                retStr += ','
            
            #行データを取得して配列を作る
            DataCell = row.find_elements(By.CLASS_NAME,'table_cells')
            #ART項目があるかどうかで変化
            if InART ==False:
                cell0 = DataCell[0].get_attribute("textContent")
                cell1 = DataCell[1].get_attribute("textContent").replace(',','')
                cell2 = DataCell[2].get_attribute("textContent").replace(',','')
                cell3 = DataCell[3].get_attribute("textContent")
                cell4 = DataCell[4].get_attribute("textContent")
                cell5 = DataCell[5].get_attribute("textContent")
                cell6 = DataCell[6].get_attribute("textContent")
                cell7 = DataCell[7].get_attribute("textContent")
                retStr += f"('{day}','{tenpo}','{chiiki}','{Title}','{cell0}','{cell1}','{cell2}','{cell3}','{cell4}','{cell5}','{cell6}','{cell7}','{self.date}','0','1/0.0')"
            else:
                cell0 = DataCell[0].get_attribute("textContent")
                cell1 = DataCell[1].get_attribute("textContent").replace(',','')
                cell2 = DataCell[2].get_attribute("textContent").replace(',','')
                cell3 = DataCell[3].get_attribute("textContent")
                cell4 = DataCell[4].get_attribute("textContent")
                cell5 = DataCell[6].get_attribute("textContent")
                cell6 = DataCell[7].get_attribute("textContent")
                cell7 = DataCell[8].get_attribute("textContent")
                ARTCoData =  DataCell[5].get_attribute("textContent")
                ARTPrData = DataCell[9].get_attribute("textContent")
                retStr += f"('{day}','{tenpo}','{chiiki}','{Title}','{cell0}','{cell1}','{cell2}','{cell3}','{cell4}','{cell5}','{cell6}','{cell7}','{self.date}','{ARTCoData}','{ARTPrData}')"
        daiDriver.quit()
        return retStr
    def reflashError(self,driver:webdriver.Chrome):
        timeOut = 0
        while(driver.title =='データベースエラー'):
            if timeOut == 1:
                return
            driver.refresh()
            timeOut +=1
    def  isART(self,target:webelement.WebElement)-> bool:
        Names = target.find_elements(By.TAG_NAME,'th')
        for Name in Names:
            if Name.text == 'ART' or Name.text == 'ART確率':
                return True 
        return False
import pyodbc
class DB:
    driver = "{SQL Server}"
    SERVER = '192.168.11.20\SQLEXPRESS'
    DATABASE = r'パチ屋DB'
    USERNAME = 'sa'
    PASSWORD = '0721'
    def __init__(self) -> None:
        connectionString = f'DRIVER={self.driver};SERVER={self.SERVER};DATABASE={self.DATABASE};UID={self.USERNAME};PWD={self.PASSWORD}'
        try:
            self.conn = pyodbc.connect(connectionString)
        except:
            print("DB connection error")
            return
    
    def InsertToDB(self,query:str):
        cursor = self.conn.cursor()
        
        
        cursor.execute(query)
        
        
        #resultID = cursor.fetchval()
        #print(f"inserted :{resultID}")
        self.conn.commit()
        print('[insert] sucsessful')
