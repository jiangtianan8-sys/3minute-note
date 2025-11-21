每次项目部署上线都需要手动去修改配置文件（比如数据库配置，或者一个自定义的配置）然后才能打包，很麻烦，网上找到 maven profile 可以完成这个工作，记录如下：

环境：eclipse + spring mvc + maven

1、直接看图，把数据库的配置单独拿出来放在了 resources_env 目录下，三个不同环境参数不同，

![0](https://note.youdao.com/yws/res/2246/9656229C23F94DD2A9CA7EFD09D9FF0D)

2，在 pom 文件中添加配置    这个引用自：http://www.cnblogs.com/raphael5200/p/6677549.html，感谢

![0](https://note.youdao.com/yws/res/2249/6228565F7B584168BE663123C5A0CC93)

<profiles> <profile> <id>devid> <properties> <env>devenv> properties> <activation> <activeByDefault>trueactiveByDefault> activation> <build> <resources> <resource> <directory>src/main/resources_env/devdirectory> resource> <resource> <directory>src/main/resourcesdirectory> resource> resources> build> profile> <profile> <id>qaid> <properties> <env>qaenv> properties> <build> <resources> <resource> <directory>src/main/resources_env/qadirectory> resource> <resource> <directory>src/main/resourcesdirectory> resource> resources> build> profile> <profile> <id>onlineid> <properties> <env>onlineenv> properties> <build> <resources> <resource> <directory>src/main/resources_env/onlinedirectory> resource> <resource> <directory>src/main/resourcesdirectory> resource> resources> build> profile> profiles>

![0](https://note.youdao.com/yws/res/2250/9B4F719F2CEE40F79FF2D7BB00F17671)

说明：这个 resources 里面的路径对应上面文件路径，resources 里面所有的配置加上各自环境的配置，

在引用 jdbc.pro 的地方如下：在 datasource.xml 中，

![0](https://note.youdao.com/yws/res/2248/638258518420475FA2C333BD95318C51)

还有 新增的 evn 那个包下面的所有文件都需要设置为资源文件，这个不必说 直接看图

![0](https://note.youdao.com/yws/res/2247/F6085514F54E486E85B38A8DEF9F6C36)

3，maven 设置要使用的环境：

项目右键 -->maven-->Select Maven profiles ，选择一个环境，修改最好清理一下项目才生效，我之前没清理，发现没起作用。

![0](https://note.youdao.com/yws/res/2245/ADB39540A20C4A59B54DCC678A072EA5)

4、然后运行项目就是你选择的环境了，或者直接导出 war 包，

  其他的多环境配置同。

来源： [https://www.cnblogs.com/xululublog/p/7803287.html](https://www.cnblogs.com/xululublog/p/7803287.html)
