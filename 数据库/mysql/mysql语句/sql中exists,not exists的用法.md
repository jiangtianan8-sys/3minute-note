exists : 强调的是是否返回结果集，不要求知道返回什么, 比如：

  select name from student where sex = 'm' and mark exists(select 1 from grade where ...) ,只要

exists 引导的子句有结果集返回，那么 exists 这个条件就算成立了,大家注意返回的字段始终为 1，如果改成“select 2 from grade where ...”，那么返回的字段就是 2，这个数字没有意义。所以 exists 子句不在乎返回什么，而是在乎是不是有结果集返回。

而 exists 与 in 最大的区别在于 in 引导的子句只能返回一个字段，比如：

  select name from student where sex = 'm' and mark in (select 1,2,3 from grade where ...)  

，in 子句返回了三个字段，这是不正确的，exists 子句是允许的，但 in 只允许有一个字段返回，在 1，2，3 中随便去了两个字段即可。

而 not exists 和 not in 分别是 exists 和 in 的 对立面。

exists （sql 返回结果集为真）  

not exists (sql 不返回结果集为真）

下面详细描述 not exists 的过程：

如下：

表 A

ID NAME  

1   A1

2   A2

3   A3

表 B

ID AID NAME

1   1     B1

2   2     B2  

3   2     B3

表 A 和表 B 是１对多的关系 A.ID => B.AID

SELECT ID,NAME FROM A WHERE EXISTS (SELECT * FROM B WHERE A.ID=B.AID)

执行结果为

1 A1

2 A2

原因可以按照如下分析

SELECT ID,NAME FROM A WHERE EXISTS (SELECT * FROM B WHERE B.AID=１)

--->SELECT * FROM B WHERE B.AID=１有值返回真所以有数据

SELECT ID,NAME FROM A WHERE EXISTS (SELECT * FROM B WHERE B.AID=2)

--->SELECT * FROM B WHERE B.AID=２有值返回真所以有数据

SELECT ID,NAME FROM A WHERE EXISTS (SELECT * FROM B WHERE B.AID=3)

--->SELECT * FROM B WHERE B.AID=３无值返回真所以没有数据

NOT EXISTS 就是反过来

SELECT ID,NAME FROM A WHERE　NOT EXIST (SELECT * FROM B WHERE A.ID=B.AID)

执行结果为

3 A3

===========================================================================

EXISTS = IN,意思相同不过语法上有点点区别，好像使用 IN 效率要差点，应该是不会执行索引的原因

SELECT ID,NAME FROM A　 WHERE　ID IN (SELECT AID FROM B)

NOT EXISTS = NOT IN ,意思相同不过语法上有点点区别

SELECT ID,NAME FROM A WHERE　ID　NOT IN (SELECT AID FROM B)

 有时候我们会遇到要选出某一列不重复,某一列作为选择条件,其他列正常输出的情况.

如下面的表 table:

Id  Name  Class Count  Date

 1   苹果    水果    10     2011-7-1

 1   桔子    水果    20     2011-7-2

 1   香蕉    水果    15     2011-7-3

 2   白菜    蔬菜    12     2011-7-1

 2   青菜    蔬菜    19     2011-7-2

如果想要得到下面的结果:(Id 唯一,Date 选最近的一次)

1   香蕉    水果    15     2011-7-3

2   青菜    蔬菜    19     2011-7-2

正确的 SQL 语句是:

SELECT Id, Name, Class, Count, Date

FROM table t

WHERE (NOT EXISTS

          (SELECT Id, Name, Class, Count, Date FROM table 

         WHERE Id = t.Id AND Date > t.Date))   ------- 不存在日期比我还大的，就是选出日期最大的项

如果用 distinct,得不到这个结果, 因为 distinct 是作用与所有列的

SELECT DISTINCT Id, Name, Class, Count, Date FROM table

结果是表 table 的所有不同列都显示出来,如下所示:

 1   苹果     水果    10     2011-7-1

 1   桔子    水果    20     2011-7-2

 1   香蕉    水果    15     2011-7-3

 2   白菜    蔬菜    12     2011-7-1

 2   青菜    蔬菜    19     2011-7-2

如果用 Group by 也得不到需要的结果,因为 Group by 要和聚合函数共同使用,所以对于 Name,Class 和 Count 列要么使用 Group by,要么使用聚合函数. 如果写成

SELECT Id, Name, Class, Count, MAX(Date) 

FROM table

GROUP BY Id, Name, Class, Count

得到的结果是

 1   苹果     水果    10    2011-7-1

 1   桔子    水果    20     2011-7-2

 1   香蕉    水果    15     2011-7-3

 2   白菜    蔬菜    12     2011-7-1

 2   青菜    蔬菜    19     2011-7-2

如果写成

SELECT Id, MAX(Name), MAX(Class), MAX(Count), MAX(Date) 

FROM table 

GROUP BY Id

得到的结果是:

 1   香蕉    水果    20     2011-7-3

 2   青菜    蔬菜    19     2011-7-2

如果用 in 有时候也得不到结果,（有的时候可以得到，如果 Date 都不相同（没有重复数据），或者是下面得到的 Max（Date）只有一个值）

SELECT DISTINCT Id, Name, Class, Count, Date FROM table

WHERE (Date IN

          (SELECT MAX(Date)

         FROM table

         GROUP BY Id))

得到的结果是：（因为 MAX(Date) 有两个值 2011-7-2，2011-7-3）

 1   桔子    水果    20     2011-7-2

 1   香蕉    水果    15     2011-7-3

 2   青菜    蔬菜    19     2011-7-2

注意 in 只允许有一个字段返回

有一种方法可以实现：

SELECT Id, Name, Class, COUNT, Date

FROM table1 t

WHERE (Date =

          (SELECT MAX(Date)

         FROM table1

         WHERE Id = t .Id))

来源： [http://www.cnblogs.com/mytechblog/articles/2105785.html](http://www.cnblogs.com/mytechblog/articles/2105785.html)
