减少文件大小有两个明显的好处，一是可以减少存储空间，二是通过网络传输文件时，可以减少传输的时间。gzip 是在 Linux 系统中经常使用的一个对文件进行压缩和解压缩的命令，既方便又好用。gzip 不仅可以用来压缩大的、较少使用的文件以节省磁盘空间，还可以和 tar 命令一起构成 Linux 操作系统中比较流行的压缩文件格式。据统计，gzip 命令对文本文件有 60%～70% 的压缩率。

1．命令格式：

gzip[参数][文件或者目录]

2．命令功能：

gzip 是个使用广泛的压缩程序，文件经它压缩过后，其名称后面会多出 ".gz" 的扩展名。

3．命令参数：

-a 或 --ascii 　使用 ASCII 文字模式。 

-c 或 --stdout 或 --to-stdout 　把压缩后的文件输出到标准输出设备，不去更动原始文件。 

-d 或 --decompress 或 ----uncompress 　解开压缩文件。 

-f 或 --force 　强行压缩文件。不理会文件名称或硬连接是否存在以及该文件是否为符号连接。 

-h 或 --help 　在线帮助。 

-l 或 --list 　列出压缩文件的相关信息。 

-L 或 --license 　显示版本与版权信息。 

-n 或 --no-name 　压缩文件时，不保存原来的文件名称及时间戳记。 

-N 或 --name 　压缩文件时，保存原来的文件名称及时间戳记。 

-q 或 --quiet 　不显示警告信息。 

-r 或 --recursive 　递归处理，将指定目录下的所有文件及子目录一并处理。 

-S<压缩字尾字符串>或 ----suffix<压缩字尾字符串> 　更改压缩字尾字符串。 

-t 或 --test 　测试压缩文件是否正确无误。 

-v 或 --verbose 　显示指令执行过程。 

-V 或 --version 　显示版本信息。 

-num 用指定的数字 num 调整压缩的速度，-1 或 --fast 表示最快压缩方法（低压缩比），-9 或 --best 表示最慢压缩方法（高压缩比）。系统缺省值为 6。 

4．使用实例：

实例 1：把 test6 目录下的每个文件压缩成.gz 文件

命令：

gzip *

输出：

[root@localhost test6]# ll

总计 604

---xr--r-- 1 root mail  302108 11-30 08:39 linklog.log

---xr--r-- 1 mail users 302108 11-30 08:39 log2012.log

-rw-r--r-- 1 mail users     61 11-30 08:39 log2013.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2014.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2015.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2016.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2017.log

[root@localhost test6]# gzip *

[root@localhost test6]# ll

总计 28

---xr--r-- 1 root mail  1341 11-30 08:39 linklog.log.gz

---xr--r-- 1 mail users 1341 11-30 08:39 log2012.log.gz

-rw-r--r-- 1 mail users   70 11-30 08:39 log2013.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2014.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2015.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2016.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2017.log.gz

[root@localhost test6]#

说明：

实例 2：把例 1 中每个压缩的文件解压，并列出详细的信息

命令：

gzip -dv *

输出：

[root@localhost test6]# ll

总计 28

---xr--r-- 1 root mail  1341 11-30 08:39 linklog.log.gz

---xr--r-- 1 mail users 1341 11-30 08:39 log2012.log.gz

-rw-r--r-- 1 mail users   70 11-30 08:39 log2013.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2014.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2015.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2016.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2017.log.gz

[root@localhost test6]# gzip -dv *

linklog.log.gz:  99.6% -- replaced with linklog.log

log2012.log.gz:  99.6% -- replaced with log2012.log

log2013.log.gz:  47.5% -- replaced with log2013.log

log2014.log.gz:   0.0% -- replaced with log2014.log

log2015.log.gz:   0.0% -- replaced with log2015.log

log2016.log.gz:   0.0% -- replaced with log2016.log

log2017.log.gz:   0.0% -- replaced with log2017.log

[root@localhost test6]# ll

总计 604

---xr--r-- 1 root mail  302108 11-30 08:39 linklog.log

