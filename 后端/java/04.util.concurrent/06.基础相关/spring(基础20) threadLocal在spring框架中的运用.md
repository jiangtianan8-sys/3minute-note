一、ThreadLocal是什么 

早在JDK 1.2的版本中就提供java.lang.ThreadLocal，ThreadLocal为解决多线程程序的并发问题提供了一种新的思路。使用这个工具类可以很简洁地编写出优美的多线程程序。 

ThreadLocal，顾名思义，它不是一个线程，而是线程的一个本地化对象。当工作于多线程中的对象使用ThreadLocal维护变量时，

ThreadLocal为每个使用该变量的线程分配一个独立的变量副本。所以每一个线程都可以独立地改变自己的副本，而不会影响其他线程所对应的副本。

从线程的角度看，这个变量就像是线程的本地变量，这也是类名中“Local”所要表达的意思。 

线程局部变量并不是Java的新发明，很多语言（如IBM XL、FORTRAN）在语法层面就提供线程局部变量。在Java中没有提供语言级支持，而以一种变通的方法，通过ThreadLocal的类提供支持。所以，在Java中编写线程局部变量的代码相对来说要笨拙一些，这也是为什么线程局部变量没有在Java开发者中得到很好普及的原因。

二、ThreadLocal的接口方法 

ThreadLocal类接口很简单，只有4个方法，我们先来了解一下。 

void set(Object value)

   设置当前线程的线程局部变量的值；

public Object get()

   该方法返回当前线程所对应的线程局部变量；

public void remove()

   将当前线程局部变量的值删除，目的是为了减少内存的占用，该方法是JDK 5.0新增的方法。需要指出的是，当线程结束后，对应该线程的局部变量将自动被垃圾回收，

所以显式调用该方法清除线程的局部变量并不是必须的操作，但它可以加快内存回收的速度；

protected Object initialValue()

   返回该线程局部变量的初始值，该方法是一个protected的方法，显然是为了让子类覆盖而设计的。这个方法是一个延迟调用方法，在线程第1次调用get()或set(Object)时才执行，并且仅执行1次。ThreadLocal中的默认实现直接返回一个null。 

值得一提的是，在JDK5.0中，ThreadLocal已经支持泛型，该类的类名已经变为ThreadLocal。

API方法也相应进行了调整，新版本的API方法分别是void set(T value)、T get()以及T initialValue()。 

ThreadLocal是如何做到为每一个线程维护变量的副本的呢？

其实实现的思路很简单：在ThreadLocal类中有一个Map，用于存储每一个线程的变量副本，Map中元素的键为线程对象，而值对应线程的变量副本。

我们自己就可以提供一个简单的实现版本： 

1. public class SimpleThreadLocal {
2. private Map valueMap = Collections.synchronizedMap(new HashMap());
3. public void set(Object newValue) {
4. //①键为线程对象，值为本线程的变量副本
5. valueMap.put(Thread.currentThread(), newValue);
6. }
7. public Object get() {
8. Thread currentThread = Thread.currentThread();
9. //②返回本线程对应的变量
10. Object o = valueMap.get(currentThread);
11. //③如果在Map中不存在，放到Map中保存起来
12. if (o == null && !valueMap.containsKey(currentThread)) {
13. o = initialValue();
14. valueMap.put(currentThread, o);
15. }
16. return o;
17. }
18. public void remove() {
19. valueMap.remove(Thread.currentThread());
20. }
21. public Object initialValue() {
22. return null;
23. }
24. }

虽然代码清单9 3中这个ThreadLocal实现版本显得比较幼稚，但它和JDK所提供的ThreadLocal类在实现思路上是非常相近的。

三、TheadLocal实例 

1. package com.baobaotao.basic;

2. public class SequenceNumber {

3. //①通过匿名内部类覆盖ThreadLocal的initialValue()方法，指定初始值
4. private static ThreadLocal seqNum = new ThreadLocal(){
5. public Integer initialValue(){
6. return 0;
7. }
8. };

9. //②获取下一个序列值
10. public int getNextNum(){
11. seqNum.set(seqNum.get()+1);
12. return seqNum.get();
13. }

14. public static void main(String[ ] args)
15. {
16. SequenceNumber sn = new SequenceNumber();

17. //③ 3个线程共享sn，各自产生序列号
18. TestClient t1 = new TestClient(sn);
19. TestClient t2 = new TestClient(sn);
20. TestClient t3 = new TestClient(sn);
21. t1.start();
22. t2.start();
23. t3.start();
24. }
25. private static class TestClient extends Thread
26. {
27. private SequenceNumber sn;
28. public TestClient(SequenceNumber sn) {
29. this.sn = sn;
30. }
31. public void run()
32. {
33. //④每个线程打出3个序列值
34. for (int i = 0; i < 3; i++) {
35. System.out.println("thread["+Thread.currentThread().getName()+
36. "] sn["+sn.getNextNum()+"]");
37. }
38. }
39. }
40. }

通常我们通过匿名内部类的方式定义ThreadLocal的子类，提供初始的变量值，如①处所示。TestClient线程产生一组序列号，在③处，我们生成3个TestClient，它们共享同一个SequenceNumber实例。运行以上代码，在控制台上输出以下的结果： 

1. thread[Thread-2] sn[1]
2. thread[Thread-0] sn[1]
3. thread[Thread-1] sn[1]
4. thread[Thread-2] sn[2]
5. thread[Thread-0] sn[2]
6. thread[Thread-1] sn[2]
7. thread[Thread-2] sn[3]
8. thread[Thread-0] sn[3]
9. thread[Thread-1] sn[3]

