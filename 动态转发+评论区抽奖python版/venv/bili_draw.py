# -*- coding: utf-8 -*-
import json
import time
import random
import urllib.request
import urllib.parse
import sqlite3

# 打包 venv\Scripts\pyinstaller.exe -F 1.py

print("*********************************************************************************")
print("***  欢迎使用 UP：Love丶伊卡洛斯 开发的b站抽奖程序 本程序开源免费          ")
print("***  请勿使用非本人仓库下载的程序，否则无法保证安全，未知程序谨慎使用        ")
print("***  本程序目前只支持动态转发、评论的抽奖，视频评论区抽奖有待开发。。。           ")
print("***  使用注意：因为涉及本地文件的操作，如果失败，则需要\"超级管理员\"权限运行   ")
print("***  温馨提示：如果以下内容输错，请重新运行程序，异常数据处理懒得做了0.0     ")
print("*********************************************************************************")


# 获取抽奖类型
global draw_type
global referer
global lucky_num
have_pic = 1


# 字符串是否是数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


while True:
    draw_type = input("请输入抽奖类型（1评论 0转发）：")
    if draw_type != '0' and draw_type != '1':
        print("请输入0或1")
        continue
    referer = input("请输入动态链接：")
    if not referer.startswith('https://t.bilibili.com'):
        print("动态链接地址不正确，请重新输入")
        continue
    lucky_num = input("请输入中奖人数：")
    if not is_number(lucky_num):
        print("请输入正确的中奖人数")
        continue
    if int(float(lucky_num)) > 0:
        break
    else:
        print("请输入正确的中奖人数")

id_set = set()
name_set = set()
lucky_set = set()

headers1 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Referer': referer,
    'origin': 'https://t.bilibili.com',
    # 'cookie': 'l=v',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400'
}


# 配置数据库
def config_db():
    global con, cur
    con = sqlite3.connect("user_data.db")
    cur = con.cursor()
    # 创建表user
    sql = "CREATE TABLE IF NOT EXISTS user(mid TEXT PRIMARY KEY,uname TEXT,message TEXT)"
    cur.execute(sql)
    # 情况表数据
    sql = "delete from user"
    cur.execute(sql)


# 获取oid、转发数、评论数函数
def get_oid(referer):
    if (referer[8] == 't'):
        print('解析为动态页面')
    else:
        print('解析为视频页面')

    dynamic_id = referer[23:len(referer) - 6]
    print("dynamic_id=" + dynamic_id)

    if len(dynamic_id) == 0:
        print("dynamic_id异常，程序终止，请检查您的输入是否有误！")
        base_info = {'ret': False}
        return base_info

    payload = {'dynamic_id': dynamic_id}
    data = urllib.parse.urlencode(payload)

    req = urllib.request.urlopen('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?%s' % data)
    ret = req.read().decode()

    # print(ret)
    json1 = json.loads(ret)
    oid = json1["data"]["card"]["desc"]["rid"]
    repost = json1["data"]["card"]["desc"]["repost"]

    tab_type = referer[-1]
    comment = 0
    # 非视频动态
    if tab_type == "2":
        comment = json1["data"]["card"]["desc"]["comment"]
    else:
        comment = 0
    # 判断动态类型
    type = json1["data"]["card"]["desc"]["type"]
    global have_pic
    if int(type) == 2:
        have_pic = 1
    else:
        have_pic = 0
    # print("oid=" + str(oid))
    base_info = {'ret': True, 'oid': oid, 'repost': repost, 'comment': comment}
    return base_info


# 获取用户信息函数
def get_user_info(referer, base_info):
    print("开始获取用户信息...")
    if int(have_pic) == 1:
        type = 11
    else:
        type = 17
        base_info["oid"] = referer[23:len(referer) - 6]
    end = 0
    for i in range(int((base_info["comment"] - 1) / 20) + 1):
        if i == 0:
            url = "https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=" + str(type) + \
                  "&oid=" + str(base_info["oid"]) + "&mode=3&plat=1&_=" + str((int(round(time.time() * 1000)) + 1));
        else:
            url = "https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=" + str(i + 1) + "&type=" + str(type) + \
                  "&oid=" + str(base_info["oid"]) + "&mode=3&plat=1&_=" + str((int(round(time.time() * 1000)) + 1));

        if i == int((base_info["comment"] - 1) / 20):
            end = 1
        get_data(url, end)
        time.sleep(0.5)