---xr--r-- 1 mail users 302108 11-30 08:39 log2012.log

-rw-r--r-- 1 mail users     61 11-30 08:39 log2013.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2014.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2015.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2016.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2017.log

[root@localhost test6]#

说明：

实例 3：详细显示例 1 中每个压缩的文件的信息，并不解压

命令：

gzip -l *

输出：

[root@localhost test6]# gzip -l *

         compressed        uncompressed  ratio uncompressed_name

               1341              302108  99.6% linklog.log

               1341              302108  99.6% log2012.log

                 70                  61  47.5% log2013.log

                 32                   0   0.0% log2014.log

                 32                   0   0.0% log2015.log

                 32                   0   0.0% log2016.log

                 32                   0   0.0% log2017.log

               2880              604277  99.5% (totals)

说明：

实例 4：压缩一个 tar 备份文件，此时压缩文件的扩展名为.tar.gz

命令：

gzip -r log.tar

输出：

[root@localhost test]# ls -al log.tar

-rw-r--r-- 1 root root 307200 11-29 17:54 log.tar

[root@localhost test]# gzip -r log.tar

[root@localhost test]# ls -al log.tar.gz 

-rw-r--r-- 1 root root 1421 11-29 17:54 log.tar.gz

说明：

实例 5：递归的压缩目录

命令：

gzip -rv test6

输出：

[root@localhost test6]# ll

总计 604

---xr--r-- 1 root mail  302108 11-30 08:39 linklog.log

---xr--r-- 1 mail users 302108 11-30 08:39 log2012.log

-rw-r--r-- 1 mail users     61 11-30 08:39 log2013.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2014.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2015.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2016.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2017.log

[root@localhost test6]# cd ..

[root@localhost test]# gzip -rv test6

test6/log2014.log:        0.0% -- replaced with test6/log2014.log.gz

test6/linklog.log:       99.6% -- replaced with test6/linklog.log.gz

test6/log2015.log:        0.0% -- replaced with test6/log2015.log.gz

test6/log2013.log:       47.5% -- replaced with test6/log2013.log.gz

test6/log2012.log:       99.6% -- replaced with test6/log2012.log.gz

test6/log2017.log:        0.0% -- replaced with test6/log2017.log.gz

test6/log2016.log:        0.0% -- replaced with test6/log2016.log.gz

[root@localhost test]# cd test6

[root@localhost test6]# ll

总计 28

---xr--r-- 1 root mail  1341 11-30 08:39 linklog.log.gz

---xr--r-- 1 mail users 1341 11-30 08:39 log2012.log.gz

-rw-r--r-- 1 mail users   70 11-30 08:39 log2013.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2014.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2015.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2016.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2017.log.gz

说明：

这样，所有 test 下面的文件都变成了 *.gz，目录依然存在只是目录里面的文件相应变成了 *.gz.这就是压缩，和打包不同。因为是对目录操作，所以需要加上 -r 选项，这样也可以对子目录进行递归了。 

实例 6：递归地解压目录

命令：

gzip -dr test6

输出：

[root@localhost test6]# ll

总计 28

---xr--r-- 1 root mail  1341 11-30 08:39 linklog.log.gz

---xr--r-- 1 mail users 1341 11-30 08:39 log2012.log.gz

-rw-r--r-- 1 mail users   70 11-30 08:39 log2013.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2014.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2015.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2016.log.gz

-rw-r--r-- 1 root mail    32 11-30 08:39 log2017.log.gz

[root@localhost test6]# cd ..

[root@localhost test]# gzip -dr test6

[root@localhost test]# cd test6

[root@localhost test6]# ll

总计 604

---xr--r-- 1 root mail  302108 11-30 08:39 linklog.log

---xr--r-- 1 mail users 302108 11-30 08:39 log2012.log

-rw-r--r-- 1 mail users     61 11-30 08:39 log2013.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2014.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2015.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2016.log

-rw-r--r-- 1 root mail       0 11-30 08:39 log2017.log

[root@localhost test6]#

说明：
