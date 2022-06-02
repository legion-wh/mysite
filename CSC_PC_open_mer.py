import re
import json
import os
import time
import datetime
import unittest

import idcardexcell
from CSC_PC_newmerchant import  NewMer
from CSC_PC_newmerchant import merinit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import HtmlTestRunner
##输入环境相关信息
envdata={
    "env": "sit",##uat  sit  pre_release  release
    "机构号":"csctest",
    "子机构号":"OO108011", #GDVIVO&001
    "设备标识":"1",
    "maxmer":"1",
 }

##开始选择开户类型，是否使用默认数据

# typemer = input("请输入商户类型:1个人 2 个体 3 企业 --->>  ")
# typemer = int(typemer)
#typemer = 1 # 强制限制开户类型
##测试报告生成路径
maxmer=envdata.get("maxmer")
maxmer=int(maxmer)
url = "https://apitest.tenserpay.xyz/"
# chrome_driver=r"F:\python3.6\chromedriver.exe"
# driver=webdriver.Chrome(executable_path=chrome_driver)
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
        merinit._clear_then_input(driver, 'reqbody_applyExternalMemberNo',"csctest" + merinit.get_time_str())
        merinit._clear_then_input(driver, "reqbody_subOrgCode", envdata.get("子机构号"))

        #merinit._select_input_readonly(driver, "reqbody_merchantRole", "1")
        merinit._clear_then_input(driver, "reqbody_deviceType", envdata.get("设备标识"))
        merinit._clear_then_input(driver, "reqbody_customerId", "BC00104726")
        merinit._clear_then_input(driver, "reqbody_customerName", "湖南翼龙商务长沙市-体验店")
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





class openmer():
    def opengerenmer(self):
        ##开个人户

        link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
        print(link_addr)
        #link_addr='https://pay-pc-sit.tenserpay.xyz/#/openAccountCustomize/ea8a49bc1cfd4c838dc167bfecce49b3'

        driver.get(link_addr)

        time.sleep(5)
        try:
            driver.find_element_by_xpath('//button[@type="button"]').click()
        except:
            print('vk无我已准备')
        time.sleep(3)
        envtest=envdata.get("env")
        #NewMer.个人商户开户(driver,envtest)
        try:
            NewMer.个人商户开户(driver,envtest)
        except:
            print('开户失败')

    def opengetinmer(self):
        ##开个体户
        link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
        #link_addr='https://pay-pc-sit.tenserpay.xyz/#/openAccountCustomize/ea8a49bc1cfd4c838dc167bfecce49b3'
        print(link_addr)
        driver.get(link_addr)
        time.sleep(5)
        driver.find_element_by_xpath('//button[@type="button"]').click()
        # try:
        #     driver.find_element_by_xpath('//button[@type="button"]').click()
        # except:
        #     print('vk无我已准备')

        time.sleep(5)
        envtest=envdata.get("env")
        #NewMer.个体商户开户(driver,envtest)
        try:
            NewMer.个体商户开户(driver,envtest)
        except:
            print('开户失败')

    def  openqiyenmer(self):
        ##开企业户
        #link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
        link_addr='https://pay-pc-sit.tenserpay.xyz/#/openAccountCustomize/23d89b18cc044bda94762b7ad5f6d296'
        print(link_addr)
        driver.get(link_addr)
        time.sleep(5)
        try:
            driver.find_element_by_xpath('//button[@type="button"]').click()
        except:
            print('vk无我已准备')
        time.sleep(5)
        envtest=envdata.get("env")
        NewMer.企业商户开户(driver,envtest)
        # try:
        #     NewMer.企业商户开户(driver,envtest)
        # except:
        #     print('开户失败')


if __name__ == '__main__':

    for i in range(0,maxmer):

        print("正在开户",i)
        chrome_driver=r"F:\python3.6\chromedriver.exe"
        driver=webdriver.Chrome(executable_path=chrome_driver)
        driver.maximize_window()
        time.sleep(3)
        o = openmer()
        o.opengerenmer();##开个人
        # try:
        #     o.opengerenmer();##开个人
        #     ##o.opengetinmer();##开个体
        #     ##o.openqiyenmer();##开企业
        # except:
        #     print("开户失败,下一次开户中")
        #
        # time.sleep(5)
        #driver.close()
    print("开户完成")

    for i in range(0,maxmer):

        print("正在开户%d",i)
        chrome_driver=r"F:\python3.6\chromedriver.exe"
        driver=webdriver.Chrome(executable_path=chrome_driver)
        driver.maximize_window()
        time.sleep(3)
        o = openmer()
        o.opengetinmer();
        try:
            #o.opengerenmer();##开个人
            o.opengetinmer();##开个体
            ##o.openqiyenmer();##开企业
        except:
            print("开户失败,下一次开户中")

        time.sleep(5)
        driver.close()
    print("开户完成")
    for i in range(0,maxmer):

        print("正在开户%d",i)
        chrome_driver=r"F:\python3.6\chromedriver.exe"
        driver=webdriver.Chrome(executable_path=chrome_driver)
        driver.maximize_window()
        time.sleep(3)
        o = openmer()
        o.openqiyenmer();##开企业
        # try:
        #     #o.opengerenmer();##开个人
        #     ##o.opengetinmer();##开个体
        #     o.openqiyenmer();##开企业
        # except:
        #     print("开户失败,下一次开户中")

        time.sleep(5)
        driver.close()
    print("开户完成")
        #openmer.opengetinmer(self);
        #openmer.openqiyenmer(self);
# if(data.get("商户类型") == "个体商户"):
#     个体企业商户开户(driver, "个体商户")
# elif(data.get("商户类型") == "企业商户"):
#     个体企业商户开户(driver, "企业商户")
# else:
#     个人商户开户(driver)
# driver.save_screenshot('screenshot.png');
# driver.quit()