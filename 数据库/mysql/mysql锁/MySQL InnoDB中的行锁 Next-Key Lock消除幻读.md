InnoDB 中有三种行锁技术：

Record Lock：单个行记录上的锁，我们通常讲的行锁，它的实质是通过对索引的加锁实现；只有通过索引条件检索数据，InnoDB 才使用行级锁，否则，InnoDB 将使用表锁。在事务隔离级别为读已提交下，仅采用 Record Lock。

Gap Lock：间隙锁，锁定一个范围，但不包含记录本身；

Next-Key Lock：Record Lock+Gap Lock，锁定一个范围，并且锁定记录本身

1. Next-Key Lock

Next-Key Lock 是结合 Record Lock 与 Gap Lock 的一种锁定方法，它锁定了包括记录本身的一个范围。

id name

10 a

20 b

50 c

如果索引为 10，20，50，那么：

Record Lock：select * from tab where id = 10 for update; //对 id=10 单行进行加锁

Gap Lock 锁范围：（- ∞

，10）（10，20）（20，50）（50，+∞）

Next-Key Lock 锁范围：（- ∞，10）[10，20）[20，50）[50，+∞

）

事务 A 事务 B

set autocommit=0;

select * from tab where id>10 for update; //查询结果为 20,50

select * from tab where id=10 for update;//执行等待,Next-Key Lock 锁机制暴露

commit;

继续执行，查询结果为 10

select * from tab where id=10 for update; //查询结果为 10

select * from tab where id=10 for update; //等待执行

commit;

继续执行，查询结果为 10

select * from tab where id=10 for update; //查询结果为 10，锁降级为 Record Lock

select * from tab where id>20 for update; //立即执行，查询结果为 50

应该从上面的例子中看出了一些问题。

Next-Key Lock 的加锁方式

当查询的索引含有唯一属性时，InnoDB 会对 Next-Key Lock 进行优化，将其降级为 Record Lock，即仅锁住索引本身，而不是范围。上表中的第三个事例中可看出.

2. 为什么会存在 Next-Key Lock

InnoDB 能在可重复读的事务隔离级别下消除幻读

一般的数据库避免幻读需要在串行化的事务隔离级别下，而 InnoDB 在可重复读的事务隔离级别下消除幻读；这样能够有效提高数据库的并发度。

3. 幻读

幻读是指在同一事务下，连续执行两次同样的 SQL 语句可能导致不同的结果，第二次的 SQL 语句可能会返回之前不存在的行。

事务 A 事务 B

SET SESSION tx_isolation=’READ-COMMITTED’;

begin; select * from tab where id>10 for update; //查询结果为 20,50

begin; insert into tab values(30,c); commit;

select * from tab where id>10 for update; //查询结果为 20,30,50; 出现幻读

4. Next-Key Lock 避免幻读

关键点在于对查询范围进行加锁，在另一个事务执行插入操作时是不被运行的，从而避免了幻读。

具体的例子可以参考第 2、3 节，不再举例。

参考：

《MySQL 技术内幕》

http://blog.csdn.net/mysteryhaohao/article/details/51669741

————————————————

版权声明：本文为 CSDN 博主「华仔的逆袭」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。

原文链接：https://blog.csdn.net/tb3039450/article/details/66475638
