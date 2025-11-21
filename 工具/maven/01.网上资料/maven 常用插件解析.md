我们都知道 Maven 本质上是一个插件框架，它的核心并不执行任何具体的构建任务，所有这些任务都交给插件来完成。

例如编译源代码是由 maven-compiler-plugin 完成的。

进一步说，每个任务对应了一个插件目标（goal），每个插件会有一个或者多个目标。

例如 maven-compiler-plugin 的 compile 目标用来编译位于 `src/main/java/` 目录下的主源码，testCompile 目标用来编译位于 `src/test/java/` 目录下的测试源码。

用户可以通过两种方式调用 Maven 插件目标。

第一种方式是将插件目标与生命周期阶段（lifecycle phase）绑定，这样用户在命令行只是输入生命周期阶段而已。

例如 Maven 默认将 maven-compiler-plugin 的 compile 目标与 compile 生命周期阶段绑定，因此命令 mvn compile 实际上是先定位到 compile 这一生命周期阶段，然后再根据绑定关系调用 maven-compiler-plugin 的 compile 目标。

第二种方式是直接在命令行指定要执行的插件目标。

例如 mvn archetype:generate 就表示调用 maven-archetype-plugin 的 generate 目标，这种带冒号的调用方式与生命周期无关。

认识上述 Maven 插件的基本概念能帮助你理解 Maven 的工作机制，不过要想更高效率地使用 Maven，了解一些常用的插件还是很有必要的，这可以帮助你避免一不小心重新发明轮子。

多年来 Maven 社区积累了大量的经验，并随之形成了一个成熟的插件生态圈。

Maven 官方有两个插件列表：

