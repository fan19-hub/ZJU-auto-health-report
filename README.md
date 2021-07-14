# ZJU_auto_punch
### 介绍：
1.  修改了“浙江大学自动打卡计划”的代码，考虑了报错，使其鲁棒性更高，并添加了注释。欢迎大家提出issue或者上传修改代码  
2.  源项目地址：https://github.com/Tishacy/ZJU-nCov-Hitcarder 
3. 本项目所有函数功能已经写明，无发送信息等泄露用户的隐私的代码，请放心使用。
**本代码仅供web学习参考，请大家认真对待健康打卡，疫情无小事！！！！！！** 

### 安装指南（根据源项目文档修改）：
1. 需**正确安装python**(一切的前提)，Chrome浏览器(若使用其他浏览器需下载对应的驱动并在代码里做相应改动)
2. 安装selenium库。可以直接在命令行中输入`pip install selenium`
3. 安装chromedriver(具体见后面P.S.)
4. 将整个项目下载到本地
5. 要先手动打一次卡，并运行一次AutoHit.py，输入你的信息，并确保不报错
6. 里面有一个名为autostart.bat的批处理文件：
```bat
ping localhost -n 4
python D:\projects\Python\AutoHit.py
```
要打开它，把里面那个路径**改成自己的AutoHit.py的路径**
然后把它放到**C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp**目录下（在有的电脑上可能会有中文路径）
这个**StartUp**目录也就是开机启动目录哈哈哈，这样每次开机就会运行啦



**P.S.** chromedriver的安装：
  - 在Chrome设置->关于Chrome查到所使用的Chrome版本号
  - 在[这里](http://npm.taobao.org/mirrors/chromedriver/)下载对应版本的chromedriver
  - 将解压后的chromedriver.exe所在目录放到python的scripts目录里（这样就不用再单独添加环境变量了）我的路径是：C:\Users\fan.19\AppData\Local\Programs\Python\Python38\Scripts
  - 在命令行里输入chromedriver看看是否正确安装
