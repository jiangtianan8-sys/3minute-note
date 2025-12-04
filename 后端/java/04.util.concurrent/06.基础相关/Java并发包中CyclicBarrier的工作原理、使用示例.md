1. CyclicBarrier的介绍与源码分析

CyclicBarrier 的字面意思是可循环（Cyclic）使用的屏障（Barrier）。它要做的事情是，让一组线程到达一个屏障（也可以叫同步点）时被阻塞，直到最后一个线程到达屏障时，屏障才会开门，所有被屏障拦截的线程才会继续干活。线程进入屏障通过CyclicBarrier的await()方法。

CyclicBarrier默认的构造方法是CyclicBarrier(int parties)，其参数表示屏障拦截的线程数量，每个线程调用await方法告诉CyclicBarrier我已经到达了屏障，然后当前线程被阻塞。

CyclicBarrier还提供一个更高级的构造函数CyclicBarrier(int parties, Runnable barrierAction)，用于在线程到达屏障时，优先执行barrierAction这个Runnable对象，方便处理更复杂的业务场景。

构造函数

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6|public CyclicBarrier(int parties) {<br><br>    this(parties, null);<br><br>}<br><br>public int getParties() {<br><br>    return parties;<br><br>}|

实现原理：在CyclicBarrier的内部定义了一个Lock对象，每当一个线程调用CyclicBarrier的await方法时，将剩余拦截的线程数减1，然后判断剩余拦截数是否为0，如果不是，进入Lock对象的条件队列等待。如果是，执行barrierAction对象的Runnable方法，然后将锁的条件队列中的所有线程放入锁等待队列中，这些线程会依次的获取锁、释放锁，接着先从await方法返回，再从CyclicBarrier的await方法中返回。

