行结构

每一行额外包含三个隐藏字段：

- DB_TRX_ID：事务 ID。行的创建时间和删除时间记录的就是此值。
- DB_ROLL_PTR：指向当前记录项的 undo 信息。
- DB_ROW_ID:：随着新行插入单调递增的一个字段。当由 innodb 自动产生聚集索引时，聚集索引包括这个 DB_ROW_ID 的值，不然的话聚集索引中不包括这个值。
- 在 insert 操作时，创建时间 = DB_ROW_ID，这时，“删除时间 ”是未定义的。
- 在 update 操作时，复制新增行的“创建时间”=DB_ROW_ID，删除时间未定义，旧数据行“创建时间”不变，删除时间=该事务的 DB_ROW_ID。
- 在 delete 操作时，相应数据行的“创建时间”不变，删除时间 = 该事务的 DB_ROW_ID。
- select 操作对两者都不修改，只读相应的数据。

Read View

dulint    low_limit_id;    /* 事务号 >= low_limit_id 的记录，对于当前 Read View 都是不可见的 */

    dulint    up_limit_id;    /* 事务号 < up_limit_id ，对于当前Read View都是可见的 */

    ulint    n_trx_ids;    /* Number of cells in the trx_ids array */

    dulint*    trx_ids;    /* Additional trx ids which the read should

                not see: typically, these are the active

                transactions at the time when the read is

                serialized, except the reading transaction

                itself; the trx ids in this array are in a

                descending order */

dulint    creator_trx_id;    /* trx id of creating transaction, or

                (0, 0) used in purge */

关于 low_limit_id，up_limit_id 的理解：

up_limit_id：当前已经提交的事务号 + 1，事务号 < up_limit_id ，对于当前 Read View 都是可见的。理解起来就是创建 Read View 视图的时候，之前已经提交的事务对于 该事务肯定是可见的。

low_limit_id：当前最大的事务号 + 1，事务号 >= low_limit_id，对于当前 Read View 都是不可见的。理解起来就是在创建 Read View 视图之后创建的事务对于该事务肯定是不可见的。

另外，trx_ids 为活跃事务 id 列表，即 Read View 初始化时当前未提交的事务列表。所以当进行 RR 读的时候，trx_ids 中的事务对于本事务是不可见的（除了自身事务，自身事务对于表的修改对于自己当然是可见的）。理解起来就是创建 RV 时，将当前活跃事务 ID 记录下来，后续即使他们提交对于本事务也是不可见的。

up_limit_id<=事务号

example

|   |   |   |   |
|---|---|---|---|
|步骤|1|2|3|
|一|begin|||
|二||begin||
|三|insert into test(score) values(1607); 假设此时事务号 21|||
|四||insert into test(score) values(1607); 此时事务号 22||
|五|此时创建读视图，up_limit_id = 21， low_limit_id = 23 活跃事务列表为 (21,22)|||
|六|||insert into test(score) values(1620); 事务号为 23|
|七|||insert into test(score) values(1621); 事务号为 24|
|八|||insert into test(score) values(1622); 事务号为 25|
|九|||select * from test; 此时的 up_limit_id 为 21，low_limit_id 为 26，活跃事务列表为（21,22），故 21，22 在活跃事务列表不可见|
|十||select * from test; 此时 low_limit_id 为 26，up_limit_id 为 21，活跃事务列表是 (21,22) 22 本事务自身可见。21 的在活跃事务列表不可见。23,24 不在活跃事务列表，可见||
|十一|select * from test; 事务内 readview 不变，low_limit_id = 23，up_limit_id = 21，活跃事务列表 （21,22）。故 21 自身可见，22 在活跃事务列表不可见。>=23 的都不可见|||

![0](https://note.youdao.com/yws/res/10662/F55219A09ECB4C95867A45122A78AC67)

![0](https://note.youdao.com/yws/res/10663/71D50736779B44B2BA8ADF81D6612401)

![0](https://note.youdao.com/yws/res/10661/6901DDD2011942DBB48D28BA5056A6ED)

![0](https://note.youdao.com/yws/res/10662/F55219A09ECB4C95867A45122A78AC67)

注意的几点：

- Read View 视图是在进行 RR 读之前创建的，而不是在事务刚 begin 时创建的。如果 Read View 视图是在事务刚 begin 时创建的，那么在步骤四中事务 22 的 Read View 就定下来了（up_limit_id = 21，low_limit_id = 23），那么在步骤十中就看不到 3 中提交的数据了，因为事务号 23,24,25 大于等于事务 22.low_limit_id
- 事务内 Read View 一旦创建就不变化了。
- 在第十步中按我之前的理解，3 中 insert 的数据是在 2 中 begin 之后插入的，按理说 2 是看不到 3 中 insert 插入的数据的。但是事务保证的是两次 select 的数据是一致的，所以 Read View 是在第一次 select 时创建的，所以 3 中 insert 的数据是在 2 中可以看到。

参考资料：[http://hedengcheng.com/?p=148](http://hedengcheng.com/?p=148)

[https://github.com/zhangyachen/zhangyachen.github.io/issues/68](https://github.com/zhangyachen/zhangyachen.github.io/issues/68)
