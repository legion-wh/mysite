# coding=utf-8
import os, sys
import random
import xlrd
import csv
from datetime import date, timedelta
import  time
from identity import IdNumber
#from StringIO import StringIO


DC_PATH="E:\学习\webui_auto\idcard\districtcode.txt"
# 随机生成手机号码
def createPhone():
		prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188"]
		return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


# 随机生成身份证号
def gennerator():
	random_sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
	id=IdNumber.generate_id(random_sex)  # 随机生成身份证号
	return id
def  compayName():
	province=["北京",
"天津",
"河北",
"山西",
"内蒙",
"辽宁",
"吉林",
"黑龙",
"上海",
"江苏",
"浙江",
"安徽",
"福建",
"江西",
"山东",
"河南",
"湖北",
"湖南",
"广东",
"广西",
"海南",
"重庆",
"四川",
"贵州",
"云南",
"西藏",
"陕西",
"甘肃",
"青海",
"宁夏",
"新疆",
"台湾"]
	num1=['一','二','三','四','五','六','七','八','九']
	num2=''.join(random.choice(num1) for i in range(3))
	compayName=random.choice(province)+num2+'维沃移动通信有限公司'
	print()
	return compayName

def businessLicenseNo():
	businessLicenseNoRANDOM=['91610133MAB0JPAK6N',
							 '91610136MAB0WX1N6T',
							 '91610721MA7002ND8H',
							 '91610138MAB0WY709K',
							 '91610103MAB0T5WG3X',
							 '91610103MAB0T5WG3X',
							 '12610000435204555T',
							 '91610132MAB0WUD578',
							 '91610112MAB0X00QXU',
							 '91610132MAB0WUHX15',
							 '12610000435203253C',
							 '12610111H165049956',
							 '92610103MAB0W4JJ9Y',
							 '92610103MAB0W4HT8E',
							 '92610103MAB0W4HF3K',
							 '92610135MAB0W4DL7R',
							 '92610103MAB0W4GX4F',
							 '92610135MAB0W4DX5W',
							 '92610135MAB0W4FY6C',
							 '92610135MAB0W4FT55',
							 '91610113MAB0W44B8P',
							 '91610131MAB0W1MC23',
							 '91610135MAB0UTTE9X',
							 '91610103MAB0UR7J44',
							 '91610131MAB0UPA7XA',
							 '91611101MAB2N5QC1J',
							 '91610133MAB0T46G5E',
							 '91610136MAB0U6JY6M',
							 '91610131MAB0TXKU8L',
							 '91610131MAB0QKMY1M',
							 '91610103MAB0TN374L',
							 '91611104MAB2M95F80',
							 '91610132MAB0TGQR56',
							 '91610722MA6YYTEK6F',
							 '91610131MAB0TAP288',
							 '91610132MAB0T27B52',
							 '91610702MA6YYR69XQ',
							 '91610132MAB0RHFH5A',
							 '91610102MAB0RLFL91',
							 '91611101MAB2LGQU8P']
	businessLicenseNo=''.join(random.choice(businessLicenseNoRANDOM))
	#print(businessLicenseNo)
	# businessLicenseNo='91310104MA1FRG'
	# zimu=['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
	# 	 'd', 'c', 'b', 'a']
	# str1=''.join(random.choice(zimu))+str(random.randint(100,999))
	# businessLicenseNo=businessLicenseNo+str1
	# businessLicenseNo=businessLicenseNo.upper()
	#print(businessLicenseNo)
	return businessLicenseNo

def legalPersonName():
	firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻水云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅卞齐康伍余元卜顾孟平" \
				"黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计成戴宋茅庞熊纪舒屈项祝董粱杜阮席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍万柯卢莫房缪干解应宗丁宣邓郁单杭洪包诸左石崔吉" \
				"龚程邢滑裴陆荣翁荀羊甄家封芮储靳邴松井富乌焦巴弓牧隗山谷车侯伊宁仇祖武符刘景詹束龙叶幸司韶黎乔苍双闻莘劳逄姬冉宰桂牛寿通边燕冀尚农温庄晏瞿茹习鱼容向古戈终居衡步都耿满弘国文东殴沃曾关红游盖益桓公晋楚闫"
	# 百家姓全部姓氏
	# firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平" \
	#             "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董粱杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮" \
	#             "龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴欎胥能苍" \
	#             "双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍舄璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空" \
	#             "曾毋沙乜养鞠须丰巢关蒯相查後荆红游竺权逯盖益桓公晋楚闫法汝鄢涂钦归海帅缑亢况后有琴梁丘左丘商牟佘佴伯赏南宫墨哈谯笪年爱阳佟言福百家姓终"
	# 百家姓中双姓氏
	# firstName2 = "万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁段干百里东郭南门呼延羊舌微生梁丘左丘东门西门南宫南宫"
	# i = random.choice(range(len(firstName2)))##未做到只取奇数，导致复姓错乱
	# firstName_name = firstName2[i:i + 2]
	# print(firstName_name)
	# 名字
	name = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘中笑贝凯歌易仁器义礼智信友上都卡被好无九加电金马钰玉忠孝'
	lastName=random.choice(name)+random.choice(name)
	legalPersonName=random.choice(firstName)+lastName

	return legalPersonName

