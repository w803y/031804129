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


def get_word(original, content):
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
    # 关键词  比率
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
    # 计算词频向量
    for i in all_keys:
        str1_count = original_document_dic.get(i, 0)
        str1_vector.append(str1_count)
        str2_count = original_document_test_dic.get(i, 0)
        str2_vector.append(str2_count)

    # 计算各自平方和
    str1_map = map(lambda x: x * x, str1_vector)
    str2_map = map(lambda x: x * x, str2_vector)

    str1_mod = reduce(lambda x, y: x + y, str1_map)
    str2_mod = reduce(lambda x, y: x + y, str2_map)

    # 计算平方根
    str1_mod = math.sqrt(str1_mod)
    str2_mod = math.sqrt(str2_mod)

    # 计算向量积
    vector_multi = reduce(lambda x, y: x + y, map(lambda x, y: x * y, str1_vector, str2_vector))

    # 计算余弦值
    cosine = float(vector_multi) / (str1_mod * str2_mod)
    return cosine


def test(doc_name):
    test_file = "C:\Users\ALIENWARE\PycharmProjects\pythonProject\sim_0.8/"+doc_name
    original_document_test = test_file
    all_key = set()
    original_document = "C:\Users\ALIENWARE\PycharmProjects\pythonProject\sim_0.8/orig.txt"
    str_Original_document = string(original_document)
    str_Original_document_test = string(original_document_test)
    original_document_dic1 = get_word(original_document, str_Original_document)
    for k, v in original_document_dic1.items():
        all_key.add(k)
    original_document_dic2 = get_word(original_document, str_Original_document_test)
    for k, v in original_document_dic2.items():
        all_key.add(k)
    cos = similar(all_key, original_document_dic1, original_document_dic2)
    print("%s 的相似度 = %.2f" % (doc_name, cos))


test("orig_0.8_add.txt")
test("orig_0.8_del.txt")
test("orig_0.8_dis_1.txt")
test("orig_0.8_dis_3.txt")
test("orig_0.8_dis_7.txt")
test("orig_0.8_dis_10.txt")
test("orig_0.8_dis_15.txt")
test("orig_0.8_mix.txt")
test("orig_0.8_rep.txt")
