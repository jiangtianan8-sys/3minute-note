![](assets/mac%20brew%20安装mysql/file-20251124100250431.png)

==> mysql@5.7

We've installed your MySQL database without a root password. To secure it run:

mysql_secure_installation

MySQL is configured to only allow connections from localhost by default

To connect run:

mysql -uroot

mysql@5.7 is keg-only, which means it was not symlinked into /usr/local,

because this is an alternate version of another formula.

If you need to have mysql@5.7 first in your PATH run:

echo 'export PATH="/usr/local/opt/mysql@5.7/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql@5.7 you may need to set:

export LDFLAGS="-L/usr/local/opt/mysql@5.7/lib"

export CPPFLAGS="-I/usr/local/opt/mysql@5.7/include"

To have launchd start mysql@5.7 now and restart at login:

brew services start mysql@5.7

Or, if you don't want/need a background service you can just run:

/usr/local/opt/mysql@5.7/bin/mysql.server start

mysql 的配置文件 my.cnf

sudo vi /usr/local/etc/my.cnf