def bankAccountNo():

	data = open('E:\学习\webui_auto\idcard\cardbin.csv', 'r', encoding="utf-8")
	#worksheet = csv.reader(data)
	reader = csv.reader(data)
	column = [row[6] for row in reader]
	card=[]
	# for i in column:  ##去除表头
	# 	if i=='card_bin':
	# 		continue
	# 	else:
	# 		#print(i)
	# 		card.append(i)
	# 	#print(icolumn)
	cardbin=random.choice(column[2:])
	bankAccountNo=cardbin+''.join(random.choice("0123456789") for i in range(19-len(cardbin)))
	#print(card)
	#print(column[2:])  ##去除表头
	#print(bankAccountNo)
	return bankAccountNo
# print("随机生成手机号："+createPhone())
# print("随机生成身份证号:"+gennerator())
# print('公司名称:'+compayName())
# print('统一社会信用代码:'+businessLicenseNo())
# print('法人名称:'+legalPersonName())
# print('银行卡号:'+bankAccountNo())

##自然人
def zrrinfo():
	zrrinfostr=[]
	zrrinfostr.append(legalPersonName())
	zrrinfostr.append(createPhone())
	zrrinfostr.append(gennerator())
	zrrinfostr.append(bankAccountNo())
	#print(zrrinfostr)
	return zrrinfostr

##企业

def qyinfo():
	qyinfostr=[]
	qyinfostr.append(compayName())
	qyinfostr.append(businessLicenseNo())
	qyinfostr.append(legalPersonName())
	qyinfostr.append(createPhone())
	qyinfostr.append(gennerator())
	qyinfostr.append(bankAccountNo())
	return qyinfostr
##个体

def gtinfo():
	gtinfostr=[]
	gtinfostr.append(compayName())
	gtinfostr.append(businessLicenseNo())
	gtinfostr.append(legalPersonName())
	gtinfostr.append(createPhone())
	gtinfostr.append(gennerator())
	gtinfostr.append(bankAccountNo())
	#print(zrrinfostr)
	return gtinfostr



class idcardexcell():
	def zrrinfo():
		zrrinfostr = []
		zrrinfostr.append(legalPersonName())
		zrrinfostr.append(createPhone())
		zrrinfostr.append(gennerator())
		zrrinfostr.append(bankAccountNo())
		# print(zrrinfostr)
		return zrrinfostr

	##企业

	def qyinfo():
		qyinfostr = []
		qyinfostr.append(compayName())
		qyinfostr.append(businessLicenseNo())
		qyinfostr.append(legalPersonName())
		return qyinfostr

	##个体

	def gtinfo():
		gtinfostr = []
		gtinfostr.append(compayName())
		gtinfostr.append(businessLicenseNo())
		gtinfostr.append(legalPersonName())
		gtinfostr.append(createPhone())
		gtinfostr.append(gennerator())
		gtinfostr.append(bankAccountNo())
		# print(zrrinfostr)
		return gtinfostr

#MER_PATH="E:\学习\webui_auto\生成开户数据\zrrmer1"+str( time.time())+".csv"
#MER_PATH="E:\学习\webui_auto\生成开户数据\zrrmer1"+str(time.strftime("%Y-%m-%d %H%M%S", time.localtime()))+".csv"

#print(qyinfo())
# row = ['5', 'hanmeimei', '23', '81']
# out = open("test.csv", "a", newline = "")
# csv_writer = csv.writer(out, dialect = "excel")
# csv_writer.writerow(row)
# 	print(qyinfo())
# 	print(gtinfo())
# 	print(zrrinfodata[0][1])
##
# 1、写入excel
# 2、钉钉
# 3、封装方法，直接调用


# 上海维勉通信科技有限公司
# 91310104MA1FRGLY50

#四要素为 姓名、手机、身份证、银行卡
#三要素为 公司名称、法人姓名、社会信用代码