《Java 源码分析》：线程池 Future、RunnableFuture、FutureTask

在使用 ThreadPoolExecutor 使用 submit 提交任务后然后交给线程池中的线程去执行，是吧

在 ThreadPoolExecutor(其实是在 AbstractExecutorService 中) 有如下几个 submit 方法，

public Future submit(Runnable task) {

if (task == null) throw new NullPointerException();

RunnableFuture ftask = newTaskFor(task, null);

execute(ftask);

return ftask;

}

public Future submit(Runnable task, T result) {

if (task == null) throw new NullPointerException();

RunnableFuture ftask = newTaskFor(task, result);

execute(ftask);

return ftask;

}

public Future submit(Callable task) {

if (task == null) throw new NullPointerException();

RunnableFuture ftask = newTaskFor(task);

execute(ftask);

return ftask;

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

submit 然后调用 executor 方法，executor 方法的内部实现在上篇博文已经分析过了哈。

这篇博文并不是想探讨 submit 方法，而是想讨论下 submit 的返回值 Future 对象.

在 submit 方法中我们看见,有一行这样的代码

RunnableFuture ftask = newTaskFor(task);

1

这行代码的功能为：对我们的 task 进行了类型的转化,task 类型是 Runnable/Callable.转化成为了一个 RunnableFuture 对象.

根据 task 类型由于有两种 Runnable/Callable,分别有两种不同的重载方法 newTaskFor.如下:

protected RunnableFuture newTaskFor(Runnable runnable, T value) {

return new FutureTask(runnable, value);

}

protected RunnableFuture newTaskFor(Callable callable) {

return new FutureTask(callable);

}

1

2

3

4

5

6

从 newTaskFor 函数中可以看到,就是直接调用了 FutureTask 的有参构造函数.

FutureTask 是继承了 RunnableFuture 类来实现的.如下:

public class FutureTask implements RunnableFuture

1

下面来看下 RunnableFuture 类的内容,如下:

/*

作为 Runnable 的 Future。成功执行 run 方法可以完成 Future 并允许访问其结果。

*/

public interface RunnableFuture extends Runnable, Future {

/**

* Sets this Future to the result of its computation
* unless it has been cancelled.

*/

void run();

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

RunnableFuture 接口比较简单，继承了 Runnable、Future 接口。并只有一个 run 方法

回到上面的所谈论的 newTaskFor 函数，如下：

protected RunnableFuture newTaskFor(Runnable runnable, T value) {

return new FutureTask(runnable, value);

}

protected RunnableFuture newTaskFor(Callable callable) {

return new FutureTask(callable);

}

1

2

3

4

5

6

看下 FutureTask 类的构造方法的内部实现如下：

/**

* Creates a {@code FutureTask} that will, upon running, execute the
* given {@code Callable}.

*

* @param callable the callable task
* @throws NullPointerException if the callable is null

*/

public FutureTask(Callable callable) {

if (callable == null)

throw new NullPointerException();

this.callable = callable;

this.state = NEW; // ensure visibility of callable

}

/*

* Creates FutureTask that will, upon running, execute the
* given Runnable, and arrange that get will return the
* given result on successful completion.

创建一个 FutureTask 对象，执行的还是里面所包含的 Runnable 对象，

如果 Runnable 对象正常执行完成，则此 FutureTask 对象调用 get 方法的时候就会得到结果 reulst。

*/

public FutureTask(Runnable runnable, V result) {

this.callable = Executors.callable(runnable, result);

this.state = NEW; // ensure visibility of callable

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

在第二个构造函数中，我们看到了

this.callable = Executors.callable(runnable, result);

1

这行代码是将 Ruunbale 类型转换为了 Callable 类型。因此，我们看下 Executors.callable(runnable, result) 方法的实现，到底是如何转化的呢？？

/*

* Returns a {@link Callable} object that, when
* called, runs the given task and returns {@code null}.

*

*/

public static Callable callable(Runnable task) {

if (task == null)

throw new NullPointerException();

return new RunnableAdapter(task, null);

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

将 Runnable 适配为一个 Callable 对象， 转化为的对象虽然是 Callable 对象了，但是调用此对象的 call 方法其实就是调用了 Runnable 接口的 run 方法并且返回值是 null。

继续往下面看

看下 RunnableAdapter 类,此类实现了 Callable 接口。

// Non-public classes supporting the public methods

/**

* A callable that runs given task and returns given result

*/

static final class RunnableAdapter implements Callable {

final Runnable task;

final T result;

RunnableAdapter(Runnable task, T result) {

this.task = task;

this.result = result;

}

public T call() {

task.run();

return result;

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

总结一下上面的逻辑

1、首先，在我们写程序的时候，我们可能在线程池中的 submit 方法来提交一个任务 task，这个任务 task 可能是 Runnable 对象，也可能是 Callable 对象。为便于处理，我们需要将 Runnable、Callable 统一起来，因此，就借助了 Executors 类中的 RunnableAdapter 类（此类为一个适配器）来将 Runnable 对象适配为一个 Callable 对象。这一适配过程在 FutureTask 类的构造方法中完成。如何适配的呢？看上面的源代码。

2、而 submit 方法要求返回一个 Future 对象，我们可以通过这个对象来获取任务的运行结果。而 FutureTask 作为 Future 的实现类实现了对任务 task 的封装，并且可以通过封装后的对象获取返回值。

上面的关系理清楚之后，我们就重点来看下 FutureTask 类。

FutureTask 类分析

Future 及其相关的类结构图如下：

即 FutureTask 实现了 RunnableFuture 接口，而 RunnableFuture 继承了 Runnable, Future 接口，因此 FutureTask 也是实现了 Future 接口的哈，即具有 Future 的所有特性。

public class FutureTask implements RunnableFuture

public interface RunnableFuture extends Runnable, Future

1

2

3

4

不仅线程池有声明周期，回顾下，线程池的生命周期有：RUNNING SHUTDOWN STOP TIDYING TERMINATED 五个状态。

而 FutureTask 也存在生命周期。如下：

1、NEW（开始状态）

2、COMPLETING（正在运行状态）

3、NORMAL （正常运行完结束状态）

4、EXCEPTIONAL (异常状态)

5、CANCELLED （取消状态）

6、INTERRUPTING （中断）

7、INTERRUPTED （中断结束状态）

源码中对这几个状态以及状态之间的转换关系如下:

/**

* The run state of this task, initially NEW. The run state
* transitions to a terminal state only in methods set,
* setException, and cancel. During completion, state may take on
* transient values of COMPLETING (while outcome is being set) or
* INTERRUPTING (only while interrupting the runner to satisfy a
* cancel(true)). Transitions from these intermediate to final
* states use cheaper ordered/lazy writes because values are unique
* and cannot be further modified.

*

* Possible state transitions:
* NEW -> COMPLETING -> NORMAL
* NEW -> COMPLETING -> EXCEPTIONAL
* NEW -> CANCELLED
* NEW -> INTERRUPTING -> INTERRUPTED

*/

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

FutureTask 类中 get 方法介绍

当我们些如下的代码时：

Future f = pool.submit(new Runnable(){...});

...

Object obj = f.get();//获取任务的返回结果

1

2

3

4

Future 中的 get 方法获取结果时里面的内部实现是什么呢？下面一起来看看

/**

* @throws CancellationException {@inheritDoc}

*/

public V get() throws InterruptedException, ExecutionException {

int s = state;

if (s <= COMPLETING)//说明任务还正在执行，需要等待

//返回值为任务执行后的状态值，可能是正常执行完，也可能是中断抛出异常返回，也可能是超时返回

s = awaitDone(false, 0L);

return report(s);

}

/**

* @throws CancellationException {@inheritDoc}

*/

public V get(long timeout, TimeUnit unit)

throws InterruptedException, ExecutionException, TimeoutException {

if (unit == null)

throw new NullPointerException();

int s = state;

if (s <= COMPLETING &&

(s = awaitDone(true, unit.toNanos(timeout))) <= COMPLETING)

throw new TimeoutException();

return report(s);

}

/*

* Awaits completion or aborts on interrupt or timeout.
* 等待完成或者是抛出异常或者是等待时间到了

*/

private int awaitDone(boolean timed, long nanos)

throws InterruptedException {

final long deadline = timed ? System.nanoTime() + nanos : 0L;

WaitNode q = null;

boolean queued = false;

for (;;) {

if (Thread.interrupted()) {//检测线程是否中断

removeWaiter(q);

throw new InterruptedException();

}

int s = state;

if (s > COMPLETING) {//执行完了，可能是正常执行完，也可能是取消、中断了，等等

if (q != null)

q.thread = null;

return s;

}

else if (s == COMPLETING) // cannot time out yet 正在执行

Thread.yield();//等待

else if (q == null)

q = new WaitNode();

else if (!queued)

queued = UNSAFE.compareAndSwapObject(this, waitersOffset,

q.next = waiters, q);

else if (timed) {//检查等待是否超时了，如果超时，则自己返回此时的状态,否则继续挂起等待

nanos = deadline - System.nanoTime();

if (nanos <= 0L) {//如果超时，则自己返回此时的状态

removeWaiter(q);

return state;

}

LockSupport.parkNanos(this, nanos);

}

else

LockSupport.park(this);//上面条件如果都不满足，则唤醒该线程

}

}

/*

如果正常执行完，则返回结果，否则根据任务的状态抛出相应的异常

*/

@SuppressWarnings("unchecked")

private V report(int s) throws ExecutionException {

Object x = outcome;

if (s == NORMAL)

return (V)x;

if (s >= CANCELLED)

throw new CancellationException();

throw new ExecutionException((Throwable)x);

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

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

get 方法里面的逻辑相当的简单，就是检查任务是否已经执行完毕，如果没有，则等待期指定完毕，否则根据任务的状态来决定是否是抛相应的异常还是返回正确的结果。

FutureTask 类中其它一些和任务状态有关的方法

//任务是否已经取消了

public boolean isCancelled() {

return state >= CANCELLED;

}

//只要不是开始状态都是返回 true

public boolean isDone() {

return state != NEW;

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

FutureTask 类中的 cancel 方法如下,

1、任务当前状态不为初始状态，则返回 false

2、任务当前装填为初始状态，但是可能刚刚中断或者是取消而 CAS 操作不成功，也是返回 false。

3、如果允许中断，则中断任务，返回 true。

此方法返回后任务要么处于运行结束状态，要么处于取消状态。isDone() 将永远返回 true，如果 cancel() 方法返回 true，isCancelled() 始终返回 true。

public boolean cancel(boolean mayInterruptIfRunning) {

if (!(state == NEW &&

UNSAFE.compareAndSwapInt(this, stateOffset, NEW,

mayInterruptIfRunning ? INTERRUPTING : CANCELLED)))

return false;

try { // in case call to interrupt throws exception

if (mayInterruptIfRunning) {

try {

Thread t = runner;

if (t != null)

t.interrupt();

} finally { // final state

UNSAFE.putOrderedInt(this, stateOffset, INTERRUPTED);

}

}

} finally {

finishCompletion();

}

return true;

}

/**

* Removes and signals all waiting threads, invokes done(), and
* nulls out callable.

*/

private void finishCompletion() {

// assert state > COMPLETING;

for (WaitNode q; (q = waiters) != null;) {//唤醒等待的所有线程节点

if (UNSAFE.compareAndSwapObject(this, waitersOffset, q, null)) {

for (;;) {

Thread t = q.thread;

if (t != null) {

q.thread = null;

LockSupport.unpark(t);

}

WaitNode next = q.next;

if (next == null)

break;

q.next = null; // unlink to help gc

q = next;

}

break;

}

}

done();

callable = null; // to reduce footprint

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

以上就是关于 FutureTask 一点点的介绍。

小结

需要注意的是以下几点

1、Runnable 对象可以通过 RunnableAdapter 适配器适配到 Callable 对象

2、Future 对象可以通过 get 方法获取任务的返回值

3、FutureTask 可以简单来看是对任务 Runnable/Callable 的封装。

参考资料

1、http://www.blogjava.net/xylz/archive/2011/02/13/344207.html

---------------------

作者：HelloWorld_EE

来源：CSDN

原文：https://blog.csdn.net/u010412719/article/details/52137262

版权声明：本文为博主原创文章，转载请附上博文链接！
