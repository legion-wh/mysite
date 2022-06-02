import re
import json
import os
import time
import datetime
import idcardexcell
from simple_newmerchant import  NewMer
from simple_newmerchant import  Chrome
from simple_newmerchant import merinit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
##输入环境相关信息
envdata={
    "env": "sit",##uat  sit  pre_release  release
    "机构号":"ts666",
    "子机构号":"GXVIVO", #vwork  dlvk  dhtest  tstest
 }

##开始选择开户类型，是否使用默认数据

typemer = input("请输入商户类型:1个人 2个体 3 企业 --->>  ")
typemer = int(typemer)
#typemer = 3  # 强制限制开户类型

url = "https://apitest.tenserpay.xyz/"
chrome_driver =r"F:\python3.6\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver)
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
        link_addr = driver.find_element_by_id("link_skip").get_attribute("href")
        if envdata.get("env")=="pre_release":
            link_addr = link_addr.replace(".tenserpay.com", "-pre.tenserpay.xyz")
            return link_addr
        else:
            return link_addr
link_addr=Geturl.autogeturl(driver,url)  ##自动生成请求链接
#prj
#link_addr='https://pay-h5vk-prj.tenserpay.xyz/#/365e25365abf41e68c3faaef3c251670'
##sit
#link_addr='https://pay-h5vk-sit.tenserpay.xyz/#/556111ecb5834e1ead1e74d64a956b1b'

##pre  把地址改成pre

driver.get(link_addr)



WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()

time.sleep(3)
#button

#driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮
if typemer == 1:
    # data.get("商户类型")== "个人商户"
    NewMer.个人商户开户(driver)
elif typemer == 2:
    # data3.get("商户类型") == "企业商户"
    NewMer.个体商户开户(driver, "个体")
elif typemer == 3:
    # data3.get("商户类型") == "企业商户"
    NewMer.企业商户开户(driver, "企业")
else:
    print("代码有误")

#driver.close()


# if(data.get("商户类型") == "个体商户"):
#     个体企业商户开户(driver, "个体商户")
# elif(data.get("商户类型") == "企业商户"):
#     个体企业商户开户(driver, "企业商户")
# else:
#     个人商户开户(driver)
# driver.save_screenshot('screenshot.png');
# driver.quit()