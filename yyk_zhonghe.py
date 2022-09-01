#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 买内裤脚本@feller
import sys

import requests, json


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


def formdata():
    # description
    print('请输入查询商品的关键字，如：平角裤 男士')
    description = input('请输入您的选择：')

    # sex
    print('请输入：1：男装 2：女装')
    choice = input('请输入您的选择：')
    # 变量赋值

    if choice == '1':
        # 条件判断:条件1

        sex = "男装"
    # 条件1的结果

    else:
        # 条件判断：其他条件
        if choice == '2':
            sex = "女装"
        else:
            print("输入错误，请从新输入，程序已退出，请再次运行")
            sys.exit()

    low, high = map(int, input("请输入价格区间，中间用空格分开。例如50 180:").split())

    # material

    material = []
    materiallis = list(map(str, input("请输入材料，中间用空格分开。例如:棉 亚麻\n").split()))
    for i in materiallis:
        material.append(i)

    # identity
    print('请选择：1：限时优惠  2：超值精选')
    identityinput = input('请输入您的选择：')
    # 变量赋值

    if identityinput == '1':
        # 条件判断:条件1

        identity = "time_doptimal"
    # 条件1的结果

    else:
        # 条件判断：其他条件
        if identityinput == '2':
            identity = "concessional_rate"
        else:
            print("输入错误，请从新输入，程序已退出，请再次运行")
            sys.exit()

    # size
    size = []
    lis = list(map(str, input("请输入尺码，中间用空格分开。例如s m l xl\n").split()))

    for i in lis:
        if i == "s":

            s = "SMA003"
            size.append(s)
        else:
            if i == "m":
                m = "SMA004"
                size.append(m)
            else:
                if i == "l":
                    l = "SMA005"
                    size.append(l)
                else:
                    if i == "xl":
                        xl = "SMA006"
                        size.append(xl)
                    else:

                        print("输入错误，请从新输入，程序已退出，请再次运行")
                        sys.exit()

    FormData = {
        "description": description,
        "sex": [
            sex
        ],
        "material": material,
        "season": [],
        "identity": [identity],
        "color": [],
        "size": size,
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


print("正在查询你的内裤再哪个门店有优惠...........")


def get_national_store(code):
    code = code

    url = 'https://d.uniqlo.cn/p/hmall-store-service/pointOfService/pointOfServiceInfo/%s/zh_CN' % code

    res = requests.get(url=url)

    res = res.text
    jsonobj = json.loads(res)
    try:
        result = jsonobj['resp']
    except:
        result = None
        print("门店信息不存在")

    tinydict = {}
    for i in result:
        tinydict[i['code']] = i['fullAddress']  # 添加  fullAddress  .displayName

    name = tinydict[f"{code}"]

    return name


def get_national_goods():
    url = 'https://a.uniqlo.cn/m/hmall-sc-service/search/searchWithDescriptionAndConditions/zh_CN'
    HEADERS = {'Content-Type': 'application/json'}
    FormData = formdata()

    res = requests.post(url=url, json=FormData, headers=HEADERS)

    res = res.text
    jsonobj = json.loads(res)
    toCntPercent = jsonobj['resp'][1]

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
    print(a)

    dizhi = []
    lsttt = list(set(numbers))
    lsttt.sort(reverse=True)
    for shuju in lsttt:
        # print(shuju)
        for mendian_code in get_keys(a, shuju):
            jianshu = ",可买" + str(shuju) + "件商品"
            dizhi.append(get_national_store((mendian_code)) + jianshu)

    print("查询结果如下：")
    if dizhi:
        for shuchu in dizhi:
            print(shuchu)
    else:
        print('查询不到商品！')
    return None


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
        tinydict[i['code']] = i['fullAddress']  # 添加  fullAddress  .displayName

    try:
        name = tinydict[f"{code}"]
    except:
        name = "门店不在上海"

    return name


def get_sh_goods():
    url = 'https://a.uniqlo.cn/m/hmall-sc-service/search/searchWithDescriptionAndConditions/zh_CN'
    HEADERS = {'Content-Type': 'application/json'}
    FormData = formdata()
    print(FormData)
    res = requests.post(url=url, json=FormData, headers=HEADERS)

    res = res.text
    print(res)
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
    print(a)

    dizhi = []
    lsttt = list(set(numbers))  # 去重  排序
    lsttt.sort(reverse=True)  # 去重  排序
    for shuju in lsttt:
        # print(shuju)
        for mendian_code in get_keys(a, shuju):
            if get_sh_store((mendian_code)) == '门店不在上海':
                continue
            else:
                # print(shuju)
                jianshu = ",可买" + str(shuju) + "件商品"
                dizhi.append(get_sh_store((mendian_code)) + jianshu)

    print("查询结果如下：")
    if dizhi:
        for shuchu in dizhi:
            print(shuchu)
    else:
        print('查询不到商品！')


def mian():
    limits = input('程序开始，请选择1.查询上海，2.查询全国')
    if limits == '1':
        get_sh_goods()

        # 条件判断:条件1
        # 1.查询上海

    # 条件1的结果

    else:
        # 条件判断：其他条件
        # 1.查询全国
        if limits == '2':
            get_national_goods()

        else:
            print("输入错误，请从新输入，程序已退出，请再次运行")
            sys.exit()
mian()
