此小节介绍几个与锁有关的有用工具。

闭锁（Latch）

闭锁（Latch）：一种同步方法，可以延迟线程的进度直到线程到达某个终点状态。通俗的讲就是，一个闭锁相当于一扇大门，在大门打开之前所有线程都被阻断，一旦大门打开所有线程都将通过，但是一旦大门打开，所有线程都通过了，那么这个闭锁的状态就失效了，门的状态也就不能变了，只能是打开状态。也就是说闭锁的状态是一次性的，它确保在闭锁打开之前所有特定的活动都需要在闭锁打开之后才能完成。

CountDownLatch是JDK 5+里面闭锁的一个实现，允许一个或者多个线程等待某个事件的发生。CountDownLatch有一个正数计数器，countDown方法对计数器做减操作，await方法等待计数器达到0。所有await的线程都会阻塞直到计数器为0或者等待线程中断或者超时。

CountDownLatch的API如下。

- public void await() throws InterruptedException
- public boolean await(long timeout, TimeUnit unit) throws InterruptedException
- public void countDown()
- public long getCount()

其中getCount()描述的是当前计数，通常用于调试目的。

下面的例子中描述了闭锁的两种常见的用法。

package xylz.study.concurrency.lock;

import java.util.concurrent.CountDownLatch;

public class PerformanceTestTool {

    public long timecost(final int times, final Runnable task) throws InterruptedException {

        if (times <= 0) throw new IllegalArgumentException();

        final CountDownLatch startLatch = new CountDownLatch(1);

        final CountDownLatch overLatch = new CountDownLatch(times);

        for (int i = 0; i < times; i++) {

            new Thread(new Runnable() {

                public void run() {

                    try {

                        startLatch.await();

                        //

                        task.run();

                    } catch (InterruptedException ex) {

                        Thread.currentThread().interrupt();

                    } finally {

                        overLatch.countDown();

                    }

                }

            }).start();

        }

        //

        long start = System.nanoTime();

        startLatch.countDown();

        overLatch.await();

        return System.nanoTime() - start;

    }

}

在上面的例子中使用了两个闭锁，第一个闭锁确保在所有线程开始执行任务前，所有准备工作都已经完成，一旦准备工作完成了就调用startLatch.countDown()打开闭锁，所有线程开始执行。第二个闭锁在于确保所有任务执行完成后主线程才能继续进行，这样保证了主线程等待所有任务线程执行完成后才能得到需要的结果。在第二个闭锁当中，初始化了一个N次的计数器，每个任务执行完成后都会将计数器减一，所有任务完成后计数器就变为了0，这样主线程闭锁overLatch拿到此信号后就可以继续往下执行了。

根据前面的[happend-before法则](http://www.blogjava.net/xylz/archive/2010/07/03/325168.html)可以知道闭锁有以下特性：

内存一致性效果：线程中调用 countDown() 之前的操作 [happen-before](http://www.blogjava.net/xylz/archive/2010/07/03/325168.html) 紧跟在从另一个线程中对应 await() 成功返回的操作。

在上面的例子中第二个闭锁相当于把一个任务拆分成N份，每一份独立完成任务，主线程等待所有任务完成后才能继续执行。这个特性在后面的线程池框架中会用到，其实FutureTask就可以看成一个闭锁。后面的章节还会具体分析FutureTask的。

同样基于探索精神，仍然需要“窥探”下CountDownLatch里面到底是如何实现await*和countDown的。

首先，研究下await()方法。内部直接调用了[AQS](http://www.blogjava.net/xylz/archive/2010/07/06/325390.html)的acquireSharedInterruptibly(1)。

public final void acquireSharedInterruptibly(int arg) throws InterruptedException {

    if (Thread.interrupted())

        throw new InterruptedException();

    if (tryAcquireShared(arg) < 0)

        doAcquireSharedInterruptibly(arg);

}

前面一直提到的都是独占锁（排它锁、互斥锁），现在就用到了另外一种锁，共享锁。

所谓共享锁是说所有共享锁的线程共享同一个资源，一旦任意一个线程拿到共享资源，那么所有线程就都拥有的同一份资源。也就是通常情况下共享锁只是一个标志，所有线程都等待这个标识是否满足，一旦满足所有线程都被激活（相当于所有线程都拿到锁一样）。这里的闭锁CountDownLatch就是基于共享锁的实现。

闭锁中关于AQS的tryAcquireShared的实现是如下代码（java.util.concurrent.CountDownLatch.Sync.tryAcquireShared）：

public int tryAcquireShared(int acquires) {

    return getState() == 0? 1 : -1;

}

在这份逻辑中，对于闭锁而言第一次await时tryAcquireShared应该总是-1，因为对于闭锁CountDownLatch而言state的值就是初始化的count值。这也就解释了为什么在countDown调用之前闭锁的count总是>0。

private void doAcquireSharedInterruptibly(int arg)

    throws InterruptedException {

    final Node node = addWaiter(Node.SHARED);

    try {

        for (;;) {

            final Node p = node.predecessor();

            if (p == head) {

                int r = tryAcquireShared(arg);

                if (r >= 0) {

                    setHeadAndPropagate(node, r);

                    p.next = null; // help GC

                    return;

                }

            }

            if (shouldParkAfterFailedAcquire(p, node) &&

                parkAndCheckInterrupt())

                break;

        }

    } catch (RuntimeException ex) {

        cancelAcquire(node);

        throw ex;

    }

    // Arrive here only if interrupted

    cancelAcquire(node);

    throw new InterruptedException();

}

上面的逻辑展示了如何通过await将所有线程串联并挂起，直到被唤醒或者条件满足或者被中断。整个过程是这样的：

1. 将当前线程节点以共享模式加入AQS的CLH队列中（相关概念参考[这里](http://www.blogjava.net/xylz/archive/2010/07/06/325390.html)和[这里](http://www.blogjava.net/xylz/archive/2010/07/07/325410.html)）。进行2。
2. 检查当前节点的前任节点，如果是头结点并且当前闭锁计数为0就将当前节点设置为头结点，唤醒继任节点，返回（结束线程阻塞）。否则进行3。
3. 检查线程是否该阻塞，如果应该就阻塞(park)，直到被唤醒（unpark）。重复2。
4. 如果2、3有异常就抛出异常（结束线程阻塞）。

这里有一点值得说明下，设置头结点并唤醒继任节点setHeadAndPropagate。由于前面tryAcquireShared总是返回1或者-1，而进入setHeadAndPropagate时总是propagate>=0，所以这里propagate==1。后面唤醒继任节点操作就非常熟悉了。

private void setHeadAndPropagate(Node node, int propagate) {

    setHead(node);

    if (propagate > 0 && node.waitStatus != 0) {

        Node s = node.next;

        if (s == null || s.isShared())

            unparkSuccessor(node);

    }

}

从上面的所有逻辑可以看出countDown应该就是在条件满足（计数为0）时唤醒头结点（时间最长的一个节点），然后头结点就会根据FIFO队列唤醒整个节点列表（如果有的话）。

从CountDownLatch的countDown代码中看到，直接调用的是AQS的releaseShared(1)，参考前面的知识，这就印证了上面的说法。

tryReleaseShared中正是采用CAS操作减少计数（每次减-1）。

public boolean tryReleaseShared(int releases) {

    for (;;) {

        int c = getState();

        if (c == 0)

            return false;

        int nextc = c-1;

        if (compareAndSetState(c, nextc))

            return nextc == 0;

    }

}

整个CountDownLatch就是这个样子的。其实有了前面原子操作和AQS的原理及实现，分析CountDownLatch还是比较容易的。