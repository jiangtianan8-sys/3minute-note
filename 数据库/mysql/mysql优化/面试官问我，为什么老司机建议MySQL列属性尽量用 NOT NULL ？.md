其实写这篇文章，也是来自一个知识星球读者的提问，他在二面的过程中被问到了，由于他简历中写道有 MySQL 调优经验，但这个问题没有回答好，二面被刷了。

其实我们刚学习 C 语言的时候，就接触过 NULL，比如下面这句代码。

int *p = NULL;

它实际上表示将指针指向一块不被使用的内存地址，一般会在宏中定义好。

那么我们常用的 Java 语言，同样也用到 null，表示一个空引用，如果你不小心引用了，那么就会抛出 NullPointerException，就像昨天 Reddit 上面很火的一张图。

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163725405.png)

关于空指针异常，我之前写过一篇文章来介绍怎么防御《[java.lang.NullPointerException](http://mp.weixin.qq.com/s?__biz=MzIzMzgxOTQ5NA==&mid=2247484982&idx=1&sn=39fe1032d17ed9f688f40e1d3fb8213f&chksm=e8fe9a3fdf891329775372afc97e45ce7ac65e2f4f1721c712613da5df541bda176086b2002d&scene=21#wechat_redirect)》。但是这篇文章没有写全，今天在这里补充一下。

其实很早之前 guava 就提供了 Optional 容器类来处理 null，其目的便是避免猝不及防的空指针。后来 java8 直接引入了 Optional，功能一样，用法上稍稍有点变化。其实还有很多开源框架，比如 Spring，common lang3等，也提供了处理空的工具类，如。

StringUtils.isBlank();   

CollectionUtils.isEmpty();

那么在 MySQL 中，NULL 表示不知道的数据。

我们在设计表的时候，经常会有老司机这么告诉我们。

字段尽可能用NOT NULL，而不是NULL，除非特殊情况。

这句话到底有没有错？

可以负责任的告诉你这句话没有错，也不是以讹传讹。

这句话首次出现在 MySQL 官网。

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163745409.png)

如果你读过《高性能 MySQL》这本书，你应该会看到这么一段，在 4.1 节提到。

广告

高性能MySQL（第3版）

作者：(美)施瓦茨,(美)扎伊采夫,(美)特卡琴科

当当

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163806188.png)

由此看来，把 NULL 改成 NOT NULL 对索引的性能并没有明显的提升。避免使用 NULL 的目的，是便于代码的可读性和可维护性。同时也便于避免下文即将出现的一些稀奇古怪的错误。

好了，下面咱们通过实验来看看，使用 NULL 会出现那些稀奇古怪的错误呢？

跟我一样在本地建两个表 t1，t2；其中一个表 name 字段允许为空，另一个表 name 字段不允许为空，分别对 name 字段建立索引，SQL 语句如下。

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163819742.png)

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163829189.png)

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163838307.png)

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163846787.png)

1、NOT IN、!= 等负向条件查询在有 NULL 值的情况下返回非空行的结果集。

比如上例中的 t2，我执行如下 SQL 语句。

SELECT * from t2 where name != '张三'

你本打算返回 id 为 2 的那行数据，然而什么都没有。

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163901870.png)

又比如这条 SQL 语句。

select * from t2 where name not in (select name from t2 where id!=1)

也返回了空结果集。

2、使用 concat 函数拼接时，首先要对各个字段进行非 NULL 判断，否则只要任何一个字段为空都会造成拼接的结果为 NULL。

比如下面这条 SQL 语句。

SELECT CONCAT("1",NULL)

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163917723.png)

3、当用count函数进行统计时，NULL 列不会计入统计。

SELECT count(name) from t2

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163929188.png)

4、查询空行数据，用 is NULL。

SELECT * FROM t2 where name is NULL

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163938754.png)

5、NULL 列需要更多的存储空间，一般需要一个额外的字节作为判断是否为 NULL 的标志位。

如果你仔细观察 t1 和 t2 表的 key_len，会发现 t2 比 t1 多了一个字节。

explain SELECT * from t2 where name = '张三'

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124163951487.png)

explain SELECT * from t1 where name = '张三'

![](assets/面试官问我，为什么老司机建议MySQL列属性尽量用%20NOT%20NULL%20？/file-20251124164001137.png)

key_len 的长度一般跟这三个因素有关，分别是数据类型，字符编码，是否为 NULL。

因此，t2 比 t1 多出的这一个字节，用于作为判断是否为 NULL 的标志位了。

马蛋，原来一切都在书中。如果面试的哪位同学多读几篇《高性能 MySQL》这本书，那个岗位就是他的了，但没有那么多如果。。。

在此，建议大家多看官方文档，多读点好书，多关注一些良心的原创技术自媒体，不要看那些无凭无据的文章，反而会以讹传讹，贻害无穷。

如果这篇文章对你有帮助，麻烦分享到你的朋友圈，来帮助更多的朋友。

参考

https://dev.mysql.com/doc/refman/5.7/en/dynamic-format.html

https://dev.mysql.com/doc/refman/5.5/en/problems-with-null.html

https://dev.mysql.com/doc/refman/5.5/en/multiple-column-indexes.html

https://dev.mysql.com/doc/internals/en/myisam-introduction.html

https://dev.mysql.com/doc/internals/en/innodb-field-contents.html