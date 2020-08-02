import pandas as pd
from efficient_apriori import apriori

# 数据预处理函数，生成transactions
def trans_generated(data):
    #选取所需数据列
    clinet_data = data.set_index('客户ID')['产品名称']
    #为数据排序
    client_data_sort = clinet_data.sort_index(ascending=False)
    #合并ID相同客户的产品名称并放入测试集
    transactions = []
    temp_index = 0
    for i, v in client_data_sort.items():
        if i != temp_index:
            temp_set = set()
            temp_index = i
            temp_set.add(v)
            transactions.append(temp_set)
        else:
            temp_set.add(v)
    return  transactions

#使用apriori算法的函数，打印频繁项集，打印关联规则
def apr(trans, min_sup, min_con):
    itemsets, rules = apriori(trans, min_support=min_sup, min_confidence=min_con)
    temp={}
    temp['Transactions'],temp['频繁项集'],temp['关联规则'] = trans, itemsets, rules
    #print(transactions)
    print('频繁项集：', itemsets)
    print('关联规则：', rules)

data = pd.read_csv('./订单表.csv', encoding='gbk')
transactions = trans_generated(data)
min_sup = 0.05
min_con = 0.4
apr(transactions, min_sup, min_con)