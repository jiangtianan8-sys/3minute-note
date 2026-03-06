 
action_str = input("请选择希望执行的操作：\n1. 创建名片\n2. 显示全部名片\n3. 查询名片\n4. 修改名片\n5. 删除名片\n请输入数字选择操作：")

#1,2,3 针对名片的操作
if action_str in ["1", "2", "3"]:
    from cards_tools import *
    if action_str == "1":
        create_card()
    elif action_str == "2":
        show_all()
    elif action_str == "3":
        search_card()

# 0 退出系统
elif action_str == "0":
    print("欢迎再次使用名片管理系统！")
    exit()

# 其他内容输入错误，需要提示用户
else:
    print("输入错误，请重新选择操作！")