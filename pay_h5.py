import re
import json
import os,sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Chrome():

    def initDriver(self, linux = False):
        options = Options()
        if(linux == True):
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("window-size=1024,768")
        options.add_argument("--no-sandbox")
        print("test...");
        print(sys.path[0]);
        driver = webdriver.Chrome(sys.path[0]+'/chromedriver',chrome_options=options)
#        driver.maximize_window()
        return  driver

def get_time_str():
    """
    获取当前时间戳，精确到毫秒
    :return:
    """
    return str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

def item_generator(json_input, lookup_key):
    """
    从dict里提取指定变量的值
    :param json_input:
    :param lookup_key:
    :return:
    """
    if isinstance(json_input, dict):
        for k, v in json_input.items():  #json_input.iteritems() in Python 2, json_input.items() in Python 3
            if k == lookup_key:
                yield v
            else:
                for child_val in item_generator(v, lookup_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_key):
                yield item_val

def _click_link(driver,link_txt):
    for link in driver.find_elements_by_xpath("//*[@href]"):
        a = link.get_attribute('href')
        if a.find(link_txt) >= 0:
            link.click()
            break
    return True

def _get_screenshot(driver):
    driver.get_screenshot_as_file(sys.path[0] + '/screenshots/' + str(int(time.time())) + ".png")
#接口测试平台选择接口
def _select_placeholder_value(driver, reqtext, value):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="'+reqtext+'"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//dd[@lay-value="'+value+'"]'))).click()
    _get_screenshot(driver)

def _select_value_value(driver, value1, value2):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="'+value1+'"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//dd[@lay-value="'+value2+'"]'))).click()
    _get_screenshot(driver)

def _input_placeholder_value(driver, placeholder, value):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="' +placeholder+ '"]'))).send_keys(value)
    _get_screenshot(driver)

#通过唯一的placeholder属性找到文本框输入文本
def _input_placeholder_readonly(driver, placeholder, value):
    el = driver.find_element_by_xpath('//input[@placeholder="'+placeholder+'"]')
    driver.execute_script("arguments[0].removeAttribute('readonly')", el);
    el.send_keys(value)
    _get_screenshot(driver)

def _clear_then_input_placeholder_readonly(driver, placeholder, value):
    el = driver.find_element_by_xpath('//input[@placeholder="' + placeholder + '"]')
    _get_screenshot(driver)

#通过兄弟元素查找到文本框，输入文本
def _select_input_readonly(driver, el_name, value):  #通过兄弟元素查找
    el = driver.find_element_by_xpath('//select[@name="'+el_name+'"]/../div/div/input')
    driver.execute_script("arguments[0].removeAttribute('readonly')", el);
    el.clear()
    el.send_keys(value)
    _get_screenshot(driver)

def _clear_then_input(driver,name, text ):
    el = driver.find_element_by_name(name)
    el.clear()
    el.send_keys(text)
    _get_screenshot(driver)

def _clear_then_input_xpath(driver,el_name,name, text ):
    el = driver.find_element_by_xpath('//input[@'+el_name+'="'+name+'"]')
    el.clear()
    el.send_keys(text)
    _get_screenshot(driver)

#滑动列表，选择省份、市、区
def _select_province_city_block(driver, addr,text):
    path = '//*[@tab="'+addr+'"]'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, path)))
    flag = False
    locator = (By.XPATH, "//p[contains(text(),'"+text+"')]")
    while(flag == False):
        try:
            WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located(locator)).click()
            flag = True
        except:
            els = driver.find_elements_by_css_selector('p')
            print("元素个数",len(els))
            cop = els[:]
            for i in els:
                if(i.text == ""):
                    cop.remove(i)
            js = "arguments[0].scrollIntoView();"
            driver.execute_script(js, cop[len(cop)-3])  #超出不可见范围会报异常
            ActionChains(driver).drag_and_drop_by_offset(cop[len(cop)-1], 50, 300).perform()
            flag = False;

def login(driver):
    time.sleep(1)
    driver.find_element_by_id('username').send_keys("yidan")
    print(1)
    driver.find_element_by_id('password').send_keys("xxxx")
    print(2)
    driver.find_element_by_id('login_btn').click()
    print(3)
    _get_screenshot(driver)

def init_page(driver):
    _select_placeholder_value(driver, "请选择环境", data.get("env"))
    _select_placeholder_value(driver, "请选择系统", "pay")
    _select_placeholder_value(driver, "请选择模块名", "叶子支付")
    time.sleep(1)  # 等到前端渲染成功
    _select_placeholder_value(driver, "请选择", "合作商户—>平台")
    time.sleep(1)  # 等待前端渲染成功
    _get_screenshot(driver)


