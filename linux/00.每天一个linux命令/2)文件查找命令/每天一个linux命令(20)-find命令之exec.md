find 是我们很常用的一个 Linux 命令，但是我们一般查找出来的并不仅仅是看看而已，还会有进一步的操作，这个时候 exec 的作用就显现出来了。 

exec 解释：

-exec  参数后面跟的是 command 命令，它的终止是以; 为结束标志的，所以这句命令后面的分号是不可缺少的，考虑到各个系统中分号会有不同的意义，所以前面加反斜杠。

{}   花括号代表前面 find 查找出来的文件名。

使用 find 时，只要把想要的操作写在一个文件里，就可以用 exec 来配合 find 查找，很方便的。在有些操作系统中只允许 -exec 选项执行诸如 l s 或 ls -l 这样的命令。大多数用户使用这一选项是为了查找旧文件并删除它们。建议在真正执行 rm 命令删除文件之前，最好先用 ls 命令看一下，确认它们是所要删除的文件。 exec 选项后面跟随着所要执行的命令或脚本，然后是一对儿{ }，一个空格和一个\，最后是一个分号。为了使用 exec 选项，必须要同时使用 print 选项。如果验证一下 find 命令，会发现该命令只输出从当前路径起的相对路径及文件名。

实例 1：ls -l 命令放在 find 命令的 -exec 选项中 

命令：

find . -type f -exec ls -l {} \;

输出： 

[root@localhost test]# find . -type f -exec ls -l {} \; 

-rw-r--r-- 1 root root 127 10-28 16:51 ./log2014.log

-rw-r--r-- 1 root root 0 10-28 14:47 ./test4/log3-2.log

-rw-r--r-- 1 root root 0 10-28 14:47 ./test4/log3-3.log

-rw-r--r-- 1 root root 0 10-28 14:47 ./test4/log3-1.log

-rw-r--r-- 1 root root 33 10-28 16:54 ./log2013.log

-rw-r--r-- 1 root root 302108 11-03 06:19 ./log2012.log

-rw-r--r-- 1 root root 25 10-28 17:02 ./log.log

-rw-r--r-- 1 root root 37 10-28 17:07 ./log.txt

-rw-r--r-- 1 root root 0 10-28 14:47 ./test3/log3-2.log

-rw-r--r-- 1 root root 0 10-28 14:47 ./test3/log3-3.log

-rw-r--r-- 1 root root 0 10-28 14:47 ./test3/log3-1.log

[root@localhost test]#

说明： 

上面的例子中，find 命令匹配到了当前目录下的所有普通文件，并在 -exec 选项中使用 ls -l 命令将它们列出。

实例 2：在目录中查找更改时间在 n 日以前的文件并删除它们

命令：

find . -type f -mtime +14 -exec rm {} \; 

输出：

[root@localhost test]# ll

总计 328

-rw-r--r-- 1 root root 302108 11-03 06:19 log2012.log

-rw-r--r-- 1 root root     33 10-28 16:54 log2013.log

-rw-r--r-- 1 root root    127 10-28 16:51 log2014.log

lrwxrwxrwx 1 root root      7 10-28 15:18 log_link.log -> log.log

-rw-r--r-- 1 root root     25 10-28 17:02 log.log

-rw-r--r-- 1 root root     37 10-28 17:07 log.txt

drwxr-xr-x 6 root root   4096 10-27 01:58 scf

drwxrwxrwx 2 root root   4096 10-28 14:47 test3

drwxrwxrwx 2 root root   4096 10-28 14:47 test4

[root@localhost test]# find . -type f -mtime +14 -exec rm {} \;

[root@localhost test]# ll

总计 312

-rw-r--r-- 1 root root 302108 11-03 06:19 log2012.log

lrwxrwxrwx 1 root root      7 10-28 15:18 log_link.log -> log.log

drwxr-xr-x 6 root root   4096 10-27 01:58 scf

drwxrwxrwx 2 root root   4096 11-12 19:32 test3

drwxrwxrwx 2 root root   4096 11-12 19:32 test4

[root@localhost test]# 

说明：

在 shell 中用任何方式删除文件之前，应当先查看相应的文件，一定要小心！当使用诸如 mv 或 rm 命令时，可以使用 -exec 选项的安全模式。它将在对每个匹配到的文件进行操作之前提示你。 

实例 3：在目录中查找更改时间在 n 日以前的文件并删除它们，在删除之前先给出提示

命令：

find . -name "*.log" -mtime +5 -ok rm {} \;

输出：

[root@localhost test]# ll

总计 312

