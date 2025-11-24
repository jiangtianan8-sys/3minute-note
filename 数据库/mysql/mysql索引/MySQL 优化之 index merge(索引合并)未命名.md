深入理解 index merge 是使用索引进行优化的重要基础之一。理解了 index merge 技术，我们才知道应该如何在表上建立索引。

1. 为什么会有index merge

我们的 where 中可能有多个条件(或者join)涉及到多个字段，它们之间进行 AND 或者 OR，那么此时就有可能会使用到 index merge 技术。index merge 技术如果简单的说，其实就是：对多个索引分别进行条件扫描，然后将它们各自的结果进行合并(intersect/union)。

MySQL5.0之前，一个表一次只能使用一个索引，无法同时使用多个索引分别进行条件扫描。但是从5.1开始，引入了 index merge 优化技术，对同一个表可以使用多个索引分别进行条件扫描。

相关文档：http://dev.mysql.com/doc/refman/5.6/en/index-merge-optimization.html (注意该文档中说的有几处错误)

The Index Merge method is used to retrieve rows with several [range](http://dev.mysql.com/doc/refman/5.6/en/explain-output.html#jointype_range) scans and to merge their results into one. The merge can produce unions, intersections, or unions-of-intersections of its underlying scans. This access method merges index scans from a single table; it does not merge scans across multiple tables.

In [EXPLAIN](http://dev.mysql.com/doc/refman/5.6/en/explain.html) output, the Index Merge method appears as [index_merge](http://dev.mysql.com/doc/refman/5.6/en/explain-output.html#jointype_index_merge) in the type column. In this case, the keycolumn contains a list of indexes used, and key_len contains a list of the longest key parts for those indexes.

index merge: 同一个表的多个索引的范围扫描可以对结果进行合并，合并方式分为三种：union, intersection, 以及它们的组合(先内部intersect然后在外面union)。

官方文档给出了四个例子：

SELECT * FROM tbl_name WHERE key1 = 10 OR key2 = 20; SELECT * FROM tbl_name WHERE (key1 = 10 OR key2 = 20) AND non_key=30; SELECT * FROM t1, t2 WHERE (t1.key1 IN (1,2) OR t1.key2 LIKE 'value%') AND t2.key1=t1.some_col; SELECT * FROM t1, t2 WHERE t1.key1=1 AND (t2.key1=t1.some_col OR t2.key2=t1.some_col2);

但是第四个例子，感觉并不会使用 index merge. 因为 t2.key1=t1.some_col 和 t2.key2=t1.some_col2 之间进行的是 OR 运算，而且 t2.key2 是复合索引的第二个字段(非第一个字段)。所以：t2.key2 = t1.some_col2 并不能使用到复合索引。(文档这里应该是错误的)

index merge 算法根据合并算法的不同分成了三种：intersect, union, sort_union. 

2. index merge 之 intersect

简单而言，index intersect merge就是多个索引条件扫描得到的结果进行交集运算。显然在多个索引提交之间是 AND 运算时，才会出现 index intersect merge. 下面两种where条件或者它们的组合时会进行 index intersect merge:

1) 条件使用到复合索引中的所有字段或者左前缀字段(对单字段索引也适用)

key_part1=const1 AND key_part2=const2 ... AND key_partN=constN

2) 主键上的任何范围条件

例子：

SELECT * FROM innodb_table WHERE primary_key < 10 AND key_col1=20; SELECT * FROM tbl_name WHERE (key1_part1=1 AND key1_part2=2) AND key2=2;

上面只说到复合索引，但是其实单字段索引显然也是一样的。比如 select * from tab where key1=xx and key2 =xxx; 也是有可能进行index intersect merge的。另外上面两种情况的 AND 组合也一样可能会进行 index intersect merge.

The Index Merge intersection algorithm performs simultaneous scans on all used indexes and produces the intersection of row sequences that it receives from the merged index scans. (intersect merge运行方式：多个索引同时扫描，然后结果取交集)

If all columns used in the query are covered by the used indexes, full table rows are not retrieved ([EXPLAIN](http://dev.mysql.com/doc/refman/5.6/en/explain.html) output contains Using index in Extra field in this case). Here is an example of such a query:(索引覆盖扫描，无需回表)

SELECT COUNT(*) FROM t1 WHERE key1=1 AND key2=1;

If the used indexes do not cover all columns used in the query, full rows are retrieved only when the range conditions for all used keys are satisfied.(索引不能覆盖，则对满足条件的再进行回表)

If one of the merged conditions is a condition over a primary key of an InnoDB table, it is not used for row retrieval, but is used to filter out rows retrieved using other conditions.

3. index merge 之 union

简单而言，index uion merge就是多个索引条件扫描，对得到的结果进行并集运算，显然是多个条件之间进行的是 OR 运算。

下面几种类型的 where 条件，以及他们的组合可能会使用到 index union merge算法：

1) 条件使用到复合索引中的所有字段或者左前缀字段(对单字段索引也适用)

2) 主键上的任何范围条件

