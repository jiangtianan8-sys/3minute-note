**初识 CopyOnWriteArrayList**

第一次见到 CopyOnWriteArrayList，是在研究 JDBC 的时候，每一个数据库的 Driver 都是维护在一个 CopyOnWriteArrayList 中的，为了证明这一点，贴两段代码，第一段在 com.mysql.jdbc.Driver 下，也就是我们写 Class.forName(“…”) 中的内容：

> public class Driver extends NonRegisteringDriver
>
>   implements java.sql.Driver
>
> {
>
>   public Driver()
>
>     throws SQLException
>
>   {
>
>   }
>
>   static
>
>   {
>
>     try
>
>     {
>
>       DriverManager.registerDriver(new Driver());
>
>     } catch (SQLException E) {
>
>       throw new RuntimeException("Can't register driver!");
>
>     }
>
>   }
>
> }

看到 com.mysql.jdbc.Driver 调用了 DriverManager 的 registerDriver 方法，这个类在 java.sql.DriverManager 下：

> public class DriverManager
>
> {
>
>     private static final CopyOnWriteArrayList<DriverInfo> 
>
>     registeredDrivers = new CopyOnWriteArrayList();
>
>     private static volatile int loginTimeout = 0;
>
>     private static volatile PrintWriter logWriter = null;
>
>     private static volatile PrintStream logStream = null;
>
>     private static final Object logSync = new Object();
>
>     static final SQLPermission SET_LOG_PERMISSION = new
>
>     SQLPermission("setLog");
>
>     …
>
> }

看到所有的 DriverInfo 都在 CopyOnWriteArrayList 中。既然看到了 CopyOnWriteArrayList，我自然免不了要研究一番为什么 JDK 使用的是这个 List。

首先提两点：

1、CopyOnWriteArrayList 位于 java.util.concurrent 包下，可想而知，这个类是为并发而设计的

2、CopyOnWriteArrayList，顾名思义，Write 的时候总是要 Copy，也就是说对于 CopyOnWriteArrayList，任何可变的操作（add、set、remove 等等）都是伴随复制这个动作的，后面会解读 CopyOnWriteArrayList 的底层实现机制

**四个关注点在 CopyOnWriteArrayList 上的答案**

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qia4ia3iaVeC6ZkTyXmqOKU9Byibp8qULDibuD25pESOM8KQeliasLL3rE2Diag/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0 "QQ20170610-235522@2x")

**如何向 CopyOnWriteArrayList 中添加元素**

对于 CopyOnWriteArrayList 来说，增加、删除、修改、插入的原理都是一样的，所以用增加元素来分析一下 CopyOnWriteArrayList 的底层实现机制就可以了。先看一段代码：

> public static void main(String[] args)
>
> {
>
>      List<Integer> list = new CopyOnWriteArrayList<Integer>();
>
>      list.add(1);
>
>      list.add(2);
>
> }

看一下这段代码做了什么，先是第 3 行的实例化一个新的 CopyOnWriteArrayList：

> public class CopyOnWriteArrayList<E>
>
>     implements List<E>, RandomAccess, Cloneable, java.io.Serializable {
>
>     private static final long serialVersionUID = 8673264195747942595L;
>
>     /** The lock protecting all mutators */
>
>     transient final ReentrantLock lock = new ReentrantLock();
>
>     /** The array, accessed only via getArray/setArray. */
>
>     private volatile transient Object[] array;
>
>     …
>
> }

> public CopyOnWriteArrayList() {
>
>     setArray(new Object[0]);
>
> }

> final void setArray(Object[] a) {
>
>     array = a;
>
> }

看到，对于 CopyOnWriteArrayList 来说，底层就是一个 Object[] array，然后实例化一个 CopyOnWriteArrayList，用图来表示非常简单：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qias3s8PQl4fj33oo43IotJvqG1IEPcxgmHJVVf9DOy6He2em5bNdT14w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

就是这样，Object array 指向一个数组大小为 0 的数组。接着看一下，第 4 行的 add 一个整数 1 做了什么，add 的源代码是：

> public boolean add(E e) {
>
> final ReentrantLock lock = this.lock;
>
> lock.lock();
>
> try {
>
>     Object[] elements = getArray();
>
>     int len = elements.length;
>
>     Object[] newElements = Arrays.copyOf(elements, len + 1);
>
>     newElements[len] = e;
>
>     setArray(newElements);
>
>     return true;
>
> } finally {
>
>     lock.unlock();
>
> }
>
> }

画一张图表示一下：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qiaKPjMaugUayT1XcW6VI7zp3YPmWrW1RMwUKjibv2z0Wzn0sklNdorQYQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2 "801753-20151206205856722-1595736205")

每一步都清楚地表示在图上了，一次 add 大致经历了几个步骤：

1、加锁

2、拿到原数组，得到新数组的大小（原数组大小 +1），实例化出一个新的数组来

3、把原数组的元素复制到新数组中去

4、新数组最后一个位置设置为待添加的元素（因为新数组的大小是按照原数组大小 +1 来的）

5、把 Object array 引用指向新数组

6、解锁

整个过程看起来比较像 ArrayList 的扩容。有了这个基础，我们再来看一下第 5 行的 add 了一个整数 2 做了什么，这应该非常简单了，还是画一张图来表示：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qiahiarJibISMib9ACK5Ju3jCgr2kdpQxcBib06osiaz5wGufOaCIIcX1p70Zw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3 "801753-20151206211902831-1935187212")

和前面差不多，就不解释了。

另外，插入、删除、修改操作也都是一样，每一次的操作都是以对 Object[] array 进行一次复制为基础的，如果上面的流程看懂了，那么研究插入、删除、修改的源代码应该不难。

**普通 List 的缺陷**

