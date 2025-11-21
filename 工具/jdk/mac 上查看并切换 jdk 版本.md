**1. 查看默认 jdk 版本**

![](https://cdn.nlark.com/yuque/0/2020/png/489387/1585578530594-a230fe43-fa70-445e-a089-594aa884b801.png?x-oss-process=image%2Fformat%2Cwebp)

**2. 查看不同 jdk 的安装位置**

```shell
/usr/libexec/java_home -V
```

![](https://cdn.nlark.com/yuque/0/2020/png/489387/1585578545508-e35459eb-75d1-4a29-8cc1-017e81b0b1fa.png?x-oss-process=image%2Fformat%2Cwebp%2Fresize%2Cw_1500%2Climit_0)

**3. 切换默认 jdk 的版本**

将下列内容 (jdk 版本替换为你想要的默认 jdk 版本) 添加至 ~/.bash_profile 中：

```shell
# JDK 1.8
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_151.jdk/Contents/Home
JRE_HOME=$JAVA_HOME/jre
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME
export JRE_HOME
export PATH
export CLASSPATH
```

让配置生效：

```shell
source ~/.bash_profile
```

重新查看 jdk 版本：

```shell
java -version
```

![](https://cdn.nlark.com/yuque/0/2020/png/489387/1585578560666-a9b87250-51ea-4ffa-93e8-5774d463cec6.png?x-oss-process=image%2Fformat%2Cwebp)

若有收获，就点个赞吧
