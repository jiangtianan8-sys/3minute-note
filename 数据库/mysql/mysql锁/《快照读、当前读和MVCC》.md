1、快照读

　　快照读是基于 MVCC 和 undo log 来实现的，适用于简单 select 语句。

　　读已提交：一个事务内操作一条数据，可以查询到另一个已提交事务操作同一条数据的最新值。（Oracle 默认隔离级别）

　　可重复读：每个事务只关注自己事务开始查询到的数据值，无论事务查询同一条数据多少次，该数据改了多少次，都只查询到事务开始之前的数据值。（MySQL 默认隔离级别）

　　而所谓 MVCC 并发版本控制，是靠 readView (事务视图) 来实现的。多个 readView 组成 undo log（回滚日志）。

　　每一个 sql 查询某条数据时，都是查询最新 readView 的该条数据的值。

　　ReadView：（查询同一条数据，因为 readView 也是针对同一条数据生成的视图）

　　读已提交：是事务中的每个 sql 语句生成一个 readView。那就是一个事务内多条 sql 语句，会生成多个 readView。而每条 sql 执行时，都是查询最新 readView 的值。

　　假如事务 A 有 2 个查询 sql 语句，在第一个查询 sql 生成一个 readView（事务视图 id = n），事务 B 对该数据做了操作，那么就会生成新的 readView（事务视图 id = n + 1），第二个查询 sql 语句获取该条数据时，就会去 readView（事务视图 id = n + 1）查询数据。

　　可重复读：是在事务开始的时候生成一个 readView。所以一个事务内的多条查询 sql ，查询同一条数据时，读取到的 readView 都是同一个，那么查询某条数据的值，也是同一个值。

　　例如事务 A 开始查询主键 id = 1 的行数据的列 age = 10，不管其他事务是否对该 age 做改变，当前事务的多条查询 sql 语句，查询 age 的值一直都是 age = 10。

[回到顶部](https://www.cnblogs.com/AlmostWasteTime/p/11466520.html#_labelTop)

2、当前读

　　当前读是基于 临键锁（行锁 + 间歇锁）来实现的，适用于 insert，update，delete， select … for update， select … lock in share mode 语句，以及加锁了的 select 语句。

　　当前读：

　　更新数据时，都是先读后写，而这个读，就是当前读。读取数据时，读取该条数据的已经提交的最新的事务，生成的 readView。

　　例如事务 A 有 2 个 sql 语句，事务开始时生成 readView（id = n），第一个 sql 操作一条数据时读当前的 readView（id = n） 。此时开始事务 B 生成 readView（id = n + 1），并且对该条数据做了操作（非简单 select 操作）。事务 A 的第 2 个 sql 语句当前读该数据时，就会读取该数据的最新事务视图 readView (id =n + 1) 的值。

　　而假如事务 A 的第二个 sql 语句操作数据时，事务 B 还未提交（非简单 select 操作），那么该条数据此时被事务 B 的写锁锁住。事务 A 的第二个 sql 语句操作数据（非简单 select 操作），那么也要获取该条数据的锁。而此时锁被事务 B 持有，事务 A 就会阻塞，等待事务 B 释放锁。
