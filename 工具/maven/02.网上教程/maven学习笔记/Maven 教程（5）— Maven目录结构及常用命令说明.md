前面提到的部分知识有涉及到 Maven 目录结构与 Maven 常用的一些命令，在这里专门给大家做个简单的介绍。

1、Maven 目录结构说明

Maven 总体目录结构如下图： 

![](assets/Maven%20教程（5）—%20Maven目录结构及常用命令说明/file-20251122083009844.png)

bin 目录：该目录包含了 mvn 运行的脚本，这些脚本用来配置 java 命令，准备好 classpath 和相关的 Java 系统属性，然后执行 Java 命令。

boot 目录：该目录只包含一个文件，以 maven3.5.2 为例，该文件为 plexus-classworlds-2.5.2.jar。plexus-classworlds 是一个类加载器框架，相对于默认的 java 类加载器，它提供了更丰富的语法以方便配置，Maven 使用该框架加载自己的类库。更多关于 classworlds 的信息请参考 [http://classworlds.codehaus.org/](http://classworlds.codehaus.org/)。对于一般的 Maven 用户来说，不必关心该文件。

conf 目录：该目录包含了一个非常重要的文件 settings.xml，Maven 的核心配置文件。

lib 目录：该目录包含了所有 Maven 运行时需要的 Java 类库，Maven 本身是分模块开发的，因此用户能看到诸如 mavn-core-3.2.2.jar、maven-model-3.2.2.jar 之类的文件，此外这里还包含一些 Maven 用到的第三方依赖如 commons-cli-1.2.jar、commons-lang-2.6.jar 等等。

2、Maven 常用命令说明

- mvn clean：表示运行清理操作（会默认把 target 文件夹中的数据清理）；
- mvn clean compile：表示先运行清理之后运行编译，会将代码编译到 target 文件夹中；
- mvn clean test：运行清理和测试；
- mvn clean package：运行清理和打包；
- mvn clean install：运行清理和安装，会将打好的包安装到本地仓库中，以便其他的项目可以调用；
- mvn clean deploy：运行清理和发布（发布到私服上面）。

上面的命令大部分都是连写的，大家也可以拆分分别执行，这是活的，看个人喜好以及使用需求，Eclipse Run As 对 maven 项目会提供常用的命令。

3、特别说明

自从 Maven3 出来之后，后续的 Eclipse IDE 中往往都集成了 Maven 项目管理工具，所以这里不会特定给大家去说怎么在 Eclipse 中安装 Maven 插件，在后续的介绍中可能会提到部分如何在 Eclipse 中配置我们自己的 Maven，这都是比较简单的内容，大家完全可以自己摸索。

祝大家都能够掌握这个好用的项目管理工具，如果喜欢关注技术的朋友还可以了解了解其他类似于这方面的技术以及框架，给大家举个简单的例子：Gradle。至于 Maven 之前的 Make、Ant 傻傻啥的，我觉得是没必要再去学习了，也基本不会用到，现实一点，吃饭的东西最要紧。

来源： [https://blog.csdn.net/liupeifeng3514/article/details/79543159](https://blog.csdn.net/liupeifeng3514/article/details/79543159)
