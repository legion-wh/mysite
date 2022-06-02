import re
import json
import os
import time
import datetime
import unittest

import idcardexcell
from PC_newmerchant import  NewMer
from PC_newmerchant import merinit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import HtmlTestRunner
import unittest
##输入环境相关信息
envdata={
    "env": "dev",##uat  sit  pre_release  release
    "机构号":"ts666",
    "子机构号":"GDVIVO", #GDVIVO&001
    "设备标识":"1",
    "开户总数":"3",
 }

mernum=int(envdata.get("开户总数"))
print(mernum)
##开始选择开户类型，是否使用默认数据

# typemer = input("请输入商户类型:1个人 2 个体 3 企业 --->>  ")
# typemer = int(typemer)
#typemer = 3 # 强制限制开户类型
##测试报告生成路径

##定义测试报告的标题和描述
#runner=HtmlTestRunner.HTMLTestRunner(output=file_path)
##测试套件
# suit=unittest.TestSuite()
# suit.addTest(FileManager_test('test_file_movefile'))

url = "https://apitest.tenserpay.xyz/"
chrome_driver=r"F:\python3.6\chromedriver.exe"
driver=webdriver.Chrome(executable_path=chrome_driver)
class Geturl():
    def autogeturl(driver,url):
        driver.get(url)
        merinit.login(driver)
        #NewMer.init_page(driver)
        merinit._select_placeholder_value(driver, "请选择环境", envdata.get("env"))
        merinit._select_placeholder_value(driver, "请选择系统", "pay")
        merinit._select_placeholder_value(driver, "请选择模块名", "叶子支付")
        time.sleep(1)  # 等到前端渲染成功
        merinit._select_placeholder_value(driver, "请选择", "合作商户—>平台")
        time.sleep(1)  # 等待前端渲染成功

        # _select_input_readonly(driver, "reqbody_deviceType", data.get("设备标识"))
        merinit._select_placeholder_value(driver, "请选择接口名称", "98 - 钱包 - /member/merchant/wallet")
        #merinit._select_placeholder_value(driver, "请选择接口名称", "308 - 四方钱包 - /member/merchant/wallet")
        time.sleep(1)
        merinit._clear_then_input(driver, "reqhead_orgCode", envdata.get("机构号"))
        #merinit._clear_then_input(driver, 'reqbody_applyExternalMemberNo',"glj821z02")
        merinit._clear_then_input(driver, 'reqbody_applyExternalMemberNo',"mocklkl" + merinit.get_time_str())
        merinit._clear_then_input(driver, "reqbody_subOrgCode", envdata.get("子机构号"))

        #merinit._select_input_readonly(driver, "reqbody_merchantRole", "1")
        merinit._clear_then_input(driver, "reqbody_deviceType", envdata.get("设备标识"))
        #time.sleep(25)
        els = driver.find_elements_by_class_name("layui-btn")
        els[2].click()  # 生成请求参数
        els[3].click()  # 点击发送按钮
        # _click_link(driver,"链接跳转")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'link_skip')))
        link_addr = driver.find_element_by_id("link_skip").get_attribute("href")
        if envdata.get("env")=="pre_release":
            link_addr = link_addr.replace(".tenserpay.com", "-pre.tenserpay.xyz")
            return link_addr
        else:
            return link_addr

#!/usr/bin/python3
# encoding:utf-8
'''
Created on 2019年9月30日
@author: EDZ
'''


