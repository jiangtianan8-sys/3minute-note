import cards_tools

while True:
  # TODO 显示功能菜单
  cards_tools.show_menu()

  action_str = input("请选择希望执行的操作：")

  #1,2,3 针对名片的操作
  if action_str in ["1", "2", "3"]:
      from cards_tools import *
      if action_str == "1":
          cards_tools.create_card()
      elif action_str == "2":
          cards_tools.show_all()
      elif action_str == "3":
          cards_tools.search_card()

  # 0 退出系统
  elif action_str == "0":
      print("欢迎再次使用名片管理系统！")
      break

  # 其他内容输入错误，需要提示用户
  else:
      print("输入错误，请重新选择操作！")