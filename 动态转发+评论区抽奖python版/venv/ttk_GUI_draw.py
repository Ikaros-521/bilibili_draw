# -*- coding: utf-8 -*-
import json
import time
import random
import requests
import sqlite3
import tkinter
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledText

# python版本：3.8.5
# 打包 pyinstaller -F 1.py
# ttk打包 使用auto-py-to-exe，--paths加载ttkbootstrap路径，打包成文件夹

# 获取抽奖类型
global draw_type
global referer
# 中奖人数
global lucky_num
global dynamic_id
global text_str
# 动态类型
global api_type

api_type = 11
draw_type = 1
dynamic_id = ""
# 打印文本框
text_str = ''

# 数据集合
id_set = set()
name_set = set()
lucky_set = set()

headers1 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Referer': 'https://t.bilibili.com',
    'origin': 'https://t.bilibili.com',
    # 'cookie': 'l=v',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 '
                  'Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400 '
}


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


# 配置数据库
def config_db():
    global con, cur
    global text_str
    # print("开始创建数据库...")
    text_str = "开始创建数据库...\n"
    text.insert(END, text_str)
    text.update()
    con = sqlite3.connect("user_data.db")
    cur = con.cursor()
    # 创建表user
    sql = "CREATE TABLE IF NOT EXISTS user(mid TEXT PRIMARY KEY,uname TEXT,message TEXT)"
    cur.execute(sql)
    # 情况表数据
    sql = "delete from user"
    cur.execute(sql)


# 获取oid、转发数、评论数函数
def get_oid():
    global text_str
    global dynamic_id
    global api_type
    global text

    if 'opus' in referer:
        text_str = "解析为动态页面\n"
        text.insert(END, text_str)
        text.update()
    elif referer[8] == 't':
        # print('解析为动态页面')
        text_str = "解析为动态页面\n"
        text.insert(END, text_str)
        text.update()
    else:
        # print('解析为视频页面')
        text_str = "解析为视频页面\n"
        text.insert(END, text_str)
        text.update()

    tab_type = "2"

    # 用户输入是否是完整复制动态链接，链接尾部 是否是 ?tab=2
    # if referer[-6:-1] == "?tab=":
    #     dynamic_id = referer[23:len(referer) - 6]
    #     tab_type = referer[-1]
    # else:
    #     dynamic_id = referer[23:len(referer)]

    temp = referer.split('?')
    temp2 = temp[0].split('/')
    dynamic_id = temp2[-1].strip()

    # print("dynamic_id=" + dynamic_id)
    text_str = "dynamic_id=" + dynamic_id + "\n"
    text.insert(END, text_str)
    text.update()

    if len(dynamic_id) == 0:
        # print("dynamic_id异常，程序终止，请检查您的输入是否有误！")
        text_str = "dynamic_id异常，程序终止，请检查您的输入是否有误！\n"
        text.insert(END, text_str)
        text.update()
        base_info = {'ret': False}
        return base_info

    API_URL = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id=' + dynamic_id
    ret = requests.get(API_URL, headers=headers1)
    json1 = ret.json()
    print(ret.text)
    # json1 = json.loads(ret)
    oid = json1["data"]["item"]["basic"]["comment_id_str"]
    repost = json1["data"]["item"]["modules"]["module_stat"]["forward"]["count"]
    # oid = json1["data"]["card"]["desc"]["rid"]
    # repost = json1["data"]["card"]["desc"]["repost"]

    comment = 0
    # 非视频动态
    if tab_type == "2":
        comment = json1["data"]["item"]["modules"]["module_stat"]["comment"]["count"]
    else:
        comment = 0
    # 判断动态类型
    api_type = json1["data"]["item"]["basic"]["comment_type"]
    # print("oid=" + str(oid))
    base_info = {'ret': True, 'oid': oid, 'repost': repost, 'comment': comment}
    print(base_info)
    return base_info


# 获取用户信息函数
def get_user_info(base_info):
    global text_str
    global api_type
    global text

    # print("开始获取用户信息...")
    text_str = "开始获取用户信息...\n"
    text.insert(END, text_str)
    text.update()
    end = 0
    for i in range(int((base_info["comment"] - 1) / 20) + 1):
        if i == 0:
            url = "https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=" + str(api_type) + \
                  "&oid=" + str(base_info["oid"]) + "&mode=3&plat=1&_=" + str((int(round(time.time() * 1000)) + 1))
        else:
            url = "https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=" + str(i + 1) + "&type=" + str(api_type) + \
                  "&oid=" + str(base_info["oid"]) + "&mode=3&plat=1&_=" + str((int(round(time.time() * 1000)) + 1))

        if i == int((base_info["comment"] - 1) / 20):
            end = 1
        get_data(url, end)
        time.sleep(0.5)


