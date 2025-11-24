假设 index（a,b,c)

|   |   |
|---|---|
|where 语句|索引是否使用|
|where a=3|Y，使用到 a|
|where a=3 and b=5|Y，使用到 a,b|
|where a=3 and b=5 and c=4|Y，使用到 a,b,c|
|where b=3 或者 where b=3 and c=4 或者 where c=4|N|
|where a=3 and c=5|Y，使用到了 a，但是 c 不可以，b 中间断了|
|where a=3 and b >4 and c=5|Y,使用到了 a 和 b，c 不能用在范围之后，b 断了|
|where a=3 and b like 'kk%' and c=4|Y，使用到 a,b,c|
|where a=3 and b like '%kk' and c=4|Y, 只用到 a|
|where a=3 and b like '%kk%' and c=4|Y, 只用到 a|
|where a=3 and b like 'k%kk%' and c=4|Y，使用到 a,b,c|

【优化总结口诀】

全值匹配我最爱，最左前缀要遵守。

带头大哥不能死，中间兄弟不能断。

索引列上少计算，范围之后全失效。

LIKE 百分写最右，覆盖索引不写星。

不等空值还有 or，索引失效要少用。
