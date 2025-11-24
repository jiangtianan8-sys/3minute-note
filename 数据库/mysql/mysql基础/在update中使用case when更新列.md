当我们需要将下面的列的值更新成汉语拼音时，那需要在 update 中使用 case when 函数：

1 

2 优化型

3 强化收益型

4 债券型

5 货币型

6 收益型

7 指数优化型

用法如下：

update test set fjjtzlx = 

(case fjjtzlx 

when ' 优化型 ' then 'YHX'

when ' 强化收益型 ' then 'QHSYX'

when ' 债券型 ' then 'ZQX'

when ' 货币型 ' then 'HBX'

when ' 收益型 ' then 'SYX'

when ' 指数优化型 ' then 'ZSYHX'

when ' 增强型 ' then 'ZQX'

else fjjtzlx end )

这样的用法只是局限于要更新的列值不是很多，不然就很麻烦了。但这个用法正好解决了我的需求，呵呵，还是挺简单的！
