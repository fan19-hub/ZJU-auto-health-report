# ZJU_auto_punch
### 介绍：
1.  修改了“浙江大学自动打卡计划”的代码，考虑了报错，使其鲁棒性更高，并添加了注释。欢迎大家提出issue或者上传修改代码 
2.  源项目地址：https://github.com/Tishacy/ZJU-nCov-Hitcarder 
3. 本项目所有函数功能已经写明，无发送信息等泄露用户的隐私的代码，请放心使用 

*本代码仅供web学习参考，请大家认真对待健康打卡，疫情无小事！！！！！！*


### 安装指南
1. 确保python，Chrome已经安装好
2. 点击python2exe.bat，将会自动为您安装运行所需库，并从python源码生成exe文件
3. 点击setup.exe进行安装*。 提示：如果chromedriver下载失败，你可以参考最下面P.S.手动下载* 
4. 之后想要一键打卡：点击AutoHit.exe即可
5. 创建AutoHit的快捷方式，放到**C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp**目录下 
- 这个StartUp目录也就是开机启动目录哈哈哈，这样每次开机就会运行啦！


### P.S. chromedriver的安装：
  - 在 Chrome设置->关于Chrome 中查到所使用的Chrome版本号
  - 在[这里](http://npm.taobao.org/mirrors/chromedriver/)下载对应版本的chromedriver
  - 将解压后的chromedriver.exe放到本目录下即可



### 各个文件功能说明：
- python2exe.bat是批处理文件，有三个功能：1.pip指令安装所需库 2.打包setup.py文件 3.打包AutoHit.py文件
- requirements.txt记录了需要安装的python库
- userdata.json包含了用户的信息
- setup是安装程序，有两个功能。1.要求你输入学号，密码和默认打卡位置并将它储存在userdata.json里 2.自动下载chromedriver
- AutoHit是打卡主程序，它会先检测网络连接。如果没网，程序会检索所有的可用wifi并逐个尝试。然后程序会从userdata.json里读取学号、密码和默认打卡地点，操作网页并打卡。程序已经考虑（但不限于）以下的错误：
1. chromdriver驱动出错时，程序会询问用户是否要重新下载chromedriver 
2. 网络连接失败，会自动寻找可用wifi并尝试连接
3. 用户使用vpn等代理工具导致网络异常，会提示“获取网页失败，可手动打开网页验证网络连接，并自行排除网络故障。提示：若使用过vpn，请在windows代理服务器设置里关闭代理即可）”
4. 登录失败，程序会启动retry模块并询问用户的选择：按回车键重试打卡，或关闭窗口退出，或输入C更改学号和密码，并自动重试 
5. 获取位置信息失败，程序将自动填写默认打卡地址。当出现当前城市与上一次不一致时，程序会询问是否修改默认打卡地址，并自动选择“其他”原因
6. 默认打卡地址丢失或者格式错误，程序将要求用户修改
7. 昨日未打卡，程序将正常填写表单

