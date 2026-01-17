经历了几天的研究，终于是明白了ThreadLocal在Spring事务管理过程中发挥的用途。下面就以图文的形式和大家分享，如有错误，欢迎指正。

大家都知道，Spring允许以声明的方式进行事务管理。通过声明的方式，程序员可以仅仅专注于业务代码，事务管理由Spring框架代为进行。

以JDBC为例，正常的事务代码可能如下：

1. dbc = new DataBaseConnection();//第1行
2. Connection con = dbc.getConnection();//第2行
3. con.setAutoCommit(false);// //第3行
4. con.executeUpdate(...);//第4行
5. con.executeUpdate(...);//第5行
6. con.executeUpdate(...);//第6行
7. con.commit();////第7行

上述代码，可以分成三个部分:

事务准备阶段：第1～3行

业务处理阶段：第4～6行

事务提交阶段：第7行 

在Spring框架中，程序员专注于设计业务处理阶段，事务准备阶段和事务提交阶段由Spring来完成。在实际开发过程中，我们仅仅编写了业务处理阶段，事务准备阶段和事务提交阶段会由Spring框架根据我们的事务相关配置文件动态生成--利用AOP。关于AOP，这里就不说了，网上有很多资料。

但是大家需要注意一个问题，在利用AOP动态生成的代码中，如何才能让三个阶段使用同一个数据源连接呢？这是很重要的。如果三个阶段使用不同的数据源连接，自然是错误的。

现在需要办到的是 让软件结构中纵向的三个阶段 使用同样的一个参数，而这三个阶段之间不可以进行参数传递。解决方案是---线程绑定。

Web容器中，每个完整的请求周期会由一个线程来处理。因此，如果我们能将一些参数绑定到线程的话，就可以实现在软件架构中跨层次的参数共享（是隐式的共享）。这是一件很牛逼的事情，在框架中被经常使用。而JAVA中恰好提供了绑定的方法--使用ThreadLocal。

ThreadLocal是一种线程本地变量，使用ThreadLocal的形式声明一个变量，该变量就会在每个线程中创建一个变量的副本。

1. public class Demo {
2. public static ThreadLocal threadLocalString = new ThreadLocal(){
3. protected String initialValue() {
4. return "";
5. }
6. };
7. public static ThreadLocal threadLocalLong =new ThreadLocal(){
8. protected Long initialValue() {
9. return 0L;
10. }
11. };
12. public static void main(String [] args){
13. threadLocalLong.set(100L);
14. threadLocalString.set("test");

15. new Thread(new Runnable() {
16. @Override
17. public void run() {
18. threadLocalString.set("thread");
19. System.out.println(threadLocalLong.get());
20. System.out.println(threadLocalString.get());
21. }
22. }).start();

23. System.out.println(threadLocalLong.get());
24. System.out.println(threadLocalString.get());
25. }
26. }

从上面的代码可看出，在不同的线程中调用同一个类对象的get()方法，输出依据线程的不同而不同。

再来看一个关于ThreadLocal的例子：

1. import java.util.HashMap;
2. import java.util.Map;

3. public class Demo {
4. public static void main(String [] args){
5. ResourceHolder.putResource("conn",new Conn("connection1"));
6. new Thread(new Runnable() {
7. @Override
8. public void run() {
9. // 该线程不会得到主线程绑定的变量
10. System.out.println(ResourceHolder.getResource("conn"));
11. }
12. }).start();

13. System.out.println(ResourceHolder.getResource("conn"));
14. new Demo().function1();
15. new Demo().function2();
16. System.out.println(ResourceHolder.getResource("conn"));
17. }
18. public void function1(){
19. System.out.println(ResourceHolder.getResource("conn"));
20. }
21. public void function2(){
22. System.out.println(ResourceHolder.getResource("conn"));
23. }
24. }

