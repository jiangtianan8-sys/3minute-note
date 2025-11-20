本原创文章属于[《Linux大棚》](http://roclinux.cn/)博客。

博客地址为[http://roclinux.cn](http://roclinux.cn/)。

文章作者为roc

希望您能通过捐款的方式支持Linux大棚博客的运行和发展。请见“[关于捐款](http://roclinux.cn/?page_id=2959)”

==

chkconfig在命令行操作时会经常用到。它可以方便地设置各个系统运行级别启动的服务。这个可要好好掌握，用熟练之后，就可以轻轻松松的管理好你的启动服务了。

- 想列出系统所有的服务启动情况：

# chkconfig –list

- 想列出mysqld服务设置情况：

#chkconfig –list mysqld

- 设定mysqld在等级3和5为开机运行服务：

# chkconfig –level 35 mysqld on

–level 35表示操作只在等级3和5执行

on表示启动，off表示关闭

- 设定mysqld在各等级为on：

# chkconfig mysqld on

“各等级”包括2、3、4、5等级

等级0表示：表示关机

等级1表示：单用户模式

等级2表示：无网络连接的多用户命令行模式

等级3表示：有网络连接的多用户命令行模式

等级4表示：不可用

等级5表示：带图形界面的多用户模式

等级6表示：重新启动

- 如何增加一个服务：

首先，服务脚本必须存放在/etc/ini.d/目录下；

其次，需要用chkconfig –add servicename来在chkconfig工具服务列表中增加此服务，此时服务会被在/etc/rc.d/rcN.d中赋予K/S入口了。

最后，你就可以上面教的方法修改服务的默认启动等级了。

- 删除一个服务：

# chkconfig –del servicename