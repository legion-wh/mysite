import re
import json
import os
import time
import datetime
import idcardexcell
from newmerchant import  NewMer
from newmerchant import  Chrome
from newmerchant import merinit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
##输入环境相关信息
envdata={
    "env": "release",##uat  sit  pre_release  release
    "机构号":"ts666",
    "子机构号":"", #GDVIVO&001
 }
filePathdir='C:\\Users\\60007861.TS\\Desktop\\V3.2.1ocr\\ocr_auto\\ocr\\'
##开始选择开户类型，是否使用默认数据

typemer = input("请输入商户类型:1个人 2 个体 3 企业 --->>  ")
typemer = int(typemer)
#typemer = 3  # 强制限制开户类型

url = "https://apitest.tenserpay.xyz/"
#chrome_driver =r"F:\python3.6\chromedriver.exe"
#driver = webdriver.Chrome(executable_path=chrome_driver)
#driver.close()
# driver.get(url)
# merinit.login(driver)
class Geturl():
    def autogeturl(driver,url):
        chrome_driver =r"F:\python3.6\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver)
        driver.get(url)
        merinit.login(driver)
        merinit._select_placeholder_value(driver, "请选择环境", envdata.get("env"))
        merinit._select_placeholder_value(driver, "请选择系统", "pay")
        merinit._select_placeholder_value(driver, "请选择模块名", "叶子支付")
        time.sleep(1)  # 等到前端渲染成功
        merinit._select_placeholder_value(driver, "请选择", "合作商户—>平台")
        time.sleep(1)  # 等待前端渲染成功

        # _select_input_readonly(driver, "reqbody_deviceType", data.get("设备标识"))
        merinit._select_placeholder_value(driver, "请选择接口名称", "98 - 钱包 - /member/merchant/wallet")
        time.sleep(1)
        merinit._clear_then_input(driver, "reqhead_orgCode", envdata.get("机构号"))
        #merinit._clear_then_input(driver, 'reqbody_applyExternalMemberNo',"glj821z02")
        merinit._clear_then_input(driver, 'reqbody_applyExternalMemberNo',"mocklkl" + merinit.get_time_str())
        merinit._clear_then_input(driver, "reqbody_subOrgCode", envdata.get("子机构号"))

        merinit._select_input_readonly(driver, "reqbody_merchantRole", "1")
        # _select_input_readonly(driver, "reqbody_deviceType", data.get("设备标识"))

        els = driver.find_elements_by_class_name("layui-btn")
        els[2].click()  # 生成请求参数
        els[3].click()  # 点击发送按钮
        # _click_link(driver,"链接跳转")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'link_skip')))
        time.sleep(2)
        link_addr = driver.find_element_by_id("link_skip").get_attribute("href")
        if envdata.get("env")=="pre_release":
            link_addr = link_addr.replace(".tenserpay.com", "-pre.tenserpay.xyz")
            return link_addr
        else:
            return link_addr
        driver.close()

#
# link_addr='https://pay-h5vk-sit.tenserpay.xyz/#/6ee7ab8965964389b459208a9b162129'
#
# driver.get(link_addr)
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()

chrome_driver =r"F:\python3.6\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver)

#filePath=filePathdir+'营业执照\\可识别\\'
filePath=filePathdir+'身份证正面\\可识别\\'
fileimges=os.listdir(filePath)
fileimge=fileimges[1]
if typemer == 1:
    link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
    print(link_addr)
    #link_addr='https://pay-h5vk-prj.tenserpay.xyz/#/365e25365abf41e68c3faaef3c251670'
    # chrome_driver =r"F:\python3.6\chromedriver.exe"


    # driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(link_addr)

    time.sleep(10)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
    except:
        print('vk无我已准备')
    time.sleep(5)
    envtest=envdata.get("env")
    try:
        filePath=filePathdir+'身份证正面\\可识别\\'
        fileimges=os.listdir(filePath)
        fileimge=fileimges[1]
        NewMer.个人商户开户(driver,filePath,fileimge)
    except Exception as e:
        print('开户失败')
        print(e)

elif typemer == 2:
    link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
    #link_addr='https://pay-h5vk-prj.tenserpay.xyz/#/365e25365abf41e68c3faaef3c251670'
    print(link_addr)
    driver.get(link_addr)
    filePath=filePathdir+'营业执照\\可识别\\'
    fileimges=os.listdir(filePath)
    fileimge=fileimges[1]
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
    except:
        print('vk无我已准备')
    time.sleep(5)
    envtest=envdata.get("env")
    try:
        NewMer.个体商户开户(driver,filePath,fileimge)
    except Exception as e:
        print('开户失败')
        print(e)

elif typemer== 3:
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

    try:

        filePath=filePathdir+'营业执照\\可识别\\'
        fileimges=os.listdir(filePath)
        fileimge=fileimges[1]
        NewMer.企业商户开户(driver,filePath,fileimge)
    except Exception as e:
        print('开户失败')
        print(e)
else:
    print("代码有误")

# driver.close()

##根据身份证图片数量，开多少账户
# filePath2=filePathdir+'身份证正面\\可识别\\'
# fileimges2=os.listdir(filePath2)
# for fileimge2 in fileimges2:
#     link_addr=Geturl.autogeturl(driver,url)
#     print(link_addr)
#     print(fileimge2)
#     time.sleep(10)
#     chrome_driver =r"D:\python3.8\chromedriver.exe"
#     driver = webdriver.Chrome(executable_path=chrome_driver)
#     driver.get(link_addr)
#
#     #time.sleep(10)
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
#
#     NewMer.个人商户开户(driver,filePath2,fileimge2)
#
#     driver.close()

# ##根据营业执照数量，开多少账户  个体
# filePath=filePathdir+'营业执照\\可识别\\'
# fileimges=os.listdir(filePath)
# for fileimge in fileimges:
#     link_addr=Geturl.autogeturl(driver,url)
#     #driver.close()
#     print(link_addr)
#     print(fileimge)
#     time.sleep(2)
#     chrome_driver =r"F:\python3.6\chromedriver.exe"
#     driver = webdriver.Chrome(executable_path=chrome_driver)
#
#     driver.get(link_addr)
#
#     time.sleep(10)
#
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
#     #NewMer.个体商户开户(driver,filePath,fileimge)
#     try:
#         NewMer.个体商户开户(driver,filePath,fileimge)
#         #NewMer.企业商户开户(driver,filePath,fileimge)
#     except:
#         print('识别失败')
# #    NewMer.企业商户开户(driver,filePath,fileimge)
#     time.sleep(5)
#     #driver.close()

# if(data.get("商户类型") == "个体商户"):
#     个体企业商户开户(driver, "个体商户")
# elif(data.get("商户类型") == "企业商户"):
#     个体企业商户开户(driver, "企业商户")
# else:
#     个人商户开户(driver)
# driver.save_screenshot('screenshot.png');
#driver.quit()