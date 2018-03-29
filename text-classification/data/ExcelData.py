import xlrd
import re
import string
import jieba
import os
import random
import jieba.posseg as pseg
from jieba import analyse

categories = ['丙肝', '乙肝', '前列腺炎', '盆腔炎', '肠胃炎', '肾炎', '肾结石', '肾绞痛', '胆囊炎', '胆结石', '胰腺炎', '阑尾炎']

workbook = xlrd.open_workbook("../source/baidu.xlsx")
sheet = workbook.sheet_by_index(0)
rows = sheet.nrows  # 行数
cols = sheet.ncols  # 列数

def readExcel(categorie):


    for i in range(2, rows):
        read_text = ''
        rowValues = sheet.row_values(i)  # 某一行数据
        while '' in rowValues:
            rowValues.remove('')
        for item in rowValues:
            # item = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]',item)
            read_text = read_text + item
        text = textFormat(read_text)
        wordList = wordCut(text)
        buildList(categorie, wordList)
    print("RUNNING" + categorie + "..............")



def textFormat(read_text):
    text = ''
    tmp_text = read_text.replace('\n', '').replace('\t', '').replace('\u3000', '').replace('\r', '')
    tmp_text = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]',tmp_text)
    for tmp in tmp_text:
        text = text+tmp
    return text


def wordCut(text):
    wordList=[]
    tfidf = analyse.extract_tags
    keywords = tfidf(text)
    for keyword in keywords:
        wordList.append(keyword)
    return wordList

def buildList(categorie,wordList):
    f_train = open('cnews/desc-train.txt', mode='a', encoding='utf-8')
    f_test = open('cnews/desc-test.txt', mode='a', encoding='utf-8')
    f_val = open('cnews/desc-val.txt', mode='a', encoding='utf-8')

    for i in range(400):
        tmp_content = random.sample(wordList,random.randint(2,6) )
        content = list2word(tmp_content).rstrip(",")
        f_train.write(categorie + '\t' + content + '\n')
    for j in range(150):
        tmp_content = random.sample(wordList, random.randint(2,6))
        content = list2word(tmp_content).rstrip(",")
        f_test.write(categorie + '\t' + content + '\n')
    for k in range(50):
        tmp_content = random.sample(wordList, random.randint(2,6))
        content = list2word(tmp_content).rstrip(",")
        f_val.write(categorie + '\t' + content + '\n')

    f_train.close()
    f_test.close()
    f_val.close()


def list2word(list):
    word = ''
    for tmp in list:
        word = word+tmp+","
    word.rsplit(",")
    return word




if __name__ == '__main__':
    # text = '丙型肝炎丙肝hepatitisC感染科消化内科肝丙型肝炎病毒感染一般表现为恶心食欲下降全身无力有血液传播性传播母婴传播丙型肝炎'
    for categorie in categories:
        readExcel(categorie)
    # wordList = wordCut(text)
    # print(wordList)