# 获取数据函数
def get_data(url, end):
    print(url)
    global text_str
    global text

    ret = requests.get(url, headers=headers1)
    try:
        json1 = ret.json()
    except Exception as e:
        text_str = str(e) + "\n调用api.bilibili.com/x/v2/reply/main 接口返回数据JSON化失败，可尝试重试，若仍不行，则可能是接口变更导致\n"
        text.insert(END, text_str)
        text.update()
        return

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

        # print("已获取" + str(len(id_set)) + "个用户的数据...")
        text_str = "已获取" + str(len(id_set)) + "个用户的数据...\n"
        text.insert(END, text_str)
        text.update()

    # print("插入一组数据组")

    if end == 1:
        # print("数据获取完毕！\n")
        text_str = "数据获取完毕！\n"
        text.insert(END, text_str)
        text.update()
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
                # print('\nid:%s  昵称:%s  评论:%s' % (row[0], row[1], row[2]))
                text_str = '\nid:%s  昵称:%s  评论:%s' % (row[0], row[1], row[2]) + '\n'
                text.insert(END, text_str)
                text.update()

        text_str = '\n\n'
        text.insert(END, text_str)
        text.update()


# 获取转发用户的数据
def get_repost_user_info(base_info):
    global text_str
    global dynamic_id
    global text

    print("开始获取用户信息...")
    text_str = "开始获取用户信息...\n"
    text.insert(END, text_str)
    text.update()

    # 用户输入是否是完整复制动态链接，链接尾部 是否是 ?tab=2
    # if referer[-6:-1] == "?tab=":
    #     dynamic_id = referer[23:len(referer) - 6]
    # else:
    #     dynamic_id = referer[23:len(referer)]

    temp = referer.split('?')
    temp2 = temp[0].split('/')
    dynamic_id = temp2[3]

    temp_num = 0
    # 根据转发数进行循环
    while temp_num < int(base_info["repost"]):
        API_URL = 'https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id=' + \
                  str(dynamic_id) + "&offset=" + str(temp_num)
        ret = requests.get(API_URL, headers=headers1)

        # print(ret.text)
        try:
            json1 = ret.json()
        except (KeyError, TypeError, IndexError) as e:
            text_str = e + "\n调用api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost " \
                           "接口返回数据JSON化失败，可尝试重试，若仍不行，则可能是接口变更导致\n "
            text.insert(END, text_str)
            text.update()
            return

        ret = ret.text

        # print(url)
        # print(ret)

        len1 = 0
        if "comments" in ret:
            len1 = len(json1["data"]["comments"])
            # print("comments=" + str(len1))
        else:
            print("可获取的数据结束！\n")
            text_str = "可获取的数据结束！\n"
            text.insert(END, text_str)
            text.update()
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
        # print("已获取" + str(len(id_set)) + "个用户的数据...")
        text_str = "已获取" + str(len(id_set)) + "个用户的数据...\n"
        text.insert(END, text_str)
        text.update()
        time.sleep(0.5)
    print("数据获取完毕！\n")
    text_str = "数据获取完毕！\n"
    text.insert(END, text_str)
    text.update()
    while len(lucky_set) < int(lucky_num):
        num = 0
        if len(id_set) > 1:
            num = random.randint(0, (len(id_set) - 1))
            lucky_set.add(num)
        else:
            print('用户数据不足2个，数据异常，程序结束')
            text_str = "用户数据不足2个，数据异常，程序结束\n"
            text.insert(END, text_str)
            text.update()
            return
    for i in range(int(lucky_num)):
        lucky_list = list(lucky_set)
        # print("lucky_num=" + str(lucky_list[i]))
        sql = "select * from user limit " + str(lucky_list[i]) + ",1"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print('\nid:%s  昵称:%s  评论:%s' % (row[0], row[1], row[2]))
            text_str = '\nid:%s  昵称:%s  评论:%s' % (row[0], row[1], row[2]) + '\n'
            text.insert(END, text_str)
            text.update()

    text_str = '\n\n'
    text.insert(END, text_str)
    text.update()


# 单选框点击
def radio_click():
    global draw_type
    draw_type = radio.get()
    # print("draw_type:" + str(draw_type))


