from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import threading
from tkinter import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import logging


# 오늘날짜
now = datetime.datetime.now()
now_date = now.strftime('%Y/%m/%d')

class HrMacro(threading.Thread):
    
    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(u'%(asctime)s [%(filename)s:%(lineno)d] %(message)s')

        self.streamingHandler = logging.StreamHandler()
        self.streamingHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamingHandler)
        
        self.driver = webdriver.Chrome(executable_path='chromedriver')
        
        # HR 화면 열기
        URL = "https://ehr.ldcc.co.kr/"
        self.driver.get(url=URL)

        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("근태 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()
        
        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, width=40)
        self.id_entry.grid(row=1, column=1)
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, show="*", width=40)
        self.pw_entry.grid(row=2, column=1)
        self.login_button = Button(self.object_frame, text="Login", width=3, height=2, command=self.login_go)
        self.login_button.grid(row=3, column=1)
        self.dp.mainloop()
    
    # 오늘이 몇주차 인지 계산
    def MonthWeek(self):
        
        # 해당 달의 몇주차 계산
        date = datetime.datetime(now.year, now.month, now.day)

        iso_calendar = date.isocalendar()

        # Currentyear = iso_calendar[0]
        Currentweek = iso_calendar[1]
        # Currentday = iso_calendar[2]

        first_day = date.replace(day=1)

        iso_calendar = first_day.isocalendar()

        Fistweek = iso_calendar[1]

        MonthWeek = Currentweek - Fistweek + 1

        return MonthWeek
    
    # 로그인 버튼 클릭
    def login_go(self):
        def task():
            
            # 아이디/passwd 입력
            self.driver.find_element(By.ID, "S_USER_ID").send_keys(self.id_entry.get())
            self.driver.find_element(By.ID, "S_PWD").send_keys(self.pw_entry.get())
            
            # 로그인버튼 클릭
            self.driver.find_element(By.XPATH, '//*[@id="divLoginBox"]/div/section/div[2]/button').click()
            time.sleep(3)
            self.select_Work()
            self.Save()
                
        newthread = threading.Thread(target=task)
        newthread.start()
        
    def select_Work(self):
        
        # 근태관리/근무내역 클릭
        self.driver.find_element(By.XPATH, '//*[@id="ulModuleList"]/li[2]/div/div').click()
        self.driver.find_element(By.XPATH, '//*[@id="ulSubMenu"]/li[2]/ul/li[2]/a').click()

        # 근무내역 
        iframe = self.driver.find_element(By.TAG_NAME,'iframe')
        self.driver.switch_to.frame(iframe)

        try:
            # 1주차부터 6주차까지 확인
            for i in range(1, 6):
                # 1주차 확인
                if self.MonthWeek() == i:
                    self.driver.find_element(By.XPATH, '//*[@id="vmCalendar"]/tbody/tr[' + str(i) + ']').click()
                    break
            
        except NoSuchElementException:
            pass 
        
        time.sleep(1)

        # ifrime에서 원래 frame으로 돌아옵니다. <-- 이 초기화를 쓰지 않아 엄청 해매임.
        self.driver.switch_to.default_content()

        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        # print('현재 페이지에 iframe은 %d개가 있습니다.' % len(iframes))

        self.driver.switch_to.frame(iframes[1])

        # 오늘 날짜 클릭
        try:
            for i in range(2, 6):
                
                if self.driver.find_element(By.XPATH, '//*[@id="sheet1-table"]/tbody/tr[2]/td/div/div[1]/table/tbody/tr[' + str(i) + ']/td[3]').text == str(now_date):
                    
                    # 근무유형 세팅
                    self.driver.find_element(By.XPATH, '//*[@id="sheet1-table"]/tbody/tr[2]/td/div/div[1]/table/tbody/tr[' + str(i) + ']/td[5]').click()
                    option = self.driver.find_element(By.XPATH, "//*[text()='일반근무']")
                    self.driver.execute_script("arguments[0].scrollIntoView();", option)
                    option.click()
                    time.sleep(1)
                    
                    # 출근시간 세팅
                    self.driver.find_element(By.XPATH, '//*[@id="sheet1-table"]/tbody/tr[2]/td/div/div[1]/table/tbody/tr[' + str(i) + ']/td[8]').click()
                    option = self.driver.find_element(By.XPATH, "//*[text()='09:00']")
                    self.driver.execute_script("arguments[0].scrollIntoView();", option)
                    option.click()
                    time.sleep(1)
                    
                    # 퇴근시간 세팅
                    self.driver.find_element(By.XPATH, '//*[@id="sheet1-table"]/tbody/tr[2]/td/div/div[1]/table/tbody/tr[' + str(i) + ']/td[10]').click()
                    option = self.driver.find_element(By.XPATH, "//*[text()='18:00']")
                    self.driver.execute_script("arguments[0].scrollIntoView();", option)
                    option.click()
                    time.sleep(1)
                    
                    break
                
        except NoSuchElementException:
                self.logger.debug("근태시간 세팅에서 NoSuchElementException 에러발생")
                pass
    
    def Save(self):
        
        try:
            # 승인버튼
            self.driver.find_element(By.XPATH, '//*[@id="appr01"]').click()
            time.sleep(1)
        except:
            pass

        try:
            # alert 확인
            if EC.alert_is_present():
                self.driver.switch_to.alert.accept()
        except:
            "팝업창 에러"
            
        time.sleep(1)

        try:
            # alert 확인
            if EC.alert_is_present():
                self.driver.switch_to.alert.accept()
        except:
            "확인창 에러"
            
        time.sleep(1)
        
HR_macro = HrMacro()
HR_macro.start()