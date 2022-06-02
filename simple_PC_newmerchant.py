import re
import json
import os
import time
import datetime
import idcardexcell
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

##初始化个体开户信息
data = {
    "信用代码":"51532800000000019L",
    "商户类型":"个人商户",
    "姓名":"宋晓华",
    "身份证号":"441424198606024413",
    "商户全称":"宋晓华自动化测试有限公司",
    "商户简称":"宋晓华自动化测试",
    "银行卡号":"6225680621007084889",
    "手机号":"15818223381",
    "本地图片路径":"E:\\学习\\webui_auto\\picture\\生产\\自然人\\",
}
data1 = {
    "信用代码":"92441900MA4WNBUY8M",
    "商户类型":"个体商户",
    "姓名":"王宝文",
    "身份证号":"440301195809187517",
    "商户全称":"东莞市万江奇奇乐玩具店",
    "商户简称":"奇奇乐玩具",
    "银行卡号":"6225680621014216110",
    "手机号":"13510111831 ",
    "本地图片路径":"E:\\学习\\webui_auto\\picture\\生产\\个体\\",
}
data2 = {
    "信用代码":"91440106MA59E1YBX7",
    "商户类型":"企业商户",
    "姓名":"李志毅",
    "身份证号":"350783198605010216",
    "商户全称":"九江阿朴科技有限公司",
    "商户简称":"九江测试",
    "银行卡号":"4000104038000563346",
    "手机号":"18576651747",
    "联系人姓名": "虢莉君",
    "联系人身份证号": "421022198904123921",
    "本地图片路径":"E:\\学习\\webui_auto\\picture\\生产\\企业\\",
}
# defalutdata=input("是否使用默认数据，输入1使用默认数据，否则使用随机数据")
defalutdata = 0  # 强制使用随机数据

class merinit():
    def get_time_str():
        """
        获取当前时间戳，精确到毫秒
        :return:
        """
        return str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))


    def get_response_text(driver):
        """
        获取执行结果
        :param driver:
        :return:执行结果的文本， 交易状态
        """
        status = 0
        print("等待结果...")
        WebDriverWait(driver, 10).until(EC.title_is('请求跳转跳转'))
        print("title:", driver.title)
        reslut = EC.title_is('请求跳转跳转')(driver)
        if reslut:
            text = driver.execute_script('var txt = document.body.innerText; return txt;')  # 运用JS来获取内容值
            if (text.find("交易成功") >= 0):
                status = 1
        return status, text


    def item_generator(json_input, lookup_key):
        """
        从dict里提取指定变量的值
        :param json_input:
        :param lookup_key:
        :return:
        """
        if isinstance(json_input, dict):
            for k, v in json_input.items():  # json_input.iteritems() in Python 2, json_input.items() in Python 3
                if k == lookup_key:
                    yield v
                else:
                    for child_val in item_generator(v, lookup_key):
                        yield child_val
        elif isinstance(json_input, list):
            for item in json_input:
                for item_val in item_generator(item, lookup_key):
                    yield item_val


    def _click_link(driver, link_txt):
        for link in driver.find_elements_by_xpath("//*[@href]"):
            a = link.get_attribute('href')
            if a.find(link_txt) >= 0:
                link.click()
                break
        return True


    def _select_placeholder_value(driver, reqtext, value):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="' + reqtext + '"]'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//dd[@lay-value="' + value + '"]'))).click()


    def _select_value_value(driver, value1, value2):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="' + value1 + '"]'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//dd[@lay-value="' + value2 + '"]'))).click()


    def _input_placeholder_value(driver, placeholder, value):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="' + placeholder + '"]'))).send_keys(value)


    # 通过唯一的placeholder属性找到文本框输入文本
    def _input_placeholder_readonly(driver, placeholder, value):
        el = driver.find_element_by_xpath('//input[@placeholder="' + placeholder + '"]')
        driver.execute_script("arguments[0].removeAttribute('readonly')", el);
        el.send_keys(value)


    def _select_placeholder_value(driver, reqtext, value):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="' + reqtext + '"]'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//dd[@lay-value="' + value + '"]'))).click()

    # 通过兄弟元素查找到文本框，输入文本
    def _select_input_readonly(driver, el_name, value):  # 通过兄弟元素查找
        el = driver.find_element_by_xpath('//select[@name="' + el_name + '"]/../div/div/input')
        driver.execute_script("arguments[0].removeAttribute('readonly')", el);
        el.clear()
        el.send_keys(value)

    def _clear_then_input(driver, name, text):
        el = driver.find_element_by_name(name)
        el.clear()
        el.send_keys(text)


    def _clear_then_input_xpath(driver, el_name, name, text):
        el = driver.find_element_by_xpath('//input[@' + el_name + '="' + name + '"]')
        el.clear()
        el.send_keys(text)


    def login(driver):
        driver.find_element_by_id('username').send_keys("guolijun")  # 登录测试平台的账号
        driver.find_element_by_id('password').send_keys("123456")  # 登录测试平台的密码
        driver.find_element_by_id('login_btn').click()


    def init_page(driver):
        _select_placeholder_value(driver, "请选择环境", data.get("env"))
        _select_placeholder_value(driver, "请选择系统", "pay")
        _select_placeholder_value(driver, "请选择模块名", "叶子支付")
        time.sleep(1)  # 等到前端渲染成功
        _select_placeholder_value(driver, "请选择", "合作商户—>平台")
        time.sleep(1)  # 等待前端渲染成功
    def isElementExist(driver,element):
        flag = True
        try:
            driver.find_element_by_tag_name(element)
            return flag

        except:
            flag = False
            return flag
