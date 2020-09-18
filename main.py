import re
import jieba
import jieba.analyse
import math
from functools import reduce


def string(file):
    with open(file, encoding='utf-8') as File:
        # 读取
        lines = File.readlines()
        line = ''.join(lines)
        # 去特殊符号
        character_string = re.sub(r"[%s]+" % ',$%^*(+)]+|[+——()?【】“”！，。？、~@#￥%……&*（）：]+', "", line)
    return character_string


def get_words(original, content):
    dictionary = {}
    return_dic = {}
    # 分词
    key_word = jieba.cut_for_search(content)
    for x in key_word:
        if x in dictionary:
            dictionary[x] += 1
        else:
            dictionary[x] = 1
    topK = 30
    tfidf = jieba.analyse.extract_tags(content, topK=topK, withWeight=True)
    stop_keyword = [line.strip() for line in original]
    for word_weight in tfidf:
        if word_weight in stop_keyword:
            continue
        word_frequency = dictionary.get(word_weight[0], 'not found')
        return_dic[word_weight[0]] = word_frequency
    return return_dic


def similar(all_keys, original_document_dic, original_document_test_dic):
    str1_vector = []
    str2_vector = []
    # 词频向量
    for i in all_keys:
        str1_count = original_document_dic.get(i, 0)
        str1_vector.append(str1_count)
        str2_count = original_document_test_dic.get(i, 0)
        str2_vector.append(str2_count)

    # 平方和
    str1_map = map(lambda x: x * x, str1_vector)
    str2_map = map(lambda x: x * x, str2_vector)

    str1_mod = reduce(lambda x, y: x + y, str1_map)
    str2_mod = reduce(lambda x, y: x + y, str2_map)

    # 平方根
    str1_mod = math.sqrt(str1_mod)
    str2_mod = math.sqrt(str2_mod)

    # 向量积
    vector_multi = reduce(lambda x, y: x + y, map(lambda x, y: x * y, str1_vector, str2_vector))

    # 余弦值
    cosine = float(vector_multi) / (str1_mod * str2_mod)
    return cosine


try:
    original_document = input("请输入原文文件：")
    original_document_test = input("请输入测试文件：")
    output = input("请输入输出文件：")
    all_key = set()
    str_Original_document = string(original_document)
    str_Original_document_test = string(original_document_test)
    original_document_dic1 = get_words(original_document, str_Original_document)
    for k, v in original_document_dic1.items():
        all_key.add(k)
    original_document_dic2 = get_words(original_document, str_Original_document_test)
    for k, v in original_document_dic2.items():
        all_key.add(k)
    cos = similar(all_key, original_document_dic1, original_document_dic2)
    f = open(output, "w", encoding="UTF-8")
    f.write(str(cos) + "\n")
    f.close()
except Exception as e:
    print(e)