# 开始抽奖按钮点击
def start_btn():
    global referer
    global lucky_num
    global text_str
    global text

    id_set.clear()
    name_set.clear()
    lucky_set.clear()

    referer = StringVar1.get()
    if len(StringVar2.get()) != 0:
        lucky_num = int(StringVar2.get())
    # print('referer:' + referer)
    # print('lucky_num:' + str(lucky_num))
    if not referer.startswith('https://t.bilibili.com') and not referer.startswith('https://www.bilibili.com/opus'):
        # print("动态链接地址不正确，请重新输入")
        text_str = "动态链接地址不正确，请重新输入!!!\n"
        text.insert(END, text_str)
        text.update()
        return
    if not is_number(lucky_num):
        # print("请输入正确的中奖人数")
        text_str = "请输入正确的中奖人数!!!\n"
        text.insert(END, text_str)
        text.update()
        return
    if int(float(lucky_num)) <= 0:
        # print("请输入正确的中奖人数")
        text_str = "请输入正确的中奖人数!!!\n"
        text.insert(END, text_str)
        text.update()
        return

    # 配置数据库
    config_db()
    # 获取oid、转发数、评论数
    base_info = get_oid()

    if base_info["ret"]:
        # print("oid=" + str(base_info["oid"]))
        # print("转发数=" + str(base_info["repost"]))
        # print("评论数=" + str(base_info["comment"]))

        text_str = "oid=" + str(base_info["oid"]) + "\n"
        text_str = text_str + "转发数=" + str(base_info["repost"]) + "\n"
        text_str = text_str + "评论数=" + str(base_info["comment"]) + "\n"
        text.insert(END, text_str)
        text.update()

        # 根据抽奖类型进行抽奖 1评论 0转发
        if int(draw_type) == 1:
            if int(lucky_num) > int(base_info["comment"]):
                text_str = "请输入正确的中奖人数!!!\n"
                text.insert(END, text_str)
                text.update()
                # 关闭游标
                cur.close()
                # 断开数据库连接
                con.close()
                return
            # 获取用户信息并抽取幸运用户
            get_user_info(base_info)
        else:
            if int(lucky_num) > int(base_info["repost"]):
                text_str = "请输入正确的中奖人数!!!\n"
                text.insert(END, text_str)
                text.update()
                # 关闭游标
                cur.close()
                # 断开数据库连接
                con.close()
                return
            get_repost_user_info(base_info)

        # 关闭游标
        cur.close()
        # 断开数据库连接
        con.close()


app = ttk.Window(title='b站动态抽奖程序', themename='litera', iconphoto='', size=[900, 600], position=None, minsize=None)
root = ttk.Frame(app, padding=10)
style = ttk.Style()

tframe = ttk.Frame(root)
tframe.pack(padx=3, fill=X, side=TOP)

bframe = ttk.Frame(root)
bframe.pack(padx=7, fill=BOTH, side=BOTTOM)

lframe = ttk.Frame(tframe)
lframe.pack(padx=8, side=LEFT, fill=BOTH, expand=YES)

rframe = ttk.Frame(tframe, padding=5)
rframe.pack(padx=2, side=RIGHT, fill=BOTH, expand=YES)

btframe = ttk.Frame(root)
btframe.pack(fill=BOTH, side=TOP)

text = ScrolledText(master=btframe, height=100, width=50, autohide=True, padding=10)
text.pack(side=LEFT, anchor=NW, pady=5, fill=BOTH, expand=YES)

input_group = ttk.Labelframe(
    master=lframe, text="配置输入", padding=10
)
input_group.pack(fill=BOTH, expand=YES)

l1 = ttk.Label(input_group, text="动态链接：")
l1.grid(row=0, column=0)

load = tkinter.StringVar()

StringVar1 = ttk.StringVar()
StringVar1.set("")
entry = ttk.Entry(input_group, width=50, textvariable=StringVar1)
entry.grid(row=0, column=1, padx='4px', pady='5px')
entry.insert(END, "例如：https://t.bilibili.com/123456789012345678")

l2 = ttk.Label(input_group, text="中奖人数：")
l2.grid(row=1, column=0)

StringVar2 = ttk.StringVar()
StringVar2.set("")
spinbox = ttk.Spinbox(master=input_group, from_=1, to=500, textvariable=StringVar2)
spinbox.grid(row=1, column=1, sticky='w', padx='4px', pady='5px')
spinbox.set(1)

rb_group = ttk.Labelframe(
    rframe, text="抽奖类型", padding=10
)
rb_group.pack(fill=X, pady=10, side=TOP)

radio = ttk.IntVar()
radio1 = ttk.Radiobutton(rb_group, text="评论", value=1, variable=radio, command=radio_click)
radio1.pack(side=LEFT, expand=YES, padx=5)
radio1.invoke()

radio2 = ttk.Radiobutton(rb_group, text="转发", value=0, variable=radio, command=radio_click)
radio2.pack(side=LEFT, expand=YES, padx=5)

cb = ttk.Button(
    master=rframe,
    text="开始抽奖",
    bootstyle=(SUCCESS, TOOLBUTTON),
    command=start_btn
)
# 调用与按钮关联的命令
# cb.invoke()
cb.pack(fill=X, pady=5)

lframe_inner = ttk.Frame(lframe)
lframe_inner.pack(fill=BOTH, expand=YES, padx=10)

root.pack(fill=BOTH, expand=YES)
app.mainloop()
