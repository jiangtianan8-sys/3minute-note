接[上回](https://blog.csdn.net/liupeifeng3514/article/details/79774572)继续，项目开发好以后，通常要在多个环境部署，象我们公司多达5种环境：本机环境(`local`)、(开发小组内自测的)开发环境(`dev`)、(提供给测试团队的)测试环境(`test`)、预发布环境(`pre`)、正式生产环境(`prod`)，每种环境都有各自的配置参数，比如：数据库连接、[远程调用](https://so.csdn.net/so/search?q=%E8%BF%9C%E7%A8%8B%E8%B0%83%E7%94%A8&spm=1001.2101.3001.7020)的ws地址等等。如果每个环境build前手动修改这些参数，显然太不fashion.

maven早就考虑到了这些问题，看下面的pom片段：

```xml
<profiles>
    <profile>
        <!-- 本地环境 -->
        <id>local</id>
        <properties>
            <db-url>jdbc:oracle:thin:@localhost:1521:XE</db-url>
            <db-username>***</db-username>
            <db-password>***</db-password>
        </properties>
    </profile>
    <profile>
        <!-- 开发环境 -->
        <id>dev</id>
        <properties>
            <db-url>jdbc:oracle:thin:@172.21.129.51:1521:orcl</db-url>
            <db-username>***</db-username>
            <db-password>***</db-password>
        </properties>
        <!-- 默认激活本环境 -->
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
    </profile>
    ...
</profiles>
```

profiles节点中，定义了二种环境：local、dev(默认激活dev环境)，可以在各自的环境中添加需要的property值，接下来修改build节点，参考下面的示例：

```xml
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>
        </resource>
    </resources>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>2.5.1</version>
            <configuration>
                <source>1.6</source>
                <target>1.6</target>
                <encoding>utf-8</encoding>
            </configuration>
        </plugin>
    </plugins>
</build>
```

resource节点是关键，它表明了哪个目录下的配置文件（不管是xml配置文件，还是properties属性文件），需要根据profile环境来替换属性值。

通常配置文件放在resources目录下，build时该目录下的文件都自动会copy到class目录下：  
![这里写图片描述](https://i-blog.csdnimg.cn/blog_migrate/48e61fa61d2f7985f50b7321056d11ad.jpeg)  
以上图为例，其中spring-database.xml的内容为：

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans 
    http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="oracle.jdbc.driver.OracleDriver" />
        <property name="url" value="${db-url}" />
        <property name="username" value="${db-username}" />
        <property name="password" value="${db-password}" />
    </bean>
</beans>
```

各属性节点的值，用占位符”`${属性名}`“占位，maven在package时，会根据profile的环境自动替换这些占位符为实际属性值。

默认情况下：

```
maven package
```

将采用默认激活的profile环境来打包，也可以手动指定环境，比如：

```
maven package -P dev
```

将自动打包成dev环境的部署包(注：参数P为大写)

最后再给2个实例的运用例子：

##### 1、开发环境与生产环境数据源采用不同方式的问题

本机开发时为了方便，很多开发人员喜欢直接用JDBC直接连接数据库，这样修改起来方便；

```
<bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
    <property name="driverClassName" value="oracle.jdbc.driver.OracleDriver" />
    <property name="url" value="${db-url}" />
    <property name="username" value="${db-username}" />
    <property name="password" value="${db-password}" />
    <property name="defaultAutoCommit" value="false" />
    <property name="initialSize" value="2" />
    <property name="maxActive" value="10" />
    <property name="maxWait" value="60000" />
</bean>
```

而生产环境，通常是在webserver(比如weblogic上)配置一个JNDI数据源，

```
<bean id="dataSource" class="org.springframework.jndi.JndiObjectFactoryBean">
    <property name="jndiName" value="appDS" />
</bean>
```

如果每次发布生产前，都要手动修改，未免太原始，可以通过maven的profile来解决。

先把配置文件改成

```xml
<bean id="${db-source-jdbc}" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
    <property name="driverClassName" value="oracle.jdbc.driver.OracleDriver" />
    <property name="url" value="${db-url}" />
    <property name="username" value="${db-username}" />
    <property name="password" value="${db-password}" />
    <property name="defaultAutoCommit" value="false" />
    <property name="initialSize" value="2" />
    <property name="maxActive" value="10" />
    <property name="maxWait" value="60000" />
</bean>
<bean id="${db-source-jndi}" class="org.springframework.jndi.JndiObjectFactoryBean">
    <property name="jndiName" value="appDS" />
</bean>
```

即用占位符来代替bean的id，然后在pom.xml里类似下面设置

```xml
<profiles>
    <profile>
        <!-- 本机环境 -->
        <id>local</id>
        <properties>
            ...
            <db-source-jdbc>dataSource</db-source-jdbc>
            <db-source-jndi>NONE</db-source-jndi>
            <db-url>jdbc:oracle:thin:@172.21.129.51:1521:orcl</db-url>
            <db-username>mu_fsu</db-username>
            <db-password>mu_fsu</db-password>
            ...
        </properties>
        <!-- 默认激活本环境 -->
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
    </profile>
    <profile>
        <!-- 生产环境 -->
        <id>pro</id>
        <properties>
            ...
            <db-source-jdbc>NONE</db-source-jdbc>
            <db-source-jndi>dataSource</db-source-jndi>
            ...
        </properties>
    </profile>
</profiles>
```

这样，`mvn clean package -P local`打包本地开发环境时，将生成

```xml
<bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
    <property name="driverClassName" value="oracle.jdbc.driver.OracleDriver" />
    <property name="url" value="jdbc:oracle:thin:@172.21.129.***:1521:orcl" />
    <property name="username" value="***" />
    <property name="password" value="***" />
    <property name="defaultAutoCommit" value="false" />
    <property name="initialSize" value="2" />
    <property name="maxActive" value="10" />
    <property name="maxWait" value="60000" />
</bean>
<bean id="NONE" class="org.springframework.jndi.JndiObjectFactoryBean">
    <property name="jndiName" value="appDS" />
</bean>
```

而打包生产环境`mvn clean package -P pro`时，生成

```xml
<bean id="NONE" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
    <property name="driverClassName" value="oracle.jdbc.driver.OracleDriver" />
    <property name="url" value="${db-url}" />
    <property name="username" value="${db-username}" />
    <property name="password" value="${db-password}" />
    <property name="defaultAutoCommit" value="false" />
    <property name="initialSize" value="2" />
    <property name="maxActive" value="10" />
    <property name="maxWait" value="60000" />
</bean>
<bean id="dataSource" class="org.springframework.jndi.JndiObjectFactoryBean">
    <property name="jndiName" value="appDS" />
</bean>
```

spring配置的其它跟数据库相关的bean，约定引用dataSource这个名称的bean即可。

##### 2、不同webserver环境，依赖jar包，是否打包的问题

weblogic上，允许多个app，把共用的jar包按约定打包成一个war文件，以library的方式部署，然后各应用在WEB-INF/weblogic.xml中，用类似下面的形式

```xml
<?xml version="1.0" encoding="utf-8"?>
<weblogic-web-app xmlns="http://www.bea.com/ns/weblogic/90">
    ...
    <library-ref>
        <library-name>my-share-lib</library-name>
    </library-ref>
</weblogic-web-app>
```

指定共享library 的名称即可。这样的好处是，即节省了服务器开销，而且各app打包时，就不必再重复打包这些jar文件，打包后的体积大大减少，上传起来会快很多。

而其它webserver上却未必有这个机制，一般为了方便，我们开发时，往往采用一些轻量级的webserver，比如：tomcat，jetty，jboss 之类，正式部署时才发布到weblogic下，这样带来的问题就是，本机打包时，要求这些依赖jar包，全打包到app的WEB-INF/lib下；而生产环境下，各应用的WEB-INF/lib下并不需要这些jar文件，同样还是用profile来搞定，先处理pom.xml，把依赖项改成类似下面的形式：

```xml
<dependency>
    <groupId>dom4j</groupId>
    <artifactId>dom4j</artifactId>
    <version>1.6.1</version>
    <scope>${jar.scope}</scope>
</dependency>
```

即scope这里，用一个占位符来代替，然后profile这样配置

```xml
<profile>
    <!-- 本机环境 -->
    <id>local</id>
    <properties>
        <jar.scope>compile</jar.scope>
        ...
    </properties>
    <!-- 默认激活本环境 -->
    <activation>
        <activeByDefault>true</activeByDefault>
    </activation>
</profile>
<profile>
    <!-- 生产环境 -->
    <id>pro</id>
    <properties>
        <jar.scope>provided</jar.scope>
        ...
    </properties>
</profile>
```

在maven里，如果一个依赖项的scope是provided，表示由容器提供，打包时将不会打包进最终的package里，所以这样配置后，生产环境打包时，依赖项的scope全变成了provided，即不打包进war文件，而本机环境下，因为scope是compile，所以会打包到war里