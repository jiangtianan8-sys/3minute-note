员工部门工资 SQL 面试题

现有 employee 表，表中有 员工编号（id） 员工年龄（age） 员工工资（salary） 员工部门（deptid）, 按要求用一条 SQL 语句完成

create table employee(  

id int  identity(1,1) primary key ,  

name varchar(50),  

salary bigint,  

deptid int);

1.查出每个部门高于部门平均工资的员工名单

select ta.* from employee ta,  

(select deptid,avg(salary) avgsal from employee group by deptid)tb   

where ta.deptid=tb.deptid and ta.salary>tb.avgsal

2、列出各个部门中工资高于本部门的平均工资的员工数和部门号，并按部门号排序。

select ta.deptid,count(*) as ‘人数’  from employee ta,  

(select deptid,avg(salary) avgsal from employee group by deptid)tb   

where ta.deptid=tb.deptid and ta.salary>tb.avgsal group by ta.deptid order by ta.deptid

3.求每个部门工资不小于 6000 的人员的平均值；

SELECT avg(salary) as ‘平均值’,deptid FROM employee  where salary >=6000 GROUP BY dept_id

4、各部门在各年龄段的平均工资

select deptid,

sum(case when age < 20 then salary else 0 end) / sum(case when age <20 then 1 else 0 end) as “20 岁以下平均工资”,

sum(case when age >= 20 and age <40 then salary else 0 end) / sum(case when age >= 20 and age <40 then 1 else 0 end) as “20 至 40 岁平均工资”,

sum(case when age >= 40 then salary else 0 end) / sum(case when age >=40 then 1 else 0 end) as “>40 岁及以上平均工资”,

from employee

group by deptid

以上 SQL 面试题，经常会出现在笔试环节，特别是 [Java](http://lib.csdn.net/base/java) 开发工程师岗位，虽然并不是很难，但对于那些比较熟悉 SSH 开发，不经常写 SQL 的同学来说，有时候还真是不知道怎么写。

来源： [http://blog.csdn.net/luoxiang183/article/details/52047832](http://blog.csdn.net/luoxiang183/article/details/52047832)
