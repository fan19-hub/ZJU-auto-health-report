# ZJU_auto_punch
### 介绍：
1.  修改了“浙江大学自动打卡计划”的代码，考虑了报错，使其鲁棒性更高，并添加了注释。欢迎大家提出issue或者上传修改代码 
2.  源项目地址：https://github.com/Tishacy/ZJU-nCov-Hitcarder 
3. 本项目所有函数功能已经写明，无发送信息等泄露用户的隐私的代码，请放心使用 

**本代码仅供web学习参考，请大家认真对待健康打卡，疫情无小事！！！！！！** 


### 安装指南（exe版已发布，https://github.com/fan19-hub/zju-auto-punch/files/6855605/exe.zip ）：
1. 确保你**正确安装python**，Chrome浏览器(若使用其他浏览器需下载对应的驱动并在代码里做相应改动)
2. 将整个项目下载到本地
3. 点击setup.bat进行安装**如果chromedriver下载失败，你可以参考最下面教程手动下载**
4. 确保你昨天或者今天打过一次卡
5. 如果你想直接打卡，可以运行AutoHit.py，或者点击autostart.bat
6. 为了实现每次开机时自动打卡，需要把autostart.bat这个文件，放到**C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp**目录下（在有的电脑上可能会有中文路径） 
- 这个**StartUp**目录也就是开机启动目录哈哈哈，这样每次开机就会运行啦！


### P.S. chromedriver的安装：
  - 在Chrome设置->关于Chrome查到所使用的Chrome版本号
  - 在[这里](http://npm.taobao.org/mirrors/chromedriver/)下载对应版本的chromedriver
  - 将解压后的chromedriver.exe放到本目录下即可（和AutoHit.py一起）

### 各个文件功能说明：
- setup.bat是一个批处理文件，它首先读取requirements.txt里面提到的python库，并进行安装，然后运行setup.py
- requirements.txt记录了需要安装的python库
- setup.py是安装程序，有三个功能。1.要求你输入学号和密码并将它储存在userdata.json里 2.自动创建autostart.bat文件 3.自动下载chromedriver
- AutoHit.py是打卡主程序，它会先检测网络连接，如果没网会等待用户联网。一分钟后还连不上就会退出。然后它从userdata.json里读取你的学号和密码用来登录，然后操作网页并打卡。如果打卡失败，用户可以按回车键重新尝试打卡，或者输入C来更改学号密码再尝试，或者关闭窗口退出
- autostart.bat是自动打卡批处理文件，它首先尝试连接ZJUWLAN，如果失败了，你必须手动连接随便一个无线网。然后它会等五秒钟，之后运行AutoHit.py。运行完之后会暂停（pause），可以按任意键退出
