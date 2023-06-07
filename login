import threading
from tkinter import *
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
import time

class App(threading.Thread):
    
    
    def __init__(self):
        super().__init__()
        self.opt = Options()
        self.opt.add_argument('window-size=800,600')
        # self.driver = webdriver.Chrome(executable_path="./chromedriver", options=self.opt)
        # self.driver = webdriver.Chrome(executable_path='D:/PythonDoc/chromedriver.exe')
        # selenium 4.대 버전
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.opt)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://ticket.interpark.com/Gate/TPLogOut.asp"
        self.driver.get(self.url)
        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("인터파크 티케팅 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()
        
        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, width=40)
        self.id_entry.grid(row=1, column=1)
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, width=40)
        self.pw_entry.grid(row=2, column=1)
        self.login_button = Button(self.object_frame, text="Login", width=4, height=2)
        self.login_button.grid(row=3, column=1)
        self.dp.mainloop()
        
        
    def login_go(self):
        def task():
            print("버튼이 클릭되었습니다.")
            # self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
            # self.driver.find_element_by_name('userId').send_keys(self.id_entry.get())
            # self.driver.find_element_by_id('userPwd').send_keys(self.pw_entry.get())
            # self.driver.find_element_by_id('btn_login').click()
            
            # self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME('iframe')))
            # self.driver.find_element(By.NAME, "userId").send_keys(self.id_entry.get())
            # self.driver.find_element(By.ID, "userPwd").send_keys(self.pw_entry.get())
            # self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME, "iframe")[0])
            # 인덱스를 사용하여 전환
            iframe = self.driver.find_elements(By.TAG_NAME,'iframe')[0]
            self.driver.switch_to.frame(iframe)
            
            self.driver.find_element(By.ID, "userId").send_keys("TEST")
            self.driver.find_element(By.ID, 'btn_login').click()
            
            
            # self.driver.find_element(By.NAME, "userId").send_keys(self.id_entry.get())
            # self.driver.find_element(By.ID, "userPwd").send_keys(self.pw_entry.get() + KeysView.ENTER)
            # self.driver.find_element(By.ID, "btn_login").click()
            print("버튼이 클릭되었습니다.")
            newthread = threading.Thread(target=task)
            newthread.start()
        task()
        
        
app = App()
app.start()

