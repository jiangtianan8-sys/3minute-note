#### 1、Maven聚合

我们在平时的开发中，项目往往会被划分为好几个模块，比如common公共模块、system系统模块、log日志模块、reports统计模块、monitor监控模块等等。这时我们肯定会出现这么一个需要，我们需要一次构件多个模块，而不用每个模块都去`mvn clean install`一次，Maven聚合就是用来实现这个需求的。

我们需要构建另外一个模块，假设是UidpWeb，然后通过该模块来构件整个项目的所有模块，POM结构如下：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.uidp</groupId>
    <artifactId>UidpWeb</artifactId>
    <packaging>pom</packaging>
    <version>0.0.1-SNAPSHOT</version>
    <name>UidpWeb</name>
    <url>http://maven.apache.org</url>

    <modules>
        <!-- parent pom -->
        <module>parent</module>
        <!-- 公共资源文件，第三方js库，图片等媒体资源 -->
        <module>ThirdParty</module>
        <!-- 公共依赖，工具包 -->
        <module>common</module>
        <!-- 日志模块 -->
        <module>log/pom-pack.xml</module>
        <!-- 第三方客户定制服务模块 -->
        <module>biz/pom-pack.xml</module>
        <!-- 客户管理 -->
        <module>customer/pom-pack.xml</module>
        <!-- 策略模块 -->
        <module>strategy/pom-pack.xml</module>
        <!-- 统计报表 -->
        <module>reports/pom-pack.xml</module>
        <!-- 监控统计 -->
        <module>monitor/pom-pack.xml</module>
        <!-- 系统管理模块 -->
        <module>sysmgr/pom-pack.xml</module>
        <!-- 统一打war包 -->
        <module>/pom-app.xml</module>
    </modules>