第一个列表的 GroupId 为 org.apache.maven.plugins，这里的插件最为成熟，具体地址为：[http://maven.apache.org/plugins/index.html](http://maven.apache.org/plugins/index.html)。

第二个列表的 GroupId 为 org.codehaus.mojo，这里的插件没有那么核心，但也有不少十分有用，其地址为：[http://mojo.codehaus.org/plugins.html](http://mojo.codehaus.org/plugins.html)。

接下来介绍一些常用的 MAVEN 插件

# maven-antrun-plugin

[http://maven.apache.org/plugins/maven-antrun-plugin/](http://maven.apache.org/plugins/maven-antrun-plugin/)

maven-antrun-plugin 能让用户在 Maven 项目中运行 Ant 任务。用户可以直接在该插件的配置以 Ant 的方式编写 Target，然后交给该插件的 run 目标去执行。

在一些由 Ant 往 Maven 迁移的项目中，该插件尤其有用。

此外当你发现需要编写一些自定义程度很高的任务，同时又觉得 Maven 不够灵活时，也可以以 Ant 的方式实现之。maven-antrun-plugin 的 run 目标通常与生命周期绑定运行。

# maven-archetype-plugin

[http://maven.apache.org/archetype/maven-archetype-plugin/](http://maven.apache.org/archetype/maven-archetype-plugin/)

Archtype 指项目的骨架，Maven 初学者最开始执行的 Maven 命令可能就是 mvn archetype:generate，这实际上就是让 maven-archetype-plugin 生成一个很简单的项目骨架，帮助开发者快速上手。

可能也有人看到一些文档写了 mvn archetype:create，但实际上 create 目标已经被弃用了，取而代之的是 generate 目标，该目标使用交互式的方式提示用户输入必要的信息以创建项目，体验更好。

maven-archetype-plugin 还有一些其他目标帮助用户自己定义项目原型，例如你由一个产品需要交付给很多客户进行二次开发，你就可以为他们提供一个 Archtype，帮助他们快速上手。

# maven-assembly-plugin

[http://maven.apache.org/plugins/maven-assembly-plugin/](http://maven.apache.org/plugins/maven-assembly-plugin/)

maven-assembly-plugin 的用途是制作项目分发包，该分发包可能包含了项目的可执行文件、源代码、readme、平台脚本等等。

maven-assembly-plugin 支持各种主流的格式如 zip、tar.gz、jar 和 war 等，具体打包哪些文件是高度可控的。

例如用户可以按文件级别的粒度、文件集级别的粒度、模块级别的粒度、以及依赖级别的粒度控制打包，此外，包含和排除配置也是支持的。

maven-assembly-plugin 要求用户使用一个名为 `assembly.xml` 的元数据文件来表述打包，它的 single 目标可以直接在命令行调用，也可以被绑定至生命周期。

# maven-dependency-plugin

[http://maven.apache.org/plugins/maven-dependency-plugin/](http://maven.apache.org/plugins/maven-dependency-plugin/)

maven-dependency-plugin 最大的用途是帮助分析项目依赖

dependency:list 能够列出项目最终解析到的依赖列表

dependency:tree 能进一步的描绘项目依赖树

dependency:analyze 可以告诉你项目依赖潜在的问题

如果你有直接使用到的却未声明的依赖，该目标就会发出警告。

maven-dependency-plugin 还有很多目标帮助你操作依赖文件，例如 dependency:copy-dependencies 能将项目依赖从本地 Maven 仓库复制到某个特定的文件夹下面。

# maven-enforcer-plugin

[http://maven.apache.org/plugins/maven-enforcer-plugin/](http://maven.apache.org/plugins/maven-enforcer-plugin/)

在一个稍大一点的组织或团队中，你无法保证所有成员都熟悉 Maven，那他们做一些比较愚蠢的事情就会变得很正常。

例如给项目引入了外部的 SNAPSHOT 依赖而导致构建不稳定，使用了一个与大家不一致的 Maven 版本而经常抱怨构建出现诡异问题。

maven-enforcer-plugin 能够帮助你避免之类问题，它允许你创建一系列规则强制大家遵守，包括设定 Java 版本、设定 Maven 版本、禁止某些依赖、禁止 SNAPSHOT 依赖。

只要在一个父 POM 配置规则，然后让大家继承，当规则遭到破坏的时候，Maven 就会报错。

除了标准的规则之外，你还可以扩展该插件，编写自己的规则。maven-enforcer-plugin 的 enforce 目标负责检查规则，它默认绑定到生命周期的 validate 阶段。

# maven-help-plugin

[http://maven.apache.org/plugins/maven-help-plugin/](http://maven.apache.org/plugins/maven-help-plugin/)

maven-help-plugin 是一个小巧的辅助工具。

最简单的 help:system 可以打印所有可用的环境变量和 Java 系统属性。

help:effective-pom 和 help:effective-settings 最为有用，它们分别打印项目的有效 POM 和有效 settings，有效 POM 是指合并了所有父 POM（包括 Super POM）后的 XML，

当你不确定 POM 的某些信息从何而来时，就可以查看有效 POM。

有效 settings 同理，特别是当你发现自己配置的 settings.xml 没有生效时，就可以用 help:effective-settings 来验证。

此外，maven-help-plugin 的 describe 目标可以帮助你描述任何一个 Maven 插件的信息，还有 all-profiles 目标和 active-profiles 目标帮助查看项目的 Profile。

# maven-release-plugin

[http://maven.apache.org/plugins/maven-release-plugin/](http://maven.apache.org/plugins/maven-release-plugin/)

maven-release-plugin 的用途是帮助自动化项目版本发布，它依赖于 POM 中的 SCM 信息。

release:prepare 用来准备版本发布，具体的工作包括检查是否有未提交代码、检查是否有 SNAPSHOT 依赖、升级项目的 SNAPSHOT 版本至 RELEASE 版本、为项目打标签等等。

release:perform 则是签出标签中的 RELEASE 源码，构建并发布。版本发布是非常琐碎的工作，它涉及了各种检查，而且由于该工作仅仅是偶尔需要，因此手动操作很容易遗漏一些细节。

maven-release-plugin 让该工作变得非常快速简便，不易出错。maven-release-plugin 的各种目标通常直接在命令行调用，因为版本发布显然不是日常构建生命周期的一部分。

# maven-resources-plugin

[http://maven.apache.org/plugins/maven-resources-plugin/](http://maven.apache.org/plugins/maven-resources-plugin/)

为了使项目结构更为清晰，Maven 区别对待 Java 代码文件和资源文件，maven-compiler-plugin 用来编译 Java 代码，maven-resources-plugin 则用来处理资源文件。

默认的主资源文件目录是 `src/main/resources`，很多用户会需要添加额外的资源文件目录，这个时候就可以通过配置 maven-resources-plugin 来实现。

此外，资源文件过滤也是 Maven 的一大特性，你可以在资源文件中使用 ${propertyName}形式的 Maven 属性，然后配置 maven-resources-plugin 开启对资源文件的过滤，

之后就可以针对不同环境通过命令行或者 Profile 传入属性的值，以实现更为灵活的构建。

# maven-surefire-plugin

[http://maven.apache.org/plugins/maven-surefire-plugin/](http://maven.apache.org/plugins/maven-surefire-plugin/)

可能是由于历史的原因，Maven 2/3 中用于执行测试的插件不是 maven-test-plugin，而是 maven-surefire-plugin。

其实大部分时间内，只要你的测试类遵循通用的命令约定（以 Test 结尾、以 TestCase 结尾、或者以 Test 开头），就几乎不用知晓该插件的存在。

然而在当你想要跳过测试、排除某些测试类、或者使用一些 TestNG 特性的时候，了解 maven-surefire-plugin 的一些配置选项就很有用了。

例如 mvn test -Dtest=FooTest 这样一条命令的效果是仅运行 FooTest 测试类，这是通过控制 maven-surefire-plugin 的 test 参数实现的。

# build-helper-maven-plugin

[http://mojo.codehaus.org/build-helper-maven-plugin/](http://mojo.codehaus.org/build-helper-maven-plugin/)

Maven 默认只允许指定一个主 Java 代码目录和一个测试 Java 代码目录，虽然这其实是个应当尽量遵守的约定，

但偶尔你还是会希望能够指定多个源码目录（例如为了应对遗留项目），build-helper-maven-plugin 的 add-source 目标就是服务于这个目的，

通常它被绑定到默认生命周期的 generate-sources 阶段以添加额外的源码目录。需要强调的是，这种做法还是不推荐的，

因为它破坏了 Maven 的约定，而且可能会遇到其他严格遵守约定的插件工具无法正确识别额外的源码目录。

build-helper-maven-plugin 的另一个非常有用的目标是 attach-artifact，

使用该目标你可以以 classifier 的形式选取部分项目文件生成附属构件，并同时 install 到本地仓库，也可以 deploy 到远程仓库。

# exec-maven-plugin

[http://mojo.codehaus.org/exec-maven-plugin/](http://mojo.codehaus.org/exec-maven-plugin/)

exec-maven-plugin 很好理解，顾名思义，它能让你运行任何本地的系统程序，

在某些特定情况下，运行一个 Maven 外部的程序可能就是最简单的问题解决方案，这就是 exec:exec 的用途，当然，该插件还允许你配置相关的程序运行参数。

除了 exec 目标之外，exec-maven-plugin 还提供了一个 java 目标，该目标要求你提供一个 mainClass 参数，然后它能够利用当前项目的依赖作为 classpath，在同一个 JVM 中运行该 mainClass。

有时候，为了简单的演示一个命令行 Java 程序，你可以在 POM 中配置好 exec-maven-plugin 的相关运行参数，然后直接在命令运行 mvn exec:java 以查看运行效果。

# jetty-maven-plugin

[http://wiki.eclipse.org/Jetty/Feature/Jetty_Maven_Plugin](http://wiki.eclipse.org/Jetty/Feature/Jetty_Maven_Plugin)

在进行 Web 开发的时候，打开浏览器对应用进行手动的测试几乎是无法避免的，这种测试方法通常就是将项目打包成 war 文件，然后部署到 Web 容器中，再启动容器进行验证，这显然十分耗时。

为了帮助开发者节省时间，jetty-maven-plugin 应运而生，它完全兼容 Maven 项目的目录结构，能够周期性地检查源文件，一旦发现变更后自动更新到内置的 Jetty Web 容器中。

做一些基本配置后（例如 Web 应用的 contextPath 和自动扫描变更的时间间隔），你只要执行 mvn jetty:run ，然后在 IDE 中修改代码，代码经 IDE 自动编译后产生变更，

再由 jetty-maven-plugin 侦测到后更新至 Jetty 容器，这时你就可以直接测试 Web 页面了。

需要注意的是，jetty-maven-plugin 并不是宿主于 Apache 或 Codehaus 的官方插件，因此使用的时候需要额外的配置 `settings.xml` 的 pluginGroups 元素，将 org.mortbay.jetty 这个 pluginGroup 加入。

# versions-maven-plugin

[http://mojo.codehaus.org/versions-maven-plugin/](http://mojo.codehaus.org/versions-maven-plugin/)

很多 Maven 用户遇到过这样一个问题，当项目包含大量模块的时候，为他们集体更新版本就变成一件烦人的事情，到底有没有自动化工具能帮助完成这件事情呢？

（当然你可以使用 sed 之类的文本操作工具，不过不在本文讨论范围）答案是肯定的，versions-maven- plugin 提供了很多目标帮助你管理 Maven 项目的各种版本信息。

例如最常用的，命令 mvn versions:set -DnewVersion=1.1-SNAPSHOT 就能帮助你把所有模块的版本更新到 1.1-SNAPSHOT。

该插件还提供了其他一些很有用的目标，display-dependency- updates 能告诉你项目依赖有哪些可用的更新；

类似的 display-plugin-updates 能告诉你可用的插件更新；然后 use- latest-versions 能自动帮你将所有依赖升级到最新版本。

最后，如果你对所做的更改满意，则可以使用 mvn versions:commit 提交，不满意的话也可以使用 mvn versions:revert 进行撤销。

# 小结

本文介绍了一些最常用的 Maven 插件，这里指的“常用”是指经常需要进行配置的插件，事实上我们用 Maven 的时候很多其它插件也是必须的，

例如默认的编译插件 maven-compiler-plugin 和默认的打包插件 maven-jar-plugin，但因为很少需要对它们进行配置，因此不在本文讨论范围。

了解常用的 Maven 插件能帮助你事倍功半地完成项目构建任务，反之你就可能会因为经常遇到一些难以解决的问题而感到沮丧。

本文介绍的插件基本能覆盖大部分 Maven 用户的日常使用需要，如果你真有非常特殊的需求，自行编写一个 Maven 插件也不是难事，更何况还有这么多开放源代码的插件供你参考。

一些常见例子

① maven-jetty-plugin 

http://blog.sina.com.cn/s/blog_62b0363101012he0.html

http://stamen.iteye.com/blog/1933452

输入：mvn jetty:run。这将在端口为 8080 的 Jetty 服务器上启动你的项目。Jetty 将持续运行，直到插件是明确停止。例如，按下<ctrl-c>，或使用 mvn jetty:stop 命令。

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

    <build>
        <finalName>rop-sample</finalName>
        <plugins>
            <!-- jetty插件 -->
            <plugin>
                <groupId>**org.mortbay.jetty**</groupId>
                <artifactId>**maven-jetty-plugin**</artifactId>
                <version>6.1.5</version>
                <configuration>
                    <webAppSourceDirectory>src/main/webapp</webAppSourceDirectory>
                    <scanIntervalSeconds>3</scanIntervalSeconds>
                    <contextPath>/</contextPath>
                    <connectors>
                        <connector implementation="org.mortbay.jetty.nio.SelectChannelConnector">
                            <port>8088</port>
                        </connector>
                    </connectors>
                </configuration>
            </plugin>
        </plugins>
    </build>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

② maven-compiler-plugin 编译源代码

在 Maven 项目下，我们需要配置 "maven-compiler-plugin" 的 "encoding" 参数

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

 <plugins>
         <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.1</version>
            <configuration>
                <encoding>UTF8</encoding>
            </configuration>
         </plugin>
    </plugins>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

需要在编译和生成的时候使用不同的 jdk 版本

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.5.1</version>
        <configuration>
          <source>1.6</source>
          <target>1.7</target>
        </configuration>
      </plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

③ maven-war-plugin 

打包 war 项目的时候排除某些 web 资源文件，这时就应该配置 maven-war-plugin 如下：

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

　<plugin>

    <groupId>**org.apache.maven.plugin**s</groupId>

    <artifactId>**maven-war-plugin**</artifactId>

    <version>2.1.1</version>

    <configuration>

      <webResources>

        <resource>

          <directory>src/main/webapp</directory>

          <excludes>

            <exclude>**/*.jpg</exclude>

          </excludes>

        </resource>

      </webResources>

    </configuration>

  </plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

④ maven-source-plugin 生成源码包

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

 <plugin>
    <groupId**>org.apache.maven.plugins**</groupId>
    <artifactId>**maven-source-plugin**</artifactId>
    <version>2.1.2</version>
    <executions>
      <execution>
        <id>attach-sources</id>
        <phase>verify</phase>
        <goals>
          <goal>jar-no-fork</goal>
        </goals>
      </execution>
    </executions>
  </plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<!-- 源代码打包插件 -->  

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <artifactId>maven-source-plugin</artifactId>
    <version>2.1</version>
    <configuration>
        <!-- <finalName>${project.build.name}</finalName> -->
        <attach>true</attach>
        <encoding>${project.build.sourceEncoding}</encoding>
    </configuration>
    <executions>
        <execution>
            <phase>compile</phase>
            <goals>
                <goal>jar</goal>
            </goals>
        </execution>
    </executions>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

⑤  maven-javadoc-plugin 生成 javadoc 包

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <groupId>**org.apache.maven.plugins**</groupId>
    <artifactId>**maven-javadoc-plugin**</artifactId>
    <version>2.7</version>
    <executions>
      <execution>
        <id>attach-javadocs</id>
          <goals>
            <goal>jar</goal>
          </goals>
      </execution>
    </executions>
  </plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

⑥ maven-assembly-plugin 

它支持各种打包文件格式，包括 zip、tar.gz、tar.bz2 等等，通过一个打包描述文件（该例中是 src/main/assembly.xml），它能够帮助用户选择具体打包哪些文件集合、依赖、模块、和甚至本地仓库文件，每个项的具体打包路径用户也能自由控制。如下就是对应上述需求的打包描述文件 src/main/assembly.xml：

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<assembly>
  <id>bin</id>
  <formats>
    <format>zip</format>
  </formats>
  <dependencySets>
    <dependencySet>
      <useProjectArtifact>true</useProjectArtifact>
      <outputDirectory>lib</outputDirectory>
    </dependencySet>
  </dependencySets>
  <fileSets>
    <fileSet>
      <outputDirectory>/</outputDirectory>
      <includes>
        <include>README.txt</include>
      </includes>
    </fileSet>
    <fileSet>
      <directory>src/main/scripts</directory>
      <outputDirectory>/bin</outputDirectory>
      <includes>
        <include>run.sh</include>
        <include>run.bat</include>
      </includes>
    </fileSet>
  </fileSets>
</assembly>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

最终生成一个 zip 格式的分发包，它包含如下的一个结构：

bin/

lib/

README.txt

最后，我们需要配置 maven-assembly-plugin 使用打包描述文件，并绑定生命周期阶段使其自动执行打包操作：

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

　<plugin>

    <groupId>**org.apache.maven.plugins**</groupId>

    <artifactId>**maven-assembly-plugin**</artifactId>

    <version>2.2.1</version>

    <configuration>

      <descriptors>

        <descriptor>src/main/assembly/assembly.xml</descriptor>

      </descriptors>

    </configuration>

    <executions>

      <execution>

        <id>make-assembly</id>

        <phase>package</phase>

        <goals>

          <goal>single</goal>

        </goals>

      </execution>

    </executions>

  </plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

运行 mvn clean package 之后，我们就能在 target/目录下得到名为 hello-world-1.0-bin.zip 的分发包了。

⑦ **maven-surefire-plugin **打包时跳过单元测试****LDER}**

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>2.6</version>
    <configuration>
        <skip>true</skip>
    </configuration>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

mvn package -Dmaven.test.skip=true 

如果单元测试中有输出中文，eclipse 的控制台里中文可能会变成乱码输出，也可以通过这个插件解决，参考配置：

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>2.16</version>
    <configuration>
        <forkMode>once</forkMode>
        <argLine>-Dfile.encoding=UTF-8</argLine>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

⑧ maven-resource-plugin

<!-- 设置资源文件的编码方式 --> 

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-resources-plugin</artifactId>
    <version>2.4.3</version>
    <executions>
        <execution>
            <phase>compile</phase>
        </execution>
    </executions>
    <configuration>
        <encoding>${project.build.sourceEncoding}</encoding>
    </configuration>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

把 web 项目的输出 copy 到 tomcat 的 webapp 下

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-resources-plugin</artifactId>
    <version>2.5</version>
    <executions>
        <execution>
            <id>deploy-website</id>
            <phase>package</phase>
            <goals>
                <goal>copy-resources</goal>
            </goals>
            <configuration>
                <outputDirectory>${server_home}/webapps/${project.build.finalName}</outputDirectory>
                <resources>
                    <resource>
                        <directory>${project.build.directory}/${project.build.finalName}</directory>
                    </resource>
                </resources>
            </configuration>
        </execution>
    </executions>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

⑨ maven-dependency-plugin

**打包时跳过单元测试**  

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-dependency-plugin</artifactId>
    <version>2.6</version>
    <executions>
        <execution>
            <id>copy-dependencies</id>
            <phase>compile</phase>
            <goals>
                <goal>copy-dependencies</goal>
            </goals>
            <configuration>
                <!-- ${project.build.directory}为Maven内置变量，缺省为target -->
                <outputDirectory>${project.build.directory}/lib</outputDirectory>
                <!-- 表示是否不包含间接依赖的包 -->
                <excludeTransitive>false</excludeTransitive>
                <!-- 表示复制的jar文件去掉版本信息 -->
                <stripVersion>true</stripVersion>
            </configuration>
        </execution>
    </executions>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

在部署 war 包时，需要将项目依赖的 jar 包，也打到 war 包中，因此就会用到上述插件

⑩ **自动拷贝 jar 包到 target 目录**

在一个 J2EE 项目中，想使用 mvn clean 命令清除 target 里的内容的同时，也清除 tomcat/webapp 下的相应目录，该怎么办呢？

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <artifactId>maven-clean-plugin</artifactId>
    <configuration>
        <verbose>true</verbose>
        <filesets>
            <fileset>
                <directory>c:/a/b/c/</directory>
            </fileset>
      </filesets>
    </configuration>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

本例中，删除的是 c:/a/b/c/目录.

当用户在该 maven 项目中执行 mvn clean 后，除了删除 clean 插件默认的

project.build.directory

project.build.outputDirectory

project.build.testOutputDirectory

project.reporting.outputDirectory

c:/a/b/c/

11、**在打包时，需要清空一些指定的目录** 

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

  <plugin>
        <groupId>**org.codehaus.mojo**</groupId>
        <artifactId>**tomcat-maven-plugin**</artifactId>
        <configuration>
            <server>tomcat6-manager</server>
            <path>/${project.build.name}</path>
            <url>http://localhost:8080/manager</url>
            <username>admin</username>
            <password>admin</password>
        </configuration>
        <executions>
            <execution>
                <phase>deploy</phase>
                <goals>
                    <goal>deploy</goal>
                </goals>
            </execution>
        </executions>
    </plugin>
</plugins>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

**利用 tomcat-maven-plugin 插件将项目自动打包并部署到 tomcat 中** 是指项目部署到 tomcat 后的项目名称  
**path：** 是指 tomcat 的 manager 访问地址  
**url：** 这个是 tomcat 服务名称设置，需要配置 maven 的 settings.xml 文件，在 servers 节点中手动配置 server，如下所示：  

<server>
    <id>tomcat6-manager</id>
    <username>admin</username>
    <password>admin</password>
</server>

12、**server：**   

cargo 插件可以帮助你完成 WAR 包到服务器的部署及服务器的启动和关闭等工作，方便，快速！

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

<plugin>
    <groupId>org.codehaus.cargo</groupId>
    <artifactId>cargo-maven2-plugin</artifactId>
    <version>1.2.0</version>
    <configuration>
        <container>
            <containerId>${server_name}</containerId>
            <home>${server_home}</home>
        </container>
        <configuration>
            <type>existing</type>
            <home>${server_home}</home>
            <properties>
                <cargo.servlet.port>8088</cargo.servlet.port>
            </properties>
        </configuration>
    </configuration>
</plugin>

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

注意，如果你的 tomcat 服务器的端口使用的不是默认的 8080（如本例中的 8088），则需要使用 cargo.servlet.port 参数将 cargo 的监听端口也配置到 tomcat 的那个监听端口（如本例中的 8088），否则使用 mvn cargo:run 启动的服务器会在 120000 毫秒（120 秒）后自动关闭！

mvn cargo:start 命令完成 WAR 包部署后，启动服务器，然后会将服务器立即关掉；

mvn cargo:run 命令完成 WAR 包部署后，启动服务器，直到你 Ctrl+C 将服务器关掉；

mvn cargo:stop 命令关闭服务器。

参考：[http://cargo.codehaus.org/Maven2+plugin](http://cargo.codehaus.org/Maven2+plugin)

![复制代码](https://assets.cnblogs.com/images/copycode.gif)

　　　　　　　　<plugin>
                <!-- 指定插件名称及版本号 -->
                <groupId>org.codehaus.cargo</groupId>
                <artifactId>cargo-maven2-plugin</artifactId>
                <version>1.2.3</version>
                <!-- 插件的Tomcat6.x配置 -->
                <configuration>
                    <!-- 容器的配置 -->
                    <container>
                        <!-- 指定服务器版本 -->
                        <containerId>tomcat6x</containerId>
                        <!-- 指定服务器的安装目录 -->
                        <home>E:\Program Files\tomcat-6.0.32</home>
                    </container>
                    <!-- 具体的配置 -->
                    <configuration>
                        <!-- 部署模式：existing、standalone等 -->
                        <type>existing</type>
                        <!-- Tomcat的位置，即catalina.home -->
                        <home>E:\Program Files\tomcat-6.0.32</home>
                        <!-- 配置属性 -->
                        <properties>
                            <!-- 管理地址 -->
                            <cargo.tomcat.manager.url>http://localhost:8080/manager</cargo.tomcat.manager.url>
                            <!-- Tomcat用户名 -->
                            <cargo.remote.username>admin</cargo.remote.username>
                            <!-- Tomcat密码 -->
                            <cargo.remote.password>admin</cargo.remote.password>
                            <!-- <cargo.jvmargs> -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8787 </cargo.jvmargs> -->
                        </properties>
                    </configuration>
                </configuration>
            </plugin>
