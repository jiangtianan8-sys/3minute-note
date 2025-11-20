以前一直在 windows 下用 SSH Secure Shell 连接远程服务器，它自带了一个可视化的文件传输工具，跟 ftp 差不多

但是它也存在一个缺陷，不支持编码的选择，遇到 utf8 就自动乱码了，另外 mac 下也没有这个工具

在 mac 下我用终端登录上去之后，想传个文件上去就犯愁了，难不成要开个 ftp？

搜了一下，果然有直接的命令行工具，名字叫 SCP

使用方式如下：

1、上传本地文件到服务器

scp /path/filename username@servername:/path/

例如 scp /var/www/test.php root@192.168.0.101:/var/www/ 把本机/var/www/目录下的 test.php 文件上传到 192.168.0.101 这台服务器上的/var/www/目录中

2、从服务器上下载文件

下载文件我们经常使用 wget，但是如果没有 http 服务，如何从服务器上下载文件呢？

scp username@servername:/path/filename /var/www/local_dir（本地目录）

例如 scp root@192.168.0.101:/var/www/test.txt 把 192.168.0.101 上的/var/www/test.txt 的文件下载到/var/www/local_dir（本地目录）

3、从服务器下载整个目录

scp -r username@servername:/var/www/remote_dir/（远程目录） /var/www/local_dir（本地目录）

例如:scp -r root@192.168.0.101:/var/www/test /var/www/

4、上传目录到服务器

scp -r local_dir username@servername:remote_dir

例如：scp -r test root@192.168.0.101:/var/www/ 把当前目录下的 test 目录上传到服务器的/var/www/ 目录
