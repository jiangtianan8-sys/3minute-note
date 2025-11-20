Linux du 命令也是查看使用空间的，但是与 df 命令不同的是 Linux du 命令是对文件和目录磁盘使用的空间的查看，还是和 df 命令有一些区别的.

1．命令格式：

du [选项][文件]

2．命令功能：

显示每个文件和目录的磁盘使用空间。

3．命令参数：

-a 或 -all  显示目录中个别文件的大小。   

-b 或 -bytes  显示目录或文件大小时，以 byte 为单位。   

-c 或 --total  除了显示个别目录或文件的大小外，同时也显示所有目录或文件的总和。 

-k 或 --kilobytes  以 KB(1024bytes) 为单位输出。

-m 或 --megabytes  以 MB 为单位输出。   

-s 或 --summarize  仅显示总计，只列出最后加总的值。

-h 或 --human-readable  以 K，M，G 为单位，提高信息的可读性。

-x 或 --one-file-xystem  以一开始处理时的文件系统为准，若遇上其它不同的文件系统目录则略过。 

-L<符号链接>或 --dereference<符号链接> 显示选项中所指定符号链接的源文件大小。   

-S 或 --separate-dirs   显示个别目录的大小时，并不含其子目录的大小。 

-X<文件>或 --exclude-from=<文件>  在<文件>指定目录或文件。   

--exclude=<目录或文件>         略过指定的目录或文件。    

-D 或 --dereference-args   显示指定符号链接的源文件大小。   

-H 或 --si  与 -h 参数相同，但是 K，M，G 是以 1000 为换算单位。   

-l 或 --count-links   重复计算硬件链接的文件。  

4．使用实例：

实例 1：显示目录或者文件所占空间 

命令：

du

输出：

[root@localhost test]# du

608     ./test6

308     ./test4

4       ./scf/lib

4       ./scf/service/deploy/product

4       ./scf/service/deploy/info

12      ./scf/service/deploy

16      ./scf/service

4       ./scf/doc

4       ./scf/bin

32      ./scf

8       ./test3

1288    .

[root@localhost test]#

说明：

只显示当前目录下面的子目录的目录大小和当前目录的总的大小，最下面的 1288 为当前目录的总大小

实例 2：显示指定文件所占空间

命令：

du log2012.log

输出：

[root@localhost test]# du log2012.log 

300     log2012.log

[root@localhost test]#

说明：

实例 3：查看指定目录的所占空间

命令：

du scf

输出：

[root@localhost test]# du scf

4       scf/lib

4       scf/service/deploy/product

4       scf/service/deploy/info

12      scf/service/deploy

16      scf/service

4       scf/doc

4       scf/bin

32      scf

[root@localhost test]#

说明：

实例 4：显示多个文件所占空间

命令：

du log30.tar.gz log31.tar.gz

输出：

[root@localhost test]# du log30.tar.gz log31.tar.gz 

4       log30.tar.gz

4       log31.tar.gz

[root@localhost test]#

说明：

实例 5：只显示总和的大小

命令：

du -s

输出：

[root@localhost test]# du -s

1288    .

[root@localhost test]# du -s scf

32      scf

[root@localhost test]# cd ..

[root@localhost soft]# du -s test

1288    test

[root@localhost soft]#

说明：

实例 6：方便阅读的格式显示

命令：

du -h test

输出：

[root@localhost soft]# du -h test

608K    test/test6

308K    test/test4

4.0K    test/scf/lib

4.0K    test/scf/service/deploy/product

4.0K    test/scf/service/deploy/info

12K     test/scf/service/deploy

16K     test/scf/service

4.0K    test/scf/doc

4.0K    test/scf/bin

32K     test/scf

8.0K    test/test3

1.3M    test

[root@localhost soft]#

说明：

实例 7：文件和目录都显示

命令：

输出：

[root@localhost soft]# du -ah test

4.0K    test/log31.tar.gz

4.0K    test/test13.tar.gz

0       test/linklog.log

0       test/test6/log2014.log

300K    test/test6/linklog.log

0       test/test6/log2015.log

4.0K    test/test6/log2013.log

300K    test/test6/log2012.log

0       test/test6/log2017.log

0       test/test6/log2016.log

608K    test/test6

0       test/log2015.log

0       test/test4/log2014.log

4.0K    test/test4/log2013.log

300K    test/test4/log2012.log

308K    test/test4

4.0K    test/scf/lib

4.0K    test/scf/service/deploy/product

4.0K    test/scf/service/deploy/info

12K     test/scf/service/deploy

16K     test/scf/service

4.0K    test/scf/doc

4.0K    test/scf/bin

32K     test/scf

4.0K    test/log2013.log

300K    test/log2012.log

0       test/log2017.log

0       test/log2016.log

4.0K    test/log30.tar.gz

4.0K    test/log.tar.bz2

4.0K    test/log.tar.gz

0       test/test3/log2014.log

4.0K    test/test3/log2013.log

8.0K    test/test3

4.0K    test/scf.tar.gz

1.3M    test

[root@localhost soft]#

说明：

实例 8：显示几个文件或目录各自占用磁盘空间的大小，还统计它们的总和

命令：

du -c log30.tar.gz log31.tar.gz

输出：

[root@localhost test]# du -c log30.tar.gz log31.tar.gz 

4       log30.tar.gz

4       log31.tar.gz

8       总计

[root@localhost test]#

说明：

加上 -c 选项后，du 不仅显示两个目录各自占用磁盘空间的大小，还在最后一行统计它们的总和。

实例 9：按照空间大小排序

命令：

du|sort -nr|more

输出：

[root@localhost test]# du|sort -nr|more

1288    .

608     ./test6

308     ./test4

32      ./scf

16      ./scf/service

12      ./scf/service/deploy

8       ./test3

4       ./scf/service/deploy/product

4       ./scf/service/deploy/info

4       ./scf/lib

4       ./scf/doc

4       ./scf/bin

[root@localhost test]#

说明：

实例 10：输出当前目录下各个子目录所使用的空间

命令：

du -h  --max-depth=1

输出：

[root@localhost test]# du -h  --max-depth=1

608K    ./test6

308K    ./test4

32K     ./scf

8.0K    ./test3

1.3M    .

[root@localhost test]#

说明：

实例 11：

命令：

   du -sh *

![](assets/每天一个linux命令(34)-du%20命令/file-20251120104025843.png)
