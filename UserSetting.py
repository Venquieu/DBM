# @author: Ven
# @data:   2020/10/3
# @brief:  define user information&settings

# 操作停顿单位时长
pause_time = 1

#相邻用户打卡时间间隔的数值范围
interval_time = [20,50]

# 在这里输入用户信息
users = [
        {
            'name':'name1',#账户,邮箱前缀
            'pw':'pw1',#密码
            'at_school':False #是否在校
        }, 
        {
            'name':'name2',#账户
            'pw':'pw2',#密码
            'profession':'profession2',#专业
            'grade':'grade2',#年级
            'campus':'campus2',#校区
            'phone':'number',#手机号
            'instructor':'name', #辅导员
            'at_school':True,
            'apartment':'apartment2',#公寓
            'room':'room2',#寝室号
            'degree':'degree2'#学位(硕士/博士)
        }, 
        #You can add more here
    ]
