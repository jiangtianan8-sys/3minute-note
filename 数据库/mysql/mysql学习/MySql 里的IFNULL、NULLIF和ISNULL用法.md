今天用到了 MySql 里的 isnull 才发现他和 MSSQL 里的还是有点区别，现在简单总结一下：

mysql 中 isnull,ifnull,nullif 的用法如下：

isnull(expr) 的用法：

如 expr 为 null，那么 isnull() 的返回值为 1，否则返回值为 0。 

mysql> select isnull(1+1);

-> 0

mysql> select isnull(1/0);

-> 1

使用= 的 null 值对比通常是错误的。 

isnull() 函数同 is null 比较操作符具有一些相同的特性。请参见有关 is null 的说明。

IFNULL(expr1,expr2) 的用法：

假如 expr1   不为   NULL，则   IFNULL()   的返回值为   expr1; 

否则其返回值为   expr2。IFNULL() 的返回值是数字或是字符串，具体情况取决于其所使用的语境。

mysql>   SELECT   IFNULL(1,0);   

                  ->   1   

mysql>   SELECT   IFNULL(NULL,10);   

   ->   10   

 mysql>   SELECT   IFNULL(1/0,10);   

           ->   10   

mysql>   SELECT   

IFNULL(1/0,'yes');   

            ->   'yes'   

IFNULL(expr1,expr2) 的默认结果值为两个表达式中更加“通用”的一个，顺序为 STRING、   REAL 或   

INTEGER。假设一个基于表达式的表的情况，     或 MySQL 必须在内存储器中储存一个临时表中 IFNULL() 的返回值：   

CREATE   TABLE   tmp   SELECT   IFNULL(1,'test')   AS   test；   

在这个例子中，测试列的类型为   CHAR(4)。      

NULLIF(expr1,expr2)  的用法：  

如果 expr1 

=   expr2     成立，那么返回值为 NULL，否则返回值为   expr1。这和 CASE   WHEN   expr1   =   expr2   

THEN   NULL   ELSE   expr1   END 相同。     

mysql>   SELECT   

NULLIF(1,1);   

           ->   NULL   

mysql>   SELECT   NULLIF(1,2);   

            ->   1  

如果参数不相等，则   MySQL   两次求得的值为     expr1   。
