是否安装过

如果安装过jdk在可以使用的情况下，没有新要求就不要更换了。如果要跟新版本，那就需要先卸载原有的jdk

卸载步骤：

查看linux上面所有的jdk安装包：```rpm -qa | grep jdk (这里会显示所有jdk的安装包)

rpm -e --nodeps 上面显示的包名 会卸载对应的包

检查是否还有jdk java -version

删除残留jdk文件

找文件夹find / -name jdk -d这条命令jdk为变量，你可以改为你想要的找的文件夹名字，它会找到所有有关的文件夹

找文件find / -name jemalloc.sh这条命令jemalloc.sh是变量，它会找到和改名字一样的文件。 如果熟悉确认查找到的文件是没用文件那就删除(慎重操作，这一步可以保留),

准备jdk安装包

JDK官网下载地址：http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

选择版本之前可以查看一下自己的linux服务器是多少位的系统

进入之后如下界面，先勾选小框框内的同意，然后选中长条形框的版本(博主选的是框内的，可以不同)

上传你解压

这里你需要准备一个服务器连接工具，博主用的是SecureCRT8.0(最好用高于7.5的，因为能够一键拖入上传文件)

点击file打开Connect SFTP Session,当窗口出现之后，我们将我们下载好的jdk拖入即可。当上传完成之后，该窗口就可以关闭了。文件会在我们下方的目录里面

解压之前最好将安装包移动到自己定义的目录中去

创建一个名为java的文件夹mkdir /usr/local/java

使用mv命令移动到刚刚创建的文件中

使用tar命令解压tar -xzvf

配置环境变量

打开环境配变量配置如下信息vi /etc/profile

JAVA_HOME=/usr/local/java/jdk1.8.0_241

CLASSPATH=$JAVA_HOME/lib/

PATH=$PATH:$JAVA_HOME/bin

export PATH JAVA_HOME CLASSPATH

1

2

3

4

其中第一句是自己解压的文件目录，编辑好了之后点击shift :然后wq退出

运行命令让配置生效

source /etc/profile

完成安装，检查是否正确

java -version

输入以上命令会出现如下界面。

出现了如上界面就证明JDK8已经安装好啦！

————————————————

版权声明：本文为CSDN博主「xlecho」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。

原文链接：https://blog.csdn.net/xlecho/article/details/97266591