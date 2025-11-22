1、Eclipse 创建 Maven 项目

使用 Eclipse 创建一个 Maven 项目非常的简单，选择菜单项 File>New>Other（也可以在项目结构空白处右击鼠标键），在弹出的对话框中选择 Maven 下的 Maven Project，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084259830.png)

然后点击 Next 按钮，Next 按钮，选择一个 Archetype 指定我们要创建的项目类型。我们选择普通的 Java 项目“maven-archetype-quickstart”，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084312723.png)

再点击 Next 按钮，输入 Group Id、Artifact Id、Version、Package，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084324401.png)

这里要注意一个问题，当我们输入 Group Id 和 Artifact Id 时 Eclipse 会自动给我们在 Package 后面组成包名，要注意包名不能大写的问题，建议 Group Id 全部使用小写，Artifact Id 如果是大写就自己手动改成自己想要的包名，这样就不会违背 Java 包命名规范了。

然后点击 Finish 按钮，Maven 项目就创建完成了。

2、Eclipse 运行 mvn 命令

在 Maven 项目或者 pom.xml 上右击，在弹出的快捷菜单中选择 Run As，就能看到常见的 Maven 命令，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084337543.png)

选择要执行的命令就能执行相应的操作了，Eclipse 会在控制台输出构建信息。

如果默认选项中没有我们要执行的命令怎么办？选择 Maven build 来自定义我们要执行的命令，在弹出对话框的 Goals 中输入我们要执行的命令，比如 clean install，设置一下 Name 说明含义，单击 Run 运行即可。Eclipse 会给我们保存这次设置，可以在 Run Configurations…中找到，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084349756.png)

保存的记录，如图： 

![](assets/Maven%20教程（8）—%20Eclipse创建Maven项目运行mvn命令/file-20251122084517980.png)
