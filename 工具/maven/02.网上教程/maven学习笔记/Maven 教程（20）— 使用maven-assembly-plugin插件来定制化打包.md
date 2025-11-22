简单的说，maven-assembly-plugin 就是用来帮助打包用的，比如说打出一个什么类型的包，包里包括哪些内容等等。

目前至少支持以下打包类型：

zip

tar

tar.gz

tar.bz2

jar

dir

war

默认情况下，打 jar 包时，只有在类路径上的文件资源会被打包到 jar 中，并且文件名是 ${artifactId}-${version}.jar，下面看看怎么用 maven-assembly-plugin 插件来定制化打包。

首先需要添加插件声明：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>2.4</version>
    <executions>
        <execution>
            <!-- 绑定到package生命周期阶段上 -->
            <phase>package</phase>
            <goals>
                <!-- 绑定到package生命周期阶段上 -->
                <goal>single</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```


使用内置的 Assembly Descriptor

要使用 maven-assembly-plugin，需要指定至少一个要使用的 assembly descriptor 文件。默认情况下，maven-assembly-plugin 内置了几个可以用的 assembly descriptor：

bin ： 类似于默认打包，会将 bin 目录下的文件打到包中；

jar-with-dependencies ： 会将所有依赖都解压打包到生成物中；

src ：只将源码目录下的文件打包；

project ： 将整个 project 资源打包。

要查看它们的详细定义，可以到 maven-assembly-plugin-2.4.jar 里去看，例如对应 bin 的 assembly descriptor 如下：

```xml
<assembly xmlns="http://maven.apache.org/plugins/maven-assembly-plugin/assembly/1.1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/plugins/maven-assembly-plugin/assembly/1.1.0 http://maven.apache.org/xsd/assembly-1.1.0.xsd">
    <id>bin</id>
    <formats>
        <format>tar.gz</format>
        <format>tar.bz2</format>
        <format>zip</format>
    </formats>
    <fileSets>
        <fileSet>
            <directory>${project.basedir}</directory>
            <outputDirectory>/</outputDirectory>
            <includes>
                <include>README*</include>
                <include>LICENSE*</include>
                <include>NOTICE*</include>
            </includes>
        </fileSet>
        <fileSet>
            <directory>${project.build.directory}</directory>
            <outputDirectory>/</outputDirectory>
            <includes>
                <include>*.jar</include>
            </includes>
        </fileSet>
        <fileSet>
            <directory>${project.build.directory}/site</directory>
            <outputDirectory>docs</outputDirectory>
        </fileSet>
    </fileSets>
</assembly>
```



自定义 Assembly Descriptor

一般来说，内置的 assembly descriptor 都不满足需求，这个时候就需要写自己的 assembly descriptor 的实现了。先从一个最简单的定义开始：

```xml
<?xml version='1.0' encoding='UTF-8'?>
<assembly xmlns="http://maven.apache.org/plugins/maven-assembly-plugin/assembly/1.1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/plugins/maven-assembly-plugin/assembly/1.1.0  
                    http://maven.apache.org/xsd/assembly-1.1.0.xsd">
    <id>demo</id>
    <formats>
        <format>jar</format>
    </formats>
    <includeBaseDirectory>false</includeBaseDirectory>
    <fileSets>
        <fileSet>
            <directory>${project.build.directory}/classes</directory>
            <outputDirectory>/</outputDirectory>
        </fileSet>
    </fileSets>
</assembly>
```

这个定义很简单：

format：指定打包类型；

includeBaseDirectory：指定是否包含打包层目录（比如 finalName 是 output，当值为 true，所有文件被放在 output 目录下，否则直接放在包的根目录下）；

fileSets：指定要包含的文件集，可以定义多个 fileSet；

directory：指定要包含的目录；

outputDirectory：指定当前要包含的目录的目的地。

要使用这个 assembly descriptor，需要如下配置：

```xml
<configuration>  
    <finalName>demo</finalName>  
    <descriptors>
        <!--描述文件路径-->
        <descriptor>assemblies/demo.xml</descriptor>  
    </descriptors>  
    <outputDirectory>output</outputDirectory>
</configuration> 
```
最后会生成一个demo-demo.jar 文件在目录 output 下，其中前一个demo来自finalName，后一个demo来自assembly descriptor中的id，其中的内容和默认的打包出来的jar类似。

如果只想有 finalName，则增加配置：

```xml
<appendAssemblyId>false</appendAssemblyId>
```

添加文件

上面演示了添加所有编译后的资源，同样的可以增加其他资源，例如想添加当前工程目录下的某个文件 b.txt ，在 assembly descriptor 的 assembly 结点下增加

```xml
<files> 
	<file> 
		<source>b.txt</source> 
		<outputDirectory>/</outputDirectory> 
	</file> 
