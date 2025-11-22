除了坐标、依赖以及仓库之外，Maven的另外两个核心概念是`生命周期`和`插件`。在有关Maven的日常使用中，[命令行](https://so.csdn.net/so/search?q=%E5%91%BD%E4%BB%A4%E8%A1%8C&spm=1001.2101.3001.7020)的输入往往就对应了生命周期，如`mvn package`就表示执行默认生命周期阶段package。Maven的生命周期是抽象的，其实际行为都由插件来完成，如`package阶段`的任务可能就会由`maven-jar-plugin`完成。`生命周期`和`插件`两者协同工作，密不可分。

#### 1、Maven生命周期

我们在开发项目的时候，我们不断地在经历编译、测试、打包、部署等过程，maven的生命周期就是对所有这些过程的一个抽象与统一，她的**生命周期包含项目的清理、初始化、编译、测试、打包、集成测试、验证、部署、站点生成等几乎所有的过程**，而且maven的生命周期是及其灵活，她**生命周期的每个阶段是通过插件来实现的**，maven也内置了很多插件，所以我们在项目进行编译、测试、打包的过程是没有感觉到。像编译是通过maven-compile-plugin实现的、测试是通过maven-surefire-plugin实现的。

**Maven有三套相互独立的生命周期**，请注意这里说的是“三套”，而且“相互独立”，初学者容易将Maven的生命周期看成一个整体，其实不然。这三套生命周期分别是：

- Clean Lifecycle 在进行真正的构建之前进行一些清理工作。
- Default Lifecycle 构建的核心部分，编译，测试，打包，部署等等。
- Site Lifecycle 生成项目报告，站点，发布站点。

我再次强调一下它们是`相互独立`的，你可以仅仅调用clean来清理工作目录，仅仅调用site来生成站点。当然你也可以直接运行`mvn clean install site`运行所有这三套生命周期。

知道了每套生命周期的大概用途和相互关系以后，来逐个详细看一下每套生命周期，Clean和Site相对比较简单，先解释一下：

每套生命周期都由一组阶段(Phase)组成，我们平时在命令行输入的命令总会对应于一个特定的阶段。比如，运行`mvn clean`，这个的clean是Clean生命周期的一个阶段。有点绕？要知道有Clean生命周期，也有clean阶段。

Clean生命周期一共包含了三个阶段：

- pre-clean 执行一些需要在clean之前完成的工作。
- clean 移除所有上一次构建生成的文件。
- post-clean 执行一些需要在clean之后立刻完成的工作。

`mvn clean`中的`clean`就是上面的clean，在一个生命周期中，运行某个阶段的时候，它之前的所有阶段都会被运行，也就是说，`mvn clean`等同于 `mvn pre-clean clean`，如果我们运行`mvn post-clean`，那么`pre-clean`、`clean`都会被运行。这是Maven很重要的一个规则，可以大大简化命令行的输入。

下面看一下Site生命周期的各个阶段：

- pre-site 执行一些需要在生成站点文档之前完成的工作。
- site 生成项目的站点文档。
- post-site 执行一些需要在生成站点文档之后完成的工作，并且为部署做准备。
- site-deploy 将生成的站点文档部署到特定的服务器上。

这里经常用到的是site阶段和site-deploy阶段，用以生成和发布Maven站点，这可是Maven相当强大的功能，Manager比较喜欢，文档及统计数据自动生成，很好看。

最后，来看一下Maven的最重要的Default生命周期，绝大部分工作都发生在这个生命周期中，这里，我只解释一些比较重要和常用的阶段：

- validate
- initialize
- generate-sources
- process-sources 处理项目主资源文件。一般来说，是对`src/main/resources`目录的内容进行变量替换等工作后，复制到项目输出的`主classpath目录`中。
- generate-resources
- process-resources
- compile 编译项目的源代码。一般来说，是编译`src/main/java`目录下的Java文件至项目输出的`主classpath目录`中。
- process-classes
- generate-test-sources
- process-test-sources 处理项目测试资源文件。一般来说，是对`src/test/resources`目录的内容进行变量替换等工作后，复制到项目输出的`测试classpath目录`中。
- generate-test-resources
- process-test-resources
- test-compile 编译项目的测试源代码。一般来说，是编译`src/test/java`目录下的Java文件至项目输出的`测试classpath目录`中。
- process-test-classes
- test 使用合适的单元测试框架运行测试。这些测试代码不会被打包或部署。
- prepare-package
- package 接受编译好的代码，打包成可发布的格式，如 JAR 。
- pre-integration-test
- integration-test
- post-integration-test
- verify
- install 将包安装至本地仓库，以让其它项目依赖。
- deploy 将最终的包复制到远程的仓库，以让其它开发人员与Maven项目使用。

基本上，根据名称我们就能猜出每个阶段的用途，关于阶段的详细解释以及其她阶段的解释，请参考 [http://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html](http://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html) 。

记住，运行任何一个阶段的时候，它前面的所有阶段都会被运行，这也就是为什么我们运行`mvn install`的时候，代码会被编译，测试，打包。

此外，Maven的插件机制是完全依赖Maven的生命周期的，因此理解生命周期至关重要，接下来我将会进一步解释Maven的插件机制。

#### 2、命令行与生命周期

从命令行执行Maven任务的最主要方式就是调用Maven的生命周期阶段。需要注意的是，**各个生命周期是相互独立的**，而**一个生命周期的阶段是有前后依赖关系的**。下面以一些常见的Maven命令为例，解释其执行的生命周期阶段：

**mvn clean**：该命令调用clean生命周期的clean阶段。实际执行的阶段为clean生命周期的`pre-clean`和`clean`阶段。

**mvn test**：该命令调用`default生命周期`的`test阶段`。实际执行的阶段为default生命周期的`validate`、`initialize`等，直到`test`的所有阶段。这也解释了为什么在执行测试的时候，项目的代码能够自动得以编译。

**mvn clean install**：该命令调用`clean生命周期`的`clean阶段`和`default生命周期`的`install阶段`。实际执行的阶段为clean生命周期的pre-clean、clean阶段，以及default生命周期的从validate至install的所有阶段。该命令结合了两个生命周期，在执行正在的项目构建之前清理项目是一个很好的实践。

**mvn clean deploy site-deploy**：该命令调用`clean生命周期`的`clean阶段`、`default生命周期`的`deploy阶段`，以及`site生命周期`的`site-deploy阶段`。实际执行的阶段为clean生命周期的pre-clean、clean阶段，default生命周期的所有阶段，以及site生命周期的所有阶段。该命令结合了Maven所有三个生命周期，且deploy为default生命周期的最后一个阶段，site-deploy为site生命周期的最后一个阶段。

由于Maven中主要的生命周期阶段并不多，而常用的Maven命令实际都是基于这些阶段简单组合而成的，因此只要对Maven生命周期有一个基本的理解，读者就可以正确而熟练地使用Maven命令。

#### 3、Maven插件机制

> 如何将插件与 Maven 的构建生命周期绑定在一起呢？通过将插件的目标（goal）与 build lifecycle 中 phase 绑定到一起，这样，当要执行某个 phase 时，就调用插件来完成绑定的目标。

通过上面的生命周期我们可以了解到，不同的生命周期绑定不同的插件；同时我们知道，下载下来的maven核心的东西不过3-4M，它主要就是通过插件来完成这些工作的，一旦碰到没有的插件，它会跑到相应的地方下载，然后来完成整个过程。那么在我们的项目中如何使用插件呢？

打开[http://maven.apache.org/plugins/index.html](http://maven.apache.org/plugins/index.html)网址，我们可以看到apache下面的很多插件，apache下面的插件是比较正规的，它里面的信息非常详细。下面我们来看看里面有个source的插件的用法。

Source插件是对源代码进行打包的一个插件，默认情况下，它会将生成的源代码放在工程目录的target下面。

Source插件具有五个**目标**：

- [source:aggregate](http://maven.apache.org/plugins/maven-source-plugin/aggregate-mojo.html) aggregrates sources for all modules in an aggregator project.
- [source:jar](http://maven.apache.org/plugins/maven-source-plugin/jar-mojo.html) is used to bundle the main sources of the project into a jar archive.
- [source:test-jar](http://maven.apache.org/plugins/maven-source-plugin/test-jar-mojo.html) on the other hand, is used to bundle the test sources of the project into a jar archive.
- [source:jar-no-fork](http://maven.apache.org/plugins/maven-source-plugin/jar-no-fork-mojo.html) is similar to jar but does not fork the build lifecycle.
- [source:test-jar-no-fork](http://maven.apache.org/plugins/maven-source-plugin/test-jar-no-fork-mojo.html) is similar to test-jar but does not fork the build lifecycle.

在我们的工程`pom.xml`中，在后面引入下面这段配置：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-source-plugin</artifactId>
            <version>2.1.2</version>
        </plugin>
    </plugins>
</build>
```

上面这段配置就是**对源码进行打包的插件**，我们运行`source:jar-no-fork`，那么在项目的目录底下的`target`会生成一个类似于`user-core-0.0.1-SNAPSHOT-sources.jar`这样的文件，即项目的源文件。那么如何将这个插件与特定的生命周期绑定呢？我们来看下面这段配置：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-source-plugin</artifactId>
            <version>2.1.2</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>jar-no-fork</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

通过这段配置，大家可以用`mvn package`将项目打包的同时会将源代码进行打包。图示说明：  
![](assets/Maven%20教程（12）—%20Maven生命周期和插件/file-20251122091509113.png)  
Apache Maven里面还有很多有用的插件，大家可以自己去试一下，里面说明很详细，大家只要按着官方文档进行配置，一般情况下是没问题的，如果大家想把插件用的非常熟练建议多请教请教大神，或者购买《Maven实战》书籍，书籍中对插件会介绍的更详细，然后再结合大神使用的经验，相信大家能够熟练地使用Maven插件机制。

结束语：今天走的路，你要记在心里，无论你与目标之间有多远，也要学会轻松地走路。只有这样，在走向目标的过程中，才不会感到烦闷，才不会被遥远的未来所吓倒。