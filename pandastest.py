import pandas as pd
import csv
import glob
import os
##定义文件路径
# ##
# 1.基础文件读写（等同于copy文件）
# 2.行中的值满足某个条件(含整理原始文件脏数据)
# 3.行中的值满足某个集合
# 4.行中的值匹配于某个模式
# 5.选取特定的列（列索引值）
# 6.选取特定的列（列标题）
# 7.选取连续的行（丢弃不需要的行）
# 8.添加标题行
# 9.读取多个csv文件，包含去重
# 10.计算每个文件中值的总和与平均值，写入新文件
# 11.计算每个文件中值的总和与平均值，写入原文件(这里先复制出一份和原来一样的文件后写入新文件)
# ###
my_file_path='E:\\学习\\webui_auto\\datasoure\\pandsdata.csv'
datasoure='E:\\学习\\webui_auto\\datasoure\\'
#with open(my_file_path,encoding='utf-8') as file:
# with open(my_file_path) as file:
#     data=pd.read_csv(file)
#     #print(data)
#     head_datas=data.head(2) ##取值前2行
#     print(head_datas)
#     tail_datas=data.tail(1)##取值最后1行
#     print('打印后1行%s',tail_datas)
    #k_csv.to_csv(k) ##打印第2行
input_file =my_file_path#sys.argv[1]
output_file = 'E:\\学习\\webui_auto\\datasoure\\csv_python_write.csv'#sys.argv[2]

def base_read_and_write():
    input_file =my_file_path#sys.argv[1]
    output_file = 'E:\\学习\\webui_auto\\datasoure\\csv_python_write.csv'#sys.argv[2]
    data_frame = pd.read_csv(input_file,encoding='gbk')
    data_frame.to_csv(output_file,index = False,encoding='gbk')

def write_row_in_col():
    input_file =my_file_path#sys.argv[1]
    output_file = 'E:\\学习\\webui_auto\\datasoure\\csv_python_write.csv'#sys.argv[2]
    data_frame = pd.read_csv(input_file,encoding='gbk')
    data_frame['price'] = data_frame['price'].str.strip('￥').str.replace(',','').astype(float)  ##去掉￥符号   到，号替换掉，并转换数据格式类型为float
    #清洗脏数据，这里有以万为单位的，也有以元为单位的，根据房产实际情况，我们把它们都整理成以万为单位的
    for i,millions_row in data_frame.iterrows():
        if millions_row['price']>10000:
            million = millions_row['price']/10000
        else:
            millions_row['price'] #等同于上面的if-else
        data_frame.at[i,'price'] = '{}'.format(million)
    #取出含有'世贸'且房价大于200万的房子
    #[,:],逗号前为行，逗号后为列，:表示所有，如选定列，例如为：df.loc[:,'A']
        data_frame_value_meets_condition = data_frame.loc[(data_frame['name'].str.contains('世茂')) & (data_frame['price']>200),:]
        data_frame_value_meets_condition.to_csv(output_file,index = False,encoding='gbk')


if __name__ == '__main__':
    print('开始你的表演')
    #base_read_and_write();
    write_row_in_col();