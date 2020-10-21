# @author: Ven
# @data:   2020/10/3
# @brief:  define class JLU_Helper,which is the backbone of DBM

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class JLU_Helper:
    '''
    class JLU_Helper is the backbone of DBM,which can help guaduate students in JLU fill in&submit the system automatically
    '''
    def __init__(self,user_data,key_words,pause_time = 1):
        self.__login_url = 'https://ehall.jlu.edu.cn/sso/login'
        self.__request_url = 'https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
        self.__user = user_data
        self.__kw = key_words
        self.__pause_time = pause_time
        self.__language = 'Chinese'
        self.status = True
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # Don't load images to ensure a high speed
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # set to developer mode to avoid recognised

        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)
        self.__wait = WebDriverWait(self.browser, 30) #time out :30s

    #login to ehall
    def login(self):
        # open login url
        try:
            self.browser.get(self.__login_url)
            time.sleep(self.__pause_time)
        except: #failed to connect to Internet
            print('--------------------------------')
            print('网络连接失败！用户{}未能登录'.format(self.__user['account']))
            print('--------------------------------')
            self.status = False
            return
        
        # check if the web page open normally
        for i in range(11):
            if self.browser.find_elements_by_name('username') == []:
                print('--------------------------------')
                print('网页显示异常！第{}次重连中...'.format(i))
                print('--------------------------------')
                self.browser.refresh()
                if (i+1)%4 == 0:
                    self.browser.get(self.__login_url)
            else:
                break
            if i == 10:
                print('--------------------------------')
                print('网页重连失败！用户{}未能登录'.format(self.__user['account']))
                print('--------------------------------')
                self.status = False
                self.browser.quit()
                return
        # adaptively waiting, input account
        self.browser.find_element_by_name('username').send_keys(self.__user['account'])
        # adaptively waiting,input password
        self.browser.find_element_by_name('password').send_keys(self.__user['pw'])
        # adaptively waiting, submit to login
        self.browser.find_element_by_name('login_submit').click()
        try:
            __ = self.browser.find_element_by_xpath("//h3[contains(text(),{})]".format(self.__kw[self.__language][0]))
        except : #Not find 
            print('--------------------------')
            print('用户{}登录失败！请重试'.format(self.__user['account']))
            print('--------------------------')
            self.status = False
            self.browser.quit()
        #otherwise login successful
        if self.status:
            print('用户{}登录成功!'.format(self.__user['account']))
        

    def fill_in_morning(self):
        '''Fill in the 1st login for the day,time is 07:01-08:00'''
        pf = self.browser.find_element_by_id('V1_CTRL40')
        pf.clear()
        time.sleep(self.__pause_time)
        pf.send_keys(self.__user['profession'])
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
            elements = self.browser.find_elements_by_xpath("//input[contains(@id,'_activeInput')]")
            assert len(elements) == 3,"Didn't find enough selection"
            kw = ['province','city','area']
            for i in range(len(elements)):
                element = elements[i]
                element.send_keys(self.__user[kw[i]])
                time.sleep(self.__pause_time)
                element.send_keys(Keys.ENTER)
                time.sleep(self.__pause_time)

            #address
            pf = self.browser.find_element_by_id('V1_CTRL39')
            pf.clear()
            pf.send_keys(self.__user['address'])
            time.sleep(self.__pause_time)
        else:
            #room
            pf = self.browser.find_element_by_id('V1_CTRL8')
            pf.clear()
            pf.send_keys(self.__user['room'])
            time.sleep(self.__pause_time)
        #degree
        if self.__user['degree'] == '硕士':
            self.browser.find_element_by_id('V1_CTRL44').click()
        elif self.__user['degree'] == '博士':
            self.browser.find_element_by_id('V1_CTRL45').click()
        else:
            print('--------------------------')
            print('用户{}学位错误，打卡失败'.format(self.__user['account']))
            print('--------------------------')
            self.status = False
            self.browser.quit()
            return
        time.sleep(self.__pause_time)
        #body temperature
        self.browser.find_element_by_id('V1_CTRL28').click()
        

    def fill_in_noon(self):
        '''Fill in the 2nd login for the day,time is 11:01-12:00'''
        self.browser.find_element_by_id('V1_CTRL19').click()
        

    def fill_in_evening(self):
        '''Fill in the 3rd login for the day,time is 17:01-18:00'''
        self.browser.find_element_by_id('V1_CTRL23').click()
 

    def fill_in_night(self):
        '''Fill in the 4th login for the day,time is 21:01-22:00'''
        self.browser.find_element_by_id('V1_CTRL23').click()
        

    def auto_fill_in(self):
        """
        auto judge time to fill in
        """
        if self.status == False:
            return #login failed and exit fill in process
        try:
            __ = self.browser.get(self.__request_url) #connect to fill_in site
        except:
            print('--------------------------')
            print('网络连接已断开！用户{}打卡失败'.format(self.__user['account']))
            print('--------------------------')
            self.status = False
            self.browser.quit()
            return
        try:
            __ = self.browser.find_element_by_xpath("//b[contains(text(),'您')]")
        except:
            self.__language = 'English' #Set language
        time.sleep(self.__pause_time)
        kw = self.__kw[self.__language]
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
            print('---------------------------------')
            print('啊偶！用户{}打卡迟到了(´༎ຶٹ༎ຶ`)'.format(self.__user['account']))
            print('---------------------------------')
            self.status = False
            self.browser.quit()
            return
        time.sleep(self.__pause_time)
        self.browser.find_element_by_class_name('command_button_content').click()
        time.sleep(2*self.__pause_time)
        try: #ensure all info is filled
            __ = self.browser.find_element_by_xpath("//span[contains(text(),'{}')]".format(kw[1])) #'If you have anything to comment,please click'
        except: #normal
            print('信息不完整，正在补充...')
            self.browser.find_element_by_xpath("//button[contains(text(),'{}')]".format(kw[2])).click() #'Ok'
            self.fill_in_morning()
            #refill the degree,when a user submit with phone in the morning while use DBM in the rest time
            time.sleep(self.__pause_time)
            self.browser.find_element_by_class_name('command_button_content').click()
            time.sleep(self.__pause_time)

        self.browser.find_element_by_xpath("//button[contains(text(),'{}')]".format(kw[3])).click() #Ok
        time.sleep(self.__pause_time)

        try:
            __ = self.browser.find_element_by_xpath("//div[contains(text(),'{}')]".format(kw[4]))#'Done successfully!'
            time.sleep(self.__pause_time)
        except:
            print('--------------------------')
            print('用户{}因不明原因办理失败！'.format(self.__user['account']))
            print('--------------------------')
            self.status = False
            return
        if self.status:
            print('用户{}办理成功！'.format(self.__user['account']))
        try:
            self.browser.find_element_by_xpath("//button[contains(text(),'{}')]".format(kw[5])).click() #Ok
        except:
            print('Warning:确认异常!')
            return
        time.sleep(4*self.__pause_time)
        self.browser.quit() #quit the browser