# 获取数据函数
def get_data(url, end):
    req = urllib.request.urlopen(url)
    ret = req.read().decode()
    # print(ret)
    json1 = json.loads(ret)
    # json1["data"]["replies"]有可能为null
    if json1["data"]["replies"] is not None:
        len1 = len(json1["data"]["replies"])
        for i in range(len1):
            mid = json1["data"]["replies"][i]["member"]["mid"]
            uname = json1["data"]["replies"][i]["member"]["uname"]
            message = json1["data"]["replies"][i]["content"]["message"]

            # 数据插入集合
            # name_set.add(uname)
            id_set.add(mid)
            # 数据插入数据库
            sql = "replace into user(mid, uname, message) values (?, ?, ?)"
            cur.execute(sql, (mid, uname, message))
            con.commit()

        print("已获取" + str(len(id_set)) + "个用户的数据...")

    # print("插入一组数据组")

    if end == 1:
        print("数据获取完毕！\n")
        # print(name_set)
        # print(id_set)
        while len(lucky_set) < int(lucky_num):
            num = random.randint(0, (len(id_set) - 1))
            lucky_set.add(num)
            # print(lucky_set)
        # id_list = list(id_set)
        # name_list = list(name_set)
        # for i in range(int(lucky_num)):
        #     print("昵称:" + name_list[i] + "  id:" + id_list[i] + "\n")

        for i in range(int(lucky_num)):
            lucky_list = list(lucky_set)
            # print("lucky_num=" + str(lucky_list[i]))
            sql = "select * from user limit " + str(lucky_list[i]) + ",1"
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print('\nid:%s  昵称:%s  评论:%s' % (row[0], row[1], row[2]))


# 获取转发用户的数据
def get_repost_user_info(referer, base_info):
    print("开始获取用户信息...")
    dynamic_id = referer[23:len(referer) - 6]
    temp_num = 0
    # 根据转发数进行循环
    while temp_num < int(base_info["repost"]):
        url = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id=" + \
              str(dynamic_id) + "&offset=" + str(temp_num);
        req = urllib.request.urlopen(url)
        ret = req.read().decode()

        # print(ret)

        json1 = json.loads(ret)
        len1 = 0
        if "comments" in ret:
            len1 = len(json1["data"]["comments"])
            # print(len1)
        else:
            print("可获取的数据结束！\n")
            break
        for i in range(len1):
            uid = json1["data"]["comments"][i]["uid"]
            uname = json1["data"]["comments"][i]["uname"]
            comment = json1["data"]["comments"][i]["comment"]

            # 数据插入集合
            # name_set.add(uname)
            id_set.add(uid)
            # 数据插入数据库
            sql = "replace into user(mid, uname, message) values (?, ?, ?)"
            cur.execute(sql, (uid, uname, comment))
            con.commit()

        temp_num += 20
        print("已获取" + str(len(id_set)) + "个用户的数据...")
        time.sleep(0.5)
    print("数据获取完毕！\n")
    while len(lucky_set) < int(lucky_num):
        num = 0
        if len(id_set) > 1:
            num = random.randint(0, (len(id_set) - 1))
            lucky_set.add(num)
        else:
            print('用户数据不足2个，数据异常，程序结束')
            return
    for i in range(int(lucky_num)):
        lucky_list = list(lucky_set)
        # print("lucky_num=" + str(lucky_list[i]))
        sql = "select * from user limit " + str(lucky_list[i]) + ",1"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print('\nid:%s  昵称:%s  评论:%s' % (row[0], row[1], row[2]))


# 配置数据库
config_db()
# 获取oid、转发数、评论数
base_info = get_oid(referer)

if base_info["ret"]:
    print("oid=" + str(base_info["oid"]))
    print("转发数=" + str(base_info["repost"]))
    print("评论数=" + str(base_info["comment"]))

    # 根据抽奖类型进行抽奖
    if (int(draw_type) == 1):
        # 获取用户信息并抽取幸运用户
        get_user_info(referer, base_info)
    else:
        get_repost_user_info(referer, base_info)

    # 关闭游标
    cur.close()
    # 断开数据库连接
    con.close()

    print("\n程序运行完毕！")
    quit = 0
    while quit != "1":
        quit = input("是否关闭程序(是1，否0)：")
