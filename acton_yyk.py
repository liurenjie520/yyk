#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 买内裤脚本@feller
import sys
import datetime

import requests, json


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


def formdata():
    # description
    # print('请输入查询商品的关键字，如：平角裤 男士')
    # description = input('请输入您的选择：')
    description='平角裤 男士'

    # sex
    # print('请输入：1：男装 2：女装')
    # choice = input('请输入您的选择：')
    # # 变量赋值
    #
    # if choice == '1':
    #     # 条件判断:条件1
    #
    #     sex = "男装"
    # # 条件1的结果
    #
    # else:
    #     # 条件判断：其他条件
    #     if choice == '2':
    #         sex = "女装"
    #     else:
    #         print("输入错误，请从新输入，程序已退出，请再次运行")
    #         sys.exit()
    sex = "男装"

    # low, high = map(int, input("请输入价格区间，中间用空格分开。例如50 180:").split())
    low=10
    high=30


    # material

    # material = []
    # materiallis = list(map(str, input("请输入材料，中间用空格分开。例如:棉 亚麻\n").split()))
    # for i in materiallis:
    #     material.append(i)
    material='棉'

    # identity
    # print('请选择：1：限时优惠  2：超值精选')
    # identityinput = input('请输入您的选择：')
    # 变量赋值

    # if identityinput == '1':
    #     # 条件判断:条件1
    #
    #     identity = "time_doptimal"
    # # 条件1的结果
    #
    # else:
    #     # 条件判断：其他条件
    #     if identityinput == '2':
    #         identity = "concessional_rate"
    #     else:
    #         print("输入错误，请从新输入，程序已退出，请再次运行")
    #         sys.exit()
    identity = "concessional_rate"

    # size
    # size = []
    # lis = list(map(str, input("请输入尺码，中间用空格分开。例如s m l xl\n").split()))
    #
    # for i in lis:
    #     if i == "s":
    #
    #         s = "SMA003"
    #         size.append(s)
    #     else:
    #         if i == "m":
    #             m = "SMA004"
    #             size.append(m)
    #         else:
    #             if i == "l":
    #                 l = "SMA005"
    #                 size.append(l)
    #             else:
    #                 if i == "xl":
    #                     xl = "SMA006"
    #                     size.append(xl)
    #                 else:
    #
    #                     print("输入错误，请从新输入，程序已退出，请再次运行")
    #                     sys.exit()
    size = "SMA004"

    FormData = {
        "description": description,
        "sex": [
            sex
        ],
        "material": [material],
        "season": [],
        "identity": [identity],
        "color": [],
        "size": [size],
        "insiteDescription": "",
        "rank": "priceAsc",
        "pageInfo": {
            "page": 1,
            "pageSize": 16
        },
        "priceRange": {
            "low": low,
            "high": high
        },
        "storeCode": [

        ]
    }
    return FormData


def get_sh_store(code):
    code = code
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
        tinydict[i['code']] = i['displayName']+"；地址："+i['fullAddress'] +"；营业时间："+i['businessHours'].rstrip('\n')+"；店铺状态："+i['shopStatus']# 添加  fullAddress  .displayName

    try:
        name = tinydict[f"{code}"]
    except:
        name = "门店不在上海"

    return name


