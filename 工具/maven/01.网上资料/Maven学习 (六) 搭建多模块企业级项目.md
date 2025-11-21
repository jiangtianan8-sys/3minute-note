首先，前面几次学习已经学会了安装maven，如何创建maven项目等，最近的学习，终于有点进展了，搭建一下企业级多模块项目。

好了，废话不多说，具体如下：

首先新建一个maven项目，pom.xml的文件如下：

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121141945974.png)

搭建多模块项目，必须要有一个packaging为pom的根目录。创建好这个maven项目后，我们对着项目右键-->new

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121141959921.png)

输入你的项目名称

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142014862.png)

这里就不重复说创建项目了，创建好的目录结构在eclipse中如下：

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142104051.png)

说明一下这些项目具体都是干嘛的：

easyframework-model：数据模型，与数据库表字段对应的实体类

easyframework-core：核心业务项目。主要是Service处理业务逻辑

easyframework-persist：数据持久层，操作低层数据库。

easyframework-utils：工具类，所有工具类都提取出来写在这个项目中。

easyframework-web :这个就是整个项目的web层了，页面的显示以及控制层

备注：创建这些项目的时候，只有easyframework-web是web项目即maven的：maven-archetype-webapp，其他的都是java项目：maven-archetype-quicktart

打开easyframework-root的pom.xml文件，你会看到模块化是这样的：

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142135425.png)

接下来是配置各个模块的依赖关系，我个人认为的项目是这样依赖的，不知道对不对，呵呵....

![](assets/Maven学习%20(六)%20搭建多模块企业级项目/file-20251121142151761.png)

举个例子easyframework-web这个项目依赖easyframework-core(业务核心)和easyframework-model(实体类)，easyframework-utils(公共的工具类)这个三个模块。

那么在怎么在easyframework-web的pom.xml中体现呢，具体如下：

![0](https://note.youdao.com/yws/res/2403/CE88FA397E0B4F26AD356D9569540EB7)

打开项目的maven依赖你会发现，已经依赖了这三个项目

![0](https://note.youdao.com/yws/res/2401/BC7B1A337CEC45768AB5CD3AC51DE0B3)

但是你应该会感觉到奇怪，为什么会有那么jar包，明明只引用了这三个项目，哪来的那么多jar包。

你会发现，我再pom.xml文件中，有个parent节点，继承了根节点的pom，这就是maven的项目继承依赖，会从父POM中继承一些值。这对构建一个大型的系统来说很有必要

这样的话你就不需要一遍又一遍的重复添加同样的依赖元素，当然，如果你在子项目中也有同样的依赖，则会覆盖父POM中的值。

父POM的的依赖如下：

![0](https://note.youdao.com/yws/res/2406/3A14BC77B6214E0B9167E320F468B4D5)

 1 <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  2    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">  3 <modelVersion>4.0.0modelVersion>  4 <groupId>com.easyframeworkgroupId>  5 <artifactId>easyframework-rootartifactId>  6 <packaging>pompackaging>  7 <version>1.0version>  8 <name>easyframework-rootname>  9 <url>http://maven.apache.orgurl> 10 <modules> 11 <module>easyframework-webmodule> 12 <module>easyframework-persistmodule> 13 <module>easyframework-coremodule> 14 <module>easyframework-utilsmodule> 15 <module>easyframework-modelmodule> 16 modules> 17 <properties> 18 19 <project.build.sourceEncoding>UTF-8project.build.sourceEncoding> 20 21 <project.reporting.outputEncoding>UTF-8project.reporting.outputEncoding> 22 <mysql.version>5.1.25mysql.version> 23 <hibernate.version>4.2.2.Finalhibernate.version> 24 <spring.version>3.2.3.RELEASEspring.version> 25 <aspectj.version>1.7.2aspectj.version> 26 properties> 27 <repositories> 28 <repository> 29 <id>springsource-repoid> 30 <name>SpringSource Repositoryname> 31 <url>http://repo.springsource.org/releaseurl> 32 repository> 33 repositories> 34 <dependencies> 35 36 37 <dependency> 38 <groupId>log4jgroupId> 39 <artifactId>log4jartifactId> 40 <version>1.2.17version> 41 dependency> 42 43 <dependency> 44 <groupId>junitgroupId> 45 <artifactId>junitartifactId> 46 <version>4.11version> 47 <scope>testscope> 48 dependency> 49 50 <dependency> 51 <groupId>mysqlgroupId> 52 <artifactId>mysql-connector-javaartifactId> 53 <version>${mysql.version}version> 54 dependency> 55 56 <dependency> 57 <groupId>org.hibernategroupId> 58 <artifactId>hibernate-coreartifactId> 59 <version>${hibernate.version}version> 60 dependency> 61 62 <dependency> 63 <groupId>org.aspectjgroupId> 64 <artifactId>aspectjweaverartifactId> 65 <version>${aspectj.version}version> 66 dependency> 67 68 <dependency> 69 <groupId>org.springframeworkgroupId> 70 <artifactId>spring-coreartifactId> 71 <version>${spring.version}version> 72 dependency> 73 <dependency> 74 <groupId>org.springframeworkgroupId> 75 <artifactId>spring-contextartifactId> 76 <version>${spring.version}version> 77 dependency> 78 <dependency> 79 <groupId>org.springframeworkgroupId> 80 <artifactId>spring-jdbcartifactId> 81 <version>${spring.version}version> 82 dependency> 83 <dependency> 84 <groupId>org.springframeworkgroupId> 85 <artifactId>spring-beansartifactId> 86 <version>${spring.version}version> 87 dependency> 88 <dependency> 89 <groupId>org.springframeworkgroupId> 90 <artifactId>spring-webartifactId> 91 <version>${spring.version}version> 92 dependency> 93 <dependency> 94 <groupId>org.springframeworkgroupId> 95 <artifactId>spring-expressionartifactId> 96 <version>${spring.version}version> 97 dependency> 98 <dependency> 99 <groupId>org.springframeworkgroupId> 100 <artifactId>spring-ormartifactId> 101 <version>${spring.version}version> 102 dependency> 103 dependencies> 104 <build> 105 <finalName>easyframework-rootfinalName> 106 <plugins> 107 <plugin> 108 <artifactId>maven-compiler-pluginartifactId> 109 <configuration> 110 <source>1.6source> 111 <target>1.6target> 112 configuration> 113 plugin> 114 plugins> 115 build> 116 project>

![0](https://note.youdao.com/yws/res/2406/3A14BC77B6214E0B9167E320F468B4D5)

当然这个父POM只是一个例子，你可以根据自己的配置添加相关的依赖，这里给一个我认为是最好用的仓库：

[http://mvnrepository.com/](http://mvnrepository.com/) 相信地球人都知道这个！哈哈.....

到此就搭建好了企业级多模块的项目环境了。