# 内置属性

主要有两个常用内置属性：`${basedir}` 项目的根目录 (包含 pom.xml 文件的目录)，`${version}` 项目版本

# POM 属性

用户可以使用该属性引用 POM 文件中对应元素的值，常用的 POM 属性包括：

`${project.build.sourceDirectory}`：项目的主源码目录，默认为 src/main/java

`${project.build.testSourceDirectory}`：项目的测试源码目录，默认为 src/test/java

`${project.build.directory}`：项目构件输出目录，默认为 target/

`${project.outputDirectory}`：项目主代码编译输出目录，默认为 target/classes/

`${project.testOutputDirectory}`：项目测试代码编译输出目录，默认为 target/test-classes/

`${project.groupId}`：项目的 groupId　　　　

`${project.artifactId}`：项目的 artifactId　　

`${project.version}`：项目的 version，与 `${version}` 等价

`${project.build.fianlName}`：项目打包输出文件的名称。默认为 `${project.artifactId}-${project.version}`

# 自定义属性

用户可以在 POM 的 `<properties>` 元素下自定义 Maven 属性

# Settings 属性

用户使用 `settings.` 开头的属性引用 settings.xml 文件中 XML 元素的值

# Java 系统属性

所有 Java 系统属性都可以使用 Maven 属性引用

# 环境变量属性

所有环境变量都可以使用以 `env.` 开头的 Maven 属性引用

---

# 在依赖中 使用 pom 变量

```
<dependencies>
    <dependency>
        <groupId>${project.groupId}</groupId>
        <artifactId>part-a</artifactId>
        <version>${project.version}</version>
    </dependency>
    <dependency>
        <groupId>${project.groupId}</groupId>
        <artifactId>part-b</artifactId>
        <version>${project-version}</version>
    </dependency>
</dependencies>
```

# 在插件中使用 pom 变量

```
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>2.5</version>
    <configuration>
        <repositoryDirectory>${project.build.directory}/test-reports</repositoryDirectory>
    </configuration>
</plugin>
```

# 自定义变量

```
<profiles>
    <profile>
        <id>dev</id>
        <properties>
            <db.driver>com.mysql.jdbc.Driver</db.driver>
            <db.url>jdbc:mysql://localhost:3360/test</db.url>
            <db.username>username</db.username>
            <db.password>password></db.password>
        </properties>
    </profile>
</profiles>
```

**Maven 属性默认只有在 POM 中才会被解析，因此需要让 Maven 解析资源文件中的 Maven 属性**。Maven 用 `maven-resources-plugin` 处理资源文件。它默认的行为只是将项目主资源文件复制到主代码编译输出目录中，将测试资源文件复制到测试代码编译输出目录中。Maven 默认的主资源目录和测试资源目录的定义是在超级 POM 中，**要为资源目录开启过滤，只要在此基础上添加一行 filtering 配置即可**。Filtering 是 maven resource 插件的功能，作用是用环境变量，pom 文件里定义的属性和指定文件里的属性替换属性文件的占位符。（超级 pom 在 apache-maven-3.3.9\lib\maven-model-builder-3.3.9.jar\org\apache\maven\model\pom-4.0.0.xml）