</project>
```

注释：

`<packaging>pom</packaging>`：对于聚合模块UidpWeb来说，`packaging`的类型必须为`pom`，否则无法构建。

`<name>UidpWeb</name>`：提供一个更容易阅读的名称，没什么其他太大作用。

`<modules>......</modules>`：这是实现聚合的标签，其下可包含多个`module`元素。

`<module>...</module>`：用来指定实现聚合的模块或者实现聚合的POM。

为了方便用户构建项目，通常将聚合模块放在项目目录的最顶层，其他模块则作为聚合模块的子目录存在，这时聚合的时候便可如我这般指定路径：

```xml
<module>parent</module>
<module>log/pom-pack.xml</module>
```

这就表示聚合模块下面的`parent`目录，聚合模块下面的`log`目录下的`pom-pack.xml`。

聚合模块下的内容只需要POM文件，它不像其他模块那样有`src/main/java`、`src/test/java`等目录。他只是用来帮助聚合其他模块构建，他本身并不会有过多的实质内容。

关于目录结构要注意的是，聚合模块既可以作为其他模块的父目录，也可以与其他模块处于平行的目录，如图：  
![](assets/Maven%20教程（14）—%20Maven聚合与继承/file-20251122091923671.png)  
如果使用平行目录，聚合模块的POM要做相应的修改，以指向正确的模块目录：

```xml
<module>../parent</module>
<module>../log/pom-pack.xml</module>
```

最后运行`mvn clean install`命令，Maven会分析聚合模块的POM、分析要构建的模块、并计算出一个反应堆构建顺序，然后根据这个顺序依次构建各个模块，这样便可以一次性构建所有聚合的模块。

#### 2、Maven继承

如果多个模块出现相同的依赖包，这样在pom.xml文件的内容出现了冗余、重复的内容，解决这个问题其实使用Maven的继承机制即可，就像Java的继承一样，父类就像一个模板，子类继承自父类，那么有些通用的方法、变量都不必在子类中再重复声明了。Maven的继承机制类似，在一个父级别的Maven的pom文件中定义了相关的常量、依赖、插件等等配置后，实际项目模块可以继承此父项目 的pom文件，重复的项不必显示的再声明一遍了，相当于父Maven项目就是个模板，等着其他子模块去继承。不过父Maven项目要高度抽象，高度提取公共的部分（交集），做到一处声明，多处使用。

与聚合一样我们需要构建另外一个模块，假设是parent，在聚合模块UidpWeb下面创建parent模块，然后通过该模块来作为所有模块的父POM，POM结构如下：

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
            <url>http://192.168.0.70:8081/content/groups/public/</url>
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

需要注意的是，他的`packaging`和聚合一样为pom，作为父模块的pom，其打包类型必须为`pom`。父模块只是为了帮助消除配置的重复，因此他本身不包含除POM的项目文件，也就不需要`src/main/java`之类的文件夹了。

有了父模块，就需要让其他模块来继承它，我们来看个实际的例子：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.uidp</groupId>
        <artifactId>UidpParent</artifactId>
        <version>0.0.1-SNAPSHOT</version>
    </parent>

    <groupId>com.uidp</groupId>
    <artifactId>log</artifactId>
    <packaging>war</packaging>
    <version>0.0.1-SNAPSHOT</version>
    <name>log</name>
    <url>http://maven.apache.org</url>

    <dependencies>

        <dependency>
            <artifactId>ThirdParty</artifactId>
            <version>0.0.1-SNAPSHOT</version>
            <groupId>${project.parent.groupId}</groupId>
            <type>war</type>
        </dependency>

        <dependency>
            <groupId>com.uidp</groupId>
            <artifactId>WebCommon</artifactId>
            <version>0.0.1-SNAPSHOT</version>
        </dependency>

        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
        </dependency>

        <!-- spring jar begin -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-beans</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context-support</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-tx</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-test</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-expression</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-aop</artifactId>
        </dependency>
        <!-- spring jar end -->

        <!-- Quartz 框架 -->
        <dependency>
            <groupId>org.quartz-scheduler</groupId>
            <artifactId>quartz</artifactId>
            <version>1.8.6</version>
        </dependency>

        <!-- mybatis db -->
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
        </dependency>

        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis-spring</artifactId>
        </dependency>

        <!-- mysql驱动依赖包 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>

        <!-- 数据库连接池 jar -->
        <dependency>
            <groupId>commons-dbcp</groupId>
            <artifactId>commons-dbcp</artifactId>
        </dependency>
        <dependency>
            <groupId>commons-pool</groupId>
            <artifactId>commons-pool</artifactId>
        </dependency>
        <dependency>
            <groupId>commons-fileupload</groupId>
            <artifactId>commons-fileupload</artifactId>
        </dependency>

        <!-- jackson -->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.codehaus.jackson</groupId>
            <artifactId>jackson-mapper-asl</artifactId>
        </dependency>

        <!-- log jar -->
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
        </dependency>

        <!-- freemarker -->
        <dependency>
            <groupId>org.freemarker</groupId>
            <artifactId>freemarker</artifactId>
        </dependency>

        <dependency>
            <groupId>com.oracle</groupId>
            <artifactId>ojdbc14</artifactId>
        </dependency>

        <!--因为api是打jar包的，所以这里用compile，如果是正常情况打war包，用private -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <scope>compile</scope>
        </dependency>

        <dependency>
            <groupId>javax.servlet.jsp</groupId>
            <artifactId>jsp-api</artifactId>
            <scope>compile</scope>
        </dependency>

        <dependency>
            <groupId>commons-lang</groupId>
            <artifactId>commons-lang</artifactId>
            <version>2.6</version>
        </dependency>

    </dependencies>

    <build>
        <plugins>

            <plugin>
                <groupId>org.mortbay.jetty</groupId>
                <artifactId>jetty-maven-plugin</artifactId>
                <version>7.2.2.v20101205</version>
                <configuration>
                    <stopKey>foo</stopKey>
                    <stopPort>9999</stopPort>
                    <webAppConfig>
                        <contextPath>/</contextPath>
                    </webAppConfig>
                    <!-- 指定额外需要监控变化的文件或文件夹，主要用于热部署中的识别文件更新 -->
                    <scanTargetPatterns>
                        <scanTargetPattern>
                            <directory>src</directory>
                            <includes>
                                <include>**/*.java</include>
                                <include>**/*.properties</include>
                            </includes>
                            <excludes>
                                <exclude>**/*.xml</exclude>
                                <exclude>**/myspecial.properties</exclude>
                            </excludes>
                        </scanTargetPattern>
                    </scanTargetPatterns>
                    <scanIntervalSeconds>1</scanIntervalSeconds>
                    <webAppSourceDirectory>${basedir}/src/main/webapp</webAppSourceDirectory><!--指定web页面的文件夹 -->
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>${maven-war-plugin.version}</version>
                <configuration>
                    <failOnMissingWebXml>false</failOnMissingWebXml>
                    <warName>${project.artifactId}</warName>
                </configuration>
            </plugin>
        </plugins>
    </build>

</project>
```

