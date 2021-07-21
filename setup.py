import os
from json import dumps
import re
from urllib.request import URLopener, urlopen
from urllib.request import urlretrieve
import zipfile
from bs4 import BeautifulSoup
def get_your_info()->None:
      '''获取用户的用户名和密码（读取json文件。如果json文件中没有，就请求用户输入并存入json）''' 
      global username
      global password

      with open('userdata.json', 'w') as f:
            #请求用户输入：
            ans='n'
            while('n' in ans or 'N' in ans):
                  username=input("请输入你的学号：")
                  password=input("请输入你的密码：")
                  ans=input("您的学号和密码是正确的吗？：是(y)否(n)")
            #创建一个用户信息的字典info_dict
            info_dict={}
            info_dict["uname"]=username
            info_dict["pwd"]=password

            #将信息存储到json中，之后自动调用
            with open('userdata.json', 'w') as f:
                  b=dumps(info_dict)
                  f.write(b)
            print('用户信息录入userdata.json成功！')
def create_bat()->None:
      path=os.getcwd()
      txt='''
netsh wlan connect name=ZJUWLAN
timeout 5
start %s\\AutoHit.exe
pause'''%path

      with open("autostart.bat",'w')as f:
            f.write(txt)
      print("autostart.bat文件创建成功！")

def get_chromedriver_version():
      chrome_path=(os.popen("where chrome")).read()
      version_pattern=re.compile(r"\d{2}[.]\d[.]\d{4}[.]\d{3}")
      for dirpath,dirnames,files in os.walk(os.path.dirname(chrome_path)):
            for dir in dirnames:
                  if re.match(version_pattern,dir)!=None:
                        return dir
def get_chromedriver()->bool:
      print("现在为您寻找并安装正确的chromedriver，如果失败，请您按照ReadMe里的教程手动安装即可")
      version=get_chromedriver_version()
      if version==None:
            print("本地找不到chrome的版本号，请手动查找：\n\t1.打开chrome浏览器\n\t2.在地址栏输入chrome://settings/help")
            version=(input("(示例:91.0.4472.101)请输入您的版本号：")).strip(' ')
      link="http://npm.taobao.org/mirrors/chromedriver/"+version+"/chromedriver_win32.zip"
      try:
            urlopen(link)
      except:
            _version=".".join(version.split(".")[:3])
            version_pattern=re.compile('%s[.]\\d{3}'%_version)
            html=urlopen("http://npm.taobao.org/mirrors/chromedriver/")
            bs = BeautifulSoup(html, 'html.parser')
            newversion=(bs.find('a',string=version_pattern)).text
            print("镜像网站上没有该版本所对应的chromedriver，为您切换了相近版本：%s"%newversion)
            link="http://npm.taobao.org/mirrors/chromedriver/"+newversion+"/chromedriver_win32.zip"
             
      print("准备下载chromedriver:")
      try:
            urlretrieve(link,os.getcwd()+"/"+"chromedriver.zip",Schedule) 
            print("chromedriver压缩包下载成功！")
            fz = zipfile.ZipFile(os.getcwd()+"/"+"chromedriver.zip", 'r')
            for file in fz.namelist():
                  fz.extract(file,os.getcwd())
            print("解压成功！")
            return 1
      except:
            print("chromedriver下载或解压失败，请到网站自行查找，手动安装 http://npm.taobao.org/mirrors/chromedriver/")
            print("您的版本号是：%s"%version)
            return 0
      
def Schedule(a,b,c):
   '''
   a:已经下载的数据块
   b:数据块的大小
   c:远程文件的大小
   '''
   per = 100.0*a*b/c
   if per > 100:
      per = 100
   print('%.2f%%' % per)

if __name__=="__main__":
      get_your_info()
      create_bat()
      get_chromedriver()
      print("下一步：请手动将autostart.bat文件放在C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp下")
      input("...按任意键退出安装程序")
      