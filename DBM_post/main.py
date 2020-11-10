# @author: Ven
# @data:   2020/10/3
# @brief:  main program of DBM,run this script to keep away from BOTHER

from UserSetting import *
from DBM import JLU_Helper
import time
import random

is_finished = False #not login yet
last_hour = -1
key_words = {
    'Chinese':['登录成功','如有其它相关说明，请点击','确定','好','办理成功','确定'],
    'English':['登录成功','If you have anything to comment,please click','Ok','Ok','Done successfully!','Ok']
}
redo = [re_login,re_connect,re_submit]

while True:
    localtime = time.asctime(time.localtime(time.time()))
    localtime_hour = localtime.split(' ')[-2]
    localtime_hour = int(localtime_hour.split(':')[0])
    if localtime_hour != last_hour:
        is_finished = False  #wait for next time
    if (not is_finished) and (7<=localtime_hour<8 or 11<=localtime_hour<12 or \
        17<=localtime_hour<18 or 21<=localtime_hour<22):
        t = random.randint(1,5)#wait for 1-5min
        print('当前时间是{}，{}min后将进行填报，请稍侯...'.format(localtime,t))
        time.sleep(60*t)
        count = 0
        failed_list = []
        for  user in users:
            print('**************************************************')
            lt = time.asctime(time.localtime(time.time()))
            print('于{}开始为用户{}填报...'.format(lt,user['account']))
            helper = JLU_Helper(user,key_words,pause_time=pause_time,retry = redo)
            helper.login()
            time.sleep(2*pause_time)
            helper.auto_fill_in()
            if helper.status: #user status
                count += 1
            else:
                failed_list.append(user)
            if user != users[-1] or count != len(users):
                t = random.randint(interval_time[0],interval_time[1])
                print('稍等{}s...'.format(t))
                time.sleep(t) #wait for 20-50s by default
        for  user in failed_list:
            print('-------------------------------------------------------')
            lt = time.asctime(time.localtime(time.time()))
            print('于{}尝试重新为用户{}填报...'.format(lt,user['account']))
            helper = JLU_Helper(user,key_words,pause_time=pause_time,retry = redo)
            helper.login()
            time.sleep(2*pause_time)
            helper.auto_fill_in()
            if helper.status: #user status
                count += 1
            if user != failed_list[-1]:
                t = random.randint(interval_time[0],interval_time[1])
                print('稍等{}s...'.format(t))
                time.sleep(t) #wait for 20-50s by default
        last_hour = localtime_hour
        is_finished = True
        lt = time.asctime(time.localtime(time.time()))
        print('本次填报已完成！完成于',lt)
        print('共有{}个用户，{}人打卡成功'.format(len(users),count))
    lt = time.asctime(time.localtime(time.time()))
    print('当前时间是{},休眠5分钟...'.format(lt))
    time.sleep(300) #scan per 5min