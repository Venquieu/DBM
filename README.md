# DBM：Don't  Bother  Me

DBM(Don't Bother Me)是一个基于爬虫技术的吉林大学自动打卡项目，致力于使吉大研究生群体免于一日四次打卡的烦恼，这也是该项目名字的由来。

DBM制作了一个自动打卡工具，用户只需设置好自己的信息并运行该工具即可，一切信息填报和提交均由打卡工具自行完成。这个打卡工具姑且就叫JLU打卡小助手吧(๑• . •๑)

## 声明

1. 本助手仅适用于**吉林大学研究生**，本科生等无法使用本系统；
2. 当出现发烧等症状时需如实填报系统，不得使用本项目自动填报，由此产生的一切后果由用户本人承担。

## 更新

由于打卡系统变更，特对本项目进行更新，同时添加一些必要的异常处理。

- 修改一日四次打卡为一日两次打卡；
- 添加必要选项，允许用户*跳过本次打卡*和*单次跳过打卡前延时*，具体使用参见<a href="##使用">使用 </a>；
- 添加为打卡失败用户重复打卡功能，若用户打卡失败，在打卡时段内将重复为用户打卡直至打卡成功；
- 添加对显示异常网页的异常捕捉及处理，同时输出必要信息。

## 安装

小助手须在PC端python环境下运行，运行前需安装：

- python 编译器
- python包 selenium
- Chrome浏览器(目前仅支持Chrome浏览器)
- 与Chrome浏览器版本一致的chromedriver

### chromedriver版本选择

chromedriver[下载地址](http://chromedriver.storage.googleapis.com/index.html)

详细的chromedriver与chrome的对应关系可参考[notes](http://chromedriver.storage.googleapis.com/2.46/notes.txt)，这里给出部分常用的版本对应关系：

| **chromedriver版本** | **支持的Chrome版本** |
| -------------------- | -------------------- |
| v2.46                | v71-73               |
| v2.45                | v70-72               |
| v2.44                | v69-71               |
| v2.43                | v69-71               |
| v2.42                | v68-70               |

同时还有一些与Chrome版本号相同的chromedriver也可供选择。

chromedriver选择应尽可能与Chrome浏览器版本一致，否则可能会出现网页不能正常连接的情况。

### Windows

1. python安装方法自行百度，推荐到[python官网](https://www.python.org/downloads/)下载安装

2. win+R打开cmd窗口，将[python安装目录]\Scripts中的pip.exe拖入cmd窗口，在之后输入```pip install selenium```

3. 打开Chrome浏览器，在设置—>关于Chrome 中查看浏览器版本

4. 下载与浏览器版本一致的[chromedriver](http://chromedriver.storage.googleapis.com/index.html)；

5. 将下载解压的```chromedriver.exe```放在[python安装目录]\Scripts目录中。

### Mac

1. 在Terminal中输入：

```
pip install selenium
```

2. 打开Chrome浏览器查看浏览器版本，下载与浏览器版本一致的[chromedriver](http://chromedriver.storage.googleapis.com/index.html)；

3. 解压后将chromedriver文件所在路径加到环境变量中。打开用户根目录下的.bash_profile文件，在最后添加```export PATH=$PATH:[chromedriver所在目录]```，保存后退出即可。

4. 在Terminal中输入：

   ```
   source ~/.bash_profile
   ```


### Linux

1. 在Terminal中输入：

```
pip install selenium #安装selenium
google-chrome --version #查看chrome浏览器版本
```

2. 下载与浏览器版本一致的[chromedriver](http://chromedriver.storage.googleapis.com/index.html)；

3. 解压后将chromedriver文件所在路径加到环境变量中。打开用户根目录下的.bashrc文件，在最后添加```export PATH="[chromedriver所在目录]:$PATH"```，保存后退出即可。

4. 在Terminal中输入

   ```
   source ~/.bashrc
   ```

   

## 使用

1. 在UserSetting.py中将用户信息改为自己的，如果有多个用户(不建议过多用户共用)，按如下形式添加，注意遵循python语法：

```
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
```

2. UserSetting.py中的```pause_time```表示每次操作后的停顿时间，默认为1s，用户可根据偏好或需求自行调整

3. 在python编译器或在命令行运行main.py，若处于打卡时段，默认从该时段开始为用户打卡


   如果处于打卡时段，且想要从下个时段开始打卡(适用于本时段已打卡的用户)，命令行输入：

   ```
   python main.py --skip
   ```

   默认情况下在打卡时段进行打卡前会等待1-5min，针对使用本项目时打卡时间即将过去的情况，可以在当前时段去除打卡等待，命令行输入：

   ```
   python main.py --do_now
   ```

   

4. 注意查看输出信息显示自己是否打卡成功。使用过程中有可能会因为网络中断、网站改版等原因打卡失败。

## 注

因可能存在的运行问题及优化需求，本项目不定时更新，请及时关注[GitHub主页](https://github.com/Venquieu/DBM)获取最新版本。

