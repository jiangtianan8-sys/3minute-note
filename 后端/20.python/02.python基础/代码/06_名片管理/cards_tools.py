# 所有名片记录的列表
card_list = []

"""
显示菜单
"""
def show_menu():
    print("*" * 50)
    print("欢迎使用【名片管理系统】V1.0")
    print("")
    print("1. 创建名片")
    print("2. 显示全部名片")
    print("3. 查询名片")
    print("")
    print("0. 退出系统")
    print("*" * 50)

"""
创建名片
"""
def create_card():
    print("-" * 50)
    print("创建名片")

    #1. 提示用户输入名片信息
    name_str = input("请输入姓名：")
    phone_str = input("请输入电话：")
    qq_str = input("请输入QQ：")
    email_str = input("请输入邮箱：")
    #2. 将名片信息保存到一个字典中
    card_dict = {"name": name_str,
                 "phone": phone_str,
                 "qq": qq_str,
                 "email": email_str}
    #3. 将名片字典添加到名片列表中
    card_list.append(card_dict)
    #4. 提示用户添加成功
    print("添加 %s 的名片成功！" % name_str)

"""
显示全部名片
"""
def show_all():
    print("-" * 50)
    print("显示全部名片")
    #1. 判断是否存在名片记录，如果没有，提示用户并且返回
    if len(card_list) == 0:
        print("当前没有任何名片记录，请使用创建功能添加名片！")
        return
    #2. 打印表头
    for name in ["姓名", "电话", "QQ", "邮箱"]:
        print(name, end="\t\t")
    print("")
    print("=" * 50)
    #3. 遍历名片列表依次输出字典信息
    for card_dict in card_list:
        print("%s\t\t%s\t\t%s\t\t%s" % (card_dict["name"],
                                        card_dict["phone"],
                                        card_dict["qq"],
                                        card_dict["email"]))  

"""
查询名片
"""
def search_card():
    print("-" * 50)
    print("查询名片")