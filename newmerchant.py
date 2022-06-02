import re
import json
import os
import time
import datetime
import idcardexcell
import random
#from newmermodule import global_vars
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
##初始化开户信息
data = {
    "外部商户号":"autogr-",
    "商户角色":"2",  #1:代理商;2:经销商
    "设备标识":"0",  #0:h5, 1:pc
    "信用代码":"51532800000000019L",
    "商户类型":"个人商户",
    "姓名":"樱瓦绑",
    "身份证号":"42707619940903615X",
    "商户全称":"樱瓦绑自动化测试有限公司",
    "商户简称":"樱瓦绑自动化测试",
    "银行卡号":"6222020502022187509",
    "手机号":"13001062868",##13001062868
    "本地图片路径":"E:\\学习\\webui_auto\\picture\\",
}
data2 = {
    "外部商户号":"autogt-",
    "商户角色":"2",  #1:代理商;2:经销商
    "设备标识":"0",  #0:h5, 1:pc
    "信用代码":"92441900MA4WNBUY8M",
    "商户类型":"个体商户",
    "姓名":"王宝文",
    "身份证号":"440301195809187517",
    "商户全称":"东莞市万江奇奇乐玩具店",
    "商户简称":"奇奇乐玩具",
    "银行卡号":"6225680621014216110",
    "手机号":"13510111831 ",
    "本地图片路径":"E:\\学习\\webui_auto\\picture\\",
}
data3 = {
    "外部商户号":"autoqy-",
    "商户角色":"2",  #1:代理商;2:经销商
    "设备标识":"0",  #0:h5, 1:pc
    "信用代码":"91310104MA1FRGLY50",
    "商户类型":"企业商户",
    "姓名":"施玉坚",
    "身份证号":"155775199607070150",
    "商户全称":"上海维勉通信科技有限公司",#重庆维沃软件技术有限公司
    "商户简称":"上海维勉通信科技有限公司",
    "银行卡号":"6222080502001639634",
    "手机号":"13002244144",
    "本地图片路径":"E:\\学习\\webui_auto\\picture\\",
}


# defalutdata=input("是否使用默认数据，输入1使用默认数据，否则使用随机数据")
defalutdata = 0  # 强制使用随机数据
filePathdir='C:\\Users\\60007861.TS\\Desktop\\V3.2.1ocr\\ocr_auto\\ocr\\'
class Chrome():

    def initDriver(self):
        options = Options()
        #        options.add_argument('--headless')
        #        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome(chrome_options=options)
        return driver

    def deleteAllCerts(self, driver, url):
        """
        删除已有的证书
        """
        driver.get(url + 'newpay/applypersoncert_input.jsp')
        script = """
            function deleteAllCerts() {
                var certs = CertStore.listAllCerts();
                if (certs.size() > 0) {
                    for (var i = 0; i < certs.size(); i++) {
                        var cert = certs.get(i);
                        cert.deleteCert();
                        console.log('delete one cert')
                    }
                } else {
                }
            }

            function getCertsSize() {
                return CertStore.listAllCerts().size()
            }

            deleteAllCerts();
            return getCertsSize();
        """
        print('remaining certs size:' + str(driver.execute_script(script)))
        return

    # driver.close()

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
        driver._select_placeholder_value(driver, "请选择环境", envdata.get("env"))
        driver._select_placeholder_value(driver, "请选择系统", "pay")
        driver._select_placeholder_value(driver, "请选择模块名", "叶子支付")
        time.sleep(1)  # 等到前端渲染成功
        driver._select_placeholder_value(driver, "请选择", "合作商户—>平台")
        time.sleep(1)  # 等待前端渲染成功
        driver._select_placeholder_value(driver, "请选择接口名称", "98 - 钱包 - /member/merchant/wallet")
        time.sleep(1)
        driver._clear_then_input(driver, "reqhead_orgCode", envdata.get("机构号"))
        driver._clear_then_input(driver, 'reqbody_applyExternalMemberNo', data.get("外部商户号") + get_time_str())
        driver._clear_then_input(driver, "reqbody_subOrgCode", envdata.get("子机构号"))
        driver._select_input_readonly(driver, "reqbody_merchantRole", data.get("商户角色"))
        # _select_input_readonly(driver, "reqbody_deviceType", data.get("设备标识"))

    def isElementExist(driver,element):
        flag = True
        try:
            driver.find_element_by_css_selector(element)
            return flag

        except:
            flag = False
            return flag

