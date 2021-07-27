# ZJU_auto_punch
### 介绍：
1.  修改了“浙江大学自动打卡计划”的代码，考虑了报错，使其鲁棒性更高，并添加了注释。欢迎大家提出issue或者上传修改代码 
2.  源项目地址：https://github.com/Tishacy/ZJU-nCov-Hitcarder 
3. 本项目所有函数功能已经写明，无发送信息等泄露用户的隐私的代码，请放心使用 

*本代码仅供web学习参考，请大家认真对待健康打卡，疫情无小事！！！！！！*


### 安装指南1（python源代码版）
1. 确保python，Chrome已经安装好
2. 下载本项目
3. 点击setup.bat进行安装。 *提示：如果chromedriver下载失败，你可以参考下面P.S.手动下载*
4. 之后想要一键打卡：点击autostart.bat（或者自己运行AutoHit这个python文件）
5. 实现每次开机时自动打卡：把autostart.bat这个文件，放到**C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp**目录下 
- 这个StartUp目录也就是开机启动目录哈哈哈，这样每次开机就会运行啦！


### 安装指南2（exe版，无需python及依赖库）：
1.  确保chrome已经安装 
2.  下载[download.zip](https://github.com/fan19-hub/zju-auto-punch/files/6856843/exe.zip)，并解压到本地 
3.  点击setup进行安装*。 提示：如果chromedriver下载失败，你可以参考最下面P.S.手动下载* 
4.  创建AutoHit的快捷方式，放到**C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp**目录下 



### P.S. chromedriver的安装：
  - 在 Chrome设置->关于Chrome 中查到所使用的Chrome版本号
  - 在[这里](http://npm.taobao.org/mirrors/chromedriver/)下载对应版本的chromedriver
  - 将解压后的chromedriver.exe放到本目录下即可



### 源代码版各个文件功能说明：
- setup.bat是一个批处理文件，它首先读取requirements.txt里面提到的python库，并进行安装，然后运行setup.py
- requirements.txt记录了需要安装的python库
- setup.py是安装程序，有三个功能。1.要求你输入学号和密码并将它储存在userdata.json里 2.自动创建autostart.bat文件 3.自动下载chromedriver
- AutoHit.py是打卡主程序，它会先检测网络连接，如果没网会等待用户联网。一分钟后还连不上就会退出。然后它从userdata.json里读取你的学号和密码用来登录，然后操作网页并打卡。如果打卡失败，用户可以按回车键重新尝试打卡，或者输入C来更改学号密码再尝试，或者关闭窗口退出
- autostart.bat是自动打卡批处理文件，它首先尝试连接ZJUWLAN，如果失败了，你必须手动连接随便一个无线网。然后它会等五秒钟，之后运行AutoHit.py。运行完之后会暂停（pause），可以按任意键退出