##个人商户开户流程###########################################################################
def 个人商户开户(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='个人商户']"))).click()
    driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮

    _input_placeholder_value(driver, "请输入经营者姓名", data.get("姓名"))
    _input_placeholder_value(driver, "请输入商户简称", data.get("商户简称")+str(int(time.time())))
#    _input_placeholder_readonly(driver,"请选择省、市、区","北京 东城区")
    driver.find_element_by_xpath('//input[@placeholder="请选择省、市、区"]').click()
    _select_province_city_block(driver, "province", "广东")
    _select_province_city_block(driver, "city", "云浮")
    _select_province_city_block(driver, "block", "罗定市")
    time.sleep(1)
    _input_placeholder_value(driver, "请输入详细地址","北京市东城区国际大厦1209室")
    _clear_then_input_placeholder_readonly(driver, "请选择省、市、区", "北京 东城区")
    _input_placeholder_value(driver, "请输入商户客服联系电话","0755666")
    _input_placeholder_value(driver, "请输入邮箱","123@qq.com")
    #driver.find_elements_by_class_name("md-image-reader")[1] #上传门店门头照
    time.sleep(1)
    el = driver.find_elements_by_class_name("md-image-reader-file")[1]
    el.send_keys(data.get("本地图片路径")+"门面照.jpg")
    el = driver.find_elements_by_class_name("md-image-reader-file")[2]
    el.send_keys(data.get("本地图片路径")+"内景照.jpg")
    time.sleep(2)
    driver.find_element_by_tag_name("button").click();

    #填写法人信息
    _input_placeholder_value(driver, "请输入法人代表姓名",data.get("姓名"))
    _input_placeholder_value(driver, "请输入法人代表身份证号",data.get("身份证号"))
    driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(data.get("本地图片路径")+"身份证正面.jpg")
    driver.find_elements_by_xpath('//input[@type="file"]')[1].send_keys(data.get("本地图片路径")+"身份证反面.jpg")
    driver.find_element_by_xpath('//input[@placeholder="请选择有效期"]').click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='长期有效']"))).click()
    _input_placeholder_readonly(driver,"请选择起始日期","2020-02-02")
#    _input_placeholder_readonly(driver,"请选择结束日期","2030-02-01")
    driver.find_element_by_tag_name("button").click();
    time.sleep(1)
    print("机构号：")
    print(data.get("机构号"))
    if(data.get("机构号") == 'ts666'):
        _input_placeholder_value(driver, "请输入本人银行卡号",data.get("银行卡号"))
    else:
        _input_placeholder_value(driver, "请输入账户号", data.get("银行卡号"))
    driver.find_element_by_xpath('//input[@placeholder="请输入银行名称"]').click()
    _input_placeholder_value(driver, "请输入银行预留手机号码", data.get("手机号"))
    _input_placeholder_value(driver,"请输入验证码","666666")
    el = driver.find_elements_by_tag_name('button')
    el[0].click()  # 发送短信按钮
 #   el[1].click()  #提交按钮

##个体跟企业商户开户流程###########################################################################
def 个体企业商户开户(driver, type):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='"+type+"']"))).click()
    driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮

    _input_placeholder_value(driver, "请输入营业执照上的名称", data.get("商户全称"))
    _input_placeholder_value(driver, "请输入商户简称", data.get("商户简称")+str(int(time.time())))
    _input_placeholder_value(driver, "请输入统一社会信用代码", data.get("信用代码"))
    if(type == '企业商户'):
        _input_placeholder_readonly(driver, "请选择营业执照类型", "个体")

    driver.find_element_by_xpath('//input[@placeholder="请选择省、市、区"]').click()
    _select_province_city_block(driver,"province","广东")
    _select_province_city_block(driver,"city","云浮")
    _select_province_city_block(driver, "block", "罗定市")

    _input_placeholder_value(driver, "请输入详细地址", "爱国大厦1001室")
    #_input_placeholder_value(driver, "请输入商户客服联系电话", "075566")
    _input_placeholder_value(driver, "请输入邮箱", "123@qq.com")
    els = driver.find_elements_by_xpath('//input[@type="file"]')
    els[0].send_keys(
        data.get("本地图片路径")+"营业执照.jpg")
    _input_placeholder_readonly(driver, "请选择起始日期", "2020-02-02")
    _input_placeholder_readonly(driver,"请选择结束日期","2030-02-01")
    els[1].send_keys(
        data.get("本地图片路径")+"门面照.jpg")
    els[2].send_keys(
        data.get("本地图片路径")+"内景照.jpg")
    time.sleep(2)


    driver.find_element_by_tag_name('button').click()  # 下一步 按钮

    # 填写法人信息
    _input_placeholder_value(driver, "请输入法人代表姓名", data.get("姓名"))
    _input_placeholder_value(driver, "请输入法人代表身份证号", data.get("身份证号"))
    els = driver.find_elements_by_xpath('//input[@type="file"]')
    els[0].send_keys(
        data.get("本地图片路径")+"身份证正面.jpg")
    els[1].send_keys(
        data.get("本地图片路径")+"身份证反面.jpg")
    driver.find_element_by_xpath('//input[@placeholder="请选择有效期"]').click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='长期有效']"))).click()
    _input_placeholder_readonly(driver, "请选择起始日期", "2020-02-02")
    #    _input_placeholder_readonly(driver,"请选择结束日期","2030-02-01")
    driver.find_element_by_tag_name('button').click()  # 下一步 按钮

    # 填写结算账户
    if (type == '企业商户'):
        _input_placeholder_value(driver, "请输入银行账号", data.get("银行卡号"))
        _input_placeholder_readonly(driver, "请选择开户银行", "中国农业银行")
        driver.find_element_by_xpath('//input[@placeholder="请选择开户银行"]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="md-cell-item-title"]').click()
        time.sleep(1)
