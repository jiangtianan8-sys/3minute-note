今天在使用SSM框架(spring/springmvc/mybatis)进行开发时，自己也是第一次使用，所以遇到的问题也比较多啊·········

我今天是在一条线程里面使用注解时，发现一直报空指针异常，仔细看了一下发现使用注解时并没有注入值，所以才一直空指针异常·····

再仔细对比一下之前我自学时的代码，发现调用流程也没有错，搞了半天也没找出什么原因······

最后想了一下，我是启动服务器的时候，就启动这条线程监听端口了，关键就在这，我这个是线程，不是我之前熟悉的action！！！

最后才知道线程里面是不能直接注入bean的，好了，不说了，直接上代码

第一步：写好获取bean的工具类

import java.util.Locale;

​

import org.springframework.beans.BeansException;

import org.springframework.context.ApplicationContext;

import org.springframework.context.ApplicationContextAware;

​

/**

* 项目名称:

* 类名: SpringContextUtil

* 描述： 获取bean的工具类，可用于在线程里面获取bean

* 创建人: awsm

* 创建时间: Dec 17, 2015 10:46:44 PM

* 修改人：awsm

* 修改时间：Dec 17, 2015 10:46:44 PM

* 修改备注：

* 版本：1.0

*/

public class SpringContextUtil implements ApplicationContextAware {

​

   private static ApplicationContext context = null;

​

   /* (non Javadoc)

    * @Title: setApplicationContext

    * @Description: spring获取bean工具类

    * @param applicationContext

    * @throws BeansException

    * @see org.springframework.context.ApplicationContextAware#setApplicationContext(org.springframework.context.ApplicationContext)

    */

   @Override

   public void setApplicationContext(ApplicationContext applicationContext)

           throws BeansException {

       this.context = applicationContext;

  }

​

   public static T getBean(String beanName){

       return (T) context.getBean(beanName);

  }

​

   public static String getMessage(String key){

       return context.getMessage(key, null, Locale.getDefault());

  }

​

}

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

第二步：在spring的配置文件里面注册这个工具类，我的是在spring-mybatis.xml，即spring和mybatis的整合配置文件中。

1

2

第三步：在线程里面获取bean

/*

        * 在线程中是不能直接从容器中获取bean的，

        * 需要另写一个工具类来获取

        * */

       KeepAliveService keepAliveService = SpringContextUtil.getBean("keepAliveService");

1

2

3

4

5

第三步就是写在线程里面的，是不是可以获取到bean啦····

代码是参考前辈的大牛的，感谢大牛的付出！！！

--------------------- 本文来自 Awsmsniper 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/u010107350/article/details/50347925?utm_source=copy