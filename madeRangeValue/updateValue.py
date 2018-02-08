#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "熠道大数据科技发展(上海)有限公司@lee"

'''
功能:
根据code查找RESULT值并生成realValue值(code的最大最小值)并插入字典表中,插入二分之一值,四分之一值功能作为保留,没有插入字典表

入口:
getAllCode() 获取字典表下所有的code

updataData() 写入字段并更新
'''

from madeRangeValue.realValue import getRealValue,changeNum
from pymongo import MongoClient
import pandas as pd
import threadpool

#获取字典表下所有的code
def getAllCode():
    result = db.dicts.find({"_classes": "化验"})
    code_result = []
    for tmp in result:
        code_result.append(tmp.get('_code'))
    return code_result

def updataData(code_result):
    for code in code_result:
        real_value=getRealValue(code)

    # value_list=changeNum(value_list)
    # if value_list:
    #     df=pd.DataFrame(value_list)
    #     value = pd.Series([df.quantile(.25),df.median()],index=['四分之一值','二分之一值'])
    #     db.dict_data_test.update({"_code": code}, {"$set": {"_realValue": real_value,"_quarterfinalValue":value[0][0],"_harfValue":value[1][0]}})
    # else:
    #     db.dict_data_test.update({"_code": code}, {"$set": {"_realValue": real_value}})
        db.dicts.update({"_code": code}, {"$set": {"_rangeValue": real_value}})
if __name__ == '__main__':
    client = MongoClient('192.168.13.234', 27017)
    db_name = 'aimedical-admin'
    db = client[db_name]
    code_result = getAllCode()
    # 多线程方法写入数据(python3.6.3版本不兼容)
    thread = threadpool.ThreadPool(8)
    item_requests = threadpool.makeRequests(updataData, code_result)
    [thread.putRequest(req) for req in item_requests]
    thread.wait()

