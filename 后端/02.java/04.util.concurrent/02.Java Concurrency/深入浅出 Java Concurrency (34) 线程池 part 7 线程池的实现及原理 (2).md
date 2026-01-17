线程池任务执行流程

我们从一个API开始接触Executor是如何处理任务队列的。

java.util.concurrent.Executor.execute(Runnable)

Executes the given task sometime in the future. The task may execute in a new thread or in an existing pooled thread. If the task cannot be submitted for execution, either because this executor has been shutdown or because its capacity has been reached, the task is handled by the current RejectedExecutionHandler.

线程池中所有任务执行都依赖于此接口。这段话有以下几个意思：

1. 任务可能在将来某个时刻被执行，有可能不是立即执行。为什么这里有两个“可能”？继续往下面看。
2. 任务可能在一个新的线程中执行或者线程池中存在的一个线程中执行。
3. 任务无法被提交执行有以下两个原因：线程池已经关闭或者线程池已经达到了容量限制。
4. 所有失败的任务都将被“当前”的任务拒绝策略RejectedExecutionHandler 处理。

回答上面两个“可能“。任务可能被执行，那不可能的情况就是上面说的情况3；可能不是立即执行，是因为任务可能还在队列中排队，因此还在等待分配线程执行。了解完了字面上的问题，我们再来看具体的实现。

public void execute(Runnable command) {

    if (command == null)

        throw new NullPointerException();

    if (poolSize >= corePoolSize || !addIfUnderCorePoolSize(command)) {

        if (runState == RUNNING && workQueue.offer(command)) {

            if (runState != RUNNING || poolSize == 0)

                ensureQueuedTaskHandled(command);

        }

        else if (!addIfUnderMaximumPoolSize(command))

            reject(command); // is shutdown or saturated

    }

}

这一段代码看起来挺简单的，其实这就是线程池最重要的一部分，如果能够完全理解这一块，线程池还是挺容易的。整个执行流程是这样的：

1. 如果任务command为空，则抛出空指针异常，返回。否则进行2。
2. 如果当前线程池大小 大于或等于 核心线程池大小，进行4。否则进行3。
3. 创建一个新工作队列（线程，参考上一节），成功直接返回，失败进行4。
4. 如果线程池正在运行并且任务加入线程池队列成功，进行5，否则进行7。
5. 如果线程池已经关闭或者线程池大小为0，进行6，否则直接返回。
6. 如果线程池已经关闭则执行拒绝策略返回，否则启动一个新线程来进行执行任务，返回。
7. 如果线程池大小 不大于 最大线程池数量，则启动新线程来进行执行，否则进行拒绝策略，结束。

文字描述步骤不够简单？下面图形详细表述了此过程。

![0](https://note.youdao.com/yws/res/10397/2CC5D0CAE4914E4CA4CF4399AEC71C62)

老实说这个图比上面步骤更难以理解，那么从何入手呢。

流程的入口很简单，我们就是要执行一个任务（Runnable command)，那么它的结束点在哪或者有哪几个？

根据左边这个图我们知道可能有以下几种出口：

（1）图中的P1、P7，我们根据这条路径可以看到，仅仅是将任务加入任务队列（offer(command)）了；

（2）图中的P3，这条路径不将任务加入任务队列，但是启动了一个新工作线程（Worker）进行扫尾操作，用户处理为空的任务队列；

（3）图中的P4，这条路径没有将任务加入任务队列，但是启动了一个新工作线程（Worker），并且工作现场的第一个任务就是当前任务；

（4）图中的P5、P6，这条路径没有将任务加入任务队列，也没有启动工作线程，仅仅是抛给了任务拒绝策略。P2是任务加入了任务队列却因为线程池已经关闭于是又从任务队列中删除，并且抛给了拒绝策略。

如果上面的解释还不清楚，可以去研究下面两段代码：

java.util.concurrent.ThreadPoolExecutor.addIfUnderCorePoolSize(Runnable)

java.util.concurrent.ThreadPoolExecutor.addIfUnderMaximumPoolSize(Runnable)

java.util.concurrent.ThreadPoolExecutor.ensureQueuedTaskHandled(Runnable)

那么什么时候一个任务被立即执行呢？

在线程池运行状态下，如果线程池大小 小于 核心线程池大小或者线程池已满（任务队列已满）并且线程池大小 小于 最大线程池大小（此时线程池大小 大于 核心线程池大小的），用程序描述为：

runState == RUNNING && ( poolSize < corePoolSize || poolSize < maxnumPoolSize && workQueue.isFull())

上面的条件就是一个任务能够被立即执行的条件。

有了execute的基础，我们看看ExecutorService中的几个submit方法的实现。

    public Future submit(Runnable task) {

        if (task == null) throw new NullPointerException();

        RunnableFuture ftask = newTaskFor(task, null);

        execute(ftask);

        return ftask;

    }

    public  Future submit(Runnable task, T result) {

        if (task == null) throw new NullPointerException();

        RunnableFuture ftask = newTaskFor(task, result);

        execute(ftask);

        return ftask;

    }

    public  Future submit(Callable task) {

        if (task == null) throw new NullPointerException();

        RunnableFuture ftask = newTaskFor(task);

        execute(ftask);

        return ftask;

    }

很简单，不是么？对于一个线程池来说复杂的地方也就在execute方法的执行流程。在下一节中我们来讨论下如何获取任务的执行结果，也就是Future类的使用和原理。

[Inside.java.concurrency 34.thread pool.part7_threadpoolexecutor_execute](http://www.slideshare.net/xylz/insidejavaconcurrency-34thread-poolpart7threadpoolexecutorexecute)

View more [documents](http://www.slideshare.net/) from [xylz](http://www.slideshare.net/xylz).