通过前面几部分知识，我们对 maven 已经有了初步的印象，就像 Make 的 Makefile、Ant 的 build.xml 一样，Maven 项目的核心是 pom.xml。POM(Project Object Model，项目对象模型) 定义了项目的基本信息，用于描述项目如何构建，声明依赖，等等。我们来看看 maven 中 pom.xml 文件主要标签的意思及其用法，来看一下 pom.xml 文件的结构：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
​
    <groupId>com.uidp</groupId>
    <artifactId>UidpParent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>pom</packaging>
​
    <!--当前项目的全称(名称) -->
    <name>UidpParent</name>
    <!--当前项目的主页的URL -->
    <url>http://maven.apache.org</url>
​
    <!--配置常用属性或定义一系列版本号 -->
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
​
        <repository-url>http://192.168.0.70:8081/content/groups/public/</repository-url>
​
        <maven-compiler-plugin.version>3.1</maven-compiler-plugin.version>
        <maven-war-plugin.version>2.4</maven-war-plugin.version>
        <maven-javadoc-plugin.version>2.9.1</maven-javadoc-plugin.version>
        <maven-release-plugin.version>2.4.1</maven-release-plugin.version>
        <maven-deploy-plugin.version>2.7</maven-deploy-plugin.version>
​
        <junit.version>4.11</junit.version>
        <oracle.version>10.2.0.4</oracle.version>
        <springframework.version>3.2.8.RELEASE</springframework.version>
        <mybatis.version>3.2.2</mybatis.version>
        <mybatis-spring.version>1.2.0</mybatis-spring.version>
        <mysql-driver.version>5.1.25</mysql-driver.version>
        <aspectjweaver.version>1.7.3</aspectjweaver.version>
​
        <commons-dbcp.version>1.4</commons-dbcp.version>
        <commons-pool.version>1.5.5</commons-pool.version>
        <commons-fileupload.version>1.2.2</commons-fileupload.version>
​
        <log4j.version>1.2.17</log4j.version>
        <slf4j-api.version>1.7.5</slf4j-api.version>
        <slf4j-log4j12.version>1.7.5</slf4j-log4j12.version>
​
        <freemarker.version>2.3.19</freemarker.version>
​
        <jackson-core.version>2.5.0</jackson-core.version>
        <jackson-mapper-asl.version>1.9.7</jackson-mapper-asl.version>
​
        <javax.servlet-api.version>3.0.1</javax.servlet-api.version>
        <jsp-api.version>2.2</jsp-api.version>
        <kryo.version>1.04</kryo.version>
        <snakeyaml.version>1.8</snakeyaml.version>
        <jedis.version>2.0.0</jedis.version>
        <commons-lang.version>2.6</commons-lang.version>
​
        <mockito-core.version>1.8.5</mockito-core.version>
        <powermock-core.version>1.4.9</powermock-core.version>
        <powermock-api-mockito.version>1.4.9</powermock-api-mockito.version>
        <powermock-module-junit4.version>1.4.9</powermock-module-junit4.version>
    </properties>
​
    <!--依赖管理 -->
    <dependencyManagement>
        <dependencies>
​
            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>${junit.version}</version>
                <scope>test</scope>
            </dependency>
