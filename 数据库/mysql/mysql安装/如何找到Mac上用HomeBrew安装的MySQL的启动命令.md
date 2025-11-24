1. 找 HomeBrew 安装的包列表， 找到 MySQL 的 formula

```shell
1. $ brew list
2. apache-spark heroku-node mysql@5.7 openssl@1.1 sbt
3. autoconf icu4c ncurses pkg-config scala@2.12
4. gdb libevent node pyenv tmux
5. heroku maven openjdk readline yarn
```

2. 查看 MySQL 的 info

```shell
1. $ brew info mysql@5.7
2. mysql@5.7: stable 5.7.31 (bottled) [keg-only]
3. Open source relational database management system
4. https://dev.mysql.com/doc/refman/5.7/en/
5. /usr/local/Cellar/mysql@5.7/5.7.31 (319 files, 232.4MB)
6. Poured from bottle on 2020-09-17 at 22:12:10
7. From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/mysql@5.7.rb
8. License: GPL-2.0
9. ==> Dependencies
10. Build: cmake ✘
11. Required: openssl@1.1 ✔
12. ==> Caveats
13. We've installed your MySQL database without a root password. To secure it run:
14. mysql_secure_installation

15. MySQL is configured to only allow connections from localhost by default

16. To connect run:
17. mysql -uroot

18. mysql@5.7 is keg-only, which means it was not symlinked into /usr/local,
19. because this is an alternate version of another formula.

20. If you need to have mysql@5.7 first in your PATH run:
21. echo 'export PATH="/usr/local/opt/mysql@5.7/bin:$PATH"' >> /Users/XXXXXXXXXXXXXXX/.bash_profile

22. For compilers to find mysql@5.7 you may need to set:
23. export LDFLAGS="-L/usr/local/opt/mysql@5.7/lib"
24. export CPPFLAGS="-I/usr/local/opt/mysql@5.7/include"

25. For pkg-config to find mysql@5.7 you may need to set:
26. export PKG_CONFIG_PATH="/usr/local/opt/mysql@5.7/lib/pkgconfig"

27. To have launchd start mysql@5.7 now and restart at login: # 看这里就是启动命令
28. brew services start mysql@5.7
29. Or, if you don't want/need a background service you can just run: # 这个也可以
30. /usr/local/opt/mysql@5.7/bin/mysql.server start
31. ==> Analytics
32. install: 23,712 (30 days), 72,627 (90 days), 285,643 (365 days)
33. install-on-request: 23,118 (30 days), 70,677 (90 days), 277,917 (365 days)
34. build-error: 0 (30 days)
```

37. 按照提示启动就成功了

```shell
1. $ /usr/local/opt/mysql@5.7/bin/mysql.server start
2. Starting MySQL
```
