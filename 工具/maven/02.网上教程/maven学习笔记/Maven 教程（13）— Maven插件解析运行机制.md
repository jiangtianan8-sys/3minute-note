这里给大家详细说一下 Maven 的运行机制，让大家不仅知其然，更知其所以然。

# 1、插件保存在哪里？

与我们所依赖的构件一样，插件也是基于坐标保存在我们的 Maven 仓库当中的。在用到插件的时候会先从本地仓库查找插件，如果本地仓库没有则从远程仓库查找插件并下载到本地仓库。

与普通的依赖构件不同的是，Maven 会区别对待普通依赖的远程仓库与插件的远程仓库。前面提到的配置远程仓库只会对普通的依赖有效果。当 Maven 需要的插件在本地仓库不存在时是不会去我们以前配置的远程仓库查找插件的，而是需要有专门的插件远程仓库，我们来看看怎么配置插件远程仓库，在 `pom.xml` 加入如下内容：

```xml
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
```

大家可以发现，除了 `pluginRepositories` 和 `pluginRepository` 与以前配置远程仓库不同以外，其他的都是一样的，所代表的含义也是一样的。Maven 的父 POM 中也是有内置一个插件仓库的，我现在用的电脑安装的是 Maven 3.0.4 版本，我们可以找到这个文件：`${M2_HOME}/lib/maven-model-builder-3.0.4.jar`，打开该文件，能找到超级父 POM：`\org\apache\maven\model\pom-4.0.0.xml`，它是所有 Maven POM 的父 POM，所有 Maven 项目都继承该配置。

我们来看看默认的远程插件仓库配置的是啥：

```xml
<pluginRepositories>
    <pluginRepository>
      <id>central</id>
      <name>Central Repository</name>
      <url>http://repo.maven.apache.org/maven2</url>
      <layout>default</layout>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
      <releases>
        <updatePolicy>never</updatePolicy>
      </releases>
    </pluginRepository>
</pluginRepositories>
```

默认插件仓库的地址就是中央仓库咯，它关闭了对 snapshots 的支持，防止引入 snapshots 版本的插件而导致不稳定的构件。一般来说，中央仓库所包含的插件完全能够满足我们的需要，只有在少数情况下才要配置，比如项目的插件无法在中央仓库找到，或者自己编写了插件才会配置自己的远程插件仓库。

# 2、插件命令运行解析

我们来看这样一个命令：

```
mvn compiler:compiler
```

这个命令会调用 `maven-compiler-plugin` 插件并执行 `compiler` 目标，大家有木有觉得很神奇？我们在 `pom.xml` 中配置插件往往是这样：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.1</version>
    <configuration>
        <source>1.7</source> <!-- 源代码使用的开发版本 -->
        <target>1.7</target> <!-- 需要生成的目标class文件的编译版本 -->
    </configuration>
</plugin>
```

`maven-compiler-plugin` 插件默认执行的目标为 `compiler`，那么命令的完整写法应该是：mvn org.apache.maven.plugins:maven-compiler-plugin:3.1:compiler 才对啊，为什么 `mvn compiler:compiler` 也能完美的执行？

我们来看看 Maven 到底干了些神马来做到如此牛逼的功能：

**① 插件默认 groupId**

Maven 默认以 org.apache.maven.plugins 作为 groupId，到这里我们的命令应该是长这样的：

```
mvn org.apache.maven.plugins:compiler:compiler
```

我们也可以配置自己默认的 groupId，在 Maven 的 `settings.xml` 中添加如下内容，前面提过最好将 `settings.xml` 放在用户目录的 `.m2` 下：

```xml
<pluginGroups>
    <!-- pluginGroup
     | Specifies a further group identifier to use for plugin lookup.
    <pluginGroup>com.your.plugins</pluginGroup>
    -->
    <pluginGroup>com.your.plugins</pluginGroup>
