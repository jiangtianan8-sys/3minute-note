CountDownLatch是计数器，只能使用一次，而CyclicBarrier的计数器提供reset功能，可以多次使用。但是我不那么认为它们之间的区别仅仅就是这么简单的一点。我们来从jdk作者设计的目的来看，javadoc是这么描述它们的：

CountDownLatch: A synchronization aid that allows one or more threads to wait until a set of operations being performed in other threads completes.(CountDownLatch: 一个或者多个线程，等待其他多个线程完成某件事情之后才能执行；) CyclicBarrier : A synchronization aid that allows a set of threads to all wait for each other to reach a common barrier point.(CyclicBarrier : 多个线程互相等待，直到到达同一个同步点，再继续一起执行。)

对于CountDownLatch来说，重点是“一个线程（多个线程）等待”，而其他的N个线程在完成“某件事情”之后，可以终止，也可以等待。而对于CyclicBarrier，重点是多个线程，在任意一个线程没有完成，所有的线程都必须等待。

CountDownLatch是计数器，线程完成一个记录一个，只不过计数不是递增而是递减，而CyclicBarrier更像是一个阀门，需要所有线程都到达，阀门才能打开，然后继续执行。

![0](https://note.youdao.com/yws/res/5027/047072A187A043DB80CFD9AC4C676201)

CyclicBarrier和CountDownLatch的区别这部分内容参考了如下两篇文章：

- [https://blog.csdn.net/u010185262/article/details/54692886](https://blog.csdn.net/u010185262/article/details/54692886)
- [https://blog.csdn.net/tolcf/article/details/50925145?utm_source=blogxgwz0](https://blog.csdn.net/tolcf/article/details/50925145?utm_source=blogxgwz0)

来源： [https://github.com/Snailclimb/JavaGuide/blob/master/Java/Multithread/AQS.md](https://github.com/Snailclimb/JavaGuide/blob/master/Java/Multithread/AQS.md)