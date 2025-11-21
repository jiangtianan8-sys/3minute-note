mvn 参数 -N、-U 理解

1. 关于 -N

-N,--non-recursive Do not recurse into sub-projects

意思是，不递归到子项目 (子模块)。

举例：

一个父项目下 Father 面有 3 个子项目 A、B、C，都生成 jar 包，则有 Father.jar、A.jar、B.jar、C.jar;

这个时候 A 项目依赖了 B、C 项目。

此时如果使用 mvn clean install -N，则只会把 Father.jar 安装到本地仓库 (~/.m2/repository)，

而不会安装其他三个包

造成的问题是，如果你此时使用如下命令拷贝依赖包，则会报错：说找不到依赖包 B.jar/C.jar

mvn dependency:copy-dependencies -DoutputDirectory=$WORKSPACE/dependencies

2. 关于 -U

-U,--update-snapshots Forces a check for missing releases

and updated snapshots on remote repositories

意思是：强制刷新本地仓库不存在 release 版和所有的 snapshots 版本。

- 对于 release 版本，本地已经存在，则不会重复下载
- 对于 snapshots 版本，不管本地是否存在，都会强制刷新，但是刷新并不意味着把 jar 重新下载一遍。

只下载几个比较小的文件，通过这几个小文件确定本地和远程仓库的版本是否一致，再决定是否下载

如图所示：只有 18:32 时间的文件是强制刷新下来的文件

![](assets/mvn%20-N和-U的用法/file-20251121144631601.png)

关于 mvn 各个阶段的工作

1. mvn clean: 清除各个模块 target 目录及里面的内容
2. mvn validate:
3. mvn compile: 静态编译，根据 xx.java 生成 xx.class 文件
4. mvn test: 单元测试
5. mvn package: 打包，生成各个模块下面的 target 目录及里面的内容
6. mvn verify:
7. mvn install： 把打好的包放入本地仓库 (~/.m2/repository)
8. mvn site:
9. mvn deploy: 部署，把包发布到远程仓库
