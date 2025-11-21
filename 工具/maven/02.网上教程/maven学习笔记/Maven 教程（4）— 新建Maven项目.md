我们以简单的 helloworld 来作为入门的实例，有些人说掌握了 helloworld 你就掌握了这门技术的一半了，对于 maven 来说，你掌握 helloworld，你可能还稀里糊涂的。

1、从 maven 模板创建一个项目

在命令提示符（Windows）中，浏览到要创建 Java 项目的文件夹。键入以下命令：

来源： [https://blog.csdn.net/liupeifeng3514/article/details/79542203](https://blog.csdn.net/liupeifeng3514/article/details/79542203)

mvn archetype:generate -DgroupId={project-packaging} -DartifactId={project-name} -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

1

project-packaging：项目包名 

project-name：项目名称

这告诉 Maven 来从 maven-archetype-quickstart 模板创建 Java 项目。如果忽视 archetypeArtifactId 选项，一个巨大的 Maven 模板列表将列出。

例如，这里的工作目录是 D:\workspace_maven，执行命令过程时间可能比较久，看个人的网络状况。 

![](assets/Maven%20教程（4）—%20新建Maven项目/file-20251121155850931.png)

在上述情况下，一个新的 Java 项目命名 “HelloWorld”, 而整个项目的目录结构会自动创建。

注意：有少数人说 mvn archetype:generate 命令未能生成项目结构。 如果您有任何类似的问题，不用担心，只需跳过此步骤，手动创建文件夹。

我使用的命令：

mvn archetype:generate -DgroupId=com.lpf.mvn -DartifactId=HelloWorld -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

1

2、Maven 项目目录布局

- src/main/java：用来存放源代码
- src/main/resources：用来存放源代码的资源文件
- src/test/java：用来存放单元测试代码
- src/test/resources：用来存放测试代码的资源文件

3、在 Eclipse IDE 中使用我们的项目

为了使它成为一个 Eclipse 项目，进入到 “HelloWorld” 项目目录，键入以下命令： 

![](assets/Maven%20教程（4）—%20新建Maven项目/file-20251121155911005.png)

执行以上命令后，它自动下载更新相关资源和配置信息（需要等待一段时间），并产生 Eclipse IDE 所要求的所有项目文件。要导入项目到 Eclipse IDE 中：

选择 “File -> Import… -> General-> Existing Projects into Workspace”，将“HelloWord 项目导入到 Eclipse 中”。

1

2

项目导入到 Eclipse IDE 中，如图： 

![](assets/Maven%20教程（4）—%20新建Maven项目/file-20251121155924532.png)

4、更新 POM 文件

默认的 pom.xml 太简单了，很多时候，你需要添加编译器插件来告诉 Maven 使用哪个 JDK 版本来编译项目，我们用 4.12 版本的 junit，并用插件指明使用哪个 JDK 版本。

```xml
 <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
​
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>2.3.2</version>
                <configuration>
                    <source>1.7</source>
                    <target>1.7</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

5、运行 maven 项目

现在，我们将使用 Maven 这个项目，并输出编译成一个 “jar” 的文件。pom.xml 文件中包元素 packaging 定义应该输出什么包。如图： 

![](assets/Maven%20教程（4）—%20新建Maven项目/file-20251121160025634.png)

回到我们的项目目录，输入命令： mvn package 

![](assets/Maven%20教程（4）—%20新建Maven项目/file-20251121160035012.png)

它编译，运行单元测试并打包项目成一个 jar 文件，并把它放在 project/target 文件夹。 

![](assets/Maven%20教程（4）—%20新建Maven项目/file-20251121160045974.png)

最后，我们来运行一下这个 jar 文件，看看运行结果： 

![](assets/Maven%20教程（4）—%20新建Maven项目/file-20251121160055754.png)

打印输出：“HelloWorld”。
