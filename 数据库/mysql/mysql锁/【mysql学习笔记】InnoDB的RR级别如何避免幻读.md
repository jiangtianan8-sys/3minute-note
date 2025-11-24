RR 级别 (REPEATABLE-READ 隔离级别) 引入【next-key lock】避免幻读

next-key lock 组成

record lock(记录锁)

gap lock(间隙锁)

gap lock 应用场景

非唯一索引当前读

不走索引的当前读

仅命中部分结果的结果集当前读

主键索引或者唯一索引

1. 如果 where 条件全部命中，则不会用 gap lock 锁，只会加 record lock(记录锁)

2.如果 where 条件部分命中，则会用 gap lock 锁

————————————————

版权声明：本文为 CSDN 博主「qgwperfect」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。

原文链接：https://blog.csdn.net/qgwperfect/article/details/89487145