常用的 List 有 ArrayList、LinkedList、Vector，其中前两个是线程非安全的，最后一个是线程安全的。我有一种场景，两个线程操作了同一个 List，分别对同一个 List 进行迭代和删除，就如同下面的代码：

> public static class T1 extends Thread
>
> {
>
>     private List<Integer> list;
>
>     public T1(List<Integer> list)
>
>     {
>
>         this.list = list;
>
>     }
>
>     public void run()
>
>     {
>
>         for (Integer i : list)
>
>         {
>
>         }
>
>     }
>
> }
>
> public static class T2 extends Thread
>
> {
>
>     private List<Integer> list;
>
>     public T2(List<Integer> list)
>
>     {
>
>         this.list = list;
>
>     }
>
>     public void run()
>
>     {
>
>         for (int i = 0; i < list.size(); i++)
>
>         {
>
>             list.remove(i);
>
>         }
>
>     }
>
> }

首先我在这两个线程中放入 ArrayList 并启动这两个线程：

> public static void main(String[] args)
>
> {
>
>     List<Integer> list = new ArrayList<Integer>();
>
>     for (int i = 0; i < 10000; i++)
>
>     {
>
>         list.add(i);
>
>     }
>
>     T1 t1 = new T1(list);
>
>     T2 t2 = new T2(list);
>
>     t1.start();
>
>     t2.start();
>
> }

运行结果为：

> Exception in thread "Thread-0" java.util.ConcurrentModificationException
>
>     at java.util.AbstractList$Itr.checkForComodification(AbstractList.java:372)
>
>     at java.util.AbstractList$Itr.next(AbstractList.java:343)
>
>     at com.xrq.test60.TestMain$T1.run(TestMain.java:19)

把 ArrayList 换成 LinkedList，main 函数的代码就不贴了，运行结果为：

> Exception in thread "Thread-0" java.util.ConcurrentModificationException
>
>     at java.util.LinkedList$ListItr.checkForComodification(LinkedList.java:761)
>
>     at java.util.LinkedList$ListItr.next(LinkedList.java:696)
>
>     at com.xrq.test60.TestMain$T1.run(TestMain.java:19)

可能有人觉得，这两个线程都是线程非安全的类，所以不行。其实这个问题和线程安不安全没有关系，换成 Vector 看一下运行结果：

> Exception in thread "Thread-0" java.util.ConcurrentModificationException
>
>     at java.util.AbstractList$Itr.checkForComodification(AbstractList.java:372)
>
>     at java.util.AbstractList$Itr.next(AbstractList.java:343)
>
>     at com.xrq.test60.TestMain$T1.run(TestMain.java:19)

Vector 虽然是线程安全的，但是只是一种相对的线程安全而不是绝对的线程安全，它只能够保证增、删、改、查的单个操作一定是原子的，不会被打断，但是如果组合起来用，并不能保证线程安全性。比如就像上面的线程 1 在遍历一个 Vector 中的元素、线程 2 在删除一个 Vector 中的元素一样，势必产生并发修改异常，也就是 fail-fast。

**CopyOnWriteArrayList 的作用**

把上面的代码修改一下，用 CopyOnWriteArrayList：

> public static void main(String[] args)
>
> {
>
>     List<Integer> list = new CopyOnWriteArrayList<Integer>();
>
>     for (int i = 0; i < 10; i++)
>
>     {
>
>         list.add(i);
>
>     }
>
>     T1 t1 = new T1(list);
>
>     T2 t2 = new T2(list);
>
>     t1.start();
>
>     t2.start();
>
> }

可以运行一下这段代码，是没有任何问题的。

看到我把元素数量改小了一点，因为我们从上面的分析中应该可以看出，CopyOnWriteArrayList 的缺点，就是修改代价十分昂贵，每次修改都伴随着一次的数组复制；但同时优点也十分明显，就是在并发下不会产生任何的线程安全问题，也就是绝对的线程安全，这也是为什么我们要使用 CopyOnWriteArrayList 的原因。

另外，有两点必须讲一下。我认为 CopyOnWriteArrayList 这个并发组件，其实反映的是两个十分重要的分布式理念：

**（1）读写分离**

我们读取 CopyOnWriteArrayList 的时候读取的是 CopyOnWriteArrayList 中的 Object[] array，但是修改的时候，操作的是一个新的 Object[] array，读和写操作的不是同一个对象，这就是读写分离。这种技术数据库用的非常多，在高并发下为了缓解数据库的压力，即使做了缓存也要对数据库做读写分离，读的时候使用读库，写的时候使用写库，然后读库、写库之间进行一定的同步，这样就避免同一个库上读、写的 IO 操作太多

**（2）最终一致**

对 CopyOnWriteArrayList 来说，线程 1 读取集合里面的数据，未必是最新的数据。因为线程 2、线程 3、线程 4 四个线程都修改了 CopyOnWriteArrayList 里面的数据，但是线程 1 拿到的还是最老的那个 Object[] array，新添加进去的数据并没有，所以线程 1 读取的内容未必准确。不过这些数据虽然对于线程 1 是不一致的，但是对于之后的线程一定是一致的，它们拿到的 Object[] array 一定是三个线程都操作完毕之后的 Object array[]，这就是最终一致。最终一致对于分布式系统也非常重要，它通过容忍一定时间的数据不一致，提升整个分布式系统的可用性与分区容错性。当然，最终一致并不是任何场景都适用的，像火车站售票这种系统用户对于数据的实时性要求非常非常高，就必须做成强一致性的。

最后总结一点，随着 CopyOnWriteArrayList 中元素的增加，CopyOnWriteArrayList 的修改代价将越来越昂贵，因此，CopyOnWriteArrayList 适用于读操作远多于修改操作的并发场景中。