def get_sh_goods():
    url = 'https://a.uniqlo.cn/m/hmall-sc-service/search/searchWithDescriptionAndConditions/zh_CN'
    HEADERS = {'Content-Type': 'application/json'}
    FormData = formdata()
    # print(FormData)
    res = requests.post(url=url, json=FormData, headers=HEADERS)

    res = res.text
    # print(res)
    jsonobj = json.loads(res)
    try:
        toCntPercent = jsonobj['resp'][1]
    except:
        print("查询不到商品！")
        toCntPercent = ''

    mendian = []
    mendian_v2 = []
    a = {}
    numbers = []
    for i in toCntPercent:
        try:
            mendian.append(i["stores"])
        except:
            print("查询不到商品！")

    for j in mendian:

        for code in j:
            mendian_v2.append(code)

    for w in mendian_v2:
        if mendian_v2.count(w) > 1:
            a[w] = mendian_v2.count(w)
            # print((mendian_v2.count(w)))
            numbers.append(mendian_v2.count(w))
    # print(a)

    dizhi = []
    lsttt = list(set(numbers))  # 去重  排序
    lsttt.sort(reverse=True)  # 去重  排序
    for shuju in lsttt:
        # print(shuju)
        # 根据value反查key
        for mendian_code in get_keys(a, shuju):
            if get_sh_store((mendian_code)) == '门店不在上海':
                continue
            else:
                # print(shuju)
                jianshu = ",可买" + str(shuju) + "件商品；"
                dizhi.append(get_sh_store((mendian_code)) + jianshu)

    print("查询结果如下：")
    summary=[]
    content = ''
    if dizhi:
        for shuchu in dizhi:
            summary.append(shuchu)
            content =content+shuchu+"\n\n"
            # print(shuchu)
    else:
        print('查询不到商品！')
    summary_v2="查询结果如下："+'\n'+summary[0]+'\n'+summary[1]+'\n'+summary[2]
    now = "------------------" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "------------------"+"\n"
    with open("content.txt", "a",encoding='utf-8') as file:
        file.write(now)
        file.write(content)
    # print(summary[0])

    # print(summary[1])

    url = 'http://wxpusher.zjiecode.com/api/send/message'
    HEADERS = {'Content-Type': 'application/json'}
    FormData = {
        "appToken": "AT_iaPxpUE0FLNUECu1zFnKhFR7R9NU5K8e",
        "content": content,
        "summary": summary_v2,
        "contentType": 1,

        "topicIds": [

        ],
        "uids": [
            "UID_noWsar4x3r0zd4WqjCaoD5CIX9Xi"
        ],
        "url": ""
    }
    res = requests.post(url=url, json=FormData, headers=HEADERS)
    # print(res.text)
    res = res.text
    jsonobj = json.loads(res)
    toCntPercent = jsonobj['code']
    summary_v3 = "查询结果如下："+'\n'+summary[0]+'\n'+summary[1]
    if toCntPercent == 1001:
        print("消息摘要过长，正在重试发送2个")
        url = 'http://wxpusher.zjiecode.com/api/send/message'
        HEADERS = {'Content-Type': 'application/json'}
        FormData = {
            "appToken": "AT_iaPxpUE0FLNUECu1zFnKhFR7R9NU5K8e",
            "content": content,
            "summary": summary_v3,
            "contentType": 1,

            "topicIds": [

            ],
            "uids": [
                "UID_noWsar4x3r0zd4WqjCaoD5CIX9Xi"
            ],
            "url": ""
        }
        res = requests.post(url=url, json=FormData, headers=HEADERS)
        # print(res.text)
        res = res.text
        jsonobj = json.loads(res)
        toCntPercent = jsonobj['code']
        summary_v4 = "查询结果如下：" + '\n' + summary[0]
        if toCntPercent == 1001:
            print("消息摘要过长，正在重试发送1个")
            url = 'http://wxpusher.zjiecode.com/api/send/message'
            HEADERS = {'Content-Type': 'application/json'}
            FormData = {
                "appToken": "AT_iaPxpUE0FLNUECu1zFnKhFR7R9NU5K8e",
                "content": content,
                "summary": summary_v4,
                "contentType": 1,

                "topicIds": [

                ],
                "uids": [
                    "UID_noWsar4x3r0zd4WqjCaoD5CIX9Xi"
                ],
                "url": ""
            }
            res = requests.post(url=url, json=FormData, headers=HEADERS)
            # print(res.text)
        else:
            print("消息摘要正常")
    else:
        print("消息摘要正常")


get_sh_goods()
