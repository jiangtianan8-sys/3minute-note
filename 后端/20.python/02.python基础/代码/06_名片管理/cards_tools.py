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

    #1. 提示用户输入要查询的姓名
    find_name = input("请输入要查询的姓名：")
    #2. 遍历名片列表，查询要查找的姓名，如果没有找到，需要提示用户
    for card_dict in card_list:
        if card_dict["name"] == find_name:
            print("姓名\t\t电话\t\tQQ\t\t邮箱")
            print("=" * 50)
            print("%s\t\t%s\t\t%s\t\t%s" % (card_dict["name"],
                                            card_dict["phone"],
                                            card_dict["qq"],
                                            card_dict["email"]))
            
            # 针对找到的名片记录执行修改和删除的操作
            deal_card(card_dict)
            break
    else:
        print("抱歉没有找到 %s 的名片！" % find_name)

"""
修改和删除名片
"""
def deal_card(find_dict):
    print(find_dict)
    action_str = input("请选择要执行的操作：" \
    "1. 修改 2. 删除 0. 返回上级菜单")
    if action_str == "1":
        find_dict["name"] = input("请输入姓名：")
        find_dict["phone"] = input("请输入电话：")
        find_dict["qq"] = input("请输入QQ：")
        find_dict["email"] = input("请输入邮箱：")
        print("修改名片成功！")
    elif action_str == "2":
        card_list.remove(find_dict)
        print("删除名片成功！") 