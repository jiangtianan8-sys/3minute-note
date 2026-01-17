这一节主要是谈谈读写锁的实现。

上一节中提到，ReadWriteLock看起来有两个锁：readLock/writeLock。如果真的是两个锁的话，它们之间又是如何相互影响的呢？

事实上在ReentrantReadWriteLock里锁的实现是靠java.util.concurrent.locks.ReentrantReadWriteLock.Sync完成的。这个类看起来比较眼熟，实际上它是AQS的一个子类，这中类似的结构在CountDownLatch、ReentrantLock、Semaphore里面都存在。同样它也有两种实现：公平锁和非公平锁，也就是java.util.concurrent.locks.ReentrantReadWriteLock.FairSync和java.util.concurrent.locks.ReentrantReadWriteLock.NonfairSync。这里暂且不提。

在ReentrantReadWriteLock里面的锁主体就是一个Sync，也就是上面提到的FairSync或者NonfairSync，所以说实际上只有一个锁，只是在获取读取锁和写入锁的方式上不一样，所以前面才有读写锁是独占锁的两个不同视图一说。

ReentrantReadWriteLock里面有两个类：ReadLock/WriteLock，这两个类都是Lock的实现。

清单1 ReadLock 片段

public static class ReadLock implements Lock, java.io.Serializable  {

    private final Sync sync;

    protected ReadLock(ReentrantReadWriteLock lock) {

        sync = lock.sync;

    }

    public void lock() {

        sync.acquireShared(1);

    }

    public void lockInterruptibly() throws InterruptedException {

        sync.acquireSharedInterruptibly(1);

    }

    public  boolean tryLock() {

        return sync.tryReadLock();

    }

    public boolean tryLock(long timeout, TimeUnit unit) throws InterruptedException {

        return sync.tryAcquireSharedNanos(1, unit.toNanos(timeout));

    }

    public  void unlock() {

        sync.releaseShared(1);

    }

    public Condition newCondition() {

        throw new UnsupportedOperationException();

    }

}

清单2 WriteLock 片段

public static class WriteLock implements Lock, java.io.Serializable  {

    private final Sync sync;

    protected WriteLock(ReentrantReadWriteLock lock) {

        sync = lock.sync;

    }

    public void lock() {

        sync.acquire(1);

    }

    public void lockInterruptibly() throws InterruptedException {

        sync.acquireInterruptibly(1);

    }

    public boolean tryLock( ) {

        return sync.tryWriteLock();

    }

    public boolean tryLock(long timeout, TimeUnit unit) throws InterruptedException {

        return sync.tryAcquireNanos(1, unit.toNanos(timeout));

    }

    public void unlock() {

        sync.release(1);

    }

    public Condition newCondition() {

        return sync.newCondition();

    }

    public boolean isHeldByCurrentThread() {

        return sync.isHeldExclusively();

    }

    public int getHoldCount() {

        return sync.getWriteHoldCount();

    }

}

清单1描述的是读锁的实现，清单2描述的是写锁的实现。显然WriteLock就是一个独占锁，这和ReentrantLock里面的实现几乎相同，都是使用了AQS的acquire/release操作。当然了在内部处理方式上与ReentrantLock还是有一点不同的。对比清单1和清单2可以看到，ReadLock获取的是共享锁，WriteLock获取的是独占锁。

在AQS章节中介绍到AQS中有一个state字段（int类型，32位）用来描述有多少线程获持有锁。在独占锁的时代这个值通常是0或者1（如果是重入的就是重入的次数），在共享锁的时代就是持有锁的数量。在上一节中谈到，ReadWriteLock的读、写锁是相关但是又不一致的，所以需要两个数来描述读锁（共享锁）和写锁（独占锁）的数量。显然现在一个state就不够用了。于是在ReentrantReadWrilteLock里面将这个字段一分为二，高位16位表示共享锁的数量，低位16位表示独占锁的数量（或者重入数量）。2^16-1=65536，这就是上节中提到的为什么共享锁和独占锁的数量最大只能是65535的原因了。

有了上面的知识后再来分析读写锁的获取和释放就容易多了。

清单3 写入锁获取片段

protected final boolean tryAcquire(int acquires) {

    Thread current = Thread.currentThread();

    int c = getState();

    int w = exclusiveCount(c);

    if (c != 0) {

        if (w == 0 || current != getExclusiveOwnerThread())

            return false;

        if (w + exclusiveCount(acquires) > MAX_COUNT)

            throw new Error("Maximum lock count exceeded");

    }

    if ((w == 0 && writerShouldBlock(current)) ||

        !compareAndSetState(c, c + acquires))

        return false;

    setExclusiveOwnerThread(current);

    return true;

}

清单3 是写入锁获取的逻辑片段，整个工作流程是这样的：

