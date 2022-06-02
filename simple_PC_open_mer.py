import re
import json
import os
import time
import datetime
import idcardexcell
from simple_PC_newmerchant import  NewMer
from simple_PC_newmerchant import merinit
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
    "子机构号":"GXVIVO", #dhtest  vwork dlvk
    "设备标识":"1",
 }

##开始选择开户类型，是否使用默认数据

typemer = input("请输入商户类型:1个人 2 个体 3 企业 --->>  ")
typemer = int(typemer)
#typemer = 1 # 强制限制开户类型


url = "https://apitest.tenserpay.xyz/"
chrome_driver=r"F:\python3.6\chromedriver.exe"
driver=webdriver.Chrome(executable_path=chrome_driver)
driver.get(url)
merinit.login(driver)
#init_page(driver)

merinit._select_placeholder_value(driver, "请选择环境", envdata.get("env"))
merinit._select_placeholder_value(driver, "请选择系统", "pay")
merinit._select_placeholder_value(driver, "请选择模块名", "叶子支付")
time.sleep(1)  # 等到前端渲染成功
merinit._select_placeholder_value(driver, "请选择", "合作商户—>平台")
time.sleep(1)  # 等待前端渲染成功



merinit._select_placeholder_value(driver, "请选择接口名称", "98 - 钱包 - /member/merchant/wallet")
time.sleep(1)
merinit._clear_then_input(driver, "reqhead_orgCode", envdata.get("机构号"))
merinit._clear_then_input(driver, 'reqbody_applyExternalMemberNo',"auto" + merinit.get_time_str())
merinit._clear_then_input(driver, "reqbody_subOrgCode", envdata.get("子机构号"))
merinit._clear_then_input(driver, "reqbody_deviceType", envdata.get("设备标识"))
time.sleep(2)

#_select_placeholder_value(driver, "请选择模块名", "叶子支付")
time.sleep(1)  # 等到前端渲染成功

els = driver.find_elements_by_class_name("layui-btn")
els[2].click()  # 生成请求参数
els[3].click()  # 点击发送按钮
#_click_link(driver,"链接跳转")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'link_skip')))
link_addr = driver.find_element_by_id("link_skip").get_attribute("href")
driver.get(link_addr)
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
#driver.get('https://pay-pc-prj.tenserpay.xyz/#/vwork/openAccount/7b373acb672d4d6bba8aa1e4ee9c0320')  ##直接跳转链接调试
time.sleep(6)

if typemer == 1:
     NewMer.个人商户开户(driver)
     # driver.find_element_by_xpath('//button[text()="获取验证码"]').click()
     # driver.find_element_by_id('coordinated_smsCode').send_keys('666666')
     # # id=agreement选中
     # # driver.find_element_by_id('agreement').click()
     # driver.find_element_by_xpath('//span[@class="ant-checkbox"]').click()
     # ##提交按钮
     # driver.find_element_by_xpath('//button[@type="submit"]').click()
elif typemer== 2:
    NewMer.个体商户开户(driver)
elif typemer== 3:
     NewMer.企业商户开户(driver)
     # driver.find_element_by_xpath('//button[text()="获取验证码"]').click()
     # driver.find_element_by_id('coordinated_smsCode').send_keys('666666')
     # # 选中勾选
     # driver.find_element_by_xpath('//span[@class="ant-checkbox"]').click()
     # ##提交按钮
     # time.sleep(0)
     # driver.find_element_by_xpath('//button[@type="submit"]').click()
     # driver.find_element_by_xpath('//button[@type="submit"]').click()
else:
     print("代码有误")

