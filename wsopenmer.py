import pandas as pd
from dingtalkchatbot.chatbot import DingtalkChatbot
import idcardexcell
import csv
import  pandas as pd
import random
#WebHook地址

webhook = "https://oapi.dingtalk.com/robot/send?access_token=215aa98d6e614cbe6a9ae10c582c5982da28ecb5b54481502b5bf424afa58668"
secret = 'SECe00db544a79816f1239a1a28a604614e80c856c11a785877f1f132cd81c47828'
#初始化机器人小丁

xiaoding = DingtalkChatbot(webhook,secret=secret)
##指定发送人
at_mobiles = ['18576651747']

##默认开户数据
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
    "信用代码":"91360430MA39AWPG2H",
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

# defalutdata=input("是否使用默认数据，输入0读取excel数据，输入1使用默认数据，否则使用随机数据")
defalutdata = 2  # 强制使用随机数据

mertype=1  ##定义商户类型 0自然人 1个体  2企业

# 913201140802643630
# 91330110MA2CD3C31U
# 914403005879163755
# 91320114302509363B
# 91110105MA01F7G43G
# 91441900MA51A07P0B
# 91330106MA2CFM5B5H

if defalutdata==1:
    if mertype==0:
        certName=data.get('姓名')
        cardno=data.get('银行卡号')
        certNo=data.get('身份证号')
        mobile=data.get('手机号')
    elif mertype==1:
        companyName=data1.get('商户全称')
        firmCertNo=data1.get('信用代码')
        legalName=data1.get('姓名')
        certName=data1.get('姓名')
        cardno=data1.get('银行卡号')
        certNo=data1.get('身份证号')
        mobile=data1.get('手机号')
    elif mertype==2:
        companyName=data1.get('商户全称')
        firmCertNo=data1.get('信用代码')
        legalName=data1.get('姓名')
    else:
        print("商户类型输入有误")

elif defalutdata!=1:
    if mertype==0:
        zrrinfo=idcardexcell.zrrinfo()
        certName=zrrinfo[0]
        cardno=zrrinfo[3]
        certNo=zrrinfo[2]
        mobile=zrrinfo[1]
    elif mertype==1:
        gtinfo=idcardexcell.gtinfo()
        companyName=gtinfo[0]
        firmCertNo=gtinfo[1]
        legalName=gtinfo[2]
        certName=gtinfo[2]
        cardno=gtinfo[5]
        certNo=gtinfo[4]
        mobile=gtinfo[3]
        ##存储随机生成的四要素数据，并用于开户
        headers=['companyName','firmCertNo','legalName','certName','cardno','certNo','mobile']
        rows=[companyName,firmCertNo,legalName,certName,cardno,certNo,mobile]
        print(rows)
        filepath='E:\\学习\\webui_auto\\datasoure\\wsdata\\'
        with open(filepath+'wsdata.csv', 'w', encoding="utf-8",newline='') as f:
            f_csv=csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerow(rows)
            print("存储成功")
            f.close()

    elif mertype==2:
        qyinfo=idcardexcell.qyinfo()
        companyName=qyinfo[0]
        firmCertNo=qyinfo[1]
        legalName=qyinfo[2]
    else:
       print("商户类型输入有误")


if __name__ == '__main__':
    if mertype==0:
        print('自然人商户开户')
        xiaoding.send_text(msg='三要素封装\n'+'cardNo='+cardno+',certNo='+certNo+',certName='+certName+',mobile='+mobile+',verificationType=F,envRadio=stable '+
                               '四要素封装\n'+'cardNo='+cardno+',certNo='+certNo+',certName='+certName+',mobile='+mobile+'verificationType=T,envRadio=stable ', at_mobiles=at_mobiles)
    elif mertype==1:
        print('个体商户开户')
        xiaoding.send_text(msg='个体商户开户\n'+
                               '工商信息绑存：\n'+'companyName='+companyName+',legalName='+legalName+',firmCertNo='+firmCertNo+',envRadio=stable \n'+
                               '三要素封装\n'+'cardNo='+cardno+',certNo='+certNo+',certName='+certName+',mobile='+mobile+'verificationType=F,envRadio=stable '+
                               '四要素封装\n'+'cardNo='+cardno+',certNo='+certNo+',certName='+certName+',mobile='+mobile+'verificationType=T,envRadio=stable ', at_mobiles=at_mobiles)
    elif mertype==2:
        print('企业商户开户')
        xiaoding.send_text(msg='工商信息绑存：\n'+'companyName='+companyName+',legalName='+legalName+',firmCertNo='+firmCertNo+',envRadio=stable ', at_mobiles=at_mobiles)
        xiaoding.send_text(msg='企业开户激活,打款验证金额:\n'+
                               'SELECT x.bank_payment_verify_id FROM pay_member.member_bankcard x WHERE internal_member_no = 314844043794227200 ', at_mobiles=at_mobiles)
    else:
        print('不可识别')