1. 持有锁线程数非0（c=getState()不为0），如果写线程数（w）为0（那么读线程数就不为0）或者独占锁线程（持有锁的线程）不是当前线程就返回失败，或者写入锁的数量（其实是重入数）大于65535就抛出一个Error异常。否则进行2。
2. 如果当且写线程数位0（那么读线程也应该为0，因为步骤1已经处理c!=0的情况），并且当前线程需要阻塞那么就返回失败；如果增加写线程数失败也返回失败。否则进行3。
3. 设置独占线程（写线程）为当前线程，返回true。

清单3 中 exclusiveCount(c)就是获取写线程数（包括重入数），也就是state的低16位值。另外这里有一段逻辑是当前写线程是否需要阻塞writerShouldBlock(current)。清单4 和清单5 就是公平锁和非公平锁中是否需要阻塞的片段。很显然对于非公平锁而言总是不阻塞当前线程，而对于公平锁而言如果AQS队列不为空或者当前线程不是在AQS的队列头那么就阻塞线程，直到队列前面的线程处理完锁逻辑。

清单4 公平读写锁写线程是否阻塞

final boolean writerShouldBlock(Thread current) {

    return !isFirst(current);

}

清单5 非公平读写锁写线程是否阻塞

final boolean writerShouldBlock(Thread current) {

    return false;

}

写入锁的获取逻辑清楚后，释放锁就比较简单了。清单6 描述的写入锁释放逻辑片段，其实就是检测下剩下的写入锁数量，如果是0就将独占锁线程清空（意味着没有线程获取锁），否则就是说当前是重入锁的一次释放，所以不能将独占锁线程清空。然后将剩余线程状态数写回AQS。

清单6 写入锁释放逻辑片段

protected final boolean tryRelease(int releases) {

    int nextc = getState() - releases;

    if (Thread.currentThread() != getExclusiveOwnerThread())

        throw new IllegalMonitorStateException();

    if (exclusiveCount(nextc) == 0) {

        setExclusiveOwnerThread(null);

        setState(nextc);

        return true;

    } else {

        setState(nextc);

        return false;

    }

}

清单3~6 描述的写入锁的获取释放过程。读取锁的获取和释放过程要稍微复杂些。 清单7描述的是读取锁的获取过程。

清单7 读取锁获取过程片段

protected final int tryAcquireShared(int unused) {

    Thread current = Thread.currentThread();

    int c = getState();

    if (exclusiveCount(c) != 0 &&

        getExclusiveOwnerThread() != current)

        return -1;

    if (sharedCount(c) == MAX_COUNT)

        throw new Error("Maximum lock count exceeded");

    if (!readerShouldBlock(current) &&

        compareAndSetState(c, c + SHARED_UNIT)) {

        HoldCounter rh = cachedHoldCounter;

        if (rh == null || rh.tid != current.getId())

            cachedHoldCounter = rh = readHolds.get();

        rh.count++;

        return 1;

    }

    return fullTryAcquireShared(current);

}

final int fullTryAcquireShared(Thread current) {

    HoldCounter rh = cachedHoldCounter;

    if (rh == null || rh.tid != current.getId())

        rh = readHolds.get();

    for (;;) {

        int c = getState();

        int w = exclusiveCount(c);

        if ((w != 0 && getExclusiveOwnerThread() != current) ||

            ((rh.count | w) == 0 && readerShouldBlock(current)))

            return -1;

        if (sharedCount(c) == MAX_COUNT)

            throw new Error("Maximum lock count exceeded");

        if (compareAndSetState(c, c + SHARED_UNIT)) {

            cachedHoldCounter = rh; // cache for release

            rh.count++;

            return 1;

        }

    }

}

读取锁获取的过程是这样的：

1. 如果写线程持有锁（也就是独占锁数量不为0），并且独占线程不是当前线程，那么就返回失败。因为允许写入线程获取锁的同时获取读取锁。否则进行2。
2. 如果读线程请求锁数量达到了65535（包括重入锁），那么就跑出一个错误Error，否则进行3。
3. 如果读线程不用等待（实际上是是否需要公平锁），并且增加读取锁状态数成功，那么就返回成功，否则进行4。
4. 步骤3失败的原因是CAS操作修改状态数失败，那么就需要循环不断尝试去修改状态直到成功或者锁被写入线程占有。实际上是过程3的不断尝试直到CAS计数成功或者被写入线程占有锁。

在清单7 中有一个对象HoldCounter，这里暂且不提这是什么结构和为什么存在这样一个结构。

接下来根据清单8 我们来看如何释放一个读取锁。同样先不理HoldCounter，关键的在于for循环里面，其实就是一个不断尝试的CAS操作，直到修改状态成功。前面说过state的高16位描述的共享锁（读取锁）的数量，所以每次都需要减去2^16，这样就相当于读取锁数量减1。实际上SHARED_UNIT=1<<16。

清单8 读取锁释放过程

