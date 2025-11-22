1、Eclipse创建Maven项目

使用Eclipse创建一个Maven项目非常的简单，选择菜单项File>New>Other（也可以在项目结构空白处右击鼠标键），在弹出的对话框中选择Maven下的Maven Project，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084259830.png)

然后点击Next按钮，Next按钮，选择一个Archetype指定我们要创建的项目类型。我们选择普通的Java项目“maven-archetype-quickstart”，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084312723.png)

再点击Next按钮，输入Group Id、Artifact Id、Version、Package，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084324401.png)

这里要注意一个问题，当我们输入Group Id和Artifact Id时Eclipse会自动给我们在Package后面组成包名，要注意包名不能大写的问题，建议Group Id全部使用小写，Artifact Id如果是大写就自己手动改成自己想要的包名，这样就不会违背Java包命名规范了。

然后点击Finish按钮，Maven项目就创建完成了。

2、Eclipse运行mvn命令

在Maven项目或者pom.xml上右击，在弹出的快捷菜单中选择Run As，就能看到常见的Maven命令，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084337543.png)

选择要执行的命令就能执行相应的操作了，Eclipse会在控制台输出构建信息。

如果默认选项中没有我们要执行的命令怎么办？选择Maven build来自定义我们要执行的命令，在弹出对话框的Goals中输入我们要执行的命令，比如clean install，设置一下Name说明含义，单击Run运行即可。Eclipse会给我们保存这次设置，可以在Run Configurations…中找到，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084349756.png)

保存的记录，如图： 

![0](https://note.youdao.com/yws/res/2304/26F9E1F9BA4446F483377B8B945AF11E)