await源码

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7|public int await() throws InterruptedException, BrokenBarrierException {<br><br>    try {<br><br>        return dowait(false, 0L);<br><br>    } catch (TimeoutException toe) {<br><br>        throw new Error(toe); // cannot happen<br><br>    }<br><br>}|

dowait源码

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10<br><br>11<br><br>12<br><br>13<br><br>14<br><br>15<br><br>16<br><br>17<br><br>18<br><br>19<br><br>20<br><br>21<br><br>22<br><br>23<br><br>24<br><br>25<br><br>26<br><br>27<br><br>28<br><br>29<br><br>30<br><br>31<br><br>32<br><br>33<br><br>34<br><br>35<br><br>36<br><br>37<br><br>38<br><br>39<br><br>40<br><br>41<br><br>42<br><br>43<br><br>44<br><br>45<br><br>46<br><br>47<br><br>48<br><br>49<br><br>50<br><br>51<br><br>52<br><br>53<br><br>54<br><br>55<br><br>56<br><br>57<br><br>58<br><br>59<br><br>60<br><br>61<br><br>62<br><br>63<br><br>64<br><br>65<br><br>66|private int dowait(boolean timed, long nanos)<br><br>    throws InterruptedException, BrokenBarrierException,<br><br>           TimeoutException {<br><br>    final ReentrantLock lock = this.lock;<br><br>    lock.lock();<br><br>    try {<br><br>        final Generation g = generation;<br><br>        if (g.broken)<br><br>            throw new BrokenBarrierException();<br><br>        if (Thread.interrupted()) {<br><br>            breakBarrier();<br><br>            throw new InterruptedException();<br><br>        }<br><br>        int index = --count;<br><br>        if (index == 0) {  // tripped<br><br>            boolean ranAction = false;<br><br>            try {<br><br>                final Runnable command = barrierCommand;<br><br>                if (command != null)<br><br>                    command.run();<br><br>                ranAction = true;<br><br>                nextGeneration();<br><br>                return 0;<br><br>            } finally {<br><br>                if (!ranAction)<br><br>                    breakBarrier();<br><br>            }<br><br>        }<br><br>        // loop until tripped, broken, interrupted, or timed out<br><br>        for (;;) {<br><br>            try {<br><br>                if (!timed)<br><br>                    trip.await();<br><br>                else if (nanos > 0L)<br><br>                    nanos = trip.awaitNanos(nanos);<br><br>            } catch (InterruptedException ie) {<br><br>                if (g == generation && ! g.broken) {<br><br>                    breakBarrier();<br><br>                    throw ie;<br><br>                } else {<br><br>                    // We're about to finish waiting even if we had not<br><br>                    // been interrupted, so this interrupt is deemed to<br><br>                    // "belong" to subsequent execution.<br><br>                    Thread.currentThread().interrupt();<br><br>                }<br><br>            }<br><br>            if (g.broken)<br><br>                throw new BrokenBarrierException();<br><br>            if (g != generation)<br><br>                return index;<br><br>            if (timed && nanos <= 0L) {<br><br>                breakBarrier();<br><br>                throw new TimeoutException();<br><br>            }<br><br>        }<br><br>    } finally {<br><br>        lock.unlock();<br><br>    }<br><br>}|

当最后一个线程到达屏障点，也就是执行dowait方法时，会在return 0 返回之前调用finally块中的breakBarrier方法。

breakBarrier源代码

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5|private void breakBarrier() {<br><br>    generation.broken = true;<br><br>    count = parties;<br><br>    trip.signalAll();<br><br>}|

CyclicBarrier主要用于一组线程之间的相互等待，而CountDownLatch一般用于一组线程等待另一组些线程。实际上可以通过CountDownLatch的countDown()和await()来实现CyclicBarrier的功能。即 CountDownLatch中的countDown()+await() = CyclicBarrier中的await()。注意：在一个线程中先调用countDown()，然后调用await()。

其它方法：CycliBarrier对象可以重复使用，重用之前应当调用CyclicBarrier对象的reset方法。

reset源码

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10|public void reset() {<br><br>    final ReentrantLock lock = this.lock;<br><br>    lock.lock();<br><br>    try {<br><br>        breakBarrier();   // break the current generation<br><br>        nextGeneration(); // start a new generation<br><br>    } finally {<br><br>        lock.unlock();<br><br>    }<br><br>}|

2. 使用示例

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4<br><br>5<br><br>6<br><br>7<br><br>8<br><br>9<br><br>10<br><br>11<br><br>12<br><br>13<br><br>14<br><br>15<br><br>16<br><br>17<br><br>18<br><br>19<br><br>20<br><br>21<br><br>22<br><br>23<br><br>24<br><br>25<br><br>26<br><br>27<br><br>28<br><br>29<br><br>30<br><br>31<br><br>32<br><br>33<br><br>34<br><br>35<br><br>36<br><br>37<br><br>38<br><br>39<br><br>40|package javalearning;<br><br>import java.util.Random;<br><br>import java.util.concurrent.BrokenBarrierException;<br><br>import java.util.concurrent.CyclicBarrier;<br><br>import java.util.concurrent.ExecutorService;<br><br>import java.util.concurrent.Executors;<br><br>public class CyclicBarrierDemo {<br><br>    private CyclicBarrier cb = new CyclicBarrier(4);<br><br>    private Random rnd = new Random();<br><br>    class TaskDemo implements Runnable{<br><br>        private String id;<br><br>        TaskDemo(String id){<br><br>            this.id = id;<br><br>        }<br><br>        @Override<br><br>        public void run(){<br><br>            try {<br><br>                Thread.sleep(rnd.nextInt(1000));<br><br>                System.out.println("Thread " + id + " will wait");<br><br>                cb.await();<br><br>                System.out.println("-------Thread " + id + " is over");<br><br>            } catch (InterruptedException e) {<br><br>            } catch (BrokenBarrierException e) {<br><br>            }<br><br>        }<br><br>    }<br><br>    public static void main(String[] args){<br><br>        CyclicBarrierDemo cbd = new CyclicBarrierDemo();<br><br>        ExecutorService es = Executors.newCachedThreadPool();<br><br>        es.submit(cbd.new TaskDemo("a"));<br><br>        es.submit(cbd.new TaskDemo("b"));<br><br>        es.submit(cbd.new TaskDemo("c"));<br><br>        es.submit(cbd.new TaskDemo("d"));<br><br>        es.shutdown();<br><br>    }<br><br>}|

在这个示例中，我们创建了四个线程a、b、c、d，这四个线程提交给了线程池。四个线程不同时间到达cb.await()语句，当四个线程都输出“Thread x will wait”以后才会输出“Thread x is over”。

运行结果

Thread d will wait

Thread a will wait

Thread c will wait

Thread b will wait

-------Thread b is over

-------Thread d is over

-------Thread a is over

-------Thread c is over

 3. 参考内容

[1] http://ifeve.com/concurrency-cyclicbarrier/

来源： [https://www.cnblogs.com/nullzx/p/5271964.html](https://www.cnblogs.com/nullzx/p/5271964.html)