-rw-r--r-- 1 root root 302108 11-03 06:19 log2012.log

lrwxrwxrwx 1 root root      7 10-28 15:18 log_link.log -> log.log

drwxr-xr-x 6 root root   4096 10-27 01:58 scf

drwxrwxrwx 2 root root   4096 11-12 19:32 test3

drwxrwxrwx 2 root root   4096 11-12 19:32 test4

[root@localhost test]# find . -name "*.log" -mtime +5 -ok rm {} \;

< rm … ./log_link.log > ? y

< rm … ./log2012.log > ? n

[root@localhost test]# ll

总计 312

-rw-r--r-- 1 root root 302108 11-03 06:19 log2012.log

drwxr-xr-x 6 root root   4096 10-27 01:58 scf

drwxrwxrwx 2 root root   4096 11-12 19:32 test3

drwxrwxrwx 2 root root   4096 11-12 19:32 test4

[root@localhost test]#

说明：

在上面的例子中， find 命令在当前目录中查找所有文件名以.log 结尾、更改时间在 5 日以上的文件，并删除它们，只不过在删除之前先给出提示。 按 y 键删除文件，按 n 键不删除。 

实例 4：-exec 中使用 grep 命令

命令：

find /etc -name "passwd*" -exec grep "root" {} \;

输出：

[root@localhost test]# find /etc -name "passwd*" -exec grep "root" {} \;

root:x:0:0:root:/root:/bin/bash

root:x:0:0:root:/root:/bin/bash

[root@localhost test]#

说明：

任何形式的命令都可以在 -exec 选项中使用。  在上面的例子中我们使用 grep 命令。find 命令首先匹配所有文件名为“ passwd*”的文件，例如 passwd、passwd.old、passwd.bak，然后执行 grep 命令看看在这些文件中是否存在一个 root 用户。

实例 5：查找文件移动到指定目录  

命令：

find . -name "*.log" -exec mv {} .. \;

输出：

[root@localhost test]# ll

总计 12drwxr-xr-x 6 root root 4096 10-27 01:58 scf

drwxrwxr-x 2 root root 4096 11-12 22:49 test3

drwxrwxr-x 2 root root 4096 11-12 19:32 test4

[root@localhost test]# cd test3/

[root@localhost test3]# ll

总计 304

-rw-r--r-- 1 root root 302108 11-03 06:19 log2012.log

-rw-r--r-- 1 root root     61 11-12 22:44 log2013.log

-rw-r--r-- 1 root root      0 11-12 22:25 log2014.log

[root@localhost test3]# find . -name "*.log" -exec mv {} .. \;

[root@localhost test3]# ll

总计 0[root@localhost test3]# cd ..

[root@localhost test]# ll

总计 316

-rw-r--r-- 1 root root 302108 11-03 06:19 log2012.log

-rw-r--r-- 1 root root     61 11-12 22:44 log2013.log

-rw-r--r-- 1 root root      0 11-12 22:25 log2014.log

drwxr-xr-x 6 root root   4096 10-27 01:58 scf

drwxrwxr-x 2 root root   4096 11-12 22:50 test3

drwxrwxr-x 2 root root   4096 11-12 19:32 test4

[root@localhost test]#

实例 6：用 exec 选项执行 cp 命令  

命令：

find . -name "*.log" -exec cp {} test3 \;

输出：

[root@localhost test3]# ll

总计 0[root@localhost test3]# cd ..

[root@localhost test]# ll

总计 316

-rw-r--r-- 1 root root 302108 11-03 06:19 log2012.log

-rw-r--r-- 1 root root     61 11-12 22:44 log2013.log

-rw-r--r-- 1 root root      0 11-12 22:25 log2014.log

drwxr-xr-x 6 root root   4096 10-27 01:58 scf

drwxrwxr-x 2 root root   4096 11-12 22:50 test3

drwxrwxr-x 2 root root   4096 11-12 19:32 test4

[root@localhost test]# find . -name "*.log" -exec cp {} test3 \;

cp: “./test3/log2014.log” 及 “test3/log2014.log” 为同一文件

cp: “./test3/log2013.log” 及 “test3/log2013.log” 为同一文件

cp: “./test3/log2012.log” 及 “test3/log2012.log” 为同一文件

[root@localhost test]# cd test3

[root@localhost test3]# ll

总计 304

-rw-r--r-- 1 root root 302108 11-12 22:54 log2012.log

-rw-r--r-- 1 root root     61 11-12 22:54 log2013.log

-rw-r--r-- 1 root root      0 11-12 22:54 log2014.log

[root@localhost test3]#
