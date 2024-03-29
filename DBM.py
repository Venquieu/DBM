# @author: Ven
# @data:   2020/10/3
# @brief:  define class JLU_Helper,which is the backbone of DBM

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotVisibleException
import time

class JLU_Helper:
    '''
    class JLU_Helper is the backbone of DBM,which can help guaduate students in JLU fill in&submit the system automatically
    '''
    def __init__(self,user_data,key_words,pause_time = 1):
        self.__login_url = 'https://ehall.jlu.edu.cn'
        self.__request_url = 'https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
        self.__user = user_data
        self.__kw = key_words
        self.__pause_time = pause_time
        self.__language = 'Chinese'
        self.status = True

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('blink-settings=imagesEnabled=false') # Don't load images to ensure a high speed
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) # set to developer mode to avoid recognised

        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser.set_script_timeout(30)
        self.browser.implicitly_wait(32)

    #login to ehall
    def login(self):
        # open login url
        try:
            self.browser.get(self.__login_url)
            time.sleep(self.__pause_time)
        except: #failed to connect to Internet
            print('Error:登录页面连接异常,用户{}登录失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
        
        # check if the web page open normally
        try:
            __ = self.browser.find_element_by_xpath("//title[contains(text(),'统一身份认证')]")
        except : #Not find 
            print('Error:登录页面显示异常,用户{}登录失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
                
        # adaptively waiting, input account
        self.browser.find_element_by_name('username').send_keys(self.__user['account'])
        # adaptively waiting,input password
        self.browser.find_element_by_name('password').send_keys(self.__user['pw'])
        # adaptively waiting, submit to login
        try:
            login_submit = self.browser.find_element_by_name('login_submit')
            login_submit.click()
        except TimeoutException:
            print('Error:登录系统响应超时，用户{}登录失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return

        try:
            __ = self.browser.find_element_by_xpath("//title[contains(text(),'办事大厅')]")
        except : #Not find 
            try:
                self.browser.find_elements_by_xpath("//div[contains(text(),'密码错误')]")
                print('用户{}密码错误,登录失败'.format(self.__user['account']))
            except:
                print('Error:登录系统显示异常,用户{}登录失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
        #otherwise login successful
        if self.status:
            print('用户{}登录成功!'.format(self.__user['account']))
        
    def fill_info(self):
        '''
        Fill in the user information,as the system upgrade,there is no need for this matter any more
        '''
        try:
            _ = self.__user['profession']
        except KeyError:
            print('Error：用户{}打卡失败,请为用户提供完整信息'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
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
        #phone number
        phone = self.browser.find_element_by_id('V1_CTRL67')
        phone.clear()
        time.sleep(self.__pause_time)
        phone.send_keys(self.__user['phone'])
        time.sleep(self.__pause_time)
        #instructor
        ins = self.browser.find_element_by_xpath("//input[contains(@id,'_activeInput')]")
        ins.send_keys(self.__user['instructor'])
        time.sleep(3*self.__pause_time)
        ins.send_keys(Keys.ENTER)
        time.sleep(self.__pause_time)
        #location
        if self.__user['at_school']:
            self.browser.find_element_by_id('V1_CTRL63').click()
            time.sleep(2*self.__pause_time)
            select = Select(self.browser.find_element_by_id('V1_CTRL46'))
            select.select_by_visible_text('在校实习实训实验')
            time.sleep(self.__pause_time)
            #apartment
            select = Select(self.browser.find_element_by_id('V1_CTRL7'))
            select.select_by_visible_text(self.__user['apartment'])
            time.sleep(self.__pause_time)
            #room
            room = self.browser.find_element_by_id('V1_CTRL8')
            room.clear()
            room.send_keys(self.__user['room'])
        else:
            print('Error:暂不支持校外打卡内容填充,请手动完成！用户{}登录失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
        #degree
        if self.__user['degree'] == '硕士':
            self.browser.find_element_by_id('V1_CTRL44').click()
        elif self.__user['degree'] == '博士':
            self.browser.find_element_by_id('V1_CTRL45').click()
        else:
            print('Critical:用户{}学位信息录入错误，打卡失败,请及时修正！'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
        time.sleep(self.__pause_time)
        return True

    def fill_in_morning(self,fill_info = False):
        '''Fill in the 1st login for the day,time is 06:01-12:00'''
        if fill_info:
            is_success = self.fill_info()
            if not is_success:
                return False
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #body temperature
        self.browser.find_element_by_id('V1_CTRL28').click()
        return True
        
    def fill_in_noon(self):
        '''
        This function is eliminated due to the system update.\n
        Original description:
            Fill in the 2nd login for the day,time is 11:01-12:00'''
        self.browser.find_element_by_id('V1_CTRL19').click()
        
    def fill_in_evening(self):
        '''
        This function is eliminated due to the system update.\n
        Original description:
            Fill in the 3rd login for the day,time is 17:01-18:00'''
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        self.browser.find_element_by_id('V1_CTRL23').click()
 
    def fill_in_night(self):
        '''Login in and submit for the day,time is 20:01-24:00'''
        #self.browser.find_element_by_id('V1_CTRL23').click()
        pass

    def auto_fill_in(self, fill_info):
        """
        auto judge time to fill in
        """
        if self.status == False:
            return #login failed and exit fill in process
        try:
            self.browser.get(self.__request_url) #connect to fill_in site
        except:
            print('Error:打卡页面连接异常,用户{}打卡失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return

        try:
            __ = self.browser.find_element_by_xpath("//title[contains(text(),'研究生每日健康')]")
        except TimeoutException:
            print('Error:打卡页面连接超时,用户{}打卡失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
        except NoSuchElementException:
            print('Error:打卡页面显示异常,用户{}打卡失败'.format(self.__user['account']))
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
        if 6<=localtime<12: #morning
            is_success = self.fill_in_morning(fill_info)
            if not is_success:
                self.status = False
                self.browser.quit()
                return
        elif 20<=localtime<24: #night
            self.fill_in_night()
        else: # later for fill in
            print('Error:用户{}打卡迟到了(´༎ຶٹ༎ຶ`)'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
        time.sleep(2*self.__pause_time)

        try:
            submit = self.browser.find_elements_by_xpath("//nobr[text()='提交']")
            submit[-1].click()
        except:
            print('打卡页面加载超时，用户{}打卡失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return

        time.sleep(2*self.__pause_time)

        try: #ensure all info is filled
            __ = self.browser.find_element_by_xpath("//span[contains(text(),'{}')]".format(kw[1])) #'If you have anything to comment,please click'
        except: #abnormal
            try:
                _ = self.browser.find_element_by_xpath("//div[contains(text(),'{}')]".format(kw[0]))
                print('Warning:信息不完整，正在补充...')
                self.browser.find_element_by_xpath("//button[contains(text(),'{}')]".format(kw[2])).click() #'Ok'
                self.fill_info()
                #refill the degree,when a user submit with phone in the morning while use DBM in the rest time
                time.sleep(self.__pause_time)
            except:
                print('Warning:提交显示异常，刷新页面...')
                self.browser.refresh()
                time.sleep(self.__pause_time)
            
            try:
                submit = self.browser.find_elements_by_xpath("//nobr[text()='提交']")
                for submit_button in submit:
                    try:
                        submit_button.click()
                        break
                    except ElementNotVisibleException:
                        continue
            except:
                print('Error:提交显示异常,用户{}打卡失败'.format(self.__user['account']))
                self.status = False
                self.browser.quit()
                return

        try: #still have problem
            __ = self.browser.find_element_by_xpath("//span[contains(text(),'{}')]".format(kw[1])) #'If you have anything to comment,please click'
        except: #abnormal
            print('Error:提交时加载超时,用户{}打卡失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return
        self.browser.find_element_by_xpath("//button[contains(text(),'{}')]".format(kw[3])).click() #Ok
        time.sleep(self.__pause_time)

        try:
            __ = self.browser.find_element_by_xpath("//div[contains(text(),'{}')]".format(kw[4]))#'Done successfully!'
            time.sleep(3*self.__pause_time)
        except: #Submission fail
            print('Error:提交确认时加载超时,用户{}打卡失败'.format(self.__user['account']))
            self.status = False
            self.browser.quit()
            return

        if self.status:
            print('用户{}办理成功！'.format(self.__user['account']))
        try:
            confirm = self.browser.find_element_by_xpath("//button[contains(text(),'{}')]".format(kw[5])) #Ok
            confirm.click()
        except:
            print('Warning:确认超时')
        time.sleep(4*self.__pause_time)
        self.browser.quit() #quit the browser
