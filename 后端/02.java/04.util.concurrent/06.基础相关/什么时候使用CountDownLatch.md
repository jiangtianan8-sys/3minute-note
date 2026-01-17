正如每个Java文档所描述的那样，[CountDownLatch](http://docs.oracle.com/javase/7/docs/api/java/util/concurrent/CountDownLatch.html)是一个同步工具类，它允许一个或多个线程一直等待，直到其他线程的操作执行完后再执行。在[Java并发](http://howtodoinjava.com/category/core-java/multi-threading/)中，countdownlatch的概念是一个常见的[面试题](http://howtodoinjava.com/category/core-java/interview/http://)，所以一定要确保你很好的理解了它。在这篇文章中，我将会涉及到在Java并发编 程中跟CountDownLatch相关的以下几点：

目录

- CountDownLatch是什么？
- CountDownLatch如何工作？
- 在实时系统中的应用场景
- 应用范例
- 常见的面试题

CountDownLatch是什么

CountDownLatch是在java1.5被引入的，跟它一起被引入的并发工具类还有CyclicBarrier、Semaphore、[ConcurrentHashMap](http://howtodoinjava.com/2013/05/27/best-practices-for-using-concurrenthashmap/)和[BlockingQueue](http://howtodoinjava.com/2012/10/20/how-to-use-blockingqueue-and-threadpoolexecutor-in-java/)，它们都存在于java.util.concurrent包下。CountDownLatch这个类能够使一个线程等待其他线程完成各自的工作后再执行。例如，应用程序的主线程希望在负责启动框架服务的线程已经启动所有的框架服务之后再执行。

CountDownLatch是通过一个计数器来实现的，计数器的初始值为线程的数量。每当一个线程完成了自己的任务后，计数器的值就会减1。当计数器值到达0时，它表示所有的线程已经完成了任务，然后在闭锁上等待的线程就可以恢复执行任务。

![0](https://note.youdao.com/yws/res/4989/D9073870B3104AA189E7CA8FBF1F6B01)

CountDownLatch的伪代码如下所示：

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6|//Main thread start<br><br>//Create CountDownLatch for N threads<br><br>//Create and start N threads<br><br>//Main thread wait on latch<br><br>//N threads completes there tasks are returns<br><br>//Main thread resume execution|

CountDownLatch如何工作

CountDownLatch.java类中定义的构造函数：

|   |   |
|---|---|
|1<br><br>2|//Constructs a CountDownLatch initialized with the given count.<br><br>public void CountDownLatch(int count) {...}|

构造器中的计数值（count）实际上就是闭锁需要等待的线程数量。这个值只能被设置一次，而且CountDownLatch没有提供任何机制去重新设置这个计数值。

与CountDownLatch的第一次交互是主线程等待其他线程。主线程必须在启动其他线程后立即调用CountDownLatch.await()方法。这样主线程的操作就会在这个方法上阻塞，直到其他线程完成各自的任务。

其他N 个线程必须引用闭锁对象，因为他们需要通知CountDownLatch对象，他们已经完成了各自的任务。这种通知机制是通过 CountDownLatch.countDown()方法来完成的；每调用一次这个方法，在构造函数中初始化的count值就减1。所以当N个线程都调 用了这个方法，count的值等于0，然后主线程就能通过await()方法，恢复执行自己的任务。

在实时系统中的使用场景

让我们尝试罗列出在java实时系统中CountDownLatch都有哪些使用场景。我所罗列的都是我所能想到的。如果你有别的可能的使用方法，请在留言里列出来，这样会帮助到大家。

1. 实现最大的并行性：有时我们想同时启动多个线程，实现最大程度的并行性。例如，我们想测试一个单例类。如果我们创建一个初始计数为1的CountDownLatch，并让所有线程都在这个锁上等待，那么我们可以很轻松地完成测试。我们只需调用 一次countDown()方法就可以让所有的等待线程同时恢复执行。
2. 开始执行前等待n个线程完成各自任务：例如应用程序启动类要确保在处理用户请求前，所有N个外部系统已经启动和运行了。
3. 死锁检测：一个非常方便的使用场景是，你可以使用n个线程访问共享资源，在每次测试阶段的线程数目是不同的，并尝试产生死锁。

CountDownLatch使用例子

在这个例子中，我模拟了一个应用程序启动类，它开始时启动了n个线程类，这些线程将检查外部系统并通知闭锁，并且启动类一直在闭锁上等待着。一旦验证和检查了所有外部服务，那么启动类恢复执行。

BaseHealthChecker.java：这个类是一个Runnable，负责所有特定的外部服务健康的检测。它删除了重复的代码和闭锁的中心控制代码。

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10<br><br>11<br><br>12<br><br>13<br><br>14<br><br>15<br><br>16<br><br>17<br><br>18<br><br>19<br><br>20<br><br>21<br><br>22<br><br>23<br><br>24<br><br>25<br><br>26<br><br>27<br><br>28<br><br>29<br><br>30<br><br>31<br><br>32<br><br>33<br><br>34<br><br>35<br><br>36<br><br>37<br><br>38<br><br>39<br><br>40|public abstract class BaseHealthChecker implements Runnable {<br><br>    private CountDownLatch _latch;<br><br>    private String _serviceName;<br><br>    private boolean _serviceUp;<br><br>    //Get latch object in constructor so that after completing the task, thread can countDown() the latch<br><br>    public BaseHealthChecker(String serviceName, CountDownLatch latch)<br><br>    {<br><br>        super();<br><br>        this._latch = latch;<br><br>        this._serviceName = serviceName;<br><br>        this._serviceUp = false;<br><br>    }<br><br>    @Override<br><br>    public void run() {<br><br>        try {<br><br>            verifyService();<br><br>            _serviceUp = true;<br><br>        } catch (Throwable t) {<br><br>            t.printStackTrace(System.err);<br><br>            _serviceUp = false;<br><br>        } finally {<br><br>            if(_latch != null) {<br><br>                _latch.countDown();<br><br>            }<br><br>        }<br><br>    }<br><br>    public String getServiceName() {<br><br>        return _serviceName;<br><br>    }<br><br>    public boolean isServiceUp() {<br><br>        return _serviceUp;<br><br>    }<br><br>    //This methos needs to be implemented by all specific service checker<br><br>    public abstract void verifyService();<br><br>}|

NetworkHealthChecker.java：这个类继承了BaseHealthChecker，实现了verifyService()方法。DatabaseHealthChecker.java和CacheHealthChecker.java除了服务名和休眠时间外，与NetworkHealthChecker.java是一样的。

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10<br><br>11<br><br>12<br><br>13<br><br>14<br><br>15<br><br>16<br><br>17<br><br>18<br><br>19<br><br>20<br><br>21|public class NetworkHealthChecker extends BaseHealthChecker<br><br>{<br><br>    public NetworkHealthChecker (CountDownLatch latch)  {<br><br>        super("Network Service", latch);<br><br>    }<br><br>    @Override<br><br>    public void verifyService()<br><br>    {<br><br>        System.out.println("Checking " + this.getServiceName());<br><br>        try<br><br>        {<br><br>            Thread.sleep(7000);<br><br>        }<br><br>        catch (InterruptedException e)<br><br>        {<br><br>            e.printStackTrace();<br><br>        }<br><br>        System.out.println(this.getServiceName() + " is UP");<br><br>    }<br><br>}|

ApplicationStartupUtil.java：这个类是一个主启动类，它负责初始化闭锁，然后等待，直到所有服务都被检测完。

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10<br><br>11<br><br>12<br><br>13<br><br>14<br><br>15<br><br>16<br><br>17<br><br>18<br><br>19<br><br>20<br><br>21<br><br>22<br><br>23<br><br>24<br><br>25<br><br>26<br><br>27<br><br>28<br><br>29<br><br>30<br><br>31<br><br>32<br><br>33<br><br>34<br><br>35<br><br>36<br><br>37<br><br>38<br><br>39<br><br>40<br><br>41<br><br>42<br><br>43<br><br>44<br><br>45<br><br>46<br><br>47<br><br>48<br><br>49<br><br>50<br><br>51<br><br>52|public class ApplicationStartupUtil<br><br>{<br><br>    //List of service checkers<br><br>    private static Listhecker> _services;<br><br>    //This latch will be used to wait on<br><br>    private static CountDownLatch _latch;<br><br>    private ApplicationStartupUtil()<br><br>    {<br><br>    }<br><br>    private final static ApplicationStartupUtil INSTANCE = new ApplicationStartupUtil();<br><br>    public static ApplicationStartupUtil getInstance()<br><br>    {<br><br>        return INSTANCE;<br><br>    }<br><br>    public static boolean checkExternalServices() throws Exception<br><br>    {<br><br>        //Initialize the latch with number of service checkers<br><br>        _latch = new CountDownLatch(3);<br><br>        //All add checker in lists<br><br>        _services = new ArrayListaseHealthChecker>();<br><br>        _services.add(new NetworkHealthChecker(_latch));<br><br>        _services.add(new CacheHealthChecker(_latch));<br><br>        _services.add(new DatabaseHealthChecker(_latch));<br><br>        //Start service checkers using executor framework<br><br>        Executor executor = Executors.newFixedThreadPool(_services.size());<br><br>        for(final BaseHealthChecker v : _services)<br><br>        {<br><br>            executor.execute(v);<br><br>        }<br><br>        //Now wait till all services are checked<br><br>        _latch.await();<br><br>        //Services are file and now proceed startup<br><br>        for(final BaseHealthChecker v : _services)<br><br>        {<br><br>            if( ! v.isServiceUp())<br><br>            {<br><br>                return false;<br><br>            }<br><br>        }<br><br>        return true;<br><br>    }<br><br>}|

现在你可以写测试代码去检测一下闭锁的功能了。

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10<br><br>11<br><br>12|public class Main {<br><br>    public static void main(String[] args)<br><br>    {<br><br>        boolean result = false;<br><br>        try {<br><br>            result = ApplicationStartupUtil.checkExternalServices();<br><br>        } catch (Exception e) {<br><br>            e.printStackTrace();<br><br>        }<br><br>        System.out.println("External services validation completed !! Result was :: "+ result);<br><br>    }<br><br>}|

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9|Output in console:<br><br>Checking Network Service<br><br>Checking Cache Service<br><br>Checking Database Service<br><br>Database Service is UP<br><br>Cache Service is UP<br><br>Network Service is UP<br><br>External services validation completed !! Result was :: true|

常见面试题

可以为你的下次面试准备以下一些CountDownLatch相关的问题：

- 解释一下CountDownLatch概念?
- CountDownLatch 和CyclicBarrier的不同之处?
- 给出一些CountDownLatch使用的例子?
-  CountDownLatch 类中主要的方法?

下载上述例子的源代码，请点击如下链接：

- [源码下载](https://docs.google.com/file/d/0B7yo2HclmjI4Rl9EUUl2cmI0X28/edit?usp=sharing)