​
            <!-- spring jar begin -->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-web</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-webmvc</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-beans</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context-support</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-core</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-jdbc</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-tx</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-test</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-expression</artifactId>
                <version>${springframework.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-aop</artifactId>
                <version>${springframework.version}</version>
            </dependency>
            <!-- spring jar end -->
​
            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis</artifactId>
                <version>${mybatis.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis-spring</artifactId>
                <version>${mybatis-spring.version}</version>
            </dependency>
​
            <dependency>
                <groupId>mysql</groupId>
                <artifactId>mysql-connector-java</artifactId>
                <version>${mysql-driver.version}</version>
            </dependency>
​
            <dependency>
                <groupId>com.oracle</groupId>
                <artifactId>ojdbc14</artifactId>
                <version>${oracle.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.aspectj</groupId>
                <artifactId>aspectjweaver</artifactId>
                <version>${aspectjweaver.version}</version>
            </dependency>
​
​
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
​
​
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
​
            <!-- freemarker -->
            <dependency>
                <groupId>org.freemarker</groupId>
                <artifactId>freemarker</artifactId>
                <version>${freemarker.version}</version>
            </dependency>
​
​
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
​
            <dependency>
                <groupId>javax.servlet</groupId>
                <artifactId>javax.servlet-api</artifactId>
                <version>${javax.servlet-api.version}</version>
                <scope>provided</scope>
            </dependency>
​
            <dependency>
                <groupId>javax.servlet.jsp</groupId>
                <artifactId>jsp-api</artifactId>
                <version>${jsp-api.version}</version>
                <scope>provided</scope>
            </dependency>
​
            <dependency>
                <groupId>com.googlecode</groupId>
                <artifactId>kryo</artifactId>
                <version>${kryo.version}</version>
            </dependency>
​
            <dependency>
                <groupId>org.yaml</groupId>
                <artifactId>snakeyaml</artifactId>
                <version>${snakeyaml.version}</version>
            </dependency>
​
            <dependency>
                <groupId>redis.clients</groupId>
                <artifactId>jedis</artifactId>
                <version>${jedis.version}</version>
            </dependency>
​
            <dependency>
                <groupId>commons-lang</groupId>
                <artifactId>commons-lang</artifactId>
                <version>${commons-lang.version}</version>
            </dependency>
​
​
            <dependency>
                <groupId>org.mockito</groupId>
                <artifactId>mockito-core</artifactId>
                <version>${mockito-core.version}</version>
                <scope>test</scope>
            </dependency>
​
            <dependency>
                <groupId>org.powermock</groupId>
                <artifactId>powermock-core</artifactId>
                <version>${powermock-core.version}</version>
                <scope>test</scope>
            </dependency>
​
            <dependency>
                <groupId>org.powermock</groupId>
                <artifactId>powermock-api-mockito</artifactId>
                <version>${powermock-api-mockito.version}</version>
                <scope>test</scope>
            </dependency>
​
            <dependency>
                <groupId>org.powermock</groupId>
                <artifactId>powermock-module-junit4</artifactId>
                <version>${powermock-module-junit4.version}</version>
                <scope>test</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
​
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
​
    <!--构建管理 -->
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
​
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-javadoc-plugin</artifactId>
                <version>${maven-javadoc-plugin.version}</version>
            </plugin>
​
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-release-plugin</artifactId>
                <version>${maven-release-plugin.version}</version>
            </plugin>
​
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
​
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

我们可以看到 maven 的 pom.xml 文件结构非常清晰，把项目创建好后，我们基本上是在 dependencies 元素下添加一些子元素及 plugins 元素下添加一些插件，下面我们来介绍一下各个元素的含义：

1. project：是所有 pom.xml 的根元素，并且在里面定义了命名空间和 xsd 元素；
2. modelVersion：当前 pom 模型的版本；
3. groupId：定义当前 maven 项目隶属的实际项目，并会根据这给项目建立包结构；
4. artifactId：定义项目中的某个模块名称，如果只有一个模块那就是项目的名称；
5. version：定义 maven 项目当前所处的版本号，默认 0.0.1-SNAPSHOT 为快照版本；
6. packaging：定义 maven 项目的打包方式，可以是 jar 包、war 包、pom；
7. dependencies：元素底下就是加入依赖包的地方，那么我们从哪里查询依赖包呢，可以查询的地方比较多，我给出一个大家用得比较多的仓库：[http://mvnrepository.com](http://mvnrepository.com/)；
8. 每个 dependency 都是一个依赖包，依赖包也就是在 dependency 里面定义各个依赖包的坐标，这样 maven 就会从网上下载依赖包到你本地仓库中，有所不同的是 dependency 元素包含了一个子元素，这个就是对 maven 生命周期的一个说明，当然除了上面四个子元素外，还包含几个其他的元素。 
		a. type：说明依赖的类型；
		b. optional：标记依赖是否可选；
		c. exclusions：用来排斥传递依赖。

我们具体来看看这个结构：

  ```xml

  <dependency>                          

    <groupId>实际项目</groupId>          

    <artifactId>模块</artifactId>      

    <version>版本</version>            

    <type>依赖类型</type>                

    <scope>依赖范围</scope>              

    <optional>依赖是否可选</optional>      

    <!-- 主要用于排除传递性依赖 -->              

    <exclusions>                      

        <exclusion>                  

            <groupId>…</groupId>      

            <artifactId>…</artifactId>

        </exclusion>                  

    </exclusions>                    

</dependency>

  ```

Maven 是通过 groupId、artifactId、version 这三个类似于坐标的元素来确定唯一性的，因此这三个元素对于每个依赖大多是必须的，后面会详细介绍依赖、聚合、继承等知识点。

没有任何实际的 Java 代码，我们能够定义一个 Maven 项目的 POM，这体现了 Maven 的一大优点，它能让项目对象模型最大程度地与实际代码相独立，我们可以称之为解耦。这在很大程度上避免了 Java 代码和 POM 代码的相互影响。只要我们定义的 POM 稳定后，日常的 Java 代码开发工作中基本不会涉及到 POM 的修改。