</files>
```

也可以改变打包后的文件名，例如上面的 b.txt ，希望打包后的名字为 b.txt.bak， 只需要在 file 里添加以下配置 ：

```xml
<destName>b.txt.bak</destName>
```

排除文件

在 fileSet 里可以使用 includes 和 excludes 来更精确的控制哪些文件要添加，哪些文件要排除。

例如要排除某个目录下所有的 txt 文件：

```xml
<fileSet>  
    <directory>${project.build.directory}/classes</directory>  
    <outputDirectory>/</outputDirectory>  
    <excludes>  
        <exclude>**/*.txt</exclude>  
    </excludes>  
</fileSet>
```
或者某个目录下只想 .class 文件：

```xml
<fileSet>
    <directory>${project.build.directory}/classes</directory>
    <outputDirectory>/</outputDirectory>
    <includes>
        <include>**/*.class</include>
    </includes>
</fileSet>
```
添加依赖
如果想把一些依赖库打到包里，可以用 dependencySets 元素，例如最简单的，把当前工程的所有依赖都添加到包里：

```xml
<dependencySets> 
	<dependencySet> 
		<outputDirectory>/</outputDirectory> 
	</dependencySet> 
</dependencySets>
```
在assembly下添加以上配置，则当前工程的依赖和工程本身生成的jar都会被打包进来。

如果要排除工程自身生成的 jar，则可以添加



```xml
<useProjectArtifact>false</useProjectArtifact>
```

unpack 参数可以控制依赖包是否在打包进来时是否解开，例如解开所有包，添加以下配置：

```xml
<unpack>true</unpack>
```

和 fileSet 一样，可以使用 excludes 和 includes 来更详细的控制哪些依赖需要打包进来；另外 useProjectAttachments，useTransitiveDependencies，useTransitiveFiltering 等参数可以对间接依赖、传递依赖进行控制。

其他选项

moduleSets：当有子模块时候用；

repositories：想包含库的时候用；

containerDescriptorHandlers：可以进行一些合并，定义 ArtifactHandler 之类的时候可以用，（可以参考：说明）；

componentDescriptors：如上所述，可以包含一些 componentDescriptor 定义，这些定义可以被多个 assembly 共享。

Assembly Plugin 更多配置

上面已经看到了一些 Assembly Plugin 本身的配置，例如 finalName， outputDirectory， appendAssemblyId 和 descriptors 等，除了这些还有其他的一些可配置参数，参见：single，其中某些参数会覆盖在 assembly descriptor 中的参数。有一个比较有用的参数是： archive，它的详细配置在：archive。

下面介绍一些 archive 的用法。

指定 Main-Class

archive 的一个重要用处就是配置生成的 MANIFEST.MF 文件。默认会生成一个 MANIFEST.MF 文件，不过这个文件默认值没什么意义。如果想指定生成 jar 的 Main-Class，可以如下配置：

```xml
<archive> <manifest> <mainClass>demo.DemoMain</mainClass> </manifest> </archive>
```
下面来看一个项目中实际配置的文件：

pom 文件：

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>${maven-assembly-plugin.version}</version>
    <configuration>
        <descriptors>
            <descriptor>package.xml</descriptor>
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
一键获取完整项目代码

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

assembly descriptor 文件：

<assembly>
    <id>${assembly-id}</id>
    <!-- 最终打包成一个用于发布的war文件 -->
    <formats>
        <format>${assembly-format}</format>
    </formats>

    <fileSets>
        <!-- 把项目公用的配置文件，打包进zip文件的config目录 -->
        <fileSet>
            <directory>${project.basedir}/src/main/resources/base</directory>
            <outputDirectory>WEB-INF/classes</outputDirectory>
        </fileSet>

        <!-- 把项目环境的配置文件，打包进zip文件的config目录 -->
        <fileSet>
            <directory>${project.basedir}/src/main/resources/${env}</directory>
            <outputDirectory>WEB-INF/classes</outputDirectory>
        </fileSet>

        <!-- 打包项目自己编译出来的jar文件 -->
        <fileSet>
            <directory>${project.build.directory}</directory>
            <outputDirectory>WEB-INF/lib</outputDirectory>
            <includes>
                <include>*.jar</include>
            </includes>
        </fileSet>

        <!-- 打包项目依赖的jar文件 -->
        <fileSet>
            <directory>${project.build.directory}</directory>
            <outputDirectory>/</outputDirectory>
            <includes>
                <include>WEB-INF/lib/*.jar</include>
            </includes>
        </fileSet>
    </fileSets>
</assembly>
一键获取完整项目代码

————————————————

版权声明：本文为 CSDN 博主「挖坑埋你」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。

原文链接：https://blog.csdn.net/liupeifeng3514/article/details/79777976