</pluginGroups>
```

不过说实在的，没必要动他就别去动他了，我们用 Maven 只是解决一些刚需的问题，没必要的设置就尽量不去动他，别把 Maven 搞得太复杂，虽然 Maven 的却有点小复杂，跟大家扯这些只是希望大家能够对 maven 理解的更深入那么一点点，并不是建议大家一定要去使用某些东西，大家在平时的开发中要谨记这一点。

② 我们来看看 Maven 插件远程仓库的元数据 `org/apache/maven/plugins/maven-metadata.xml`，Maven 默认的远程仓库是 `http://repo.maven.apache.org/maven2/`，所有插件元数据路径则是：`http://repo.maven.apache.org/maven2/org/apache/maven/plugins/maven-metadata.xml`，我们找到 compiler 插件的元数据，如图：
![](assets/Maven%20教程（13）—%20Maven插件解析运行机制/file-20251122091809694.png)
这里会根据 prefix 指定的前缀找到对应的 artifactId，到这里我们的命令应该长成了这样：

```
mvn org.apache.maven.plugins:maven-compiler-plugin:compiler
```

③ 我们再根据 `groupId` 和 `artifactId` 找到 `maven-compiler-plugin` 插件单个的元数据，路径为 [http://repo.maven.apache.org/maven2/org/apache/maven/plugins/maven-compiler-plugin/maven-metadata.xml](http://repo.maven.apache.org/maven2/org/apache/maven/plugins/maven-compiler-plugin/maven-metadata.xml)，如图：
![](assets/Maven%20教程（13）—%20Maven插件解析运行机制/file-20251122091818732.png)
maven 将所有的远程插件仓库及本地仓库元数据归并后，就能找到 release 的版本（maven3 后为了保证项目构建的稳定性默认使用 release 版本），到这里命令就被扩展成为这样：

```
mvn org.apache.maven.plugins:maven-compiler-plugin:3.6.0:compiler
```

如果执行的是 `mvn compiler:compiler` 命令，由于 `maven-compiler-plugin` 的最新版本已经到了 3.6.0，则默认会使用此版本。最后的 `compiler` 则是插件要执行的目标咯，看到这里大家应该明白 `mvn compiler:compiler` 命令为什么能够得到完美的运行了吧。

# 3、Maven 超级 POM

最后给大家把超级父 POM 贴出来，再次强调，如果我们没有在自己的 `pom.xml` 中配置相应的内容，则默认会使用超级父 POM 配置的内容。我现在用的电脑安装的是 Maven 3.5.2 版本，我们可以找到这个文件：`${M2_HOME}/lib/maven-model-builder-3.5.2.jar`，打开该文件，能找到超级父 POM：`\org\apache\maven\model\pom-4.0.0.xml`，它是所有 Maven POM 的父 POM，所有 Maven 项目都继承该配置。

```xml
<?xml version="1.0" encoding="UTF-8"?>

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

<!-- START SNIPPET: superpom -->
<project>
  <modelVersion>4.0.0</modelVersion>

  <repositories>
    <repository>
      <id>central</id>
      <name>Central Repository</name>
      <url>https://repo.maven.apache.org/maven2</url>
      <layout>default</layout>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>
  </repositories>

  <pluginRepositories>
    <pluginRepository>
      <id>central</id>
      <name>Central Repository</name>
      <url>https://repo.maven.apache.org/maven2</url>
      <layout>default</layout>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
      <releases>
        <updatePolicy>never</updatePolicy>
      </releases>
    </pluginRepository>
  </pluginRepositories>

  <build>
    <directory>${project.basedir}/target</directory>
    <outputDirectory>${project.build.directory}/classes</outputDirectory>
    <finalName>${project.artifactId}-${project.version}</finalName>
    <testOutputDirectory>${project.build.directory}/test-classes</testOutputDirectory>
    <sourceDirectory>${project.basedir}/src/main/java</sourceDirectory>
    <scriptSourceDirectory>${project.basedir}/src/main/scripts</scriptSourceDirectory>
    <testSourceDirectory>${project.basedir}/src/test/java</testSourceDirectory>
    <resources>
      <resource>
        <directory>${project.basedir}/src/main/resources</directory>
      </resource>
    </resources>
    <testResources>
      <testResource>
        <directory>${project.basedir}/src/test/resources</directory>
      </testResource>
    </testResources>
    <pluginManagement>
      <!-- NOTE: These plugins will be removed from future versions of the super POM -->
      <!-- They are kept for the moment as they are very unlikely to conflict with lifecycle mappings (MNG-4453) -->
      <plugins>
        <plugin>
          <artifactId>maven-antrun-plugin</artifactId>
          <version>1.3</version>
        </plugin>
        <plugin>
          <artifactId>maven-assembly-plugin</artifactId>
          <version>2.2-beta-5</version>
        </plugin>
        <plugin>
          <artifactId>maven-dependency-plugin</artifactId>
          <version>2.8</version>
        </plugin>
        <plugin>
          <artifactId>maven-release-plugin</artifactId>
          <version>2.3.2</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>

  <reporting>
    <outputDirectory>${project.build.directory}/site</outputDirectory>
  </reporting>

  <profiles>
    <!-- NOTE: The release profile will be removed from future versions of the super POM -->
    <profile>
      <id>release-profile</id>

      <activation>
        <property>
          <name>performRelease</name>
          <value>true</value>
        </property>
      </activation>

      <build>
        <plugins>
          <plugin>
            <inherited>true</inherited>
            <artifactId>maven-source-plugin</artifactId>
            <executions>
              <execution>
                <id>attach-sources</id>
                <goals>
                  <goal>jar</goal>
                </goals>
              </execution>
            </executions>
          </plugin>
          <plugin>
            <inherited>true</inherited>
            <artifactId>maven-javadoc-plugin</artifactId>
            <executions>
              <execution>
                <id>attach-javadocs</id>
                <goals>
                  <goal>jar</goal>
                </goals>
              </execution>
            </executions>
          </plugin>
          <plugin>
            <inherited>true</inherited>
            <artifactId>maven-deploy-plugin</artifactId>
            <configuration>
              <updateReleaseInfo>true</updateReleaseInfo>
            </configuration>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>

</project>
<!-- END SNIPPET: superpom -->
```

很多插件是超级父 POM 当中并没有配置的，如果用户使用某个插件时没有设定版本，那么则会根据我上述所说的规则去仓库中查找可用的版本，然后做出选择。在 Maven2 中，插件的版本会被解析至 latest。也就是说，当用户使用某个非核心插件且没有声明版本的时候，Maven 会将版本解析为所有可用仓库中的最新版本，latest 表示的就是最新版本，而这个版本很有可能是快照版本。

当插件为快照版本时，就会出现潜在的问题。昨天还好好的，可能今天就出错了，其原因是这个快照版本发生了变化导致的。为了防止这类问题，Maven3 调整了解析机制，当插件没有声明版本的时候，不再解析至 latest，而是使用 release。这样就避免了由于快照频繁更新而导致的不稳定问题。但是这样就好了吗？不写版本号其实是不推荐的做法，例如，我使用的插件发布了一个新版本，而这个 release 版本与之前的版本的行为发生了变化，这种变化依然可能导致我们项目的瘫痪。所以使用插件的时候，应该一直显式的设定版本，这也解释了 Maven 为什么要在超级父 POM 中为核心插件设定版本咯。

结束语：当你感到悲哀痛苦时，最好是去学些什么东西，学习会使你从悲哀痛苦中走出来，学习会使你永远立于不败之地。说实在的，不要太在意眼前所发生的一切，更重要的是培养自己的个人能力，如今待在公司亦或者跳槽，决定你能不能继续走下去的一定是你的个人能力，作为年轻人，在公司更看重的不应该是薪水的高低，而是公司能给你带来多大的成长环境。找个好的公司其实不比找个合适的女朋友简单，作为年轻人我们一定要不断的提升个人能力，就跟找女朋友似的，往往就是你越有本事就越能够不将就，你个人能力越强则越有选择公司的资本。
