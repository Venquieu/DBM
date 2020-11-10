# @author: Ven
# @data:   2020/10/3
# @brief:  define user information&settings

# 操作停顿单位时长
pause_time = 1

#相邻用户打卡时间间隔的数值范围
interval_time = [20,50]

#网页显示异常时重试次数
re_login = 4 #重新登录
re_connect = 4 #重新进入打卡页面
re_submit = 3 #重新提交

# 在这里输入用户信息
users = [
		#住学校
        {
            'name':'name1',#账户
            'pw':'pw1',#密码
            'profession':'profession1',#专业
            'grade':'grade1',#年级
            'campus':'campus1',#校区
            'apartment':'apartment1',#公寓
            'room':'room1',#寝室号
            'degree':'degree1'#学位(硕士/博士)
        }, 
        #走读
        {
            'account':'account2',  #账户
            'pw':'pw2',    #密码
            'profession':'profession2', #专业
            'grade':'grade2', #年级
            'campus':'campus2', #校区
            'apartment':'apartment2', #填 校外居住
            'province':'province2', #省
            'city':'city2', #市
            'area':'area2', #区
            'address':'address2', #具体地址
            'degree':'degree2' #学位(硕士/博士)
        }
        #You can add more here
    ]
