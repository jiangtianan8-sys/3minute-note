项目位置：[https://github.com/hhyo/archery](https://github.com/hhyo/archery)

# 背景

SQL 审核是对 MySQL 语句写法的统一化，标准化，避免因为 SQL 的不规范、语法错误等导致出现误删、误更新数据、数据库性能下降等问题。早期的人工审核，针对标准这个问题其实是很吃力的，标准越多，DBA 越累，开发也越累；因为 Inception 诞生了，Inception 不止是一个自动化审核工 具，同时还具备执行，生成对影响数据的回滚语句等功能。

# 简介

基于 inception 的自动化 SQL 操作平台，支持工单、审核、定时任务、邮件、OSC 等功能，还可配置 MySQL 查询、慢查询管理、会话管理等，将 Inception 封装成可视化平台，方便开发、运维人员使用。同时集成了部分 DB 运维功能，如：MySQL 优化建议（[SQLAdvisor](https://github.com/Meituan-Dianping/SQLAdvisor)，[SOAR](https://github.com/XiaoMi/soar)），MySQL EXPLAIN 细化（MySQLTuning），闪回（[binlog2sql](https://github.com/danfengcao/binlog2sql)），慢 SQL 展示、会话管理、锁等待信息查看等等。项目地址：[https://github.com/hhyo/Archery](https://github.com/hhyo/Archery)

# 主要功能

[archery平台功能列表](https://github.com/hhyo/Archery/wiki/%E5%8A%9F%E8%83%BD%E5%88%97%E8%A1%A8)

![](http://media.teamshub.com/10000/tm/2019/08/15/970e0ffc-60d0-4fc2-8a67-f7140ba2186c/abcc1775-25e0-4dd5-88b2-c69a65d13d97.png)

- 自动审核

发起 SQL 上线，工单提交，由 inception 自动审核，审核通过后需要由审核人进行人工审核

- 人工审核

inception 自动审核通过的工单，由其他研发工程师或研发经理来审核，DBA 操作执行 SQL

为什么要有人工审核？

这是遵循运维领域线上操作的流程意识，一个工程师要进行线上数据库 SQL 更新，最好由另外一个工程师来把关 很多时候 DBA 并不知道 SQL 的业务含义，所以人工审核最好由其他研发工程师或研发经理来审核. 这是 archer 的设计理念

- 回滚数据展示

工单内可展示回滚语句，支持一键提交回滚工单

- 定时执行 SQL

审核通过的工单可由 DBA 选择定时执行，执行前可修改执行时间，可随时终止

- pt-osc 执行

支持 pt-osc 执行进度展示，并且可以点击中止 pt-osc 进程

- MySQL 查询

库、表、关键字自动补全 查询结果集限制、查询结果导出、表结构展示、多结果集展示

- MySQL 查询权限管理

基于 inception 解析查询语句，查询权限支持限制到表级 查询权限申请、审核和管理，支持审核流程配置，多级审核

- MySQL 查询动态脱敏

基于 inception 解析查询语句，配合脱敏字段配置、脱敏规则 (正则表达式) 实现敏感数据动态脱敏

- 慢日志管理

基于 percona-toolkit 的 pt_query_digest 分析和存储慢日志，并在 web 端展现

- 邮件通知

可配置邮件提醒，对上线申请、权限申请、审核结果等进行通知 对异常登录进行通知

# 文档

[inception的使用规范和说明](https://inception-document.readthedocs.io/zh_CN/latest/)

[goInception的使用文档](https://hanchuanchuan.github.io/goInception/)

[archery平台使用文档](https://github.com/hhyo/archery/wiki)

[archery平台功能列表](https://github.com/hhyo/Archery/wiki/%E5%8A%9F%E8%83%BD%E5%88%97%E8%A1%A8)

[MySQL数据库设计规范](http://172.18.231.123:9123/dbaprinciples/)

# docker 方式安装

## 启动

进入 docker-compose 文件夹

```bash
#启动
docker-compose -f docker-compose.yml up -d

#表结构初始化
docker exec -ti archery /bin/bash
cd /opt/archery
source /opt/venv4archery/bin/activate
python3 manage.py makemigrations sql  
python3 manage.py migrate

#数据初始化
python3 manage.py loaddata initial_data.json

#创建管理用户
python3 manage.py createsuperuser

#重启服务
docker restart archery

#日志查看和问题排查
docker logs archery -f --tail=10
/downloads/log/archery.log
```

## 访问

[http://172.18.231.123:9123/](http://172.18.231.123:9123/)

## 导出、导入镜像

docker save -o archery.tar hanchuanchuan/goinception redis:5 mysql:5.7 mongo:3.6 hhyo/inception hhyo/archery

docker load < archery.tar

## 初始化慢 SQL 表结构与 goinception 配置信息

登陆 archery 数据库

```bash
mysql -h172.18.231.123 -P13336 -uroot -p123456 archery

source /mysql/archery/src/init_sql/mysql_slow_query_review.sql

source /mysql/archery/src/init_sql/goinception_param_template.sql
```

## SQLAdvisor

功能说明：利用美团 SQLAdvisor 对收集的慢日志进行优化，一键获取优化建议，项目地址 [SQLAdvisor](https://github.com/Meituan-Dianping/SQLAdvisor)

# 体验环境

[archery SQL审核平台演示](http://172.18.231.123:9123/)

用户 admin admin1234

dbproxy-118:16066/iddbs 或 dbproxy-117:16066/iddbs

```lua
普通表 tb_default   <table name="tb_default" dataNode="dn1"/>

全局表 tb_global    <table name="tb_global" dataNode="dn$1-6" type="global"/>

拆分表 tb_sharding  <table name="tb_sharding" dataNode="dn$1-4" rule="mod-long4"/>
```
