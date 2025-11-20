本原创文章属于 [《Linux大棚》](http://roclinux.cn/) 博客。

博客地址为 [http://roclinux.cn](http://roclinux.cn/)。

文章作者为 roc

希望您能通过捐款的方式支持 Linux 大棚博客的运行和发展。请见“[关于捐款](http://roclinux.cn/?page_id=2959)”

==

service 命令，顾名思义，就是用于管理 Linux 操作系统中服务的命令。

1. 声明：这个命令不是在所有的 linux 发行版本中都有。主要是在 redhat、fedora、mandriva 和 centos 中。
2. 此命令位于/sbin 目录下，用 file 命令查看此命令会发现它是一个脚本命令。
3. 分析脚本可知此命令的作用是去/etc/init.d 目录下寻找相应的服务，进行开启和关闭等操作。
4. 开启 httpd 服务器：service httpd start

start 可以换成 restart 表示重新启动，stop 表示关闭，reload 表示重新载入配置。

5. 关闭 mysql 服务器：service mysqld stop
6. 强烈建议大家将 service 命令替换为/etc/init.d/mysqld stop

over~
