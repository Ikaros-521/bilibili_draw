# -*- coding: utf-8 -*-
import json
import time
import random
import urllib.request
import urllib.parse
import sqlite3
import tkinter
from tkinter import END, messagebox

# python版本：3.8.12
# 打包 pyinstaller -F 1.py

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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400'
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
    text.insert(tkinter.INSERT, text_str)
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
    if referer[8] == 't':
        # print('解析为动态页面')
        text_str = "解析为动态页面\n"
        text.insert(tkinter.INSERT, text_str)
        text.update()
    else:
        # print('解析为视频页面')
        text_str = "解析为视频页面\n"
        text.insert(tkinter.INSERT, text_str)
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
    dynamic_id = temp2[3]

    # print("dynamic_id=" + dynamic_id)
    text_str = "dynamic_id=" + dynamic_id + "\n"
    text.insert(tkinter.INSERT, text_str)
    text.update()

    if len(dynamic_id) == 0:
        # print("dynamic_id异常，程序终止，请检查您的输入是否有误！")
        text_str = "dynamic_id异常，程序终止，请检查您的输入是否有误！\n"
        text.insert(tkinter.INSERT, text_str)
        text.update()
        base_info = {'ret': False}
        return base_info

    # payload = {'dynamic_id': dynamic_id}
    payload = { 'timezone_offset': '-480', 'id': dynamic_id}
    data = urllib.parse.urlencode(payload)
    # print(data)

    req = urllib.request.urlopen('https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?%s' % data)
    # req = urllib.request.urlopen('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?%s' % data)
    ret = req.read().decode()

    # print(ret)
    json1 = json.loads(ret)
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
    # print(base_info)
    return base_info


# 获取用户信息函数
def get_user_info(base_info):
    global text_str
    global api_type
    # print("开始获取用户信息...")
    text_str = "开始获取用户信息...\n"
    text.insert(tkinter.INSERT, text_str)
    text.update()
    if int(api_type) == 17:
        # 用户输入是否是完整复制动态链接，链接尾部 是否是 ?tab=2
        if referer[-6:-1] == "?tab=":
            base_info["oid"] = referer[23:len(referer) - 6]
        else:
            base_info["oid"] = referer[23:len(referer)]
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

        # print("已获取" + str(len(id_set)) + "个用户的数据...")
        text_str = "已获取" + str(len(id_set)) + "个用户的数据...\n"
        text.insert(tkinter.INSERT, text_str)
        text.update()

    # print("插入一组数据组")

    if end == 1:
        # print("数据获取完毕！\n")
        text_str = "数据获取完毕！\n"
        text.insert(tkinter.INSERT, text_str)
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
                text.insert(tkinter.INSERT, text_str)
                text.update()

        text_str = '\n\n'
        text.insert(tkinter.INSERT, text_str)
        text.update()


# 获取转发用户的数据
def get_repost_user_info(base_info):
    global text_str
    global dynamic_id
    print("开始获取用户信息...")
    text_str = "开始获取用户信息...\n"
    text.insert(tkinter.INSERT, text_str)
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
        url = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id=" + \
              str(dynamic_id) + "&offset=" + str(temp_num)
        req = urllib.request.urlopen(url)
        ret = req.read().decode()

        # print(url)
        # print(ret)

        json1 = json.loads(ret)
        len1 = 0
        if "comments" in ret:
            len1 = len(json1["data"]["comments"])
            # print(len1)
        else:
            print("可获取的数据结束！\n")
            text_str = "可获取的数据结束！\n"
            text.insert(tkinter.INSERT, text_str)
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
        text.insert(tkinter.INSERT, text_str)
        text.update()
        time.sleep(0.5)
    print("数据获取完毕！\n")
    text_str = "数据获取完毕！\n"
    text.insert(tkinter.INSERT, text_str)
    text.update()
    while len(lucky_set) < int(lucky_num):
        num = 0
        if len(id_set) > 1:
            num = random.randint(0, (len(id_set) - 1))
            lucky_set.add(num)
        else:
            print('用户数据不足2个，数据异常，程序结束')
            text_str = "用户数据不足2个，数据异常，程序结束\n"
            text.insert(tkinter.INSERT, text_str)
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
            text.insert(tkinter.INSERT, text_str)
            text.update()

    text_str = '\n\n'
    text.insert(tkinter.INSERT, text_str)
    text.update()


