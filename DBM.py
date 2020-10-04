# @author: Ven
# @data:   2020/10/3
# @brief:  define class JLU_Helper,which is the backbone of DBM

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver import ActionChains
import time

class JLU_Helper:
    '''
    class JLU_Helper is the backbone of DBM,which can help guaduate students in JLU fill in&submit the system automatically
    '''
    def __init__(self,user_data,pause_time = 1):
        self.__login_url = 'https://ehall.jlu.edu.cn/sso/login'
        self.__request_url = 'https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
        self.__user = user_data
        self.__pause_time = pause_time
        self.status = True
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # Don't load images to ensure a high speed
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # set to developer mode to avoid recognised

        self.browser = webdriver.Chrome(options=options)
        self.__wait = WebDriverWait(self.browser, 20) #time out :20s



    #login to ehall
    def login(self):
        # open login url
        try:
            self.browser.get(self.__login_url)
        except: #failed to connect to Internet
            print('-------------')
            print('网络连接失败！')
            print('-------------')
            self.status = False
            return
        # adaptively waiting, input account
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('username').send_keys(self.__user['account'])
        # adaptively waiting,input password
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('password').send_keys(self.__user['pw'])
        # adaptively waiting, submit to login
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('login_submit').click()
        try:
            self.browser.find_element_by_xpath("//h3[contains(text(),'登录成功')]")
        except : #Not find 
            print('==========================')
            print('||用户{}登录失败！请重试||'.format(self.__user['account']))
            print('==========================')
            self.status = False
        #otherwise login successful
        if self.status:
            print('用户{}登录成功'.format(self.__user['account']))
        

    def fill_in_morning(self):
        '''Fill in the 1st login for the day,time is 07:01-08:00'''
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_id('V1_CTRL40').send_keys(self.__user['profession'])
        time.sleep(self.__pause_time)
        #grade
        select = Select(self.browser.find_element_by_id('V1_CTRL41'))
        select.select_by_visible_text(self.__user['grade'])
        time.sleep(self.__pause_time)
        #campus
        select = Select(self.browser.find_element_by_id('V1_CTRL42'))
        select.select_by_visible_text(self.__user['campus'])
        time.sleep(self.__pause_time)
        #apartment
        select = Select(self.browser.find_element_by_id('V1_CTRL7'))
        select.select_by_visible_text(self.__user['apartment'])
        time.sleep(self.__pause_time)

        if self.__user['apartment'] == '校外居住':
            #province
            select = Select(self.browser.find_element_by_id('V1_CTRL35'))
            select.select_by_visible_text(self.__user['province'])
            time.sleep(self.__pause_time)
            #city
            select = Select(self.browser.find_element_by_id('V1_CTRL37'))
            select.select_by_visible_text(self.__user['city'])
            time.sleep(self.__pause_time)
            #area
            select = Select(self.browser.find_element_by_id('V1_CTRL38'))
            select.select_by_visible_text(self.__user['area'])
            time.sleep(self.__pause_time)
            #address
            self.browser.find_element_by_id('V1_CTRL39').send_keys(self.__user['address'])
            time.sleep(self.__pause_time)
        else:
            #room
            self.browser.find_element_by_id('V1_CTRL8').send_keys(self.__user['room'])
            time.sleep(self.__pause_time)
        #degree
        if self.__user['degree'] == '硕士':
            self.browser.find_element_by_id('V1_CTRL44').click()
        elif self.__user['degree'] == '博士':
            self.browser.find_element_by_id('V1_CTRL45').click()
        else:
            print('用户{}学位错误，打卡失败，怕不是个本科生噢'.format(self.__user['account']))
            self.status = False
            return
        time.sleep(self.__pause_time)
        #body temperature
        self.browser.find_element_by_id('V1_CTRL28').click()
        

    def fill_in_noon(self):
        '''Fill in the 2nd login for the day,time is 11:01-12:00'''
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_id('V1_CTRL19').click()
        

    def fill_in_evening(self):
        '''Fill in the 3rd login for the day,time is 17:01-18:00'''
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_id('V1_CTRL23').click()
 

    def fill_in_night(self):
        '''Fill in the 4th login for the day,time is 21:01-22:00'''
        pass
        

    def auto_fill_in(self):
        """
        auto judge time to fill in
        """
        if self.status == False:
            return #login failed and exit fill in process
        try:
            self.browser.get(self.__request_url) #connect to fill_in site
        except:
            print('---------------')
            print('网络连接已断开！')
            print('---------------')
            self.status = False
            return
        localtime = time.asctime(time.localtime(time.time()))
        localtime = localtime.split(' ')[-2]
        localtime = int(localtime.split(':')[0])
        if 7<=localtime<8: #morning
            self.fill_in_morning()
        elif 11<=localtime<12: #noon
            self.fill_in_noon()
        elif 17<=localtime<18: #evening
            self.fill_in_evening()
        elif 21<=localtime<22: #night
            self.fill_in_night()
        else: # later for fill in 
            print('-------------------------')
            print('||啊偶！打卡迟到了(´༎ຶٹ༎ຶ`)||')
            print('-------------------------')
        self.browser.implicitly_wait(30)
        time.sleep(self.__pause_time)
        self.browser.find_element_by_class_name('command_button_content').click()
        self.browser.implicitly_wait(30)
        time.sleep(self.__pause_time)
        try: #ensure all info is filled
            self.browser.find_element_by_xpath("//span[contains(text(),'如有其它相关说明，请点击')]")
        except: #normal
            print('信息不完整，正在补充...')
            self.browser.find_element_by_xpath("//button[contains(text(),'确定')]").click()
            self.fill_in_morning()
            self.browser.implicitly_wait(30)
            time.sleep(self.__pause_time)
            self.browser.find_element_by_class_name('command_button_content').click()

        self.browser.find_element_by_xpath("//button[contains(text(),'好')]").click()
        self.browser.implicitly_wait(30)
        time.sleep(self.__pause_time)

        try:
            self.browser.find_element_by_xpath("//div[contains(text(),'办理成功')]")
        except:
            print('==================')
            print('用户{}打卡失败！'.format(self.__user['account']))
            print('==================')
            self.status = False
        if self.status:
            print('用户{}办理成功！'.format(self.__user['account']))
        self.browser.find_element_by_xpath("//button[contains(text(),'确定')]").click()
        time.sleep(4*self.__pause_time)
        self.browser.quit() #quit the browser