class NewMer():
    ##个人商户开户流程###########################################################################
    def 个人商户开户(driver,filePath,fileimge):
        time.sleep(3)
        for i in driver.find_elements_by_css_selector('dd'):
            if (i.text == '个人商户'):
                i.click()
        driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮
        zrrdata = idcardexcell.zrrinfo()
        if (defalutdata == 1):
            merinit._input_placeholder_value(driver, "请输入经营者姓名",data.get("姓名"))
            #merinit._input_placeholder_value(driver, "请输入商户简称", data.get("商户简称"))
            merinit._input_placeholder_value(driver, "请输入商户简称", "拉卡拉测试")
        else:
            merinit._input_placeholder_value(driver, "请输入经营者姓名", zrrdata[0])
            #merinit._input_placeholder_value(driver, "请输入商户简称", zrrdata[0])
            merinit._input_placeholder_value(driver, "请输入商户简称", "拉卡拉测试")

        merinit._input_placeholder_readonly(driver, "请选择省、市、区", "河北 秦皇岛 海港区")
        driver.find_element_by_xpath('//input[@placeholder="请选择省、市、区"]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/p').click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/p').click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/div[1]/div/div[1]/p').click()
        merinit._input_placeholder_value(driver, "请输入详细地址", "北京市东城区国际大厦1209室")
        #merinit._input_placeholder_value(driver, "请输入商户客服联系电话", "0755666")
        merinit._input_placeholder_value(driver, "请输入邮箱", "123@qq.com")
        # driver.find_elements_by_class_name("md-image-reader")[1] #上传门店门头照
        time.sleep(1)
        el = driver.find_elements_by_class_name("md-image-reader-file")[0]
        el.send_keys(data.get("本地图片路径") + "门面照.jpg")
        el = driver.find_elements_by_class_name("md-image-reader-file")[1]
        el.send_keys(data.get("本地图片路径") + "内景照.jpg")
        time.sleep(2)
        driver.find_element_by_tag_name("button").click();

        # 填写法人信息
        time.sleep(2)
        # if (defalutdata == 1):
        #     merinit._input_placeholder_value(driver, "请输入法人代表姓名", data.get("姓名"))
        #     merinit._input_placeholder_value(driver, "请输入法人代表身份证号", data.get("身份证号"))
        # else:
        #     merinit._input_placeholder_value(driver, "请输入法人代表姓名", zrrdata[0])
        #     merinit._input_placeholder_value(driver, "请输入法人代表身份证号", zrrdata[2])
        driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(filePath+fileimge)
        time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'md-dialog-btn'))).click()
            # WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, 'quarter-content'))).click()
        except:
            print("没有上传成功")
        #driver.find_elements_by_xpath('//input[@type="file"]')[1].send_keys(data.get("本地图片路径") + "身份证反面.jpg")
        
        # driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(data.get("本地图片路径") + "身份证正面.jpg")
        time.sleep(5)
        driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(data.get("本地图片路径") + "身份证反面.jpg")
        time.sleep(5)
        driver.find_element_by_xpath('//a[@class="md-dialog-btn"]').click()
        #time.sleep(5)
        # try:
        #     WebDriverWait(driver, 15).until(
        #         EC.element_to_be_clickable((By.CLASS_NAME, 'md-dialog-btn'))).click()
        #     # WebDriverWait(driver, 10).until(
        #     #     EC.element_to_be_clickable((By.CLASS_NAME, 'quarter-content'))).click()
        # except:
        #     print("没有上传成功")
        time.sleep(5)
        # merinit._input_placeholder_readonly(driver, "请选择起始日期", "2020-02-02")
        # merinit._input_placeholder_readonly(driver, "请选择结束日期", "2030-02-01")
        driver.find_element_by_tag_name("button").click();
        if (defalutdata == 1):
            merinit._input_placeholder_value(driver, "请输入账户号", data.get("银行卡号"))
            driver.find_element_by_xpath('//input[@placeholder="请输入银行名称"]').click()
            merinit._input_placeholder_value(driver, "请输入银行预留手机号码", data.get("手机号"))
        else:
            #if merinit.isElementExist(driver, "请输入账户号") is True:
            #banknoele = driver.find_element_by_xpath('//input[@placeholder="请输入账户号"]')
            #merinit._input_placeholder_value(driver, "请输入本人银行卡号", zrrdata[3])
            #merinit._input_placeholder_value(driver, "请输入账户号", zrrdata[3])
            merinit._input_placeholder_value(driver, "请输入账户号", data.get("银行卡号"))
            driver.find_element_by_xpath('//input[@placeholder="请输入本人银行卡号"]').click()
            merinit._input_placeholder_value(driver, "请输入银行预留手机号码", zrrdata[1])

        el = driver.find_elements_by_tag_name('button')
        el[0].click()  # 发送短信按钮
        time.sleep(1)
        merinit._input_placeholder_value(driver, "请输入验证码", "666666")