class dataselect:
    def nowday():
        time1 = '今年今日'
        time1=time.localtime(time.time())
        timenow=str(time1.tm_year)+'年'+str(time1.tm_mon)+'月'+str(time1.tm_mday)+'日'
        #print(str(time1))
        return timenow

    def nextyearday():
        time2 = '明年今日'
        time2 = time.localtime(time.time())
        timenextnow=str(time2.tm_year+1)+'年'+str(time2.tm_mon+1)+'月'+str(time2.tm_mday)+'日'
        return  timenextnow

# time1=dataselect.nowday()
# print(time1)
# time2=dataselect.nextyearday()
# print(time2)

class NewMer():
    ##个人商户开户流程###########################################################################
    def 个人商户开户(driver):
        # 个人商户开户(driver)
        if merinit.isElementExist(driver, "button") is True:
            driver.find_element_by_tag_name('button').click()
            # driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮
            time.sleep(3)
        zrrdata = idcardexcell.zrrinfo()
        if (defalutdata == 1):
            driver.find_element_by_id('coordinated_legalPersonName').send_keys(data.get("姓名"))
            driver.find_element_by_id('coordinated_legalPersonIdNo').send_keys(data.get("身份证号"))
            driver.find_element_by_id('coordinated_contactMobile').send_keys(data.get("手机号"))
        else:
            driver.find_element_by_id('coordinated_legalPersonName').send_keys(zrrdata[0])
            driver.find_element_by_id('coordinated_legalPersonIdNo').send_keys(zrrdata[2])
            driver.find_element_by_id('coordinated_contactMobile').send_keys(zrrdata[1])
        driver.find_element_by_id('coordinated_registeredAddress').send_keys("广东省深圳市宝安区新安街道壹方城")
        driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(data.get("本地图片路径") + "身份证正面.jpg")
        driver.find_elements_by_xpath('//input[@type="file"]')[1].send_keys(data.get("本地图片路径") + "身份证反面.jpg")
        time.sleep(3)
        driver.find_element_by_xpath('//button[text()="获取验证码"]').click()
        driver.find_element_by_id('smsCode').send_keys('666666')
        driver.find_element_by_xpath('//input[@type="checkbox"]').click()

        ##提交按钮
        driver.find_element_by_xpath('//button[@type="submit"]').click()

    def 个体商户开户(driver):

        time.sleep(5)
        try:
            driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮
        except:
            print("vk无我已准备")
        #time.sleep(2)
        # driver.find_element_by_xpath(
        #     '//*[@id="app"]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[1]/div[2]').click()
        time.sleep(2)
        driver.find_elements_by_xpath('//div[@role="tab"]')[1].click()


        time.sleep(1)
        qydata = idcardexcell.gtinfo()
        driver.find_element_by_id('coordinated_registeredAddress').send_keys("北京市东城区国际大厦1209室")
        driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(data1.get("本地图片路径") + "营业执照.jpg")
        driver.find_elements_by_xpath('//input[@type="file"]')[1].send_keys(data1.get("本地图片路径") + "身份证正面.jpg")
        driver.find_elements_by_xpath('//input[@type="file"]')[2].send_keys(data1.get("本地图片路径") + "身份证反面.jpg")
        driver.find_element_by_xpath('//span[@class="ant-cascader-picker-label"]').click()
        if (defalutdata == 1):
            driver.find_element_by_id('coordinated_merchantName').send_keys(data1.get("商户全称"))
            driver.find_element_by_id('coordinated_businessLicenseNo').send_keys(data1.get("信用代码"))
            driver.find_element_by_id('coordinated_legalPersonName').send_keys(data1.get("姓名"))
            driver.find_element_by_id('coordinated_legalPersonIdNo').send_keys(data1.get("身份证号"))
            driver.find_element_by_id('coordinated_contactMobile').send_keys(data1.get("手机号"))
        else:
            driver.find_element_by_id('coordinated_merchantName').send_keys(qydata[0])
            driver.find_element_by_id('coordinated_businessLicenseNo').send_keys(qydata[1])
            driver.find_element_by_id('coordinated_legalPersonName').send_keys(qydata[2])
            driver.find_element_by_id('coordinated_legalPersonIdNo').send_keys(qydata[4])
            driver.find_element_by_id('coordinated_contactMobile').send_keys(qydata[3])

        time.sleep(2)
        for i in driver.find_elements_by_css_selector('li'):
            if (i.text == '河北'):
                i.click()
                for i in driver.find_elements_by_css_selector('li'):
                    if (i.text == '石家庄'):
                        i.click()
                        for i in driver.find_elements_by_css_selector('li'):
                            if (i.text == '长安区'):
                                i.click()

        time.sleep(3)
        driver.find_element_by_xpath('//button[text()="获取验证码"]').click()
        driver.find_element_by_id('coordinated_smsCode').send_keys('666666')
        #driver.find_element_by_id('agreement').click()
        driver.find_element_by_xpath('//input[@type="checkbox"]').click()

        ##提交按钮
        driver.find_element_by_xpath('//button[@type="submit"]').click()

    def 企业商户开户(driver):
        if merinit.isElementExist(driver, "button") is True:
            driver.find_element_by_tag_name('button').click()
            # driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮
            time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[1]/div[3]').click()


        time.sleep(1)
        qydata = idcardexcell.qyinfo()
        driver.find_element_by_id('coordinated_registeredAddress').send_keys("北京市东城区国际大厦1209室")
        driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(data2.get("本地图片路径") + "营业执照.jpg")
        driver.find_elements_by_xpath('//input[@type="file"]')[1].send_keys(data2.get("本地图片路径") + "身份证正面.jpg")
        driver.find_elements_by_xpath('//input[@type="file"]')[2].send_keys(data2.get("本地图片路径") + "身份证反面.jpg")
        driver.find_element_by_xpath('//span[@class="ant-cascader-picker-label"]').click()
        if (defalutdata == 1):
            driver.find_element_by_id('coordinated_merchantName').send_keys(data2.get("商户全称"))
            driver.find_element_by_id('coordinated_businessLicenseNo').send_keys(data2.get("信用代码"))
            driver.find_element_by_id('coordinated_legalPersonName').send_keys(data2.get("姓名"))
            driver.find_element_by_id('coordinated_legalPersonIdNo').send_keys(data2.get("身份证号"))
            driver.find_element_by_id('coordinated_contactMobile').send_keys(data2.get("手机号"))
        else:
            driver.find_element_by_id('coordinated_merchantName').send_keys(qydata[0])
            driver.find_element_by_id('coordinated_businessLicenseNo').send_keys(qydata[1])
            driver.find_element_by_id('coordinated_legalPersonName').send_keys(qydata[2])
            driver.find_element_by_id('coordinated_legalPersonIdNo').send_keys(qydata[4])
            driver.find_element_by_id('coordinated_contactMobile').send_keys(qydata[3])

        time.sleep(2)
        for i in driver.find_elements_by_css_selector('li'):
            if (i.text == '河北'):
                i.click()
                for i in driver.find_elements_by_css_selector('li'):
                    if (i.text == '石家庄'):
                        i.click()
                        for i in driver.find_elements_by_css_selector('li'):
                            if (i.text == '长安区'):
                                i.click()

        time.sleep(3)
        driver.find_element_by_xpath('//button[text()="获取验证码"]').click()
        driver.find_element_by_id('coordinated_smsCode').send_keys('666666')
        #driver.find_element_by_id('agreement').click()
        driver.find_element_by_xpath('//input[@type="checkbox"]').click()

        ##提交按钮
        driver.find_element_by_xpath('//button[@type="submit"]').click()

##初始化个人、自然人开户信息

