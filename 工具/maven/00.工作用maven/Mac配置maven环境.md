1、下载 Maven： [http://maven.apache.org/download.cgi](http://maven.apache.org/download.cgi)

2、把下载到的压缩包解压到相应目录，本机的目录结构是/Users/jiangzhiqiang/local/apache-maven-3.2.53，然后配置一下环境变量。看看~/下是否有.bash_profile 文件，如果没有就创建一个，环境变量要配置在这个文件中。

3.编辑文件

vim /etc/profile

4. 增加环境变量

export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_45.jdk/Contents/Home

export JRE_HOME=$JAVA_HOME/jre

export MAVEN_HOME=/Users/tongcheng/workspace/java/apache-maven-3.3.3

export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib

export PATH=$JAVA_HOME/bin:$MAVEN_HOME/bin:$PATH

export JAVA_HOME PATH CLASSPATH

5.在终端执行强制生效命令

source /etc/profile

6、在新的命令行窗口执行 mvn -v，如果正常显示了 maven 的版本等信息，就是配置成功了。
