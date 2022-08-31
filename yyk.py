#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 买内裤脚本@feller
import requests, json

def get_mendian(id):
    id = id
    url = 'https://d.uniqlo.cn/p/hmall-store-service/i/site/base/queryOthers/zh_CN'
    HEADERS = {'Content-Type': 'application/json'}
    FormData = {
        "areaId": "310000",

        "type": "2"
    }
    res = requests.post(url=url, json=FormData, headers=HEADERS)

    res = res.text
    jsonobj = json.loads(res)
    toCntPercent = jsonobj['resp']

    tinydict = {}
    for i in toCntPercent:
        tinydict[i['code']] = i['fullAddress']  # 添加  fullAddress  .displayName

    try:
        name = tinydict[f"{id}"]
    except:
        name = "门店不在上海"

    return name

def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


url = 'https://a.uniqlo.cn/m/hmall-sc-service/search/searchWithDescriptionAndConditions/zh_CN'
HEADERS = {'Content-Type': 'application/json'}
FormData = {
    "description": "平角裤 男士",
    "sex": [
        "男装"
    ],
    "material": [
        "棉"
    ],
    "season": [],
    "identity": [],
    "color": [],
    "size": [
        "SMA004"
    ],
    "insiteDescription": "",
    "rank": "overall",
    "pageInfo": {
        "page": 1,
        "pageSize": 16
    },
    "priceRange": {
        "low": 10,
        "high": 30
    },
    "storeCode": [
        "119427",
        "113506",
        "101428"
    ]
}
res = requests.post(url=url, json=FormData, headers=HEADERS)

res = res.text
jsonobj = json.loads(res)
toCntPercent = jsonobj['resp'][1]
mendian =[]
mendian_v2=[]
a = {}
numbers = []
for i in toCntPercent:

    mendian.append(i["stores"])


for j in mendian:


    for code in j:

        mendian_v2.append(code)

for w in mendian_v2:
    if mendian_v2.count(w)>1:

        a[w] = mendian_v2.count(w)
        # print((mendian_v2.count(w)))
        numbers.append(mendian_v2.count(w))
# print(a)


dizhi=''
lsttt=list(set(numbers))
lsttt.sort(reverse=True)
for shuju in lsttt:
    # print(shuju)
    for mendian_code in get_keys(a, shuju):
        if get_mendian((mendian_code))=='门店不在上海':
            continue
        else:
            dizhi = get_mendian((mendian_code))+","+dizhi


print(dizhi)