# 关于弹窗提示
def about():
    # 弹出对话框
    messagebox.showinfo(title='关于', message='欢迎使用 UP：Love丶伊卡洛斯 开发的b站抽奖程序 本程序开源免费\n'
                                            '请勿使用非本人仓库下载的程序，否则无法保证安全，未知程序谨慎使用\n'
                                            '本程序目前只支持动态转发、评论的抽奖，视频评论区抽奖有待开发。。。\n'
                                            '使用注意：因为涉及本地文件的操作，如果失败，则需要\"超级管理员\"权限运行\n'
                                            '温馨提示：如果以下内容输错，请重新运行程序，异常数据处理懒得做了0.0')


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

    id_set.clear()
    name_set.clear()
    lucky_set.clear()

    referer = StringVar1.get()
    if len(StringVar2.get()) != 0:
        lucky_num = int(StringVar2.get())
    # print('referer:' + referer)
    # print('lucky_num:' + str(lucky_num))
    if not referer.startswith('https://t.bilibili.com'):
        # print("动态链接地址不正确，请重新输入")
        text_str = "动态链接地址不正确，请重新输入!!!\n"
        text.insert(tkinter.INSERT, text_str)
        text.update()
        return
    if not is_number(lucky_num):
        # print("请输入正确的中奖人数")
        text_str = "请输入正确的中奖人数!!!\n"
        text.insert(tkinter.INSERT, text_str)
        text.update()
        return
    if int(float(lucky_num)) <= 0:
        # print("请输入正确的中奖人数")
        text_str = "请输入正确的中奖人数!!!\n"
        text.insert(tkinter.INSERT, text_str)
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
        text.insert(tkinter.INSERT, text_str)
        text.update()

        # 根据抽奖类型进行抽奖 1评论 0转发
        if int(draw_type) == 1:
            # 获取用户信息并抽取幸运用户
            get_user_info(base_info)
        else:
            get_repost_user_info(base_info)

        # 关闭游标
        cur.close()
        # 断开数据库连接
        con.close()


# 清空输入框按钮点击
def clear_in():
    e2.delete(0, END)
    e3.delete(0, END)


# 清空输出框按钮点击
def clear_out():
    text.delete(0.0, tkinter.END)


window = tkinter.Tk()
window.title("b站动态抽奖程序")
window.geometry("1000x900+200+100")
# 菜单栏
menu = tkinter.Menu(window)
# Open放在菜单栏中，就是装入容器
menu.add_command(label='关于', command=about)
# 创建菜单栏完成后，配置让菜单栏menu显示出来
window.config(menu=menu)

# 创建一个主frame，长在主window窗口上
frame = tkinter.Frame(window)
frame.pack()

# 创建第二层框架frame，长在主框架frame上面
# 上
frame_t = tkinter.Frame(frame)
# 下
frame_b = tkinter.Frame(frame)

# frame_t.pack(side=tkinter.TOP)
# frame_b.pack(side=tkinter.BOTTOM)
frame_t.grid(row=0, column=0)
frame_b.grid(row=1, column=0)

# 创建标签
l1 = tkinter.Label(frame_t, text='抽奖类型：', width=10, font=('microsoft yahei', 16))
l2 = tkinter.Label(frame_t, text='动态链接：', width=10, font=('microsoft yahei', 16))
l3 = tkinter.Label(frame_t, text='中奖人数：', width=10, font=('microsoft yahei', 16))

radio = tkinter.IntVar()
radio.set(1)
radio1 = tkinter.Radiobutton(frame_t, text="评论", font=('microsoft yahei', 16), width=10, justify='left', value=1,
                             variable=radio, command=radio_click, padx=1)
radio1.grid(row=0, column=1)
radio2 = tkinter.Radiobutton(frame_t, text="转发", font=('microsoft yahei', 16), width=10, justify='left', value=0,
                             variable=radio, command=radio_click, padx=1)
radio2.grid(row=0, column=2)
button1 = tkinter.Button(frame_t, text="开始抽奖", command=start_btn, font=('microsoft yahei', 12), width=16, height=1)
button1.grid(row=0, column=3)

StringVar1 = tkinter.StringVar()
StringVar1.set("")
e2 = tkinter.Entry(frame_t, show=None, width=42, textvariable=StringVar1, font=('microsoft yahei', 16))
StringVar2 = tkinter.StringVar()
StringVar2.set("1")
e3 = tkinter.Entry(frame_t, show=None, width=42, textvariable=StringVar2, font=('microsoft yahei', 16))

button2 = tkinter.Button(frame_t, text="清空输入框", command=clear_in, font=('microsoft yahei', 12), width=16, height=1)
button2.grid(row=1, column=2)
button3 = tkinter.Button(frame_t, text="清空输出框", command=clear_out, font=('microsoft yahei', 12), width=16, height=1)
button3.grid(row=2, column=2)

l1.grid(row=0, column=0)
l2.grid(row=1, column=0)
e2.grid(row=1, column=1)
l3.grid(row=2, column=0)
e3.grid(row=2, column=1)

# 创建滚动条
scroll = tkinter.Scrollbar(frame_b)
text = tkinter.Text(frame_b, font=('microsoft yahei', 14), width=80, height=30)
# side放到窗体的那一侧
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
text.pack(side=tkinter.LEFT, fill=tkinter.Y)
# text.grid(row=3, column=0)
# scroll.grid(row=3, column=1)
# 关联
scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)

window.mainloop()

