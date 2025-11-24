前段时间安装 mysql5.7 后，第一次登陆发现空密码怎么都登陆不成功，后来网上查了一下发现，从 5.7 开始会自动生成一个随机密码了。

1. 查看初始密码

grep 'temporary password' /var/log/mysqld.log 2016-07-08T02:25:46.311098Z 1 [Note] A temporary password is generated for root@localhost: MtPqF0/oN5zo 其中“MtPqF0/oN5zo”就为我们要找的初始密码

另外一种方法查看默认密码：

cat /root/.mysql_secret The random password set for the root userat Fri Jan 10 20:00:34 2014 (local time): aJqZsA2m “aJqZsA2m”就是我们要找的初始密码

ps：这上面两种方法都是在网上找的，第一个方法我是在 log 中没有找到对应的密码记录，第二方法找到的密码也登陆不进去，不知道哪里操作错误了，最后还是使用的下面的 mysql 找回密码大招登陆进去的

1. mysql 密码找回

- 方法一:

vi /etc/my.cnf

在 [mysqld] 下加上 skip-grant-tables，如：

[mysqld] datadir=/var/lib/mysql socket=/var/lib/mysql/mysql.sock skip-grant-tables

重启 mysql

service mysqld restart

登陆 mysql 后就可以修改密码了

mysql -u root update mysql.user set authentication_string=PASSWORD('123456') where User='root'; flush privileges;

然后改回 my.cnf 重启 mysql。

- 方法 2：

先暂停 mysql

以不检查权限的方式启动

bin/mysqld_safe --skip-grant-tables &

登陆 mysql 后就可以修改密码了

mysql -u root update mysql.user set authentication_string=PASSWORD('123456') where User='root'; flush privileges;

然后重启 mysql 就 ok 了

service mysqld restart

登录后任何操作都会有这个提示：

ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1

还需要刷新一次密码才行

set password for root@localhost = password('123456'); flush privileges;

作者：超凡陆战队

链接：https://www.jianshu.com/p/0a40cbaa79a0

來源：简书

简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
