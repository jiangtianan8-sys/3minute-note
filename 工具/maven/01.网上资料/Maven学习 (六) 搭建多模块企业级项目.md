首先，前面几次学习已经学会了安装 maven，如何创建 maven 项目等，最近的学习，终于有点进展了，搭建一下企业级多模块项目。

好了，废话不多说，具体如下：

首先新建一个 maven 项目，pom.xml 的文件如下：

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121141945974.png)

搭建多模块项目，必须要有一个 packaging 为 pom 的根目录。创建好这个 maven 项目后，我们对着项目右键 -->new

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121141959921.png)

输入你的项目名称

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142014862.png)

这里就不重复说创建项目了，创建好的目录结构在 eclipse 中如下：

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142104051.png)

说明一下这些项目具体都是干嘛的：

easyframework-model：数据模型，与数据库表字段对应的实体类

easyframework-core：核心业务项目。主要是 Service 处理业务逻辑

easyframework-persist：数据持久层，操作低层数据库。

easyframework-utils：工具类，所有工具类都提取出来写在这个项目中。

easyframework-web : 这个就是整个项目的 web 层了，页面的显示以及控制层

备注：创建这些项目的时候，只有 easyframework-web 是 web 项目即 maven 的：maven-archetype-webapp，其他的都是 java 项目：maven-archetype-quicktart

打开 easyframework-root 的 pom.xml 文件，你会看到模块化是这样的：

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142135425.png)

接下来是配置各个模块的依赖关系，我个人认为的项目是这样依赖的，不知道对不对，呵呵....

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142151761.png)

举个例子 easyframework-web 这个项目依赖 easyframework-core(业务核心) 和 easyframework-model(实体类)，easyframework-utils(公共的工具类) 这个三个模块。

那么在怎么在 easyframework-web 的 pom.xml 中体现呢，具体如下：

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142221287.png)

打开项目的 maven 依赖你会发现，已经依赖了这三个项目

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142237180.png)

但是你应该会感觉到奇怪，为什么会有那么 jar 包，明明只引用了这三个项目，哪来的那么多 jar 包。

你会发现，我再 pom.xml 文件中，有个 parent 节点，继承了根节点的 pom，这就是 maven 的项目继承依赖，会从父 POM 中继承一些值。这对构建一个大型的系统来说很有必要

这样的话你就不需要一遍又一遍的重复添加同样的依赖元素，当然，如果你在子项目中也有同样的依赖，则会覆盖父 POM 中的值。

父 POM 的的依赖如下：

 ```xml

 1 <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

  2     xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">

  3     <modelVersion>4.0.0</modelVersion>

  4     <groupId>com.easyframework</groupId>

  5     <artifactId>easyframework-root</artifactId>

  6     <packaging>pom</packaging>

  7     <version>1.0</version>

  8     <name>easyframework-root</name>

  9     <url>http://maven.apache.org</url>

 10     <modules>

 11         <module>easyframework-web</module>

 12         <module>easyframework-persist</module>

 13         <module>easyframework-core</module>

 14         <module>easyframework-utils</module>

 15         <module>easyframework-model</module>

 16     </modules>

 17     <properties>

 18         <!--指定Maven用什么编码来读取源码及文档 -->

 19         <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

 20         <!--指定Maven用什么编码来呈现站点的HTML文件 -->

 21         <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>

 22         <mysql.version>5.1.25</mysql.version>

 23         <hibernate.version>4.2.2.Final</hibernate.version>

 24         <spring.version>3.2.3.RELEASE</spring.version>

 25         <aspectj.version>1.7.2</aspectj.version>

 26     </properties>

 27     <repositories>

 28         <repository>

 29             <id>springsource-repo</id>

 30             <name>SpringSource Repository</name>

 31             <url>http://repo.springsource.org/release</url>

 32         </repository>

 33     </repositories>

 34     <dependencies>

 35

 36         <!-- log4j -->

 37         <dependency>

 38             <groupId>log4j</groupId>

 39             <artifactId>log4j</artifactId>

 40             <version>1.2.17</version>

 41         </dependency>

 42         <!-- junit -->

 43         <dependency>

 44             <groupId>junit</groupId>

 45             <artifactId>junit</artifactId>

 46             <version>4.11</version>

 47             <scope>test</scope>

 48         </dependency>

 49         <!-- mysql数据库驱动 -->

 50         <dependency>

 51             <groupId>mysql</groupId>

 52             <artifactId>mysql-connector-java</artifactId>

 53             <version>${mysql.version}</version>

 54         </dependency>

 55         <!-- hibernate4 -->

 56         <dependency>

 57             <groupId>org.hibernate</groupId>

 58             <artifactId>hibernate-core</artifactId>

 59             <version>${hibernate.version}</version>

 60         </dependency>

 61         <!-- aspectjweaver -->

 62         <dependency>

 63             <groupId>org.aspectj</groupId>

 64             <artifactId>aspectjweaver</artifactId>

 65             <version>${aspectj.version}</version>

 66         </dependency>

 67         <!-- spring3 -->

 68         <dependency>

 69             <groupId>org.springframework</groupId>

 70             <artifactId>spring-core</artifactId>

 71             <version>${spring.version}</version>

 72         </dependency>

 73         <dependency>

 74             <groupId>org.springframework</groupId>

 75             <artifactId>spring-context</artifactId>

 76             <version>${spring.version}</version>

 77         </dependency>

 78         <dependency>

 79             <groupId>org.springframework</groupId>

 80             <artifactId>spring-jdbc</artifactId>

 81             <version>${spring.version}</version>

 82         </dependency>

 83         <dependency>

 84             <groupId>org.springframework</groupId>

 85             <artifactId>spring-beans</artifactId>

 86             <version>${spring.version}</version>

 87         </dependency>

 88         <dependency>

 89             <groupId>org.springframework</groupId>

 90             <artifactId>spring-web</artifactId>

 91             <version>${spring.version}</version>

 92         </dependency>

 93         <dependency>

 94             <groupId>org.springframework</groupId>

 95             <artifactId>spring-expression</artifactId>

 96             <version>${spring.version}</version>

 97         </dependency>

 98         <dependency>

 99             <groupId>org.springframework</groupId>

100             <artifactId>spring-orm</artifactId>

101             <version>${spring.version}</version>

102         </dependency>

103     </dependencies>

104     <build>

105         <finalName>easyframework-root</finalName>

106         <plugins>

107             <plugin>

108                 <artifactId>maven-compiler-plugin</artifactId>

109                 <configuration>

110                     <source>1.6</source>

111                     <target>1.6</target>

112                 </configuration>

113             </plugin>

114         </plugins>

115     </build>

116 </project>

 ```

当然这个父 POM 只是一个例子，你可以根据自己的配置添加相关的依赖，这里给一个我认为是最好用的仓库：

[http://mvnrepository.com/](http://mvnrepository.com/) 相信地球人都知道这个！哈哈.....

到此就搭建好了企业级多模块的项目环境了。
