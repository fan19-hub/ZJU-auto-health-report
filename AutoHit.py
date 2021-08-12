""""
@reference: https://github.com/Tishacy/ZJU-nCov-Hitcarder
@Author: fan19-hub
Date:7/14/2021
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

import json
from time import sleep
import os
import zipfile

from re import findall
from re import compile,match
from urllib.request import URLopener, urlopen, urlretrieve
from bs4 import BeautifulSoup

SUCCESS=1
FAILURE=0
SYS_FAILURE=0
username=""
password=""
visible=0


def auto_connect_wifi():

      #check network
      print("\n\n正在检查网络连接：")
      exit_code = os.system('ping www.baidu.com')
      if not exit_code:
            print("\n\n报告：网络连接正常")
            return 1

      #automatically try to connect wifi
      print("\n\n报告：无网络连接\n")
      wifi_info=os.popen("netsh wlan show profile").read()  #get wifi list
      wifi_list=findall(r"(?:所有用户配置文件 : )(.*)(?:\n)",wifi_info)
      for i in range(5):
            wifi_name=wifi_list[i]
            os.system("netsh wlan connect name=%s"%wifi_name)
            print("正在尝试连接%s"%wifi_name,end="")
            wait(1,5)
            exit_code=os.system('ping www.baidu.com')
            if(exit_code):
                  print("%s连接失败"%wifi_name)
            else:
                  return 1
      print("自动尝试连接失败，请您手动联网",end="")
      wait(1,10)
      print("将直接为您执行之后的程序")
      


def get_your_info():
      """ 获取用户的用户名和密码（读取json文件。如果json文件中没有，就请求用户输入并存入json） """
      global username
      global password
      global area_default

      try:
            with open('userdata.json', 'r',encoding="utf-8") as f:
                  content = f.read()
            #json文件不为空，那就直接读取
            info_dict= json.loads(content)
            try:
                  username=info_dict["uname"]
                  password=info_dict["pwd"]
            except:
                  print("用户名或密码信息丢失。请修改")
                  info_dict=modify_json()

            try:
                  area_default=(info_dict["area"].strip()).split(" ")
                  assert len(area_default)==3
            except:
                  print('''默认打卡地址丢失，或者userdata.json文件内部地址格式不正确（正确格式："浙江省 杭州市 西湖区"）修改：''')
                  info_dict=modify_json()
      except:
            info_dict=modify_json()


            
def modify_json():
      global username
      global password
      global area_default
      ans='n'
      while('n' in ans or 'N' in ans or "否" in ans):
                  #请求用户输入：
            username=input("请输入你的学号：")
            password=input("请输入你的密码：")
            print("请输入默认打卡地址：")
            sheng=input("省（例如浙江省）：").strip()
            shi=input("市（例如杭州市）：").strip()
            xian=input("县区（例如西湖区）：").strip()
            area_default=sheng+" "+shi+" "+xian
            ans=input("您输入的信息是正确的吗？选n以修改：是(y)否(n)")
     
      #创建一个用户信息的字典info_dict
      info_dict={}
      info_dict["uname"]=username
      info_dict["pwd"]=password
      info_dict["area"]=area_default

      #将信息存储到json中，之后自动调用
      with open('userdata.json', 'w',encoding='utf-8') as f:
            b=json.dumps(info_dict)
            f.write(b)
      return info_dict   



def openPage(url):
      global visible
      """ 打开网页 """
      opt = Options()

      if not visible:
            opt.add_argument('--headless')
      opt.add_argument('--disable-gpu')
      
      
      try:
            driver_path=r".\chromedriver.exe"
            browser = webdriver.Chrome(executable_path=driver_path, chrome_options = opt)
      except:
            print("\n错误：chromedriver出错，请检查：\n1、chromedriver是否与AutoHit在同一文件夹下 \n2、chromedriver版本是否与chrome浏览器版本匹配")
            a=input("是否获取chromedriver：y/n：")
            if a!="n":
                  get_chromedriver()
            return None
     
     
      try:
            if browser!=None:
                  browser.get(url)
      except:
            print("获取网页失败，可手动打开网页验证网络连接，并自行排除网络故障。提示：若使用过vpn，请在windows代理服务器设置里关闭代理即可）")
            browser.close()
            return None
      
      return browser



def login(browser,username, password)->bool:
      """ 浙大统一认证登录 """
      try:
            #输入用户名
            usr = browser.find_element_by_id("username")
            usr.send_keys(username)

            #输入密码
            psw = browser.find_element_by_id("password")
            psw.send_keys(password)

            #按提交按钮
            loginbtn = browser.find_element_by_id("dl")
            loginbtn.click()
      except:
            print("登录界面提交用户名、密码失败，请邮件联系开发者 fan.19@intl.zju.edu.cn")
            os.system("pause")
            assert SYS_FAILURE
      #检查登录是否成功
      try:
            error =browser.find_element_by_xpath("//p[@id='errormsg']/span[@id='msg']")
            print("登录失败：",error.text)
            if visible==1:
                  os.system("pause")
            return FAILURE
      
      except:
            return SUCCESS



def submit(browser)->bool:      
      """ 提交健康打卡 """
      global visible
      global area_default
      try:
            #是否意向接种
            js ='document.getElementsByName("sfyxjzxgym")[0].children[1].children[0].click()'  # js点击元素， HTML DOM children 属性，注意是Elements复数
            browser.execute_script(js)  # 执行js语句

            #是否是不宜接种人群
            js ='document.getElementsByName("sfbyjzrq")[0].children[1].children[4].click()' 
            browser.execute_script(js)  # 执行js语句

            #接种情况
            js ='document.getElementsByName("jzxgymqk")[0].children[1].children[1].click()' 
            browser.execute_script(js)


            #今日是否因发热请假未到岗（教职工）或未返校（学生）
            js ='document.getElementsByName("sffrqjwdg")[0].children[1].children[1].click()' 
            browser.execute_script(js)

            #今日是否因发热外的其他原因请假未到岗（教职工）或未返校（学生）
            js ='document.getElementsByName("sfqtyyqjwdg")[0].children[1].children[1].click()' 
            browser.execute_script(js)


            #健康码情况
            js ='document.getElementsByName("sfsqhzjkk")[0].children[1].children[0].click()' 
            browser.execute_script(js)
            #健康码颜色
            js ='document.getElementsByName("sqhzjkkys")[0].children[1].children[0].click()' 
            browser.execute_script(js)
      except:
            print("是否意向接种 至 健康码颜色 题目中有一些 未点击成功，但问题不大")


      try:
            #是否在校
            # item1 = browser.find_element_by_xpath("//div[@name='sfzx']/div/div[2]")
            # item1.click()
            js ='document.getElementsByName("sfzx")[0].children[1].children[0].click()'  
            browser.execute_script(js) # 执行js语句
      except:
            print("是否在校 点击失败，请邮件联系开发者 fan.19@intl.zju.edu.cn")
            os.system("pause")
            assert SYS_FAILURE

      try:
            #本人家庭成员(包括其他密切接触人员)是否有近14日入境或近14日拟入境的情况
            # item2 = browser.find_element_by_xpath("//div[@name='sfymqjczrj']/div/div[2]")
            # item2.click()
            js ='document.getElementsByName("sfymqjczrj")[0].children[1].children[1].click()'  # js点击元素， HTML DOM children 属性，注意是Elements复数
            browser.execute_script(js)  # 执行js语句
      except:
            print("本人家庭成员(包括其他密切接触人员)是否有近14日入境或近14日拟入境的情况 题目点击失败，请邮件联系开发者 fan.19@intl.zju.edu.cn")
            os.system("pause")
            assert SYS_FAILURE

      #位置信息
      try:
            # addrs = browser.find_element_by_xpath("//input[@placeholder='点击获取地理位置 Click to get geographic location']")
            # addrs.click()

            js ='document.getElementsByName("area")[0].children[1].click()'  # js点击元素， HTML DOM children 属性，注意是Elements复数
            browser.execute_script(js)  # 执行js语句
            for _ in range(30):
                  sleep(0.5)
                  page_loading_container=browser.find_element_by_xpath("//div[@class='page-loading-container']")
                  if page_loading_container.get_attribute("style")=="display: none;":
                        break
            js ='document.getElementsByClassName("wapat-inner")[0].children[1].children[0].click()'  # js点击元素， HTML DOM children 属性，注意是Elements复数
            browser.execute_script(js)  # 执行js语句
            # 找到省份下拉菜单
            e1 = browser.find_element_by_xpath("//select[@class='hcqbtn hcqbtn-danger']")
            # 按文本选择
            Select(e1).select_by_visible_text(area_default[0])            
            # 找到城市下拉菜单
            e2 = browser.find_element_by_xpath("//select[@class='hcqbtn hcqbtn-warning']")
            # 按文本选择
            Select(e2).select_by_visible_text(area_default[1])
            # 找到县市区下拉菜单
            e2 = browser.find_element_by_xpath("//select[@class='hcqbtn hcqbtn-primary']")
            # 按文本选择
            Select(e2).select_by_visible_text(area_default[2])
            try:
                  _=browser.find_element_by_name("bztcyy")
                  print("当前地点与上次不在同一城市。默认为您选择的地点是：%s"%area_default)
                  a=input("是否修改默认地点 (下次生效)？是(y)/否(n)")
                  if 'y' in a or 'Y' in a or "是" in a:
                        modify_json()
                  js ='document.getElementsByName("bztcyy")[0].children[1].children[5].click()'  # js点击元素， HTML DOM children 属性，注意是Elements复数
                  browser.execute_script(js)  # 执行js语句
            except:
                  pass
      except:
            pass
            
      try:
            # 上述信息真实准确
            js ='document.getElementsByName("sfqrxxss")[0].children[0].children[0].click()' 
            browser.execute_script(js)
            # item3 = browser.find_element_by_xpath("//div[@name='sfqrxxss']/div/div/span")
            # item3.click()
      except:
            print("上述信息真实准确  点击失败。 请邮件联系开发者 fan.19@intl.zju.edu.cn")
            os.system("pause")
            assert SYS_FAILURE
            
      if visible==1:
            os.system("pause")
            return SUCCESS
      try:
            #提交信息 
            js ='document.getElementsByClassName("footers")[0].children[0].click()' 
            browser.execute_script(js)
            # button1 = browser.find_element_by_xpath("//div[@class='footers']/a")
            # button1.click()
      except:
            print("提交信息按钮 点击失败。 请邮件联系开发者 fan.19@intl.zju.edu.cn")

      try:
            js ='document.getElementsByClassName("wapcf-btn-box")[0].children[1].click()' 
            browser.execute_script(js)
            # button2 = browser.find_element_by_xpath("//div[@class='wapcf-btn-box']/div[2]")
            # button2.click()
      except:
            a=browser.find_element_by_xpath("//div[@class='wapat-inner']")
            if "每天只能填报一次" in a.text:
                  print("每天只能填报一次，您已提交过")
                  print("打卡完成")
                  return SUCCESS
            else:
                  print(a.text)
                  print("自动打卡出了点小问题，为您打开网页哦~，请手动填写一下")
                  visible=1
                  return FAILURE
      print("打卡成功！")
      return SUCCESS


def retry_setting():
      """询问用户以何种方式重试"""
      global visible
      visible=1
      
      print("您可以：\n\t按回车键重试打卡\n\t或关闭窗口退出\n\t或输入C更改学号和密码，并自动重试")
      command=input(":")
      if "C" in command or "c" in command:            #if you want to change the ID or password
            open("userdata.json", 'w').close()
            get_your_info()


def wait(sleep_sec,num,char="."):
      '''用闪烁的小点来计时'''
      for _ in range(num):
            print(char,end="")
            sleep(sleep_sec)
      print(' ')

      
def get_chromedriver()->bool:
      "自动下载合适版本的chromedriver"
      try:
            chrome_path=(os.popen("where chrome")).read()
            version_pattern=compile(r"(\d{2}[.]\d[.]\d{4}[.]\d{2,3}|2[.]\d{1,2})")
            for _,dirnames,_ in os.walk(os.path.dirname(chrome_path)):
                  for dir in dirnames:
                        if match(version_pattern,dir)!=None:
                              version=dir
      except Exception as e:
            print("报错！错误信息：",e)
      if version==None:
            print("本地找不到chrome的版本号，请手动查找：\n\t1.打开chrome浏览器\n\t2.在地址栏输入chrome://settings/help")
            while 1:
                  version=(input("(示例:91.0.4472.101)请输入您的版本号：")).strip(' ')
                  if match(r"(\d{2}[.]\d[.]\d{4}[.]\d{2,3}|2[.]\d{1,2})",version)!=None:
                        break
                  print("格式有误，请重新输入")
      link="http://npm.taobao.org/mirrors/chromedriver/"+version+"/chromedriver_win32.zip"
      ans='n'
      while('n' in ans or 'N' in ans):
            print("请确保您的网络连接正常")
            ans=input('您的网络连接是否正常？是(y)否(n)')
      try:
            urlopen(link)
      except:
            try:
                  _version=".".join(version.split(".")[:3])
                  version_pattern=compile('%s[.]\\d{3}'%_version)
                  html=urlopen("http://npm.taobao.org/mirrors/chromedriver")
                  bs = BeautifulSoup(html, 'html.parser')
                  newversion=(bs.find('a',string=version_pattern)).text[:-1]
                  print("镜像网站上没有该版本所对应的chromedriver，为您切换了相近版本：%s"%newversion)
                  link="http://npm.taobao.org/mirrors/chromedriver/"+newversion+"/chromedriver_win32.zip"
            except Exception as e:
                  print("报错！错误信息：",e)
                  return 0

      print("准备下载chromedriver:")
      try:
            urlretrieve(link,os.getcwd()+"/"+"chromedriver.zip",Schedule) 
            print("chromedriver压缩包下载成功！")
            fz = zipfile.ZipFile(os.getcwd()+"/"+"chromedriver.zip", 'r')
            for file in fz.namelist():
                  fz.extract(file,os.getcwd())
            print("\n\n获取成功！")
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


def main():
      global visible

      auto_connect_wifi()

      get_your_info()

      for _ in range(3):    #try at most three times              
            bs=openPage("https://healthreport.zju.edu.cn/ncov/wap/default/index")   

            if bs==None or FAILURE==login(bs, username, password):      #if opening page or loging failed
                  retry_setting()
            else:                                  #if opening page and login succeed
                  res=submit(bs)                #submit the page
                  try:
                        bs.close()               #close it
                  except:
                        pass
                  if res==SUCCESS:
                        input("\n...按回车键退出")
                        return
      print("连续三次打卡失败，程序退出",end="")
      wait(1,10)


if __name__ == "__main__":
      main()

