本帖子是行转列的一个逆向操作——列转行，看下面一个面试题  

面试题2： 柠檬班第30期学生要毕业了，他们的Linux、MySQL、Java成绩数据表 tb_lemon_grade_column中， 表中字段student_name，Linux，MySQL，Java分别表示学生姓名、Linux成绩、MySQL成绩、Java成绩， 数据图1所示。请写出一条SQL，将图1的数据变成图2的形式（列转行）

![](assets/【数据库】SQL经典面试题%20-%20行列转换二%20-%20列转行/file-20251124195831561.png)

请点击此处输入图片描述

下图示：

1：使用上节课学的知识，获得以列的形式展示的成绩数据（行转列）

SELECT student_name,SUM(CASE COURSE when 'Linux' THEN SCORE ELSE 0 END) as

'Linux',SUM(CASE COURSE when 'MySQL' THEN SCORE ELSE 0 END) as 'MySQL',SUM(CASE

COURSE when 'Java' THEN SCORE ELSE 0 END) as 'Java'FROM tb_lemon_grade

结果如下：

![](assets/【数据库】SQL经典面试题%20-%20行列转换二%20-%20列转行/file-20251124195841977.png)

请点击此处输入图片描述

2：使用导出功能，将数据导入到Excel

![](assets/【数据库】SQL经典面试题%20-%20行列转换二%20-%20列转行/file-20251124195850094.png)

请点击此处输入图片描述

点击下一步，选择保存位置，输入保存的文件名

![](assets/【数据库】SQL经典面试题%20-%20行列转换二%20-%20列转行/file-20251124195858561.png)

请点击此处输入图片描述

点击下一步，点击开始，讲数据导入到本地

3：使用导入功能，将导出的Excel表导入到数据库

选择表，点击右键选择导入向导

![](assets/【数据库】SQL经典面试题%20-%20行列转换二%20-%20列转行/file-20251124195907731.png)

请点击此处输入图片描述

选择Excel文件，点击下一步，选择刚才保存的Excel文件，输入要保存的表，进行导入

![](assets/【数据库】SQL经典面试题%20-%20行列转换二%20-%20列转行/file-20251124195915465.png)

请点击此处输入图片描述

4：导入完成，就生成了一个表，查看下数据

![](assets/【数据库】SQL经典面试题%20-%20行列转换二%20-%20列转行/file-20251124195924179.png)

请点击此处输入图片描述

5：上面是使用导入本地文件的方式新建了一个表，并且把文件的数据也导入进来了，

如果是数据本身已经存在数据库中，我们还有更简单的方法，使用的是创建表的CREATE TABLE语法，可以新建表，并且把结果集的数据也会初始化到新建表中，如下所示：

CREATE TABLE new_tables(SELECT student_name,MAX(IF(COURSE = 'Linux',SCORE,0)) 'Linux',MAX(IF(COURSE = 'MySQL',SCORE,0)) 'MySQL',MAX(IF(COURSE = 'Java',SCORE,0)) 'Java'FROM tb_lemon_grade

6：怎么列传行呢？使用UNION ALL，然后行转列

SELECT student_name,'linux' course,linux score FROM tb_lemon_student2

7：我们想排下序怎么办呢？ 采用子查询的方式（注意子查询中的别名a，一定要写上别名）

SELECT student_name,'linux' course,linux score from tb_lemon_student2

结果如下：

![](//upload-images.jianshu.io/upload_images/7391770-ebdbd93134c87218?imageMogr2/auto-orient/strip|imageView2/2/w/640/format/webp)

请点击此处输入图片描述

今天就分享到这里了。如果大家觉得还不错，就点个赞吧！！！！

  
  
作者：柠檬班软件测试  
链接：https://www.jianshu.com/p/ed587c76872f  
来源：简书  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。