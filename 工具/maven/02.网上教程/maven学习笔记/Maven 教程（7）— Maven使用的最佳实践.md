1、设置MAVEN_OPTS环境变量

通常需要设置MAVEN_OPTS的值为-Xms128m -Xmx512m，因为Java默认的最大可用内存往往不能够满足Maven运行的需要，比如在项目较大时，使用Maven生成项目站点需要占用大量的内存，如果没有该配置，则很容易得到java.lang.OutOfMemeoryError异常。因此，一开始就配置该环境变量是推荐的做法。

2、配置用户范围settings.xml

Maven用户可以选择配置Maven安装目录conf下的settings.xml或者系统用户目录.m2下的settings.xml。前者是全局范围的，整台机器上的所有用户都会直接受到该配置的影响，而后者是用户范围的，只有当前用户才会受到该配置的影响。

推荐使用用户范围的settings.xml，主要是为了避免无意识地影响到系统中的其他用户。如果有切实的需求，需要统一系统中所有用户的settings.xml配置，当然应该使用全局范围的settings.xml。

除了影响范围这一因素，配置用户范围settings.xml文件还便于Maven升级。直接修改conf目录下的settings.xml会导致Maven升级的不便，每次升级到新版本的Maven，都需要复制settings.xml文件。如果使用.m2目录下的settings.xml，就不会影响到Maven安装文件，升级时就不需要触动settings.xml文件。

一般情况下.m2目录下是没有settings.xml配置文件的，需要我们复制conf下面的settings.xml至.m2目录下，然后再进行修改。

3、不要使用IDE内嵌的Maven

Eclipse在集成Maven时，都会安装上一个内嵌的Maven，这个内嵌的Maven通常会比较新，但不一定很稳定，而且往往也和在命令行使用的Maven不是同一个版本。这里会有两个潜在的问题：

- 首先，较新版本的Maven存在很多不稳定因素，容易造成一些难以理解的问题；
- 其次，除了IDE，也经常还会使用命令行的Maven，如果版本不一致，容易造成构建行为的不一致，这是我们所不希望看到的。

因此，应该在IDE中配置Maven插件时使用与命令行一致的Maven。

在Eclipse环境中，点击菜单栏中的Window，然后选择Preferences，在弹出的对话框中展开左边的Maven项，选择Installations子项，在右边的面板中，能够看到有一个默认的EMBEDDED Maven安装被选中了。单击Add…按钮，然后选择Maven安装目录，添加完毕之后选择我们自己安装的Maven，点击OK按钮，如图： 

![0](https://note.youdao.com/yws/res/2297/042E2C2A8B1B4F33B763C621C8CE1A32)

其他类似的IDE或许在集成的时候也内嵌了Maven，同理，我们最好将它改为我们自己安装的Maven。

4、在Eclipse中指定使用的settings.xml配置文件

在Eclipse环境中，点击菜单栏中的Window，然后选择Preferences，在弹出的对话框中展开左边的Maven项，选择User Settings子项，在右边的面板中，单击Browse…按钮，然后选择对应的settings.xml文件，设置完毕之后点击OK按钮，如图： 

![0](https://note.youdao.com/yws/res/2296/0ED867C255FE4BC693A5D67A58778660)