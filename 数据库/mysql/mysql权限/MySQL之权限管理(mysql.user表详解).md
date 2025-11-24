[mysql.user表中Host为%的含义](http://www.cnblogs.com/wanghetao/p/3804653.html)

　　Host列指定了允许用户登录所使用的IP，比如user=root Host=192.168.1.1。这里的意思就是说root用户只能通过192.168.1.1的客户端去访问。 　　而%是个通配符，如果Host=192.168.1.%，那么就表示只要是IP地址前缀为“192.168.1.”的客户端都可以连接。如果Host=%，表示所有IP都有连接权限。、 　　这也就是为什么在开启远程连接的时候，大部分人都直接把Host改成%的缘故，为了省事。

1：新增用户：

注：[MySQL数据库](http://lib.csdn.net/base/mysql)下user表中，Host和User为两个主键列（primary key），已经各版本下非空未设置默认字段。

登录后，切换db：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> use mysql;  
2. Reading table information for completion of table and column names  
3. You can turn off this feature to get a quicker startup with -A  

4. Database changed  

新增用户：

注：限制kaka用户的登陆ip为10.155.123.55，ip为随手写入，如果正确配置为您有效登陆ip，所有ip登陆，则设置Host为 '%'

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> INSERT INTO mysql.user(Host,User,Password) VALUES("10.155.123.55","kaka",PASSWORD("kaka123"));  

在版本 5.6.27:

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> INSERT INTO mysql.user(Host,User,Password,ssl_cipher,x509_issuer,x509_subject) VALUES("10.155.123.55","kaka",PASSWORD("kaka123"),"","","");  
2. Query OK, 1 row affected (0.03 sec)  

新增用户（全sql）：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. INSERT  INTO `user`(`Host`,`User`,`Password`,`Select_priv`,`Insert_priv`,`Update_priv`,`Delete_priv`,`Create_priv`,`Drop_priv`,`Reload_priv`,`Shutdown_priv`,`Process_priv`,`File_priv`,`Grant_priv`,`References_priv`,`Index_priv`,`Alter_priv`,`Show_db_priv`,`Super_priv`,`Create_tmp_table_priv`,`Lock_tables_priv`,`Execute_priv`,`Repl_slave_priv`,`Repl_client_priv`,`Create_view_priv`,`Show_view_priv`,`Create_routine_priv`,`Alter_routine_priv`,`Create_user_priv`,`Event_priv`,`Trigger_priv`,`Create_tablespace_priv`,`ssl_type`,`ssl_cipher`,`x509_issuer`,`x509_subject`,`max_questions`,`max_updates`,`max_connections`,`max_user_connections`,`plugin`,`authentication_string`,`password_expired`) VALUES ('%','root','*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','','','','',0,0,0,0,'mysql_native_password','','N');  

新增用户完成，刷新[mysql](http://lib.csdn.net/base/mysql)的系统权限相关表

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> flush privileges;  
2. Query OK, 0 rows affected (0.00 sec)  

设置遇到问题，请查看：[MySQL配置和设置问题小结](http://blog.csdn.net/typa01_kk/article/details/49107407)

重启生效：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. [root@Tony_ts_tian bin]# service mysqld restart  
2. Shutting down MySQL.... SUCCESS!   
3. Starting MySQL. SUCCESS!   

查询用户，Host,User,Password：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql>  SELECT Host,User,Password FROM mysql.user;    
2. +----------------+------+-------------------------------------------+  
3. | Host           | User | Password                                  |  
4. +----------------+------+-------------------------------------------+  
5. | localhost      | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
6. | tony\_ts\_tian | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
7. | 127.0.0.1      | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
8. | ::1            | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
9. | 10.155.123.55  | kaka | *90B3D884FB6092549F244125549B77C000A0F9C6 |  
10. | %              | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
11. +----------------+------+-------------------------------------------+  
12. 6 rows in set (0.00 sec)  

2：修改信息，密码，类似可修改其他字段。

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> UPDATE `user` SET Password=PASSWORD("123456") WHERE Host='10.155.123.55' AND User='kaka';  
2. Query OK, 1 row affected (0.02 sec)  
3. Rows matched: 1  Changed: 1  Warnings: 0  
4. mysql> flush privileges;  
5. Query OK, 0 rows affected (0.00 sec)  
6. mysql> SELECT Host,User,Password FROM `user`;  
7. 前:  
8. | 10.155.123.55  | kaka | *90B3D884FB6092549F244125549B77C000A0F9C6 |  
9. 后：  
10. | 10.155.123.55  | kaka | *6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9 |  

3：删除用户：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> DELETE FROM `user` WHERE Host='10.155.123.55' AND User='kaka';  
2. Query OK, 1 row affected (0.00 sec)  

3. mysql> flush privileges;  
4. Query OK, 0 rows affected (0.00 sec)  

5. mysql> SELECT Host,User,Password FROM `user`;  
6. +----------------+------+-------------------------------------------+  
7. | Host           | User | Password                                  |  
8. +----------------+------+-------------------------------------------+  
9. | localhost      | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
10. | tony\_ts\_tian | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
11. | 127.0.0.1      | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
12. | ::1            | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
13. | %              | root | *71ABCA8B06D46066CEF8062A75256E66243D0FC8 |  
14. +----------------+------+-------------------------------------------+  
15. 5 rows in set (0.00 sec)  

16. 权限分配

[plain] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. GRANT语法：     
2.    GRANT 权限 ON 数据库.* TO 用户名@'登录主机' IDENTIFIED BY '密码'  
3. 权限：  
4.    ALL,ALTER,CREATE,DROP,SELECT,UPDATE,DELETE  
5.    新增用户：权限为USAGE,即为："无权限",想要创建一个没有权限的用户时,可以指定USAGE  
6. 数据库：  
7.      *.*              表示所有库的所有表  
8.      mylove.*         表示mylove库的所有表  
9.      mylove.loves     表示mylove库的loves表   
10. 用户名：  
11.      MySQL的账户名  
12. 登陆主机：  
13.      允许登陆到MySQL Server的客户端ip  
14.      '%'表示所有ip  
15.      'localhost' 表示本机  
16.      '10.155.123.55' 特定IP  
17. 密码：  
18.       MySQL的账户名对应的登陆密码  

注： IDENTIFIED BY '密码'，可选。

        GRANT会覆盖用户的部分信息，跟insert 、update执行功能一样。

给用户kaka分配test数据库下user表的查询select权限：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> GRANT SELECT ON test.user TO kaka@'10.155.123.55' IDENTIFIED BY '123456';  
2. Query OK, 0 rows affected (0.00 sec)  
3. mysql> flush privileges;  
4. Query OK, 0 rows affected (0.00 sec)  
5. mysql> show Grants for 'kaka'@'10.155.123.55';  
6. +-----------------------------------------------------------------------------------------------------------------+  
7. | Grants for kaka@10.155.123.55                                                                                   |  
8. +-----------------------------------------------------------------------------------------------------------------+  
9. | GRANT USAGE ON *.* TO 'kaka'@'10.155.123.55' IDENTIFIED BY PASSWORD '*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9' |  
10. | GRANT SELECT ON `test`.`user` TO 'kaka'@'10.155.123.55'                                                         |  
11. +-----------------------------------------------------------------------------------------------------------------+  
12. 2 rows in set (0.00 sec)  

为了快速[测试](http://lib.csdn.net/base/softwaretest)，我要把ip切回%，ip全访问：

使用和测试：

数据库和数据表请看： [MySQL数据定义语句：CREATE（创建）命令、ALTER（修改）命令、DROP（删除）](http://blog.csdn.net/typa01_kk/article/details/49131993)

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> use mysql  
2. Reading table information for completion of table and column names  
3. You can turn off this feature to get a quicker startup with -A  
4. Database changed  
5. 修改权限Host为所有ip登陆：  
6. mysql> UPDATE `user` SET Host='%' WHERE Host='10.155.123.55' AND User='kaka';  
7. Query OK, 1 row affected (0.00 sec)  
8. Rows matched: 1  Changed: 1  Warnings: 0  
9. 查看kaka的权限：  
10. mysql> show grants for 'kaka'@'10.155.123.55';  
11. +-----------------------------------------------------------------------------------------------------------------+  
12. | Grants for kaka@10.155.123.55                                                                                   |  
13. +-----------------------------------------------------------------------------------------------------------------+  
14. | GRANT USAGE ON *.* TO 'kaka'@'10.155.123.55' IDENTIFIED BY PASSWORD '*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9' |  
15. | GRANT SELECT ON `test`.`user` TO 'kaka'@'10.155.123.55'                                                         |  
16. +-----------------------------------------------------------------------------------------------------------------+  
17. 2 rows in set (0.00 sec)  
18. 刷新MySQL的系统权限相关表  
19. mysql> flush privileges;  
20. Query OK, 0 rows affected (0.00 sec)  
21. 查看kaka的权限：  
22. mysql> show grants for 'kaka'@'%';  
23. +-----------------------------------------------------------------------------------------------------+  
24. | Grants for kaka@%                                                                                   |  
25. +-----------------------------------------------------------------------------------------------------+  
26. | GRANT USAGE ON *.* TO 'kaka'@'%' IDENTIFIED BY PASSWORD '*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9' |  
27. +-----------------------------------------------------------------------------------------------------+  
28. 1 row in set (0.00 sec)  
29. 给用户kaka分配weloveshare数据库下user表的查询select权限：  
30. mysql> GRANT SELECT ON `weloveshare`.`user` TO kaka@'%';  
31. Query OK, 0 rows affected (0.00 sec)  
32. 查看kaka的权限：  
33. mysql> show grants for 'kaka'@'%';  
34. +-----------------------------------------------------------------------------------------------------+  
35. | Grants for kaka@%                                                                                   |  
36. +-----------------------------------------------------------------------------------------------------+  
37. | GRANT USAGE ON *.* TO 'kaka'@'%' IDENTIFIED BY PASSWORD '*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9' |  
38. | GRANT SELECT ON `weloveshare`.`user` TO 'kaka'@'%'                                                  |  
39. +-----------------------------------------------------------------------------------------------------+  
40. 2 rows in set (0.00 sec)  
41. 查看weloveshare数据库下user表的数据：  
42. mysql> use weloveshare  
43. Reading table information for completion of table and column names  
44. You can turn off this feature to get a quicker startup with -A  
45. Database changed  
46. mysql> select * from user;  
47. Empty set (0.00 sec)  
48. 退出当前用户：  
49. mysql> exit;  
50. Bye  
51. 切换用户kaka:  
52. [root@Tony_ts_tian ~]# mysql -u kaka -p  
53. Enter password:   
54. 登录成功。  
55. 切换数据库，查看user表数据：  
56. mysql> use weloveshare  
57. Reading table information for completion of table and column names  
58. You can turn off this feature to get a quicker startup with -A  

59. Database changed  
60. mysql> select * from user;  
61. Empty set (0.00 sec)  
62. 插入数据：  
63. mysql> INSERT INTO `weloveshare`.`user`(uname,upass,ustatus) VALUES('kaka','kaka123','0');  
64. ERROR 1142 (42000): INSERT command denied to user 'kaka'@'localhost' for table 'user'  
65. 提示：INSERT被拒绝。配置成功。  

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. 注：`weloveshare`.`user`数据库名.数据表名，kaka用户名，%为Host，ip可限制或不 localhost，%，192.168.10.%  
2. grant创建、修改、删除、更新、查询MySQL数据表结构权限：  
3. GRANT CREATE ON `weloveshare`.`user` TO kaka@'%';   
4. GRANT ALTER ON `weloveshare`.`user` TO kaka@'%';   
5. GRANT DROP ON `weloveshare`.`user` TO kaka@'%';   
6. GRANT UPDATE ON `weloveshare`.`user` TO kaka@'%';   
7. GRANT SELECT ON `weloveshare`.`user` TO kaka@'%';   
8. grant操作MySQL外键权限:  
9. GRANT REFERENCES ON `weloveshare`.`user` TO kaka@'%';   
10. grant操作MySQL 临时表权限:  
11. GRANT CREATE TEMPORARY TABLES ON `weloveshare`.`user` TO kaka@'%';   
12. grant操作MySQL索引权限  
13. GRANT INDEX ON `weloveshare`.`user` TO kaka@'%';   
14. grant操作MySQL视图、查看视图源代码权限:  
15. GRANT CREATE VIEW ON `weloveshare`.`user` TO kaka@'%';   
16. GRANT SHOW VIEW ON `weloveshare`.`user` TO kaka@'%';   
17. grant操作MySQL存储过程(查看状态,删除修改)、函数权限。  
18. GRANT CREATE ROUTINE ON `weloveshare`.`user` TO kaka@'%';   
19. GRANT CREATE ROUTINE ON `weloveshare`.`user` TO kaka@'%';   
20. GRANT EXECUTE ON `weloveshare`.`user` TO kaka@'%';  

注：其他的详细权限，请查看，备注附件（最后）。

5：查看数据库登陆所有用户：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS QUERY FROM mysql.user;  
2. +--------------------------------+  
3. | QUERY                          |  
4. +--------------------------------+  
5. | User: 'kaka'@'%';              |  
6. | User: 'root'@'%';              |  
7. | User: 'root'@'127.0.0.1';      |  
8. | User: 'root'@'::1';            |  
9. | User: 'root'@'localhost';      |  
10. | User: 'root'@'tony\_ts\_tian'; |  
11. +--------------------------------+  
12. 6 rows in set (0.00 sec)  

查看某个用户的具体权限，比如root：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> show grants for 'root'@'%';  
2. +--------------------------------------------------------------------------------------------------------------------------------+  
3. | Grants for root@%                                                                                                              |  
4. +--------------------------------------------------------------------------------------------------------------------------------+  
5. | GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY PASSWORD '*71ABCA8B06D46066CEF8062A75256E66243D0FC8' WITH GRANT OPTION |  
6. +--------------------------------------------------------------------------------------------------------------------------------+  
7. 1 row in set (0.00 sec)  

或

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> select * from mysql.user where user='root' \G  

注：\G为按列显示数据。

备注附件：

查看MySQL数据中user表的表结构：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. mysql> DESC mysql.user;  
2. +------------------------+-------------------+------+-----+-----------+-------+  
3. | Field                  | Type              | Null | Key | Default   | Extra |  
4. +------------------------+-------------------+------+-----+-----------+-------+  
5. | Host                   | char(60)          | NO   | PRI |           |       |  
6. | User                   | char(16)          | NO   | PRI |           |       |  
7. | Password               | char(41)          | NO   |     |           |       |  
8. | Select_priv            | enum('N','Y')     | NO   |     | N         |       |  
9. | Insert_priv            | enum('N','Y')     | NO   |     | N         |       |  
10. | Update_priv            | enum('N','Y')     | NO   |     | N         |       |  
11. | Delete_priv            | enum('N','Y')     | NO   |     | N         |       |  
12. | Create_priv            | enum('N','Y')     | NO   |     | N         |       |  
13. | Drop_priv              | enum('N','Y')     | NO   |     | N         |       |  
14. | Reload_priv            | enum('N','Y')     | NO   |     | N         |       |  
15. | Shutdown_priv          | enum('N','Y')     | NO   |     | N         |       |  
16. | Process_priv           | enum('N','Y')     | NO   |     | N         |       |  
17. | File_priv              | enum('N','Y')     | NO   |     | N         |       |  
18. | Grant_priv             | enum('N','Y')     | NO   |     | N         |       |  
19. | References_priv        | enum('N','Y')     | NO   |     | N         |       |  
20. | Index_priv             | enum('N','Y')     | NO   |     | N         |       |  
21. | Alter_priv             | enum('N','Y')     | NO   |     | N         |       |  
22. | Show_db_priv           | enum('N','Y')     | NO   |     | N         |       |  
23. | Super_priv             | enum('N','Y')     | NO   |     | N         |       |  
24. | Create_tmp_table_priv  | enum('N','Y')     | NO   |     | N         |       |  
25. | Lock_tables_priv       | enum('N','Y')     | NO   |     | N         |       |  
26. | Execute_priv           | enum('N','Y')     | NO   |     | N         |       |  
27. | Repl_slave_priv        | enum('N','Y')     | NO   |     | N         |       |  
28. | Repl_client_priv       | enum('N','Y')     | NO   |     | N         |       |  
29. | Create_view_priv       | enum('N','Y')     | NO   |     | N         |       |  
30. | Show_view_priv         | enum('N','Y')     | NO   |     | N         |       |  
31. | Create_routine_priv    | enum('N','Y')     | NO   |     | N         |       |  
32. | Alter_routine_priv     | enum('N','Y')     | NO   |     | N         |       |  
33. | Create_user_priv       | enum('N','Y')     | NO   |     | N         |       |  
34. | Event_priv             | enum('N','Y')     | NO   |     | N         |       |  
35. | Trigger_priv           | enum('N','Y')     | NO   |     | N         |       |  
36. | Create_tablespace_priv | enum('N','Y')     | NO   |     | N         |       |  
37. | ssl_type               | enum('','ANY','X509','SPECIFIED') | NO  || |       |  
38. | ssl_cipher             | blob              | NO   |     | NULL      |       |  
39. | x509_issuer            | blob              | NO   |     | NULL      |       |  
40. | x509_subject           | blob              | NO   |     | NULL      |       |  
41. | max_questions          | int(11) unsigned  | NO   |     | 0         |       |  
42. | max_updates            | int(11) unsigned  | NO   |     | 0         |       |  
43. | max_connections        | int(11) unsigned  | NO   |     | 0         |       |  
44. | max_user_connections   | int(11) unsigned  | NO   |     | 0         |       |  
45. | plugin                 | char(64)          | YES  || mysql_native_password ||  
46. | authentication_string  | text              | YES  |     | NULL      |       |  
47. | password_expired       | enum('N','Y')     | NO   |     | N         |       |  
48. +------------------------+-------------------+------+-----+-----------+-------+  
49. 43 rows in set (0.00 sec)  

查看root用户的所有具体权限：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1.                Host: %  
2.                User: root  
3.            Password: *71ABCA8B06D46066CEF8062A75256E66243D0FC8  
4.         Select_priv: Y  
5.         Insert_priv: Y  
6.         Update_priv: Y  
7.         Delete_priv: Y  
8.         Create_priv: Y  
9.           Drop_priv: Y  
10.         Reload_priv: Y  
11.       Shutdown_priv: Y  
12.        Process_priv: Y  
13.           File_priv: Y  
14.          Grant_priv: Y  
15.     References_priv: Y  
16.          Index_priv: Y  
17.          Alter_priv: Y  
18.        Show_db_priv: Y  
19.          Super_priv: Y  
20. eate_tmp_table_priv: Y  
21.    Lock_tables_priv: Y  
22.        Execute_priv: Y  
23.     Repl_slave_priv: Y  
24.    Repl_client_priv: Y  
25.    Create_view_priv: Y  
26.      Show_view_priv: Y  
27. Create_routine_priv: Y  
28.  Alter_routine_priv: Y  
29.    Create_user_priv: Y  
30.          Event_priv: Y  
31.        Trigger_priv: Y  
32. ate_tablespace_priv: Y  
33.            ssl_type:   
34.          ssl_cipher:   
35.         x509_issuer:   
36.        x509_subject:   
37.       max_questions: 0  
38.         max_updates: 0  
39.     max_connections: 0  
40. ax_user_connections: 0  
41.              plugin: mysql_native_password  
42. thentication_string:   
43.    password_expired: N  

参数说明：

[sql] [view plain](http://blog.csdn.net/typa01_kk/article/details/49126365#) [copy](http://blog.csdn.net/typa01_kk/article/details/49126365#)

1. Select_priv：用户可以通过SELECT命令选择数据。  
2. Insert_priv：用户可以通过INSERT命令插入数据;  
3. Update_priv：用户可以通过UPDATE命令修改现有数据;  
4. Delete_priv：用户可以通过DELETE命令删除现有数据;  
5. Create_priv：用户可以创建新的数据库和表;  
6. Drop_priv：用户可以删除现有数据库和表;  
7. Reload_priv：用户可以执行刷新和重新加载MySQL所用各种内部缓存的特定命令,包括日志、权限、主机、查询和表;重新加载权限表;  
8. Shutdown_priv：用户可以关闭MySQL服务器;在将此权限提供给root账户之外的任何用户时,都应当非常谨慎;  
9. Process_priv：用户可以通过SHOW PROCESSLIST命令查看其他用户的进程;服务器管理;  
10. File_priv：用户可以执行SELECT INTO OUTFILE和LOAD DATA INFILE命令;加载服务器上的文件;  
11. Grant_priv：用户可以将已经授予给该用户自己的权限再授予其他用户(任何用户赋予全部已有权限);  
12. References_priv;目前只是某些未来功能的占位符；现在没有作用;  
13. Index_priv：用户可以创建和删除表索引;用索引查询表;  
14. Alter_priv：用户可以重命名和修改表结构;  
15. Show_db_priv：用户可以查看服务器上所有数据库的名字,包括用户拥有足够访问权限的数据库;可以考虑对所有用户禁用这个权限,除非有特别不可抗拒的原因;  
16. Super_priv：用户可以执行某些强大的管理功能,例如通过KILL命令删除用户进程,使用SET GLOBAL修改全局MySQL变量,执行关于复制和日志的各种命令;超级权限;  
17. Create_tmp_table_priv：用户可以创建临时表;  
18. Lock_tables_priv：用户可以使用LOCK TABLES命令阻止对表的访问/修改;  
19. Execute_priv：用户可以执行存储过程;此权限只在MySQL 5.0及更高版本中有意义;  
20. Repl_slave_priv：用户可以读取用于维护复制数据库环境的二进制日志文件;此用户位于主系统中,有利于主机和客户机之间的通信;主服务器管理;  
21. Repl_client_priv：用户可以确定复制从服务器和主服务器的位置;从服务器管理;  
22. Create_view_priv：用户可以创建视图;此权限只在MySQL 5.0及更高版本中有意义;  
23. Show_view_priv：用户可以查看视图或了解视图如何执行;此权限只在MySQL 5.0及更高版本中有意义;  
24. Create_routine_priv：用户可以更改或放弃存储过程和函数;此权限是在MySQL 5.0中引入的;  
25. Alter_routine_priv：用户可以修改或删除存储函数及函数;此权限是在MySQL 5.0中引入的;  
26. Create_user_priv：用户可以执行CREATE USER命令,这个命令用于创建新的MySQL账户;  
27. Event_priv：用户能否创建、修改和删除事件;这个权限是MySQL 5.1.6新增的;  
28. Trigger_priv：用户能否创建和删除触发器,这个权限是MySQL 5.1.6新增的;  
29. Create_tablespace_priv：创建表空间  
30. ssl_type：支持ssl标准加密安全字段  
31. ssl_cipher：支持ssl标准加密安全字段  
32. x509_issuer：支持x509标准字段  
33. x509_subject：支持x509标准字段  
34. max_questions：0 每小时允许执行多少次查询  
35. max_updates：0 每小时可以执行多少次更新  ：0表示无限制  
36. max_connections：0 每小时可以建立的多少次连接：0表示无限制  
37. max_user_connections：0 单用户可以同时具有的连接数：0表示无限制  
38. plugin：5.5.7开始,mysql引入plugins以进行用户连接时的密码验证,plugin创建外部/代理用户   
39. authentication_string：通过authentication_string可以控制两者的映射关系,(PAM plugin等,PAM可以支持多个服务名)尤其是在使用代理用户时，并须声明这一点  
40. password_expired：密码过期 Y,说明该用户密码已过期 N相反  

来源： [https://blog.csdn.net/zmx729618/article/details/78026497](https://blog.csdn.net/zmx729618/article/details/78026497)