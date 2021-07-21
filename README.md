# ZJU_auto_punch
### 介绍：
1.  修改了“浙江大学自动打卡计划”的代码，考虑了报错，使其鲁棒性更高，并添加了注释。欢迎大家提出issue或者上传修改代码 
2.  源项目地址：https://github.com/Tishacy/ZJU-nCov-Hitcarder 
3. 本项目所有函数功能已经写明，无发送信息等泄露用户的隐私的代码，请放心使用 

**本代码仅供web学习参考，请大家认真对待健康打卡，疫情无小事！！！！！！** 


### 安装指南（exe版已发布，https://github.com/fan19-hub/zju-auto-punch/files/6855605/exe.zip ）：
1. 需**正确安装python**，Chrome浏览器(若使用其他浏览器需下载对应的驱动并在代码里做相应改动)
2. 安装selenium,urllib,bs4,json库。可以直接在命令行中输入`pip install 库名`
3. 将整个项目下载到本地
4. 运行setup.py进行安装，并确保你昨天或者今天打过一次卡。**如果chromedriver下载失败，你可以参考最下面教程手动下载**
5. 接下来，你可以直接运行AutoHit.py来打卡，或者点击autostart.bat
6. 如果你想每次开机时自动打卡，那就把autostart.bat这个批处理文件，放到**C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp**目录下（在有的电脑上可能会有中文路径） 
- 这个**StartUp**目录也就是开机启动目录哈哈哈，这样每次开机就会运行啦！



### P.S. chromedriver的安装：
  - 在Chrome设置->关于Chrome查到所使用的Chrome版本号
  - 在[这里](http://npm.taobao.org/mirrors/chromedriver/)下载对应版本的chromedriver
  - 将解压后的chromedriver.exe放到本目录下即可（和AutoHit.py一起）