25. class ResourceHolder{

26. public static ThreadLocal> threadLocalMap=new ThreadLocal>();
27. public static void putResource(Object key,Object value){
28. if(threadLocalMap.get()==null)
29. threadLocalMap.set(new HashMap());
30. threadLocalMap.get().put(key, value);
31. }
32. public static Object getResource(Object key){
33. if(threadLocalMap.get()==null)
34. threadLocalMap.set(new HashMap());
35. return threadLocalMap.get().get(key);
36. }
37. public static void clearResource(Object key,Object value){
38. if(threadLocalMap.get()!=null)
39. threadLocalMap.remove();
40. }
41. }
42. class Conn{
43. private String name;

44. public Conn(String name) {
45. super();
46. this.name = name;
47. }

48. public String getName() {
49. return name;
50. }

51. public void setName(String name) {
52. this.name = name;
53. }
54. @Override
55. public String toString() {
56. return "Conn [name=" + name + "]";
57. }
58. }

现在我们可以考虑使用ThreadLocal来将 事务准备阶段使用的连接 绑定到当前线程 以便在之后的 业务处理阶段 和 事务提交阶段使用了。不过问题来了，这个ThreadLocal放在哪里呢？一种方案是写到DataSource中，但DataSource是策略模式动态配置的，况且都是第三方的，不那么容易改。

我们再一次想到AOP,为DataSource创建一个代理类，每次调用DataSource的getConn方法的时候，都由拦截器拦截并转换为对DataSource代理类的调用，在代理类中加一些猫腻；

看代码： （代理类）

1. package com.xyz.transaction;
2. import java.lang.reflect.InvocationHandler;
3. import java.lang.reflect.Method;
4. import java.lang.reflect.Proxy;

5. public class DataSourceHandler implements InvocationHandler {

6. private Object originalDataDource;
7. public Object bind(Object obj) {
8. this.originalDataDource=obj;
9. return Proxy.newProxyInstance(this.originalDataDource.getClass().getClassLoader(),
10. originalDataDource.getClass().getInterfaces(), this);
11. }
12. @Override
13. public Object invoke(Object proxy, Method method, Object[] args)
14. throws Throwable {
15. // TODO Auto-generated method stub
16. if("getConn".equals(method.getName())){//默认数据源的获取连接方法为getConn()
17. if(ResourceHolder.getResource(proxy)==null){
18. Object obj=method.invoke(originalDataDource, args);
19. ResourceHolder.addResource(proxy, obj);
20. }
21. return ResourceHolder.getResource(proxy);
22. }else{
23. return method.invoke(originalDataDource, args);
24. }
25. }

26. }

27. package com.xyz.transaction;

28. import java.util.HashMap;
29. import java.util.Map;

30. public class ResourceHolder {
31. private static ThreadLocal> threadLocalMap=new ThreadLocal>();
32. public static void addResource(Object key,Object value){
33. if(threadLocalMap.get()==null)
34. threadLocalMap.set(new HashMap());
35. threadLocalMap.get().put(key, value);
36. }
37. public static Object getResource(Object key){
38. if(threadLocalMap.get()==null)
39. threadLocalMap.set(new HashMap());
40. return threadLocalMap.get().get(key);
41. }
42. public static void clear(){
43. threadLocalMap.remove();
44. }
45. }

来看以上代码，每次访问getConn方法的时候，都查看是否在当前线程绑定的Map中有对应的连接，如果有直接返回。如果没有，再向真实的getConn请求获得一个连接并放到当前线程绑定的Map中。

流程如图所示，图片代码见附件。

笔者开设了一个讲述学习java路线的知乎live，欢迎收听[https://www.zhihu.com/lives/932192204248682496](https://www.zhihu.com/lives/932192204248682496)

提供给想深入学习和提高JAVA并发编程能力的同学，欢迎收听[https://www.zhihu.com/lives/1018219399903387648](https://www.zhihu.com/lives/1018219399903387648)

--------------------- 本文来自 E-臻 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/yizhenn/article/details/52384520?utm_source=copy