1、远程仓库的配置

在平时的开发中，我们往往不会使用默认的中央仓库，默认的中央仓库访问的速度比较慢，访问的人或许很多，有时候也无法满足我们项目的需求，可能项目需要的某些构件中央仓库中是没有的，而在其他远程仓库中有，如JBoss Maven仓库。这时，可以在pom.xml中配置该仓库，代码如下：

 ```xml
  <!-- 配置远程仓库 -->
    <repositories>
        <repository>
            <id>jboss</id>
            <name>JBoss Repository</name>
            <url>http://repository.jboss.com/maven2/</url>
            <releases>
                <enabled>true</enabled>
                <updatePolicy>daily</updatePolicy>
            </releases>
            <snapshots>
                <enabled>false</enabled>
                <checksumPolicy>warn</checksumPolicy>
            </snapshots>
            <layout>default</layout>
        </repository>
    </repositories>
 ```

repository：在repositories元素下，可以使用repository子元素声明一个或者多个远程仓库。

id：仓库声明的唯一id，尤其需要注意的是，Maven自带的中央仓库使用的id为central，如果其他仓库声明也使用该id，就会覆盖中央仓库的配置。

name：仓库的名称，让我们直观方便的知道仓库是哪个，暂时没发现其他太大的含义。

url：指向了仓库的地址，一般来说，该地址都基于http协议，Maven用户都可以在浏览器中打开仓库地址浏览构件。

releases 和 snapshots：用来控制Maven对于发布版构件和快照版构件的下载权限。需要注意的是enabled子元素，该例中releases的enabled值为true，表示开启JBoss仓库的发布版本下载支持，而snapshots的enabled值为false，表示关闭JBoss仓库的快照版本的下载支持。根据该配置，Maven只会从JBoss仓库下载发布版的构件，而不会下载快照版的构件。

layout：元素值default表示仓库的布局是Maven2及Maven3的默认布局，而不是Maven1的布局。基本不会用到Maven1的布局。

其他：对于releases和snapshots来说，除了enabled，它们还包含另外两个子元素updatePolicy和checksumPolicy。

元素updatePolicy用来配置Maven从远处仓库检查更新的频率，默认值是daily，表示Maven每天检查一次。其他可用的值包括：never-从不检查更新；always-每次构建都检查更新；interval：X-每隔X分钟检查一次更新（X为任意整数）。

元素checksumPolicy用来配置Maven检查校验和文件的策略。当构建被部署到Maven仓库中时，会同时部署对应的检验和文件。在下载构件的时候，Maven会验证校验和文件，如果校验和验证失败，当checksumPolicy的值为默认的warn时，Maven会在执行构建时输出警告信息，其他可用的值包括：fail-Maven遇到校验和错误就让构建失败；ignore-使Maven完全忽略校验和错误。

2、远程仓库的认证

大部分公共的远程仓库无须认证就可以直接访问，但我们在平时的开发中往往会架设自己的Maven远程仓库，出于安全方面的考虑，我们需要提供认证信息才能访问这样的远程仓库。配置认证信息和配置远程仓库不同，远程仓库可以直接在pom.xml中配置，但是认证信息必须配置在settings.xml文件中。这是因为pom往往是被提交到代码仓库中供所有成员访问的，而settings.xml一般只存在于本机。因此，在settings.xml中配置认证信息更为安全。

```xml
<settings>
     …
     <!--配置远程仓库认证信息-->
     <servers>
         <server>
             <id>releases</id>
             <username>admin</username>
             <password>admin123</password>
         </server>
     </servers>
     …
</settings>
```

上面代码我们配置了一个id为releases的远程仓库认证信息。Maven使用settings.xml文件中的servers元素及其子元素server配置仓库认证信息。认证用户名为admin，认证密码为admin123。这里的关键是id元素，settings.xml中server元素的id必须与pom.xml中需要认证的repository元素的id完全一致。正是这个id将认证信息与仓库配置联系在了一起。

3、部署构件至远程仓库

我们使用自己的远程仓库的目的就是在远程仓库中部署我们自己项目的构件以及一些无法从外部仓库直接获取的构件。这样才能在开发时，供其他对团队成员使用。

Maven除了能对项目进行编译、测试、打包之外，还能将项目生成的构件部署到远程仓库中。首先，需要编辑项目的pom.xml文件。配置distributionManagement元素，代码如下：

```xml
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
```

