
""""
@Author：Tishacy
reference: https://github.com/Tishacy/ZJU-nCov-Hitcarder
@Modified: fan19-hub
Date:7/14/2021
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
from time import sleep

SUCCESS=1
FAILURE=0
username=""
password=""

def check_network():
      print("\n\n正在检查网络连接：")
      for c in range(12):
            exit_code = os.system('ping www.baidu.com')
            if exit_code:
                  if(c==1):
                        print("\n\n没有网唉，快去联网！不用关闭窗口，等你一分钟\n\n")
                  sleep(5)
                  continue
            else:
                  print("\n\n检查结果：网络正常\n\n")
                  return
      raise Exception('\n\n等主人联网等了一分钟啦，没网我先撤了拜拜~')
def get_your_info():
      """ 获取用户的用户名和密码（读取json文件。如果json文件中没有，就请求用户输入并存入json） """
      global username
      global password

      with open('userdata.json', 'r') as f:
            content = f.read()
      if content=='':       
            #如果json文件是空的，也就是说你是首次运行
            #请求用户输入：
            username=input("请输入你的学号：")
            password=input("请输入你的密码：")
            
            #创建一个用户信息的字典info_dict
            info_dict={}
            info_dict["uname"]=username
            info_dict["pwd"]=password

            #将信息存储到json中，之后自动调用
            with open('userdata.json', 'w') as f:
                  b=json.dumps(info_dict)
                  content = f.write(b)
      else:
            #json文件不为空，那就直接读取
            info_dict= json.loads(content)
            username=info_dict["uname"]
            password=info_dict["pwd"]


def openPage(url):
      """ 打开网页 """
      opt = Options()
      opt.add_argument('--headless')
      opt.add_argument('--disable-gpu')
      try:
            driver_path=r".\chromedriver.exe"
            browser = webdriver.Chrome(executable_path=driver_path, chrome_options = opt)
      except:
            print("chromedriver出错，请检查：1、chromedriver是否与AutoHit.py在同一文件夹下 2、chromedriver版本是否与chrome浏览器版本匹配")
    
      try:
            browser.get(url)
      except:
            print("获取网页失败，可手动打开网页验证网络连接，并自行排除网络故障。提示：若使用过vpn，请在windows代理服务器设置里关闭代理即可）")
            browser.close()
            return None
      return browser

def login(browser,username, password)->bool:
      """ 浙大统一认证登录 """
      #输入用户名
      usr = browser.find_element_by_id("username")
      usr.send_keys(username)

      #输入密码
      psw = browser.find_element_by_id("password")
      psw.send_keys(password)

      #按提交按钮
      loginbtn = browser.find_element_by_id("dl")
      loginbtn.click()
      
      #检查登录是否成功
      try:
            error =browser.find_element_by_xpath("//p[@id='errormsg']/span[@id='msg']")
            print("登录失败：",error.text)
            return FAILURE
      
      except:
            return SUCCESS
      

def submit(browser)->bool:
      """ 提交健康打卡 """
      #是否在校
      item1 = browser.find_element_by_xpath("//div[@name='sfzx']/div/div[2]")
      item1.click()
      try:
            #地区
            addrs = browser.find_element_by_xpath("//div[@name='area']/input")
            addrs.click()
            error =browser.find_element_by_xpath("//div[@class='wapat-inner']/div[@class='wapat-title']")
            print(error.text,"，请开启位置权限再重试，打卡失败")
            return FAILURE
      
      except:
            print("获取位置信息成功")

      #本人家庭成员(包括其他密切接触人员)是否有近14日入境或近14日拟入境的情况
      item2 = browser.find_element_by_xpath("//div[@name='sfymqjczrj']/div/div[2]")
      item2.click()

      

      #上述信息真实准确
      item3 = browser.find_element_by_xpath("//div[@name='sfqrxxss']/div/div/span")
      item3.click()
      
      #提交信息 
      button1 = browser.find_element_by_xpath("//div[@class='footers']/a")
      button1.click()

      try:
            button2 = browser.find_element_by_xpath("//div[@class='wapcf-btn-box']/div[2]")
            button2.click()
      except:
            a=browser.find_element_by_xpath("//div[@class='wapat-inner']")
            if "每天只能填报一次" in a.text:
                  print("每天只能填报一次，您已提交过")
            else:
                  print("未弹出确认提交对话框，可能因为没有缓存导致默认选项未勾选，建议先手动提交一次")
                  print(a.text)
            print("打卡失败~")
            return FAILURE
      print("打卡成功！")
      return SUCCESS
     


if __name__ == "__main__":
      check_network()
      get_your_info()
      
      bs=openPage("https://healthreport.zju.edu.cn/ncov/wap/default/index")
      res=FAILURE
      if bs!=None and SUCCESS==login(bs, username, password): #if opening page and loging in successfully
            res=submit(bs) #submit the page
            bs.close() #close it
      if res==FAILURE:
            print("\n\n手动打卡网址：https://healthreport.zju.edu.cn/ncov/wap/default/index")
            print("您可以：\n\t按回车键重试打卡\n\t或关闭窗口退出\n\t或输入C更改学号和密码，并自动重试")
            command=input(":")
            if "C" in command or "c" in command:
                  open("userdata.json", 'w').close()
                  get_your_info()
            try:
                  os.system("start "+os.getcwd()+"\\AutoHit.exe")
            except:
                  os.system("python AutoHit.py")
