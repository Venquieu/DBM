# @author: Ven
# @data:   2020/10/3
# @brief:  main program of DBM,run this script to keep away from BOTHER

from UserSetting import *
from DBM import JLU_Helper
import time
import random
import argparse

key_words = {
    'Chinese':['登录成功','如有其它相关说明，请点击','确定','好','办理成功','确定'],
    'English':['登录成功','If you have anything to comment,please click','Ok','Ok','Done successfully!','Ok']
}


def timer(only_hour = False):
    '''return local time'''
    time_ = time.asctime(time.localtime(time.time()))
    if only_hour:
        hms = time_.split(' ')[-2]
        return int(hms.split(':')[0])
    return time_

def is_filling_time(local_hour):
    '''Judge if it is a filling time'''
    if (local_hour in range(6,12)) or (local_hour in range(21,23)):
        return True
    return False

def filling_process(user_info):
    '''filling process for user'''
    helper = JLU_Helper(user_info,key_words,pause_time=pause_time)
    helper.login()
    time.sleep(2*pause_time)
    helper.auto_fill_in()
    return helper.status

def main():
    parser = argparse.ArgumentParser(description="JLU helper keeps bothers away from you.")
    parser.add_argument(
        "--skip_wait",  #fill in from scratch
        action='store_true',
        default=False,
    )
    parser.add_argument(
        "--do_now", 
        action='store_false',
        default=True,
    )
    args = parser.parse_args()
    is_finished = args.skip_wait
    wait = args.do_now
    while True:
        localtime_hour = timer(only_hour=True)
        if not is_filling_time(localtime_hour):
            is_finished = False  #wait for next time
        if (not is_finished) and is_filling_time(localtime_hour):
            if wait:
                t = random.randint(1,5)#wait for 1-5min
                print('当前时间是{}，{}min后将进行填报，请稍侯...'.format(timer(),t))
                time.sleep(60*t)
            else:
                wait = True

            count = 0 # count number of user who filling succeed
            batch = 0 # filling batch
            user_list = users
            while len(user_list) > 0 and is_filling_time(timer(only_hour=True)):
                batch += 1
                failed_list = []
                print('==================================================')
                print('为用户进行第{}批填报，本批次共{}个用户'.format(batch,len(user_list)))
                for  user in user_list:
                    print('**************************************************')
                    lt = timer()
                    print('于{}开始为用户{}填报...'.format(lt,user['account']))
                    status = filling_process(user)
                    if status: #user status
                        count += 1
                    else:
                        failed_list.append(user)

                    if user != user_list[-1] or count != len(users):
                        t = random.randint(interval_time[0],interval_time[1])
                        print('稍等{}s...'.format(t))
                        time.sleep(t) #wait for 20-50s by default
                user_list = failed_list

            is_finished = True
            lt = timer()
            print('本次填报结束,结束于',lt)
            print('共有{}个用户，{}人打卡成功'.format(len(users),count))
        lt = timer()
        print('当前时间是{},休眠10分钟...'.format(lt))
        time.sleep(600) #scan per 5min

if __name__ == '__main__':
    main()