distributionManagement包含repository和snapshotRepository子元素，前者表示发布版本（稳定版本）构件的仓库，后者表示快照版本（开发测试版本）的仓库。这两个元素都需要配置id、name和url，id为远程仓库的唯一标识，name是为了方便人阅读，关键的url表示该仓库的地址。

往远程仓库部署构件的时候，往往需要认证，配置认证的方式同上。

配置正确后，运行命令mvn clean deploy，Maven就会将项目构建输出的构件部署到配置对应的远程仓库，如果项目当前的版本是快照版本，则部署到快照版本的仓库地址，否则就部署到发布版本的仓库地址。

快照版本和发布版本的区别请自行上百度查阅资料。

4、配置远程仓库的镜像

如果仓库X可以提供仓库Y存储的所有内容，那么就可以认为X是Y的一个镜像。换句话说，任何一个可以从仓库Y获得的构件，都能够从它的镜像中获取。举个例子，[http://maven.oschina.net/content/groups/public/](http://maven.oschina.net/content/groups/public/) 是中央仓库[http://repo1.maven.org/maven2/](http://repo1.maven.org/maven2/) 在中国的镜像，由于地理位置的因素，该镜像往往能够提供比中央仓库更快的服务。因此，可以配置Maven使用该镜像来替代中央仓库。编辑settings.xml，代码如下：

 ```xml
 <mirrors>
     <mirror>
      <id>maven.oschina.net</id>
      <name>maven mirror in China</name>
      <url>http://maven.oschina.net/content/groups/public/</url>
      <mirrorOf>central</mirrorOf>
    </mirror>
</mirrors>
 ```

该例中，mirrorOf的值为central，表示该配置为中央仓库的镜像，任何对于中央仓库的请求都会转至该镜像，用户也可以使用同样的方法配置其他仓库的镜像。id表示镜像的唯一标识符，name表示镜像的名称，url表示镜像的地址。

关于镜像的一个更为常见的用法是结合私服。由于私服可以代理任何外部的公共仓库(包括中央仓库)，因此，对于组织内部的Maven用户来说，使用一个私服地址就等于使用了所有需要的外部仓库，这可以将配置集中到私服，从而简化Maven本身的配置。在这种情况下，任何需要的构件都可以从私服获得，私服就是所有仓库的镜像。这时，可以配置这样的一个镜像：

 ```xml
 <!--配置私服镜像-->
<mirrors> 
    <mirror>  
        <id>nexus</id>  
        <name>internal nexus repository</name>  
        <url>http://183.238.2.182:8081/nexus/content/groups/public/</url>  
        <mirrorOf>*</mirrorOf>  
    </mirror>  
</mirrors>
1
 ```

该例中的值为星号，表示该配置是所有Maven仓库的镜像，任何对于远程仓库的请求都会被转至[http://183.238.2.182:8081/nexus/content/groups/public/](http://183.238.2.182:8081/nexus/content/groups/public/)。如果该镜像仓库需要认证，则配置一个id为nexus的认证信息即可。

需要注意的是，由于镜像仓库完全屏蔽了被镜像仓库，当镜像仓库不稳定或者停止服务的时候，Maven仍将无法访问被镜像仓库，因而将无法下载构件。

5、可用的Maven镜像仓库

   repo2

   central

   Human Readable Name for this Mirror.

   http://repo2.maven.org/maven2/

​

   ui

   central

   Human Readable Name for this Mirror.

   http://uk.maven.org/maven2/

​

   ibiblio

   central

   Human Readable Name for this Mirror.

   http://mirrors.ibiblio.org/pub/mirrors/maven2/

​

   jboss-public-repository-group

   central

   JBoss Public Repository Group

   http://repository.jboss.org/nexus/content/groups/public

​

   JBossJBPM

   central

   JBossJBPM Repository

   https://repository.jboss.org/nexus/content/repositories/releases/

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

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

上面的仓库经过测试是可以访问的。

6、仓库搜索服务地址

Sonatype Nexus：[https://repository.sonatype.org/](https://repository.sonatype.org/)

MVNrepository：[http://mvnrepository.com/](http://mvnrepository.com/)

关于依赖的搜索，个人觉得这两个是最好用的。

结束语：要得到你必须要付出，要付出你还要学会坚持，如果你真的觉得很难，那你就放弃，但是你放弃了就不要抱怨，世界真的是平衡的，我觉得人生就是这样，每个人都是通过自己的努力，去决定自己生活的样子。