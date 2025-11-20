ssh 无密码登录要使用公钥与私钥。linux 下可以用用 ssh-keygen 生成公钥/私钥对，下面我以 CentOS 为例。

本地 master 免密码登录

![316e5586-59ae-4715-8415-b53110d055ab.png](//note.youdao.com/src/38D8FC6ECF2B4F6587A9CF81F5503569)

   $ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys $ chmod 0600 ~/.ssh/authorized_keys

有机器 A(192.168.1.155)，B(192.168.1.181)。现想 A 通过 ssh 免密码登录到 B。

1.在 A 机下生成公钥/私钥对。

[chenlb@A ~]$ ssh-keygen -t rsa -P ''

-P 表示密码，-P '' 就表示空密码，也可以不用 -P 参数，这样就要三车回车，用 -P 就一次回车。

它在/home/chenlb 下生成.ssh 目录，.ssh 下有 id_rsa 和 id_rsa.pub。

2.把 A 机下的 id_rsa.pub 复制到 B 机下，在 B 机的.ssh/authorized_keys 文件里，我用 scp 复制。

[chenlb@A ~]$ scp .ssh/id_rsa.pub chenlb@192.168.1.181:/home/chenlb/id_rsa.pub 

chenlb@192.168.1.181's password:

id_rsa.pub                                    100%  223     0.2KB/s   00:00

由于还没有免密码登录的，所以要输入密码。

3.B 机把从 A 机复制的 id_rsa.pub 添加到.ssh/authorzied_keys （打错了，使用下面的代码块）文件里。

[chenlb@B ~]$ cat id_rsa.pub >> .ssh/authorized_keys

[chenlb@B ~]$ chmod 600 .ssh/authorized_keys

authorized_keys 的权限要是 600。

4.A 机登录 B 机。

[chenlb@A ~]$ ssh 192.168.1.181

The authenticity of host '192.168.1.181 (192.168.1.181)' can't be established.

RSA key fingerprint is 00:a6:a8:87:eb:c7:40:10:39:cc:a0:eb:50:d9:6a:5b.

Are you sure you want to continue connecting (yes/no)? yes

Warning: Permanently added '192.168.1.181' (RSA) to the list of known hosts.

Last login: Thu Jul  3 09:53:18 2008 from chenlb

[chenlb@B ~]$

第一次登录是时要你输入 yes。

现在 A 机可以无密码登录 B 机了。

小结：登录的机子可有私钥，被登录的机子要有登录机子的公钥。这个公钥/私钥对一般在私钥宿主机产生。上面是用 rsa 算法的公钥/私钥对，当然也可以用 dsa(对应的文件是 id_dsa，id_dsa.pub)

想让 A，B 机无密码互登录，那 B 机以上面同样的方式配置即可。

参考：SSH-KeyGen 的用法 [http://blog.163.com/chen98_2006@126/blog/static/158584272007101862513886/](http://blog.163.com/chen98_2006@126/blog/static/158584272007101862513886/)

[来源：](http://blog.163.com/chen98_2006@126/blog/static/158584272007101862513886/) [http://chenlb.iteye.com/blog/211809](http://chenlb.iteye.com/blog/211809)