上述POM中使用`parent`元素声明父模块，`parent`下的子元素`groupId`、`artifactId`和`version`指定了父模块的坐标，这三个元素是必须的。`relativePath`元素是可选的，我这里用的默认值所以并没有配置，`relativePath`元素的默认值为`../pom.xml`，也就是说，Maven默认父POM在上一层目录下。当项目构建时，Maven会首先根据relativePath检查父POM，如果找不到，再从本地仓库找。所以像我这里如果本地仓库中也没有父POM的话构建就会失败了，所以最好的做法是配置`relativePath`为`../parent/pom.xml`表示父POM的位置与在log/目录平行的parent/下。这样就算本地仓库没有父POM构建的时候也不会报错了。

大家有木有发现log的groupId和version元素是与父POM一样的，所以这里其实是可以省略不要的，但是如果log有自己专门的groupId和version，那么就显示的配置一个就好了。对于artifactId元素来说，子模块应该显式的声明，避免造成坐标冲突和混淆。

对于依赖的继承，我们可以把依赖放入`<dependencyManagement>`元素当中，这样的依赖就成了可选的，我们只要在项目中继承我们所需的依赖即可，比如：

```xml
<dependency>
　　<groupId>junit</groupId>
　　<artifactId>junit</artifactId>
　　<scope>test</scope>
</dependency>
```

我们不需要进行版本的声明，这样就可以根据自己的需要引入需要的包，而不会继承全部的包。

对于每个项目都需要继承的依赖则不放在`<dependencyManagement>`元素当中，不过个人觉得没什么必要，都放在`<dependencyManagement>`元素当中，需要的时候引入一下就好了。

插件的继承与依赖的继承是类似的，这里不过多的说明，插件也有一个`<pluginManagement></pluginManagement>`元素，放在下面的插件也表示为可选的。

在使用父POM的时候也要在聚合模块中加入：`<module>parent</module>`

应该是放在最前面，大家可以看看上面的聚合POM。

#### 3、可继承的POM元素

`groupId`和`version`是可以被继承的，那么还有哪些POM元素可以被继承呢？以下是一个完整的列表，并附带了简单的说明：

- groupId ：项目组 ID ，项目坐标的核心元素；
- version ：项目版本，项目坐标的核心元素；
- description ：项目的描述信息；
- organization ：项目的组织信息；
- inceptionYear ：项目的创始年份；
- url ：项目的 url 地址；
- develoers ：项目的开发者信息；
- contributors ：项目的贡献者信息；
- distributionManagerment ：项目的部署信息；
- issueManagement ：缺陷跟踪系统信息；
- ciManagement ：项目的持续继承信息；
- scm ：项目的版本控制信息；
- mailingListserv ：项目的邮件列表信息；
- properties ：自定义的 Maven 属性；
- dependencies ：项目的依赖配置；
- dependencyManagement ：醒目的依赖管理配置；
- repositories ：项目的仓库配置；
- build ：包括项目的源码目录配置、输出目录配置、插件配置、插件管理配置等；
- reporting ：包括项目的报告输出目录配置、报告插件配置等。

#### 4、聚合与继承的关系

区别 ：

1. 对于聚合模块来说，它知道有哪些被聚合的模块，但那些被聚合的模块不知道这个聚合模块的存在。
2. 对于继承关系的父POM来说，它不知道有哪些子模块继承于它，但那些子模块都必须知道自己的父POM是什么。

共同点 ：

1. 聚合POM与继承关系中的父POM的packaging都是pom。
2. 聚合模块与继承关系中的父模块除了POM之外都没有实际的内容。

图示：  
![](assets/Maven%20教程（14）—%20Maven聚合与继承/file-20251122091951979.png)

#### 5、有关版本的简单说明

对于用过svn或者cvs的朋友们，都会知道，每次修改都会提交一个版本到服务器上，对于我们平常所搭建的项目，大家可能没有注意到版本这个概念。其实版本对于叠加式开发的项目是个很重要的概念，通过上面的依赖，我们就可以清楚地看到一个version，这个就是引入依赖包的版本。

那么版本一共可以分为几个层次，一般来说，版本可以分为：总版本号.分支版本号.小版本号-里程碑版本。

- 总版本号：一般表示框架的变动。
- 分支版本号：一般表示增加了一些功能。
- 小版本号：在分支版本上面进行bug的修复。
- 里程碑：SNAPSHOT–>alpha–>beta–>release–>GA

结束语：关于继承所包含的内容比较多，不是三言两语就能描述的很清楚的，所以再次强烈建议大家可以购买许晓斌老师的《Maven实战》，这本书会介绍的比较详细，个人觉得最好的投资就是投资自己的学习，所以如果你是Maven的初学者，应该和我一样购买这本书籍，如果是大神，那么也就没必要看这篇博文了，营养价值并不高。