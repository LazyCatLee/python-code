#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "熠道大数据科技发展(上海)有限公司@lee"
'''
功能:
根据code查找RESULT值并生成realValue值(code的最大最小值),插入二分之一值,四分之一值功能作为保留,没有插入字典表
'''

from pymongo import MongoClient


client = MongoClient('192.168.13.234', 27017)
db_name1 = 'aimedical-cleanv1'
db_clean = client[db_name1]

# 根据code获取code的RESULT值
def getRealValue(code):

    value_result = []
    value_info = []
    result = db_clean.labdetailv1.find({"ITEM_CODE": code})
    for temp in result:
        if temp.get("RESULT", False):  # 如果能get到RESULT中的值执行if语句,否则不执行
            value_result.append(temp["RESULT"])
            value_info.append(temp['TEST_NO'])

    value_list = value_result
    value_result = list(set(value_result))
    real_value = []  # 定义一个list,存放code的最大最小值范围

    if checkValue(value_result):  # 判断RESULT结果是否能转换成数字类型的list
        value_result = changeNum(value_result)  # 将字符串类型的list转化成数字类型的
        value_result.sort()  # 对list排序

        if len(value_result) > 1:
            # 如果RESULTlist长度大于1,获得最大最小值添加到real_value中
            min_value = value_result[0]
            max_value = value_result[-1]
            real_value.append(str(min_value) + ", " + str(max_value))
        else:
            real_value = value_result

    else:
        # 枚举类型,直接返回原类型list输出
        real_value = value_result

    return real_value
    # updataData(code, real_value, value_list)  # 获得数据的TEST_NO,以查找数据RESULT对应的AGE跟SEX

# #获取result的test_no
# def getValueNo(code):
#     value_result = []
#     value_info = []
#     result = db_clean.labdetailv1.find({"ITEM_CODE": code})
#     for tmp in result:
#         # 如果能get到RESULT中的值执行if语句,否则不执行
#         if tmp.get("RESULT", False):
#             value_result.append(tmp["RESULT"])
#             value_info.append(tmp['TEST_NO'])
#     value_list = value_result
#
#     insert_data = {"CODE": code, "ValueList": value_list, "ValueInfo": value_info}
#     # insertData(insert_data)
#     return insert_data
# #将
# def insertData(code_result):
#     for code in code_result:
#         insert_data = getValueNo(code)
#         print("Insert info:" + insert_data)
#         try:
#             db_clean.made_data_test.insert(insert_data)
#         except:
#             print("Erro info:" + insert_data)


# 将字符串的list转化为数值类型的list
def changeNum(str_list):
    # # float_reg=re.compile(r'^\d+\.?\d+$')
    # float_reg = re.compile(r'^[0-9]+(.[0-9]{1,3})?$')
    # new_list=[float(f) for f in str_list if float_reg.search(f)]
    # return new_list
    new_list = []
    for _tmp in str_list:
        try:
            new_list.append(float(_tmp))
        except:
            print(_tmp)
    return new_list


# 检查list元素的类型是否数值
def checkValue(value):
    try:
        float(value[0]) and float(value[-1])
        return True
    except:
        return False


if __name__ == '__main__':
    client = MongoClient('192.168.13.234', 27017)
    db_name1 = 'aimedical-cleanv1'
    db_clean = client[db_name1]


    # 更新字典表的rangeValue字段
    # updataData(code_result)

    #将TESULT的TEST_NO数据写入数据库
    # insertData(code_result)
