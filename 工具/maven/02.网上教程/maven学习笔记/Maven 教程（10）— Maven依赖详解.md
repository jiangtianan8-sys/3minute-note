# 1、何为依赖？

比如你是个男的，你要生孩子，呸呸呸…男的怎么生孩子，所以你得依赖你老婆，不过也不一定咯，你也可以依赖其她妹子。

我们在平时的项目开发中也是同理，你需要依赖一些东西才能实现相应的功能，但相应的功能或许也可以依赖其它的东西实现，比如数据库操作吧，你可以依赖 [hibernate](https://so.csdn.net/so/search?q=hibernate&spm=1001.2101.3001.7020)，但你也可以通过 mybatis 来做。

这就是所谓的依赖关系咯。

以前我们需要手动的去找 hibernate 或者 mybatis 的 jar 包，系统抛异常我们还不知哪里报错，通过琢磨才明白没有引入相应的 jar 包，然后就去找啊找，找到了然后引入到工程当中。在这里我们就看到 maven 的好处了，它就是一个仓库，仓库里面有各种各样的包，想要什么就在 pom.xml 中依赖一下就好了，就算仓库中没有的包也可以把它扔到仓库中，想用的时候就依赖一下。

# 2、依赖的配置

```xml
<project>
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>3.8.1</version>
            <type>...</type>
            <scope>test</scope>
            <optional>...</optional>
            <exclusions>
                <exclusion>
                    <groupId>...</groupId>
                    <artifactId>...</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>
</project>
```

根元素下 project 下的 dependencies 可以包含一个或者多个 dependency 元素，以声明一个或者多个项目依赖。每个依赖可以包含的元素有：

- **groupId,artifactId 和 version**：依赖的基本坐标，对于任何一个依赖来说，基本坐标是最重要的，Maven 根据坐标才能找到需要的依赖。
- **type**：依赖的类型，对应于项目坐标定义的 packaging。大部分情况下，该元素不必声明，其默认值是 jar。
- **scope**：依赖的范围，后面会进行详解。
- **optional**：标记依赖是否可选。
- **exclusions**：用来排除传递性依赖，后面会进行详细介绍。

大部分依赖声明只包含基本坐标，然而在一些特殊情况下，其他元素至关重要，我们来看看。

# 3、依赖范围说明

由于不同的包在不同的地方用到，像 junit 我们只有在做测试的时候会用到这个包，在我们项目发布的时候，用不到这个包；还有 servlet-api，在项目编译的时候将会用到这个包，而项目发布的时候就不会用到这个包，因为一般容器已经自带这个包，如果我们导入，有可能会出现冲突，所以 maven 引入了依赖范围这个概念，即我们上面提到的 scope 来解决这个问题。Maven 中有主要有以下这几种依赖范围：

1. **test**：指的是测试范围有效，在编译打包、运行时都不会使用这个依赖。例如：junit jar 包。
2. **compile**：指的是编译范围有效，在编译、测试、打包、运行时都会将依赖存储进去。如果没有指定，就会默认使用该依赖范围。例如：hibernate.jar 包。
3. **provided**：在编译和测试的过程有效，最后生成包时不会加入，运行时自然也没效果。例如：servlet-api，因为 servlet-api，tomcat 等 web 服务器已经存在该 jar 包了，如果再打包可能会有冲突。
4. **runtime**：在测试、运行的时候依赖，在编译的时候不依赖。例如：JDBC 驱动，项目代码只需要 jdk 提供的 jdbc 接口，只有在执行测试和运行项目的时候才需要实现 jdbc 的功能。
5. **system**：系统依赖范围。该依赖范围与 provided 所表示的依赖范围一致，对于编译和测试有效，但在运行时无效。只是使用 system 范围依赖时必须通过 systemPath 元素显式地指定依赖文件的路径。由于此类依赖不是通过 Maven 仓库解析的，而且往往与本机系统绑定，可能造成构建的不可移植，因此应该谨慎使用，systemPath 元素可以引用环境变量。例如：
    ![](assets/Maven%20教程（10）—%20Maven依赖详解/file-20251122090405391.png)
6. **import(Maven 2.0.9 及以上)**：导入依赖范围。该依赖范围不会对三种 classpath 产生实际的影响。

上述除 import 以外的各种依赖范围与三种 classpath 的关系如下：
![](assets/Maven%20教程（10）—%20Maven依赖详解/file-20251122090413861.png)

# 4、传递性依赖和依赖范围

Maven 的依赖是具有传递性的，比如 A->B,B->C,那么 A 间接的依赖于 C，这就是依赖的传递性，其中 A 对于 B 是第一直接依赖，B 对于 C 是第二直接依赖，C 为 A 的传递性依赖。

在平时的开发中，如果我们的项目依赖了 spring-core，依赖范围是 compile，spring-core 又依赖了 commons-logging，依赖范围也是 compile，那么我们的项目对于 commons-logging 这一传递性依赖的范围也就是 compile。第一直接依赖的范围和第二直接依赖的范围决定了传递性依赖的范围。我们通过下面这个表格来说明，其中最左边一栏是第一直接依赖，最上面那一栏为第二直接依赖。中间交叉的是传递性依赖范围。
![](assets/Maven%20教程（10）—%20Maven依赖详解/file-20251122090424198.png)
例如：第一直接依赖范围是 Test，第二直接依赖范围是 Compile，那么传递性依赖的范围就是 Test，大家可以根据这个表去判断。

仔细观察一下表格，我们可以发现这样的规律：

- 当第二直接依赖的范围是 compile 的时候，传递性依赖的范围与第一直接依赖的范围一致；
- 当第二直接依赖的范围是 test 的时候，依赖不会得以传递；
- 当第二直接依赖的范围是 provided 的时候，只传递第一直接依赖的范围也为 provided 的依赖，且传递性依赖的范围同样为 provided；
- 当第二直接依赖的范围是 runtime 的时候，传递性依赖的范围与第一直接依赖的范围一致，但 compile 例外，此时传递性依赖的范围为 runtime。

# 5、依赖调解

下面我们来思考这样一个问题，如果 A->B->C->X(1.0),A->D-X(2.0),即 A 间接依赖 X，我们可以看到有两条路径都依赖 X，那么 maven 将会选择哪个版本的 X？maven 当中有一套自己的规则，我们来说明一下，maven 传递性依赖的一些规则以及如何排除依赖冲突。

Maven 里面对于传递性依赖有以下几个规则：

1. 最短路径原则：如果 A 对于依赖路径中有两个相同的 jar 包，那么选择路径短的那个包，路径最近者优先，上述会选 X(2.0)。
2. 第一声明优先原则：如果 A 对于依赖路径中有两个相同的 jar 包，路径长度也相同，那么依赖写在前面的优先。例如：A->B->F(1.0),A->C->F(2.0)，会选 F(1.0)。
3. 可选依赖不会被传递，如 A->B，B->C，B->D，A 对 B 直接依赖，B 对 C 和 D 是可选依赖，那么在 A 中不会引入 C 和 D。可选依赖通过 optional 元素配置，true 表示可选。如果要在 A 项目中使用 C 或者 D 则需要显式地声明 C 或者 D 依赖。

# 6、排除依赖

传递性依赖会给项目隐式的引入很多依赖，这极大的简化了项目依赖的管理，但是有些时候这种特性也会带来问题，它可能会把我们不需要的 jar 包也引入到了工程当中，使项目结构变得更复杂。或者你想替换掉默认的依赖换成自己想要的 jar 包，这时候就需要用到依赖排除。

例如：

```xml
<dependency>    
     <groupId>org.springframework</groupId>  
     <artifactId>spring-core</artifactId>  
     <version>3.2.8</version>  
     <exclusions>  
           <exclusion>      
                <groupId>commons-logging</groupId>          
                <artifactId>commons-logging</artifactId>  
           </exclusion>  
     </exclusions>  
</dependency>
```

例子中 spring-core 包依赖了 commons-logging 包，我们使用 exclusions 元素声明排除依赖，exclusions 可以包含一个或者多个 exclusion 子元素，因此可以排除一个或者多个传递性依赖。需要注意的是，声明 exclusions 的时候只需要 groupId 和 artifactId，而不需要 version 元素，这是因为只需要 groupId 和 artifactId 就能唯一定位依赖图中的某个依赖。换句话说，Maven 解析后的依赖中，不可能出现 groupId 和 artifactId 相同，但是 version 不同的两个依赖。

# 7、把依赖归为一类

在项目开发中往往会引入同一个项目中的多个 jar 包，比如最常见的 spring，如果我们项目中用到很多关于 Spring Framework 的依赖，它们分别是 spring-core-3.2.8.RELEASE，spring-beans-3.2.8.RELEASE，spring-context-3.2.8.RELEASE，它们都是来自同一项目的不同模块。因此，所有这些依赖的版本都是相同的，而且可以预见，如果将来需要升级 Spring Framework，这些依赖的版本会一起升级。因此，我们应该在一个唯一的地方定义版本，并且在 dependency 声明引用这一版本，这一在 Spring Framework 升级的时候只需要修改一处即可。

首先使用 properties 元素定义 Maven 属性，实例中定义了一个 `<springframework.version>` 子元素，其值为 3.2.8.RELEASE，有了这个属性定义之后，Maven 运行的时候会将 `pom.xml` 中所有的 `${springframework.version}` 替换成实际的值：3.2.8.RELEASE。也就是可以使用 `$` 和 `{}` 的方式引用 Maven 的属性。然后将所有 springframework 依赖的版本替换成 `<version>${springframework.version}</version>` 这个样子，就和在 Java 代码中定义了一个不变的常量一样，以后要升级版本就只需要把这个值改了。

给大家一个完整的 Maven 配置实例，如果有在使用 `maven+spring+springMVC+Mybatis+Oracle` 数据库的朋友可以直接拿去改造成自己项目所需的父 pom，配置如下：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.uidp</groupId>
    <artifactId>UidpParent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>pom</packaging>

    <name>UidpParent</name>
    <url>http://maven.apache.org</url>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

        <repository-url>http://192.168.0.70:8081/content/groups/public/</repository-url>

        <maven-compiler-plugin.version>3.1</maven-compiler-plugin.version>
        <maven-war-plugin.version>2.4</maven-war-plugin.version>
        <maven-javadoc-plugin.version>2.9.1</maven-javadoc-plugin.version>
        <maven-release-plugin.version>2.4.1</maven-release-plugin.version>
        <maven-deploy-plugin.version>2.7</maven-deploy-plugin.version>

        <junit.version>4.11</junit.version>
        <oracle.version>10.2.0.4</oracle.version>
        <springframework.version>3.2.8.RELEASE</springframework.version>
        <mybatis.version>3.2.2</mybatis.version>
        <mybatis-spring.version>1.2.0</mybatis-spring.version>
        <mysql-driver.version>5.1.25</mysql-driver.version>
        <aspectjweaver.version>1.7.3</aspectjweaver.version>

        <commons-dbcp.version>1.4</commons-dbcp.version>
        <commons-pool.version>1.5.5</commons-pool.version>
        <commons-fileupload.version>1.2.2</commons-fileupload.version>

        <log4j.version>1.2.17</log4j.version>
        <slf4j-api.version>1.7.5</slf4j-api.version>
        <slf4j-log4j12.version>1.7.5</slf4j-log4j12.version>

        <freemarker.version>2.3.19</freemarker.version>

        <jackson-core.version>2.5.0</jackson-core.version>
        <jackson-mapper-asl.version>1.9.7</jackson-mapper-asl.version>

        <javax.servlet-api.version>3.0.1</javax.servlet-api.version>
        <jsp-api.version>2.2</jsp-api.version>
        <kryo.version>1.04</kryo.version>
        <snakeyaml.version>1.8</snakeyaml.version>
        <jedis.version>2.0.0</jedis.version>
        <commons-lang.version>2.6</commons-lang.version>


        <mockito-core.version>1.8.5</mockito-core.version>
        <powermock-core.version>1.4.9</powermock-core.version>
        <powermock-api-mockito.version>1.4.9</powermock-api-mockito.version>
        <powermock-module-junit4.version>1.4.9</powermock-module-junit4.version>

    </properties>

    <dependencyManagement>
        <dependencies>

            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>${junit.version}</version>
                <scope>test</scope>
            </dependency>

            <!-- spring jar begin -->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-web</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-webmvc</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-beans</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context-support</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-core</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-jdbc</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-tx</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-test</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-expression</artifactId>
                <version>${springframework.version}</version>
            </dependency>

            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-aop</artifactId>
                <version>${springframework.version}</version>
            </dependency>
            <!-- spring jar end -->

            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis</artifactId>
                <version>${mybatis.version}</version>
            </dependency>

            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis-spring</artifactId>
                <version>${mybatis-spring.version}</version>
            </dependency>

            <dependency>
                <groupId>mysql</groupId>
                <artifactId>mysql-connector-java</artifactId>
                <version>${mysql-driver.version}</version>
            </dependency>

            <dependency>
                <groupId>com.oracle</groupId>
                <artifactId>ojdbc14</artifactId>
                <version>${oracle.version}</version>
            </dependency>

            <dependency>
                <groupId>org.aspectj</groupId>
                <artifactId>aspectjweaver</artifactId>
                <version>${aspectjweaver.version}</version>
            </dependency>


            <dependency>
                <groupId>commons-dbcp</groupId>
                <artifactId>commons-dbcp</artifactId>
                <version>${commons-dbcp.version}</version>
            </dependency>
            <dependency>
                <groupId>commons-pool</groupId>
                <artifactId>commons-pool</artifactId>
                <version>${commons-pool.version}</version>
            </dependency>
            <dependency>
                <groupId>commons-fileupload</groupId>
                <artifactId>commons-fileupload</artifactId>
                <version>${commons-fileupload.version}</version>
            </dependency>


            <!-- log jar -->
            <dependency>
                <groupId>log4j</groupId>
                <artifactId>log4j</artifactId>
                <version>${log4j.version}</version>
            </dependency>
            <dependency>
                <groupId>org.slf4j</groupId>
                <artifactId>slf4j-api</artifactId>
                <version>${slf4j-api.version}</version>
            </dependency>
            <dependency>
                <groupId>org.slf4j</groupId>
                <artifactId>slf4j-log4j12</artifactId>
                <version>${slf4j-log4j12.version}</version>
            </dependency>

            <!-- freemarker -->
            <dependency>
                <groupId>org.freemarker</groupId>
                <artifactId>freemarker</artifactId>
                <version>${freemarker.version}</version>
            </dependency>


            <!-- jackson -->
            <dependency>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-core</artifactId>
                <version>${jackson-core.version}</version>
            </dependency>
            <dependency>
                <groupId>org.codehaus.jackson</groupId>
                <artifactId>jackson-mapper-asl</artifactId>
                <version>${jackson-mapper-asl.version}</version>
            </dependency>

            <dependency>
                <groupId>javax.servlet</groupId>
                <artifactId>javax.servlet-api</artifactId>
                <version>${javax.servlet-api.version}</version>
                <scope>provided</scope>
            </dependency>

            <dependency>
                <groupId>javax.servlet.jsp</groupId>
                <artifactId>jsp-api</artifactId>
                <version>${jsp-api.version}</version>
                <scope>provided</scope>
            </dependency>

            <dependency>
                <groupId>com.googlecode</groupId>
                <artifactId>kryo</artifactId>
                <version>${kryo.version}</version>
            </dependency>

            <dependency>
                <groupId>org.yaml</groupId>
                <artifactId>snakeyaml</artifactId>
                <version>${snakeyaml.version}</version>
            </dependency>

            <dependency>
                <groupId>redis.clients</groupId>
                <artifactId>jedis</artifactId>
                <version>${jedis.version}</version>
            </dependency>

            <dependency>
                <groupId>commons-lang</groupId>
                <artifactId>commons-lang</artifactId>
                <version>${commons-lang.version}</version>
            </dependency>


            <dependency>
                <groupId>org.mockito</groupId>
                <artifactId>mockito-core</artifactId>
                <version>${mockito-core.version}</version>
                <scope>test</scope>
            </dependency>

            <dependency>
                <groupId>org.powermock</groupId>
                <artifactId>powermock-core</artifactId>
                <version>${powermock-core.version}</version>
                <scope>test</scope>
            </dependency>

            <dependency>
                <groupId>org.powermock</groupId>
                <artifactId>powermock-api-mockito</artifactId>
                <version>${powermock-api-mockito.version}</version>
                <scope>test</scope>
            </dependency>

            <dependency>
                <groupId>org.powermock</groupId>
                <artifactId>powermock-module-junit4</artifactId>
                <version>${powermock-module-junit4.version}</version>
                <scope>test</scope>
            </dependency>

        </dependencies>
    </dependencyManagement>

    <distributionManagement>
        <repository>
            <id>releases</id>
            <name>public</name>
            <url>http://59.50.95.66:8081/nexus/content/repositories/releases</url>
        </repository>
        <snapshotRepository>
            <id>snapshots</id>
            <name>Snapshots</name>
            <url>http://59.50.95.66:8081/nexus/content/repositories/snapshots</url>
        </snapshotRepository>
    </distributionManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${maven-compiler-plugin.version}</version>
                <configuration>
                    <source>1.7</source> <!-- 源代码使用的开发版本 -->
                    <target>1.7</target> <!-- 需要生成的目标class文件的编译版本 -->
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-javadoc-plugin</artifactId>
                <version>${maven-javadoc-plugin.version}</version>
            </plugin>


            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-release-plugin</artifactId>
                <version>${maven-release-plugin.version}</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-deploy-plugin</artifactId>
                <version>${maven-deploy-plugin.version}</version>
                <configuration>
                    <updateReleaseInfo>true</updateReleaseInfo>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <pluginRepositories>
        <pluginRepository>
            <id>nexus</id>
            <name>nexus</name>
            <url>${repository-url}</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </pluginRepository>
    </pluginRepositories>

</project>
```

结束语：日月如梭，光阴似箭。不知不觉马上就要到 2017 年了，很多时候真的觉得不是我们年轻人不想做的更好，大多数时候是被前面的人给压迫的越来越油条了，所谓前人如此，却要求后人如何如何，其实想想也觉得蛮搞笑的。前人尽情的挥洒着智慧，玩着小心思不断的在压榨着年轻人，年轻人无奈的在这么个环境中挣扎求存。本以为离开了一个坑会迎来一个美好的未来，没想到的是不知不觉又跳入了一个更深的大坑，甚至有些坑还是隐形的，没有点特异功能还真不一定能够发现。不过话虽如此，作为新一代的年轻人，一定要经得过惊涛骇浪，何况是这点小风小浪。
