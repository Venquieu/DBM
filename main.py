# @author: Ven
# @data:   2020/10/3
# @brief:  main program of DBM,run this script to keep away from BOTHER

from UserSetting import *
from DBM import JLU_Helper
import time
import random

is_finished = False #not login yet
last_hour = -1

while True:
    localtime = time.asctime(time.localtime(time.time()))
    localtime_hour = localtime.split(' ')[-2]
    localtime_hour = int(localtime_hour.split(':')[0])
    if localtime_hour != last_hour:
        is_finished = False  #wait for next time
    if (not is_finished) and (7<=localtime_hour<8 or 11<=localtime_hour<12 or \
        17<=localtime_hour<18 or 21<=localtime_hour<22):
        time.sleep(60*random.randint(1,6)) #wait for 1-5min
        print('当前时间是{}，自动填报中，请稍侯...'.format(localtime))
        count = 0
        for  i in range(len(users)):
            user = users[i]
            helper = JLU_Helper(user,pause_time=pause_time)
            helper.login()
            time.sleep(4*pause_time)
            helper.auto_fill_in()
            if helper.status: #user status
                count += 1
            time.sleep(random.randint(20,30)) #wait for 20-30s
        last_hour = localtime_hour
        is_finished = True
        print('本次填报已完成！完成于',localtime,'共有{}个用户，{}人打卡成功'.format(len(users),count))
    print('休眠5分钟...')
    time.sleep(300) #scan per 5min