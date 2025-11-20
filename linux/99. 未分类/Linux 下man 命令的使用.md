在刚刚接触到 Linux 的时候，我们通常需要使用 man 来查阅一些命令的帮助信息。一般使用“man 命令名称”的格式就能进行简单的查询。下面关于 man 的是用技巧介绍一下。

一、man 命令

使用权限

所有用户< /pre>

语法格式

man [[ [-c ] [-t ] [Section] ] | [-k | -f ] ] [-F] [-m] [ -MPath ] [ -r ] [ -a ]Title < /pre>

二、主要参数   

1、-c 

显示使用 cat 命令的手册信息。

2、-t

 使用 troff 命令格式化手册信息。如果在超文本信息基中查找到手册页面，则忽略该标志。

3、-k

 显示关键字数据库中包含与作为最终参数给定的字符匹配的标题的字符串的每一行。     可以输入多个标题，中间用空格隔开。     要使用 -k 标志，root 用户必须以前已输入 catman -w 以建立 /usr/share/man/whatis 文件。

4、-f

 显示在关键字数据库中仅与作为最终参数给定的命令名相关的项。可以输入多个命令名，中间用空格隔开。     使用该标志仅搜索命令物件。     要使用 -f 标志，root 用户必须以前已输入 catman -w 以建立 /usr/share/man/whatis 文件。

5、-F 

只显示首个匹配项。  

6、-m 

只在 MANPATH 或 -M 中指定的路径中搜索。  

7、-MPath 

更改 man 命令搜索手册信息的标准位置。路径是用冒号隔开的路径的列表，其中，可以使用以下特殊符号：   %D － 联机帮助页的缺省 AIX? 路径。  %L－与当前语言环境的 LC_MESSAGES 类别相对应的特定于语言环境的目录位置。   %L－与当前 LC_MESSAGES 类别的首 2 个字符相对应的特定于语言环境的目录位置。 

8、-r 

手册信息的远程搜索。如果出于某个原因，远程搜索失败，则 man 将执行本地搜索以获取请求的联机帮助页。  

9、-a

 显示所有匹配项。

三、命令的使用

1、 man 手册章节

man 命令是按照章节存储的，Linux 的 man 手册共有以下几个章节：

|   |   |   |
|---|---|---|
|章节编号|章节名称|章节主要内容|
|1|General Commands|用户在 shell 中可以操作的指令或者可执行文档|
|2|System Calls|系统调用的函数与工具等|
|3|Sunroutines|C 语言库函数|
|4|Special Files|设备或者特殊文件|
|5|File Formats|文件格式与规则|
|6|Games|游戏及其他|
|7|Macros and Conventions|表示宏、包及其他杂项|
|8|Maintenence Commands|表示系统管理员相关的命令|
|9|||

我们输入“man ls”,在屏幕的左上角会显示“”，在这里“LS”表示手册名称，而“（1）”表示该手册位于第一章节。

man 是按照手册的章节号的顺序进行搜索的，比如：

man sleep 只会显示 sleep 在章节 1 中的信息，相当于命令“man 1 sleep”。如果想查看库函数 sleep，就要输入：

man 3 sleep

2、 常用命令形式

1 要显示关于 grep 命令的信息，请输入： man grep

2 要显示包含“mkdir”字符串的 /usr/share/man/whatis 关键字数据库中的所有项，请输入：man -k mkdir

此输出等同于 apropos 命令，即：apropos mkdir

3 要显示 /usr/share/man 或 /usr/share/man/local 路径中的所有与 ftp 命令相关的物件，请输入：man –M/usr/share/man:/usr/share/man/local ftp< /pre>

4 要显示所有匹配项，输入以下命令：man –aTitle< /pre>

5 只要显示首个匹配项，输入以下命令：man –FTitle< /pre>

6 只要在 MANPATH 或 –M 中指定的路径中搜索，输入以下命令： man -m –M PATH Title< /pre>

7 要在用户定义的 PATH 中搜索，输入以下命令： man –MPATH Title< /pre>

3、添加库函数手册

ubuntu 默认是没有安装 c 语言的库函数 man 手册的，所以你在 man perror 和 sendto 之类的函数时会显示没有相关文档的问题，这个问题让我郁闷了我好久。解决方法：

sudo apt-get install manpages-dev

4、让 man 显示中文

ubuntu 源里面已经包含了中文的 man 包，所以不用从其他地方 down 了，直接

sudo apt-get install manpages-zh

但是这样 man 默认显示的还不是中文，还需要以下两步

a.把中文 man 包转换成 utf8 格式的

新建一个脚本文件

gedit t.sh

把下面内容添加进去

#!/bin/bashcd /usr/share/man/zh_CN/for k in *docd $kfor i in *.gzdo j=`echo${i%.gz}` gunzip $i iconv -f gb18030 -t utf8 $j >tmp mv tmp $j gzip $jdonecd..done

然后

sudo ./t

b.修改 man 默认的语言

sudo gedit /etc/manpath.config 把里面的所有的 /usr/share/man 改成 /usr/share/man/zh_CN

保存后退出，然后你再试一下 man ls

5、让没有中文帮助的显示英文

做完上面第二部还不够，这时你再 man 一下一些 c 语言函数（不要用 printf，socket 之类比较有名的函数，这些已经有中文帮助了）的时候就会发现竟然没有帮助，而刚才明明在第一步已经安装了啊。这是因为你上面把/usr/share/man 改成/usr/share/man/zh_CN 的操作使 man 只在中文帮助中搜索，如果没有就直接放弃，因此还需要以下操作，才能让 man 在没有中文帮助的时候自动显示英文的帮助，如果英文的也没有，哪就真的没有了。

sudo gedit /etc/manpath.config

然后搜索你刚才改过的地方，然后在其后面添加同样的一行，只是后面的目录还用原来的/usr/share/man，比如在修改后的

MANPATH_MAP /bin         /usr/share/man/zh_CN

再添加一行

MANPATH_MAP /bin         /usr/share/man

6、新安装了 ubuntu 8.04 版本，发现安装过的系统中缺少很多手册页。

用以下命令搞定了

sudo apt-get install manpages

sudo apt-get install manpages-de

sudo apt-get install manpages-de-dev

sudo apt-get install manpages-dev

7、man 信息在 Linux 系统中的存储

我的这些 man 信息都存在 Linux 系统的哪里？

[root@wupengchong ~]# manpath

/usr/kerberos/man:/usr/local/share/man:/usr/share/man/en:/usr/share/man

用 manpath 命令就可以看到了，当你 man 的时候，man 会到如上这些路径去寻找对应的帮助信息。如果没有的话，那么 man 会抱怨：

[root@wupengchong ~]# man rocrocket

No manual entry for rocrocket

8、如何重新建立 man 的数据库？

使用 makewhatis 命令就可以！

最后，给大家推荐一个 man 的非常好的网站，[http://www.linuxmanpages.com/](http://www.linuxmanpages.com/)，相当于一个网页版的 Linux 的 man 手册。
