《Java 源码分析》：CountDownLatch

Latch：闭锁。

有人把 Latch 比喻成是一个门，在门打开之前，所有想进门的线程都被阻塞，在门打开之后，所有想进门的线程全部通过，且门打开之后就不能再关闭。

CountDownLatch 是一个同步辅助类，允许一个或多个线程等待直到其它线程的一些操作已经准备完成。

CountDownLatch 是 JDK 5+ 里面闭锁的一个实现，允许一个或者多个线程等待某个事件的发生。CountDownLatch 有一个正数计数器，countDown 方法对计数器做减操作，await 方法等待计数器达到 0。所有 await 的线程都会阻塞直到计数器为 0 或者等待线程中断或者超时。

即 CountDownLatch 里面有一个计数器，当计数器不为零时所有线程一直阻塞。当计数器为零时，则所有等待此门的线程就全部唤醒开始工作。

下面这个例子就很好的介绍了 CountDownLatch 的含义和用法。

   import java.util.concurrent.CountDownLatch;

   public class CountDownLatchDemo {

       private static final int NUM = 10;

       private static CountDownLatch  doneSignal = new CountDownLatch(NUM);

       private static CountDownLatch startSignal = new CountDownLatch(1);

       public static void main(String[] args) {

           for(int i=0;i

               new Thread(){

                   @Override

                   public void run() {

                       try {

                           //System.out.println(Thread.currentThread().getName()+"   等待一个 signal....");

                           startSignal.await();

                           System.out.println(Thread.currentThread().getName()+" is running...");

                           doneSignal.countDown();

                      } catch (InterruptedException e) {

                           e.printStackTrace();

                      }

                  }

              }.start();

          }

           //模拟为其它线程的运行准备资源，例如，在所有准备从数据库中读数据的线程之前连接好数据库等操作

           init();

           startSignal.countDown();//运行到这里，就会将上面的线程全部激活

           try {

               System.out.println("main 线程 awaiting....");

               doneSignal.await();//main 线程在这里等待，等到上面的所有线程全部执行完毕后

          } catch (InterruptedException e) {

               e.printStackTrace();

          }

           System.out.println("main 线程又开始运行 ");

           System.out.println("main 线程运行结束 ");

      }

       private static void init() {

           System.out.println("main 为所有的线程的运行做准备。。。。");

      }

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

运行结果：

main 为所有的线程的运行做准备。。。。 main 线程 awaiting.... Thread-0 is running... Thread-2 is running... Thread-4 is running... Thread-6 is running... Thread-8 is running... Thread-1 is running... Thread-3 is running... Thread-5 is running... Thread-7 is running... Thread-9 is running... main 线程又开始运行 main 线程运行结束

源码分析

首先看下 CountDownLa 的构造函数，构造函数需要传入一个大于的零的数。

从构造函数中可以看到，CountDownLatch 类是直接委托给实现了 AQS 类的内部类 Sync 类实现的。

   public CountDownLatch(int count) {

       if (count < 0) throw new IllegalArgumentException("count < 0");

       this.sync = new Sync(count);

  }

   Sync(int count) {

       setState(count);//调用 AQS 类的 setState 设置状态位

  }

1

2

3

4

5

6

7

8

分析 await() 方法的内部实现

   public void await() throws InterruptedException {

       sync.acquireSharedInterruptibly(1);

  }

   /*

  具体如下：

  1、检测中断标志位

  2、调用 tryAcquireShared 方法来检查 AQS 标志位 state 是否等于 0，如果 state 等于 0，则说明不需要等待，立即返回，否则进行 3

  3、调用 doAcquireSharedInterruptibly 方法进入 AQS 同步队列进行等待，并不断的自旋检测是否需要唤醒

  */

   public final void acquireSharedInterruptibly(int arg)

           throws InterruptedException {

       if (Thread.interrupted())

           throw new InterruptedException();

       if (tryAcquireShared(arg) < 0)

           doAcquireSharedInterruptibly(arg);

  }

   /*

      函数功能：根据 AQS 的状态位 state 来返回值，

      如果为 state=0，返回 1

      如果 state=1，则返回 -1

  */

   protected int tryAcquireShared(int acquires) {

       return (getState() == 0) ? 1 : -1;

  }

   /**

    * Acquires in shared interruptible mode.

    * @param arg the acquire argument

    */

   private void doAcquireSharedInterruptibly(int arg)

       throws InterruptedException {

       final Node node = addWaiter(Node.SHARED);

       boolean failed = true;

       try {

           for (;;) {

               final Node p = node.predecessor();

               if (p == head) {

                   int r = tryAcquireShared(arg);

                   if (r >= 0) {//如果大于零，则说明需要唤醒

                       setHeadAndPropagate(node, r);

                       p.next = null; // help GC

                       failed = false;

                       return;

                  }

              }

               if (shouldParkAfterFailedAcquire(p, node) &&

                   parkAndCheckInterrupt())

                   throw new InterruptedException();

          }

      } finally {

           if (failed)

               cancelAcquire(node);

      }

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

45

46

47

48

49

50

51

52

53

54

55

调用 countDown 方法的内部实现

   /**

    * Decrements the count of the latch, releasing all waiting threads if

    * the count reaches zero.

    *

    *

If the current count is greater than zero then it is decremented.

    * If the new count is zero then all waiting threads are re-enabled for

    * thread scheduling purposes.

    *

    *

If the current count equals zero then nothing happens.

    */

   public void countDown() {

       sync.releaseShared(1);

  }

   public final boolean releaseShared(int arg) {

       if (tryReleaseShared(arg)) {

           doReleaseShared();//释放所有正在等待的线程节点

           return true;

      }

       return false;

  }

       protected boolean tryReleaseShared(int releases) {

           // Decrement count; signal when transition to zero

           for (;;) {

               int c = getState();

               if (c == 0)

                   return false;

               int nextc = c-1;

               if (compareAndSetState(c, nextc))

                   return nextc == 0;

          }

      }

   private void doReleaseShared() {

       for (;;) {

           Node h = head;

           if (h != null && h != tail) {

               int ws = h.waitStatus;

               if (ws == Node.SIGNAL) {

                   if (!compareAndSetWaitStatus(h, Node.SIGNAL, 0))

                       continue;            // loop to recheck cases

                   unparkSuccessor(h);

              }

               else if (ws == 0 &&

                        !compareAndSetWaitStatus(h, 0, Node.PROPAGATE))

                   continue;                // loop on failed CAS

          }

           if (h == head)                   // loop if head changed

               break;

      }

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

45

46

47

48

49

50

51

52

53

由于里面的代码逻辑和前面博文中介绍 Semaphore 类、ReentrantLock 基本一致，这里就不再介绍。

小结

只需要记住：CountDownLatch 是一个同步辅助类，当 CountDownLatch 类中的计数器减少为零之前所有调用 await 方法的线程都会被阻塞，如果计数器减少为零，则所有线程被唤醒继续运行。

一般的应用场景为：

1、其它的一些线程需要某个线程做准备工作。例如：数据库的连接等。

2、某个线程需要等待一些线程工作完之后清理资源。断开数据库的连接等。

来源： [https://blog.csdn.net/u010412719/article/details/52121919](https://blog.csdn.net/u010412719/article/details/52121919)