#        driver.find_element_by_tag_name('button').click()  # 下一步
        el[1].click()  # 提交按钮
        time.sleep(5)

    def 个体商户开户(driver,filePath,fileimge):
        time.sleep(5)
        for i in driver.find_elements_by_css_selector('dd'):
            if (i.text == '个体商户'):
                i.click()
        driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮
        ##上传营业执照
        time.sleep(5)
        driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(filePath+fileimge)
        time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'md-dialog-btn'))).click()
            # WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, 'quarter-content'))).click()
        except:
            print("没有上传成功")
            # merinit._input_placeholder_readonly(driver, "请选择起始日期", "2020-02-02")
        # merinit._input_placeholder_readonly(driver, "请选择结束日期", "2030-02-01")
        gtdata = idcardexcell.gtinfo()
        merinit._input_placeholder_value(driver, "请输入商户简称", "拉卡拉测试")

        merinit._input_placeholder_readonly(driver, "请选择省、市、区", "河北 秦皇岛 海港区")
        driver.find_element_by_xpath('//input[@placeholder="请选择省、市、区"]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/p').click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/p').click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/div[1]/div/div[1]/p').click()
        ##ocr自动识别
        # if (defalutdata == 1):
        #     merinit._input_placeholder_value(driver, "请输入营业执照上的名称", data2.get("商户全称"))
        #     merinit._input_placeholder_value(driver, "请输入统一社会信用代码", data2.get("信用代码"))
        # else:
        #     merinit._input_placeholder_value(driver, "请输入营业执照上的名称", gtdata[0])
        #     merinit._input_placeholder_value(driver, "请输入统一社会信用代码", gtdata[1])
        # merinit._input_placeholder_value(driver, "请输入详细地址", "广东省深圳市宝安区")
        #merinit._input_placeholder_value(driver, "请输入商户客服联系电话", "07552314256")
        merinit._input_placeholder_value(driver, "请输入邮箱", "guoljwh@163.com")
        els = driver.find_elements_by_xpath('//input[@type="file"]')

        els[0].send_keys(
            data2.get("本地图片路径") + "门面照.jpg")
        els[1].send_keys(
            data2.get("本地图片路径") + "内景照.jpg")
        time.sleep(5)
        driver.find_element_by_tag_name('button').click()  # 下一步 按钮
        time.sleep(5)
        try:
            merinit._input_placeholder_value(driver, "请输入营业执照上的名称","拉卡拉测试有限公司")
            driver.find_element_by_tag_name('button').click()  # 下一步 按钮
        except:
            print("识别成功")

        # 填写法人信息
        filePathfront=filePathdir+'身份证正面\\可识别\\'
        fileimgefronts=os.listdir(filePathfront)
        fileimgefront=random.choice(fileimgefronts)

        time.sleep(5)
        els = driver.find_elements_by_xpath('//input[@type="file"]')
        els[0].send_keys(filePathfront+fileimgefront)
        time.sleep(10)
        driver.find_element_by_xpath('//a[@class="md-dialog-btn"]').click()
        time.sleep(5)
        filePathback=filePathdir+'身份证反面\\可识别\\'
        fileimgebacks=os.listdir(filePathback)
        fileimgeback=random.choice(fileimgebacks)
        els[1].send_keys(filePathback+fileimgeback)            
        time.sleep(5)
        driver.find_element_by_xpath('//a[@class="md-dialog-btn"]').click()
        ##ocr自动识别
        # if (defalutdata == 1):
        #     merinit._input_placeholder_value(driver, "请输入法人代表姓名", data2.get("姓名"))
        #     merinit._input_placeholder_value(driver, "请输入法人代表身份证号", data2.get("身份证号"))
        # else:
        #     merinit._input_placeholder_value(driver, "请输入法人代表姓名", gtdata[2])
        #     merinit._input_placeholder_value(driver, "请输入法人代表身份证号", gtdata[4])
        # merinit._input_placeholder_readonly(driver, "请选择起始日期", "2020-02-02")
        # merinit._input_placeholder_readonly(driver, "请选择结束日期", "2030-02-01")
        driver.find_element_by_tag_name('button').click()  # 下一步 按钮

        ##输入银行信息
        if (defalutdata == 1):
            #merinit._input_placeholder_value(driver, "请输入账户号", data2.get("银行卡号"))
            merinit._input_placeholder_value(driver, "请输入账户号", data2.get("银行卡号"))
            driver.find_element_by_xpath('//input[@placeholder="请输入银行名称"]').click()
            merinit._input_placeholder_value(driver, "请输入银行预留手机号码", data2.get("手机号"))
        else:
            #merinit._input_placeholder_value(driver, "请输入账户号", data2.get("银行卡号"))
            #merinit._input_placeholder_value(driver, "请输入账户号", gtdata[5])
            merinit._input_placeholder_value(driver, "请输入本人银行卡号", gtdata[5])
            driver.find_element_by_xpath('//input[@placeholder="请输入银行名称"]').click()
            merinit._input_placeholder_value(driver, "请输入银行预留手机号码", gtdata[3])
        # merinit._input_placeholder_value(driver, "请输入验证码", "666666")
        # el = driver.find_elements_by_tag_name('button')
        # el[0].click()  # 发送短信按钮
        # #    driver.find_element_by_tag_name('button').click()  # 下一步
        # el[1].click()  # 提交按钮
        # time.sleep(5)


    def 企业商户开户(driver, filePath,fileimge):
        time.sleep(5)
        for i in driver.find_elements_by_css_selector('dd'):
            if (i.text == '企业商户'):
                i.click()
        time.sleep(5)
        driver.find_element_by_tag_name('button').click()  # 我已准备资料 按钮
        time.sleep(5)
        driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(filePath+fileimge)
        time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'md-dialog-btn'))).click()
            # WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, 'quarter-content'))).click()
        except:
            print("没有上传成功")
        qydata = idcardexcell.qyinfo()
        merinit._input_placeholder_value(driver, "请输入商户简称", "拉卡拉测试")

        try:
            time.sleep(5)
            merinit._input_placeholder_readonly(driver, "请选择营业执照类型", "企业")
        except:
            print("识别图片中没有营业执照类型")

        merinit._input_placeholder_readonly(driver, "请选择省、市、区", "河北 秦皇岛 海港区")
        driver.find_element_by_xpath('//input[@placeholder="请选择省、市、区"]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/p').click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/p').click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div/div/div[6]/div/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/div[1]/div/div[1]/p').click()
       
        #merinit._input_placeholder_value(driver, "请输入商户客服联系电话", "07552314256")
        merinit._input_placeholder_value(driver, "请输入邮箱", "guolijunwh@163.com")
        els = driver.find_elements_by_xpath('//input[@type="file"]')

        els[0].send_keys(
            data2.get("本地图片路径") + "门面照.jpg")
        els[1].send_keys(
            data2.get("本地图片路径") + "内景照.jpg")
        time.sleep(5)
        driver.find_element_by_tag_name('button').click()  # 下一步 按钮
        try:
            time.sleep(5)
            merinit._input_placeholder_value(driver, "请输入营业执照上的名称","拉卡拉测试有限公司")
            driver.find_element_by_tag_name('button').click()  # 下一步 按钮
        except:
            print("识别成功")

        # if (defalutdata == 1):
        #     merinit._input_placeholder_value(driver, "请输入营业执照上的名称", data3.get("商户全称"))
        #     merinit._input_placeholder_value(driver, "请输入统一社会信用代码", data3.get("信用代码"))
        # else:
        #     merinit._input_placeholder_value(driver, "请输入营业执照上的名称", qydata[0])
        #     ##merinit._input_placeholder_value(driver, "请输入商户简称", qydata[0])
        #     merinit._input_placeholder_value(driver, "请输入统一社会信用代码", qydata[1])
        # merinit._input_placeholder_value(driver, "请输入详细地址", "广东省深圳市宝安区")            
        # merinit._input_placeholder_readonly(driver, "请选择起始日期", "2020-02-02")
        # merinit._input_placeholder_readonly(driver, "请选择结束日期", "2030-02-01")

        # 填写法人信息
        filePathfront=filePathdir+'身份证正面\\可识别\\'
        fileimgefronts=os.listdir(filePathfront)
        fileimgefront=random.choice(fileimgefronts)

        time.sleep(5)
        els = driver.find_elements_by_xpath('//input[@type="file"]')
        els[0].send_keys(filePathfront+fileimgefront)
        time.sleep(10)
        driver.find_element_by_xpath('//a[@class="md-dialog-btn"]').click()
        time.sleep(5)
        filePathback=filePathdir+'身份证反面\\可识别\\'
        fileimgebacks=os.listdir(filePathback)
        fileimgeback=random.choice(fileimgebacks)
        els[1].send_keys(filePathback+fileimgeback)
        time.sleep(5)
        driver.find_element_by_xpath('//a[@class="md-dialog-btn"]').click()
        ##ocr自动识别
        time.sleep(5)
        # if (defalutdata == 1):
        #     merinit._input_placeholder_value(driver, "请输入法人代表姓名", data3.get("姓名"))
        #     merinit._input_placeholder_value(driver, "请输入法人代表身份证号", data3.get("身份证号"))
        # else:
        #     merinit._input_placeholder_value(driver, "请输入法人代表姓名", qydata[2])
        #     merinit._input_placeholder_value(driver, "请输入法人代表身份证号", qydata[4])
        # merinit._input_placeholder_readonly(driver, "请选择起始日期", "2020-02-02")
        # merinit._input_placeholder_readonly(driver, "请选择结束日期", "2030-02-01")
        driver.find_element_by_tag_name('button').click()  # 下一步 按钮

        # 填写结算账户
        if (defalutdata == 1):
            merinit._input_placeholder_value(driver, "请输入本人银行卡号", ''.join(random.choice("123456789") for i in range(12)))
            merinit._input_placeholder_readonly(driver, "请选择开户银行", "中国建设银行")
            driver.find_element_by_xpath('//input[@placeholder="请选择开户银行"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@class="md-cell-item-title"]').click()
            time.sleep(1)
            #        merinit._input_placeholder_readonly(driver, "请选择开户支行", "北京")
            driver.find_element_by_xpath('//input[@placeholder="请选择开户支行"]').click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@tab="province"]'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@tab="city"]'))).click()
            #        merinit._input_placeholder_readonly(driver, "请选择支行名称", "***")
            driver.find_element_by_xpath('//input[@placeholder="请选择支行名称"]').click()
            merinit._input_placeholder_readonly(driver, "请选择开户支行", "北京")
            merinit._input_placeholder_readonly(driver, "请选择支行名称", "柳芳南里支行")

        else:
            merinit._input_placeholder_value(driver, "请输入本人银行卡号",  ''.join(random.choice("123456789") for i in range(12)))
            merinit._input_placeholder_readonly(driver, "请选择开户银行", "中国建设银行")
            driver.find_element_by_xpath('//input[@placeholder="请选择开户银行"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@class="md-cell-item-title"]').click()
            time.sleep(1)
            #        merinit._input_placeholder_readonly(driver, "请选择开户支行", "北京")
            driver.find_element_by_xpath('//input[@placeholder="请选择开户支行"]').click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@tab="province"]'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@tab="city"]'))).click()
            #        merinit._input_placeholder_readonly(driver, "请选择支行名称", "***")
            driver.find_element_by_xpath('//input[@placeholder="请选择支行名称"]').click()
            merinit._input_placeholder_readonly(driver, "请选择开户支行", "北京")
            merinit._input_placeholder_readonly(driver, "请选择支行名称", "柳芳南里支行")
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li'))).click()
        time.sleep(1)
        driver.find_element_by_xpath('//input[@type="file"]').send_keys(
            data.get("本地图片路径") + "身份证正面.jpg")

        if (defalutdata == 1):
            merinit._input_placeholder_value(driver, "请输入姓名", data3.get("姓名"))
            merinit._input_placeholder_value(driver, "请输入联系人手机号码", data3.get("手机号"))
            merinit._input_placeholder_value(driver, "请输入联系人身份证号码", data3.get("身份证号"))
        else:
            merinit._input_placeholder_value(driver, "请输入姓名", qydata[2])
            merinit._input_placeholder_value(driver, "请输入联系人手机号码", qydata[3])
            merinit._input_placeholder_value(driver, "请输入联系人身份证号码", qydata[4])

        # merinit._input_placeholder_value(driver, "请输入验证码", "666666")
        # el = driver.find_elements_by_tag_name('button')
        # el[0].click()  # 发送短信按钮
        # #   driver.find_element_by_tag_name('button').click()  #下一步
        # el[1].click()  # 提交按钮
        # time.sleep(5)