# class HtmlReport(unittest.TestCase):
#     def test_1(self):
#         print('test_1错误')
#         self.assertEqual(1, 2,'说明错误')
#     def test_2(self):
#         print('test_2正确')
#         self.assertEqual(1, 1)
#     def test_3(self):
#         print('test_3错误')
#         self.assertEqual(2, 3)
# if __name__=='__main__':
#     # now = time.strftime("%Y-%m-%d %H%M%S", time.localtime(time.time()))
#     # localpath = os.getcwd()
#     # print('本文件目录位置：'+localpath)
#     # filepath = os.path.join(localpath,'Report',now +'.html')
#     file_path="E:\\学习\webui_auto\\测试报告\\"
#     print('报告存放路径  ：'+file_path)
#
#     ts = unittest.TestSuite()#实例化
#     #按类加载全部testxxx测试用例
#     ts.addTest(unittest.TestLoader().loadTestsFromTestCase(HtmlReport))
#     #按函数加载testxxx测试用例
#     #ts.addTest(HtmlReport('test_1'))
#     #打开文件位置，如果没有则新建一个文件
#     filename = open(file_path,'wb')
#     htmlroport = HtmlTestRunner.HTMLTestRunner(stream=filename,title='PC开户报告',description='PC开户报告-vk-叶子',tester='虢莉君',output=file_path)
#
#     htmlroport.run(ts)
class openmer(unittest.TestCase):
    def opengerenmer(self):
        ##开个人户
        link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
        print(link_addr)
        #link_addr='https://pay-h5vk-prj.tenserpay.xyz/#/365e25365abf41e68c3faaef3c251670'

        driver.get(link_addr)

        time.sleep(10)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
        except:
            print('vk无我已准备')
        time.sleep(5)
        envtest=envdata.get("env")
        try:
            NewMer.个人商户开户(driver,envtest)
        except:
            print('开户失败')

    def opengetinmer(self):
        ##开个体户
        link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
        #link_addr='https://pay-h5vk-prj.tenserpay.xyz/#/365e25365abf41e68c3faaef3c251670'
        print(link_addr)
        driver.get(link_addr)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
        except:
            print('vk无我已准备')
        time.sleep(5)
        envtest=envdata.get("env")
        try:
            NewMer.个体商户开户(driver,envtest)
        except:
            print('开户失败')

    def  openqiyenmer(self):
        ##开企业户
        link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
        #link_addr='https://pay-pc-pre.tenserpay.xyz/#/openAccount/8daef70dd1ff4da5b41247a17e03f8c7'
        print(link_addr)
        driver.get(link_addr)

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
        except:
            print('vk无我已准备')
        time.sleep(5)
        envtest=envdata.get("env")
        NewMer.企业商户开户(driver,envtest)
        try:
            NewMer.企业商户开户(driver,envtest)
        except:
            print('开户失败')

class Baidu(unittest.TestCase):
    def setUp(self):
        '''测试准备工作'''
        self.driver = webdriver.Chrome()#初始化浏览器，注意要配置Chromedriver路径，比如：将chrome.exe放在C:\Program Files (x86)\Google\Chrome\Application路径下
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)#隐形等待，隐形等待时我们不会感觉到真的过了10秒，它会等到当前页面元素加载完毕。
        self.base_url = 'https://www.baidu.com/'

    def test_baidu_search(self):
        '''测试百度搜索'''
        self.driver.get(self.base_url)
        self.driver.find_element_by_id('kw').clear()
        self.driver.find_element_by_id('kw').send_keys('测试工程师')
        self.driver.find_element_by_id('su').click()
        time.sleep(1)# 显性等待，会明显感觉到程序等待的时间长度，比如:time.sleep(2)，会明显感觉程序等待了2秒钟。

    def tearDown(self):
        '''资源释放'''
        self.driver.quit()

if __name__ == '__main__':
    testunit = unittest.TestSuite()#初始化测试用例集合对象，构建测试套件
    for i in range(0,mernum):
        testunit.addTest(openmer("opengerenmer"))#把测试用例加入到测试用力集合中去，将用例加入到检测套件中
    fp = open('./result.html','wb')#定义测试报告存放路径
    runner =HtmlTestRunner.HTMLTestRunner(stream=fp,report_name='开户测试报告',descriptions="fdsfsf")#定义测试报告
    #HtmlTestRunner.HTMLTestRunner(report_title="",report_name='fsfs')
    runner.run(testunit)#执行测试用例
    fp.close()



# driver.save_screenshot('screenshot.png');
# driver.quit()