protected final boolean tryReleaseShared(int unused) {

    HoldCounter rh = cachedHoldCounter;

    Thread current = Thread.currentThread();

    if (rh == null || rh.tid != current.getId())

        rh = readHolds.get();

    if (rh.tryDecrement() <= 0)

        throw new IllegalMonitorStateException();

    for (;;) {

        int c = getState();

        int nextc = c - SHARED_UNIT;

        if (compareAndSetState(c, nextc))

            return nextc == 0;

    }

}

好了，现在回头看HoldCounter到底是一个什么东西。首先我们可以看到只有在获取共享锁（读取锁）的时候加1，也只有在释放共享锁的时候减1有作用，并且在释放锁的时候抛出了一个IllegalMonitorStateException异常。而我们知道IllegalMonitorStateException通常描述的是一个线程操作一个不属于自己的监视器对象的引发的异常。也就是说这里的意思是一个线程释放了一个不属于自己或者不存在的共享锁。

前面的章节中一再强调，对于共享锁，其实并不是锁的概念，更像是计数器的概念。一个共享锁就相对于一次计数器操作，一次获取共享锁相当于计数器加1，释放一个共享锁就相当于计数器减1。显然只有线程持有了共享锁（也就是当前线程携带一个计数器，描述自己持有多少个共享锁或者多重共享锁），才能释放一个共享锁。否则一个没有获取共享锁的线程调用一次释放操作就会导致读写锁的state（持有锁的线程数，包括重入数）错误。

明白了HoldCounter的作用后我们就可以猜到它的作用其实就是当前线程持有共享锁（读取锁）的数量，包括重入的数量。那么这个数量就必须和线程绑定在一起。

在Java里面将一个对象和线程绑定在一起，就只有ThreadLocal才能实现了。所以毫无疑问HoldCounter就应该是绑定到线程上的一个计数器。

清单9 线程持有读取锁数量的计数器

static final class HoldCounter {

    int count;

    final long tid = Thread.currentThread().getId();

    int tryDecrement() {

        int c = count;

        if (c > 0)

            count = c - 1;

        return c;

    }

}

static final class ThreadLocalHoldCounter

    extends ThreadLocal {

    public HoldCounter initialValue() {

        return new HoldCounter();

    }

}

清单9 描述的是线程持有读取锁数量的计数器。可以看到这里使用ThreadLocal将HoldCounter绑定到当前线程上，同时HoldCounter也持有线程Id，这样在释放锁的时候才能知道ReadWriteLock里面缓存的上一个读取线程（cachedHoldCounter）是否是当前线程。这样做的好处是可以减少ThreadLocal.get()的次数，因为这也是一个耗时操作。需要说明的是这样HoldCounter绑定线程id而不绑定线程对象的原因是避免HoldCounter和ThreadLocal互相绑定而GC难以释放它们（尽管GC能够智能的发现这种引用而回收它们，但是这需要一定的代价），所以其实这样做只是为了帮助GC快速回收对象而已。

除了readLock()和writeLock()外，Lock对象还允许tryLock()，那么ReadLock和WriteLock的tryLock()不一样。清单10 和清单11 分别描述了读取锁的tryLock()和写入锁的tryLock()。

读取锁tryLock()也就是tryReadLock()成功的条件是：没有写入锁或者写入锁是当前线程，并且读线程共享锁数量没有超过65535个。

写入锁tryLock()也就是tryWriteLock()成功的条件是: 没有写入锁或者写入锁是当前线程，并且尝试一次修改state成功。

清单10 读取锁的tryLock()

final boolean tryReadLock() {

    Thread current = Thread.currentThread();

    for (;;) {

        int c = getState();

        if (exclusiveCount(c) != 0 &&

            getExclusiveOwnerThread() != current)

            return false;

        if (sharedCount(c) == MAX_COUNT)

            throw new Error("Maximum lock count exceeded");

        if (compareAndSetState(c, c + SHARED_UNIT)) {

            HoldCounter rh = cachedHoldCounter;

            if (rh == null || rh.tid != current.getId())

                cachedHoldCounter = rh = readHolds.get();

            rh.count++;

            return true;

        }

    }

}

清单11 写入锁的tryLock()

final boolean tryWriteLock() {

    Thread current = Thread.currentThread();

    int c = getState();

    if (c != 0) {

        int w = exclusiveCount(c);

        if (w == 0 ||current != getExclusiveOwnerThread())

            return false;

        if (w == MAX_COUNT)

            throw new Error("Maximum lock count exceeded");

    }

    if (!compareAndSetState(c, c + 1))

        return false;

    setExclusiveOwnerThread(current);

    return true;

}

整个读写锁的逻辑大概就这么多，其实真正研究起来也不是很复杂，真正复杂的东西都在AQS里面。

锁部分的原理和思想都介绍完了，下一节里面会对锁机进行小节，并对线程并发也会有一些简单的小节。