from math import e
from operator import index, indexOf
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
import gc
class Scrayp:
    targetURL =r"https://ana-slo.com/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/"
    ad = '#google_vignette'
    todayDatetime =  datetime.datetime.today() 
    extantionPath =r"C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\gighmmpiobklfepjocnamgkkbiglidom\\5.21.0_0.crx"
    profilePath =r'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
    userName = 'ユーザー1'
    def __init__(self,Area:str) -> None:
        self.areaName = Area
        self.date =f'{self.todayDatetime.year}/{self.todayDatetime.month}/{self.todayDatetime.day}' 
        self.start_webdriver()
        
    def start_webdriver(self):
        options = Options()
        
        #options.add_argument(f"--profile-directory={self.userName}")
        options.add_extension(self.extantionPath)
       # options.add_argument(r"--user-data-dir=./profile")       
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--enable-sync-extensions')
        #options.add_argument('--headless')
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
        
        #
        skipHoleName = ''
        #
        flag = True
        for hole in holeList:
            if skipHoleName  not  in hole.text and flag == False:
                continue
            flag = True
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
        options.add_extension(self.extantionPath)
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
                
                
                insert.InsertToDB( innerQuery)
            except  Exception as e :
                print('[error]' +cell.text )
                print(e)
                continue
        #リソース開放
        NewDriver.quit()
        insert.close()
        gc.collect()
    def GetDaiData(self,URL:str,day:str,TenpoName:str) -> str:
        retStr =''
        tenpo = TenpoName[0:indexOf(TenpoName,'\n')]
        chiiki =self.areaName + TenpoName.replace(tenpo,'').replace('\n','')
        options = Options()
        #options.add_argument(fr"--user-data-dir={self.profilePath}")
        #options.add_argument(f"--profile-directory={self.userName}")
        options.add_extension(self.extantionPath)
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
        DaiCols =  daiDriver.find_elements(By.XPATH,'//*[@id="all_data_table"]/thead/tr/th')
        #InART = self.isART(DaiCols)

        queryHeader = f'Insert into アナスロ元データ([年月日],[店舗名] ,[地域名],[機種名]{self.AddqueryHeader(DaiCols)},[データ作成年月日]) VALUES'
        
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
            datastr='('
            index = -1
            datastr += f"'{day}','{tenpo}','{chiiki}','{Title}'"
            for Data in DataCell:
                index += 1
                datastr += f",'{DataCell[index].get_attribute('textContent').replace(',','')}'"
            
            retStr += datastr +f",'{self.date}'"
            retStr += ')'
        daiDriver.quit()
        gc.collect()
        return queryHeader + retStr
    def AddqueryHeader(self,cols:list[webelement.WebElement])->str:
        
        retstr =''
        for Name in cols:
            if Name.accessible_name !='機種名':
                retstr += f',[{Name.accessible_name }]'
        return retstr
    def reflashError(self,driver:webdriver.Chrome):
        timeOut = 0
        while(driver.title =='データベースエラー'):
            if timeOut == 1:
                return
            driver.refresh()
            timeOut +=1
    
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
    def close(self):
        self.conn.close()
    def InsertToDB(self,query:str):
        cursor = self.conn.cursor()
        
        
        cursor.execute(query)
        
        
        
        self.conn.commit()
        cursor.close()
        
        print('[insert] sucsessful')