#        _input_placeholder_readonly(driver, "请选择开户支行", "北京")
        driver.find_element_by_xpath('//input[@placeholder="请选择开户支行"]').click()
        _select_province_city_block(driver,"province","广东")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@tab="city"]'))).click()
#        _input_placeholder_readonly(driver, "请选择支行名称", "***")
        driver.find_element_by_xpath('//input[@placeholder="请选择支行名称"]').click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//li'))).click()
        time.sleep(1)
        driver.find_element_by_xpath('//input[@type="file"]').send_keys(
        data.get("本地图片路径")+"身份证正面.jpg")
        _input_placeholder_value(driver,"请输入姓名",data.get("姓名"))
        _input_placeholder_value(driver,"请输入联系人手机号码",data.get("手机号"))
        _input_placeholder_value(driver, "请输入联系人身份证号码", data.get("身份证号"))
    else:
        if (data.get("机构号") == 'ts666'):
            _input_placeholder_value(driver, "请输入本人银行卡号", data.get("银行卡号"))
        else:
            _input_placeholder_value(driver, "请输入账户号", data.get("银行卡号"))
        _input_placeholder_value(driver, "请输入银行预留手机号码", data.get("手机号"))
    _input_placeholder_value(driver, "请输入验证码", "666666")
    el = driver.find_elements_by_tag_name('button')
    el[0].click()  #发送短信按钮
#    el[1].click()  #提交按钮


data = {
    "env": "uat", #uat ,pre_release
    "机构号":"ts666",
    "外部商户号":"usernamedot0078",
    "商户角色":"2",  #1:代理商;2:经销商
    "设备标识":"0",  #0:h5, 1:pc
    "信用代码":"91533867000000019Y",
    "商户类型":"企业商户",
    "姓名":"秘请·誉伍",
    "身份证号":"520112198004084192",
    "商户全称":"一点点测试商户",
    "商户简称":"一点点",
    "银行卡号":"6222022868275200945",
    "手机号":"13510798562",
    "本地图片路径":sys.path[0]+"/picture/",
}


url = "https://apitest.tenserpay.xyz/"
chrome = Chrome()
driver = chrome.initDriver()
driver.get(url)
login(driver)
init_page(driver)

_select_placeholder_value(driver, "请选择接口名称", "98 - 钱包 - /member/merchant/wallet")
time.sleep(1)
_clear_then_input(driver, "reqhead_orgCode",data.get("机构号"))
_clear_then_input(driver,'reqbody_applyExternalMemberNo',data.get("外部商户号"))

_select_input_readonly(driver,"reqbody_merchantRole",data.get("商户角色"))
_clear_then_input(driver,'reqbody_deviceType',data.get("设备标识"))
#_clear_then_input(driver, "reqbody_subOrgCode", "GDVIVO")

els = driver.find_elements_by_class_name("layui-btn")
els[2].click()  #生成请求参数
els[3].click()  #点击发送按钮
#_click_link(driver,"链接跳转")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'link_skip')))
link_addr = driver.find_element_by_id("link_skip").get_attribute("href")
print(link_addr)
link_addr = link_addr.replace(".tenserpay.com", "-pre.tenserpay.xyz")
print(link_addr)
driver.get(link_addr)
#WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.XPATH, "//*[text()='开通聚合支付']"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button'))).click()
if(data.get("商户类型") == "个体商户"):
    个体企业商户开户(driver, "个体商户")
elif(data.get("商户类型") == "企业商户"):
    print(data.get("商户类型"))
    个体企业商户开户(driver, "企业商户")
else:
    个人商户开户(driver)