考查输出的结果信息，我们发现每个线程所产生的序号虽然都共享同一个Sequence Number实例，但它们并没有发生相互干扰的情况，而是各自产生独立的序列号，这是因为我们通过ThreadLocal为每一个线程提供了单独的副本。

四、与Thread同步机制的比较 

ThreadLocal和线程同步机制相比有什么优势呢？ThreadLocal和线程同步机制都是为了解决多线程中相同变量的访问冲突问题。

在同步机制中，通过对象的锁机制保证同一时间只有一个线程访问变量。这时该变量是多个线程共享的，使用同步机制要求程序缜密地分析什么时候对变量进行读写，什么时候需要锁定某个对象，什么时候释放对象锁等繁杂的问题，程序设计和编写难度相对较大。 

而ThreadLocal则从另一个角度来解决多线程的并发访问。ThreadLocal为每一个线程提供一个独立的变量副本，从而隔离了多个线程对访问数据的冲突。因为每一个线程都拥有自己的变量副本，从而也就没有必要对该变量进行同步了。ThreadLocal提供了线程安全的对象封装，在编写多线程代码时，可以把不安全的变量封装进ThreadLocal。 

由于ThreadLocal中可以持有任何类型的对象，低版本JDK所提供的get()返回的是Object对象，需要强制类型转换。但JDK 5.0通过泛型很好的解决了这个问题，在一定程度上简化ThreadLocal的使用，代码清单9-2就使用了JDK 5.0新的ThreadLocal版本。 

概括起来说，对于多线程资源共享的问题，同步机制采用了“以时间换空间”的方式：访问串行化，对象共享化。而ThreadLocal采用了“以空间换时间”的方式：访问并行化，对象独享化。前者仅提供一份变量，让不同的线程排队访问，而后者为每一个线程都提供了一份变量，因此可以同时访问而互不影响。 

五、Spring使用ThreadLocal解决线程安全问题 

我们知道在一般情况下，只有无状态的Bean才可以在多线程环境下共享，在Spring中，绝大部分Bean都可以声明为singleton作用域。就是因为Spring对一些Bean（如RequestContextHolder、TransactionSynchronizationManager、LocaleContextHolder等）中非线程安全的“状态性对象”采用ThreadLocal进行封装，让它们也成为线程安全的“状态性对象”，因此有状态的Bean就能够以singleton的方式在多线程中正常工作了。 

一般的Web应用划分为展现层、服务层和持久层三个层次，在不同的层中编写对应的逻辑，下层通过接口向上层开放功能调用。在一般情况下，从接收请求到返回响应所经过的所有程序调用都同属于一个线程，如图9-2所示。 

![0](C:\Users\hp\Documents\My%20Knowledge\temp\463a0a73-c793-4063-8ce5-7e65a56b69af\128\index_files\0.9612313276367257.png)

这样用户就可以根据需要，将一些非线程安全的变量以ThreadLocal存放，在同一次请求响应的调用线程中，所有对象所访问的同一ThreadLocal变量都是当前线程所绑定的。 

下面的实例能够体现Spring对有状态Bean的改造思路：

1. public class TopicDao {
2. //①一个非线程安全的变量
3. private Connection conn;
4. public void addTopic(){
5. //②引用非线程安全变量
6. Statement stat = conn.createStatement();
7. …
8. }
9. }

由于①处的conn是成员变量，因为addTopic()方法是非线程安全的，必须在使用时创建一个新TopicDao实例（非singleton）。下面使用ThreadLocal对conn这个非线程安全的“状态”进行改造：

1. import java.sql.Connection;
2. import java.sql.Statement;
3. public class TopicDao {

4. //①使用ThreadLocal保存Connection变量
5. private static ThreadLocal connThreadLocal = new ThreadLocal();
6. public static Connection getConnection(){

7. //②如果connThreadLocal没有本线程对应的Connection创建一个新的Connection，
8. //并将其保存到线程本地变量中。
9. if (connThreadLocal.get() == null) {
10. Connection conn = ConnectionManager.getConnection();
11. connThreadLocal.set(conn);
12. return conn;
13. }else{
14. //③直接返回线程本地变量
15. return connThreadLocal.get();
16. }
17. }
18. public void addTopic() {

19. //④从ThreadLocal中获取线程对应的
20. Statement stat = getConnection().createStatement();
21. }
22. }

不同的线程在使用TopicDao时，先判断connThreadLocal.get()是否为null，如果为null，则说明当前线程还没有对应的Connection对象，这时创建一个Connection对象并添加到本地线程变量中；如果不为null，则说明当前的线程已经拥有了Connection对象，直接使用就可以了。这样，就保证了不同的线程使用线程相关的Connection，而不会使用其他线程的Connection。因此，这个TopicDao就可以做到singleton共享了。 

当然，这个例子本身很粗糙，将Connection的ThreadLocal直接放在Dao只能做到本Dao的多个方法共享Connection时不发生线程安全问题，但无法和其他Dao共用同一个Connection，要做到同一事务多Dao共享同一个Connection，必须在一个共同的外部类使用ThreadLocal保存Connection。但这个实例基本上说明了Spring对有状态类线程安全化的解决思路。在本章后面的内容中，我们将详细说明Spring如何通过ThreadLocal解决事务管理的问题。

--------------------- 本文来自 小米加大炮 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/zengdeqing2012/article/details/77098994?utm_source=copy