3) 任何符合 index intersect merge 的where条件；

上面三种 where 条件进行 OR 运算时，可能会使用 index union merge算法。

例子：

SELECT * FROM t1 WHERE key1=1 OR key2=2 OR key3=3; SELECT * FROM innodb_table WHERE (key1=1 AND key2=2) OR (key3='foo' AND key4='bar') AND key5=5;

第一个例子，就是三个 单字段索引 进行 OR 运算，所以他们可能会使用 index union merge算法。

第二个例子，复杂一点。(key1=1 AND key2=2) 是符合 index intersect merge; (key3='foo' AND key4='bar') AND key5=5 也是符合index intersect merge，所以 二者之间进行 OR 运算，自然可能会使用 index union merge算法。

4. index merge 之 sort_union

This access algorithm is employed when the WHERE clause was converted to several range conditions combined by [OR](http://dev.mysql.com/doc/refman/5.6/en/logical-operators.html#operator_or), but for which the Index Merge method union algorithm is not applicable.(多个条件扫描进行 OR 运算，但是不符合 index union merge算法的，此时可能会使用 sort_union算法)

官方文档给出了两个例子：

SELECT * FROM tbl_name WHERE key_col1 < 10 OR key_col2 < 20; SELECT * FROM tbl_name WHERE (key_col1 > 10 OR key_col2 = 20) AND nonkey_col=30;

但是显然：因为 key_col2 不是复合索引的第一个字段，对它进行 OR 运算，是不可能使用到索引的。所以这两个例子应该也是错误的，它们实际上并不会进行 index sort_union merge算法。

The difference between the sort-union algorithm and the union algorithm is that the sort-union algorithm must first fetch row IDs for all rows and sort them before returning any rows.(sort-union合并算法和union合并算法的不同点，在于返回结果之前是否排序，为什么需要排序呢？可能是因为两个结果集，进行并集运算，需要去重，所以才进行排序？？？)

5. index merge的局限

1）If your query has a complex WHERE clause with deep [AND](http://dev.mysql.com/doc/refman/5.6/en/logical-operators.html#operator_and)/[OR](http://dev.mysql.com/doc/refman/5.6/en/logical-operators.html#operator_or) nesting and MySQL does not choose the optimal plan, try distributing terms using the following identity laws:

(x AND y) OR z = (x OR z) AND (y OR z) (x OR y) AND z = (x AND z) OR (y AND z)

如果我们的条件比较复杂，用到多个 and / or 条件运算，而MySQL没有使用最优的执行计划，那么可以使用上面的两个等式将条件进行转换一下。

2）Index Merge is not applicable to full-text indexes. We plan to extend it to cover these in a future MySQL release.(全文索引没有index merge)

3）Before MySQL 5.6.6, if a range scan is possible on some key, the optimizer will not consider using Index Merge Union or Index Merge Sort-Union algorithms. For example, consider this query:

SELECT * FROM t1 WHERE (goodkey1 < 10 OR goodkey2 < 20) AND badkey < 30;

For this query, two plans are possible:

An Index Merge scan using the (goodkey1 < 10 OR goodkey2 < 20) condition.

A range scan using the badkey < 30 condition.

However, the optimizer considers only the second plan.

这一点对以低版本的MySQL是一个很大的缺陷。就是如果where条件中有 >, <, >=, <=等条件，那么优化器不会使用 index merge，而且还会忽略其他的索引，不会使用它们，哪怕他们的选择性更优。

6. 对 index merge 的进一步优化

index merge使得我们可以使用到多个索引同时进行扫描，然后将结果进行合并。听起来好像是很好的功能，但是如果出现了 index intersect merge，那么一般同时也意味着我们的索引建立得不太合理，因为 index intersect merge 是可以通过建立 复合索引进行更一步优化的。

比如下面的select:

SELECT * FROM t1 WHERE key1=1 AND key2=2 AND key3=3;

显然我们是可以在这三个字段上建立一个复合索引来进行优化的，这样就只需要扫描一个索引一次，而不是对三个所以分别扫描一次。

percona官网有一篇 比较复合索引和index merge 的好文章：[Multi Column indexes vs Index Merge](https://www.percona.com/blog/2009/09/19/multi-column-indexes-vs-index-merge/)

7. 复合索引的最左前缀原则

上面我们说到，对复合索引的非最左前缀字段进行 OR 运算，是无法使用到复合索引的。比如：

SELECT * FROM tbl_name WHERE (key_col1 > 10 OR key_col2 = 20) AND nonkey_col=30;

其原因是，MySQL中的索引，使用的是B+tree, 也就是说他是：先按照复合索引的 第一个字段的大小来排序，插入到 B+tree 中的，当第一个字段值相同时，在按照第二个字段的值比较来插入的。那么如果我们需要对：OR key_col2 = 20 这样的条件也使用复合索引，那么该怎么操作呢？应该要对复合索引进行全扫描，找出所有 key_col2 =20 的项，然后还要回表去判断 nonkey_col=30，显然代价太大了。所以一般而言 OR key_col2 = 20这样的条件是无法使用到复合索引的。如果一定要使用索引，那么可以在 col2 上单独建立一个索引。

复合索引的最左前缀原则：

MySQL中的复合索引，查询时只会使用到最左前缀，比如：

![0](https://note.youdao.com/yws/res/1625/7E234E16F1234AF0A4B0BB3F53C97B1F)

mysql> show index from role_goods; +------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+ | Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | +------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+ | role_goods | 0 | PRIMARY | 1 | id | A | 22816 | NULL | NULL | | BTREE | | | | role_goods | 1 | roleId | 1 | roleId | A | 1521 | NULL | NULL | YES | BTREE | | | | role_goods | 1 | goodsId | 1 | goodsId | A | 1521 | NULL | NULL | YES | BTREE | | | | role_goods | 1 | roleId_2 | 1 | roleId | A | 1901 | NULL | NULL | YES | BTREE | | | | role_goods | 1 | roleId_2 | 2 | status | A | 4563 | NULL | NULL | YES | BTREE | | | | role_goods | 1 | roleId_2 | 3 | number | A | 22816 | NULL | NULL | YES | BTREE | | | +------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+ 6 rows in set (0.00 sec)

![0](https://note.youdao.com/yws/res/1627/045988F07DFC4A3397B94A728148786B)

上面有一个复合索引：roleId_2(roleId,status,number)，如果条件是： where roleId=xxx and number=xxx，那么此时只会使用到最左前缀roleId，而不会使用到 number 来进行过滤。因为它们中间存在一个字段 status 没有出现在where条件中。实验如下所示：

![0](https://note.youdao.com/yws/res/1626/CE94B2D0E1094BFBAA13ABF21C61606A)

mysql> explain select * from role_goods where roleId=100000001 and status=1 and number=1 limit 1; +----+-------------+------------+------+-----------------+----------+---------+-------------------+------+-------+ | id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra | +----+-------------+------------+------+-----------------+----------+---------+-------------------+------+-------+ | 1 | SIMPLE | role_goods | ref | roleId,roleId_2 | roleId_2 | 23 | const,const,const | 13 | NULL | +----+-------------+------------+------+-----------------+----------+---------+-------------------+------+-------+ 1 row in set (0.00 sec) mysql> explain select * from role_goods where roleId=100000001 and status=1 limit 1; +----+-------------+------------+------+-----------------+----------+---------+-------------+------+-------+ | id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra | +----+-------------+------------+------+-----------------+----------+---------+-------------+------+-------+ | 1 | SIMPLE | role_goods | ref | roleId,roleId_2 | roleId_2 | 14 | const,const | 13 | NULL | +----+-------------+------------+------+-----------------+----------+---------+-------------+------+-------+ 1 row in set (0.00 sec) mysql> explain select * from role_goods where roleId=100000001 and number=1 limit 1; +----+-------------+------------+------+-----------------+--------+---------+-------+------+-------------+ | id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra | +----+-------------+------------+------+-----------------+--------+---------+-------+------+-------------+ | 1 | SIMPLE | role_goods | ref | roleId,roleId_2 | roleId | 9 | const | 14 | Using where | +----+-------------+------------+------+-----------------+--------+---------+-------+------+-------------+ 1 row in set (0.01 sec)

mysql> explain select * from role_goods ignore index(roleId) where roleId=100000001 and number=1 limit 1;

+----+-------------+------------+------+---------------+----------+---------+-------+------+-----------------------+

| id | select_type | table      | type | possible_keys | key      | key_len | ref   | rows | Extra                 |

+----+-------------+------------+------+---------------+----------+---------+-------+------+-----------------------+

|  1 | SIMPLE      | role_goods | ref  | roleId_2      | roleId_2 | 9       | const |   14 | Using index condition |

+----+-------------+------------+------+---------------+----------+---------+-------+------+-----------------------+

1 row in set (0.01 sec)

![0](https://note.youdao.com/yws/res/1628/7E44FD65C6064E34AF8982DDD6A13D25)

可以看到 key_len 的变化：

显然最后一个查询仅仅使用到符合索引中的 roleId, 没有使用到 number. number使用在了 index conditon(也就是索引的push down技术)

注意最左前缀，并不是是指：一定要按照各个字段出现在where中的顺序来建立复合索引的。比如

where status=2 and roleId=xxx and number = xxx

该条件建立符合索引，我们并不需要按照status,roleId，number它们出现的顺序来建立索引：

alter table role_goods add index sin(status,roleId,number)

这是对最左前缀极大的误解。因为 where status=2 and roleId=xxx and number = xxx 和 where roleId=xxx and number = xxx and status=2它们是等价的。复合索引，哪个字段放在最前面，需要根据哪个字段经常出现在where条件中，哪个字段的选择性最好来判断的。

来源： [https://www.cnblogs.com/digdeep/archive/2015/11/18/4975977.html](https://www.cnblogs.com/digdeep/archive/2015/11/18/4975977.html)