首先，ThreadLocal 不是用来解决共享对象的多线程访问问题的，一般情况下，通过ThreadLocal.set() 到线程中的对象是该线程自己使用的对象，其他线程是不需要访问的，也访问不到的。各个线程中访问的是不同的对象。 

另外，说ThreadLocal使得各线程能够保持各自独立的一个对象，并不是通过ThreadLocal.set()来实现的，而是通过每个线程中的new 对象 的操作来创建的对象，每个线程创建一个，不是什么对象的拷贝或副本。通过ThreadLocal.set()将这个新创建的对象的引用保存到各线程的自己的一个map中，每个线程都有这样一个map，执行ThreadLocal.get()时，各线程从自己的map中取出放进去的对象，因此取出来的是各自自己线程中的对象，ThreadLocal实例是作为map的key来使用的。 

如果ThreadLocal.set()进去的东西本来就是多个线程共享的同一个对象，那么多个线程的ThreadLocal.get()取得的还是这个共享对象本身，还是有并发访问问题。 

下面来看一个hibernate中典型的ThreadLocal的应用： 

Java代码  

![0](https://note.youdao.com/yws/res/4981/43942B5E86A746B288D17F7F5416544A)

1. private static final ThreadLocal threadSession = new ThreadLocal();  

2. public static Session getSession() throws InfrastructureException {  
3.     Session s = (Session) threadSession.get();  
4.     try {  
5.         if (s == null) {  
6.             s = getSessionFactory().openSession();  
7.             threadSession.set(s);  
8.         }  
9.     } catch (HibernateException ex) {  
10.         throw new InfrastructureException(ex);  
11.     }  
12.     return s;  
13. }  

可以看到在getSession()方法中，首先判断当前线程中有没有放进去session，如果还没有，那么通过sessionFactory().openSession()来创建一个session，再将session set到线程中，实际是放到当前线程的ThreadLocalMap这个map中，这时，对于这个session的唯一引用就是当前线程中的那个ThreadLocalMap（下面会讲到），而threadSession作为这个值的key，要取得这个session可以通过threadSession.get()来得到，里面执行的操作实际是先取得当前线程中的ThreadLocalMap，然后将threadSession作为key将对应的值取出。这个session相当于线程的私有变量，而不是public的。 

显然，其他线程中是取不到这个session的，他们也只能取到自己的ThreadLocalMap中的东西。要是session是多个线程共享使用的，那还不乱套了。 

试想如果不用ThreadLocal怎么来实现呢？可能就要在action中创建session，然后把session一个个传到service和dao中，这可够麻烦的。或者可以自己定义一个静态的map，将当前thread作为key，创建的session作为值，put到map中，应该也行，这也是一般人的想法，但事实上，ThreadLocal的实现刚好相反，它是在每个线程中有一个map，而将ThreadLocal实例作为key，这样每个map中的项数很少，而且当线程销毁时相应的东西也一起销毁了，不知道除了这些还有什么其他的好处。 

总之，ThreadLocal不是用来解决对象共享访问问题的，而主要是提供了保持对象的方法和避免参数传递的方便的对象访问方式。归纳了两点： 

1。每个线程中都有一个自己的ThreadLocalMap类对象，可以将线程自己的对象保持到其中，各管各的，线程可以正确的访问到自己的对象。 

2。将一个共用的ThreadLocal静态实例作为key，将不同对象的引用保存到不同线程的ThreadLocalMap中，然后在线程执行的各处通过这个静态ThreadLocal实例的get()方法取得自己线程保存的那个对象，避免了将这个对象作为参数传递的麻烦。 

当然如果要把本来线程共享的对象通过ThreadLocal.set()放到线程中也可以，可以实现避免参数传递的访问方式，但是要注意get()到的是那同一个共享对象，并发访问问题要靠其他手段来解决。但一般来说线程共享的对象通过设置为某类的静态变量就可以实现方便的访问了，似乎没必要放到线程中。 

ThreadLocal的应用场合，我觉得最适合的是按线程多实例（每个线程对应一个实例）的对象的访问，并且这个对象很多地方都要用到。 

下面来看看ThreadLocal的实现原理（jdk1.5源码） 

Java代码  

![0](https://note.youdao.com/yws/res/4976/CDC7E3A140654158BFD6C8EAB33F4766)

1. public class ThreadLocal {  
2.     /** 
3.      * ThreadLocals rely on per-thread hash maps attached to each thread 
4.      * (Thread.threadLocals and inheritableThreadLocals).  The ThreadLocal 
5.      * objects act as keys, searched via threadLocalHashCode.  This is a 
6.      * custom hash code (useful only within ThreadLocalMaps) that eliminates 
7.      * collisions in the common case where consecutively constructed 
8.      * ThreadLocals are used by the same threads, while remaining well-behaved 
9.      * in less common cases. 
10.      */  
11.     private final int threadLocalHashCode = nextHashCode();  

12.     /** 
13.      * The next hash code to be given out. Accessed only by like-named method. 
14.      */  
15.     private static int nextHashCode = 0;  

16.     /** 
17.      * The difference between successively generated hash codes - turns 
18.      * implicit sequential thread-local IDs into near-optimally spread 
19.      * multiplicative hash values for power-of-two-sized tables. 
20.      */  
21.     private static final int HASH_INCREMENT = 0x61c88647;  

22.     /** 
23.      * Compute the next hash code. The static synchronization used here 
24.      * should not be a performance bottleneck. When ThreadLocals are 
25.      * generated in different threads at a fast enough rate to regularly 
26.      * contend on this lock, memory contention is by far a more serious 
27.      * problem than lock contention. 
28.      */  
29.     private static synchronized int nextHashCode() {  
30.         int h = nextHashCode;  
31.         nextHashCode = h + HASH_INCREMENT;  
32.         return h;  
33.     }  

34.     /** 
35.      * Creates a thread local variable. 
36.      */  
37.     public ThreadLocal() {  
38.     }  

39.     /** 
40.      * Returns the value in the current thread's copy of this thread-local 
41.      * variable.  Creates and initializes the copy if this is the first time 
42.      * the thread has called this method. 
43.      * 
44.      * @return the current thread's value of this thread-local 
45.      */  
46.     public T get() {  
47.         Thread t = Thread.currentThread();  
48.         ThreadLocalMap map = getMap(t);  
49.         if (map != null)  
50.             return (T)map.get(this);  

51.         // Maps are constructed lazily.  if the map for this thread  
52.         // doesn't exist, create it, with this ThreadLocal and its  
53.         // initial value as its only entry.  
54.         T value = initialValue();  
55.         createMap(t, value);  
56.         return value;  
57.     }  

58.     /** 
59.      * Sets the current thread's copy of this thread-local variable 
60.      * to the specified value.  Many applications will have no need for 
61.      * this functionality, relying solely on the {@link #initialValue} 
62.      * method to set the values of thread-locals. 
63.      * 
64.      * @param value the value to be stored in the current threads' copy of 
65.      *        this thread-local. 
66.      */  
67.     public void set(T value) {  
68.         Thread t = Thread.currentThread();  
69.         ThreadLocalMap map = getMap(t);  
70.         if (map != null)  
71.             map.set(this, value);  
72.         else  
73.             createMap(t, value);  
74.     }  

75.     /** 
76.      * Get the map associated with a ThreadLocal. Overridden in 
77.      * InheritableThreadLocal. 
78.      * 
79.      * @param  t the current thread 
80.      * @return the map 
81.      */  
82.     ThreadLocalMap getMap(Thread t) {  
83.         return t.threadLocals;  
84.     }  

85.     /** 
86.      * Create the map associated with a ThreadLocal. Overridden in 
87.      * InheritableThreadLocal. 
88.      * 
89.      * @param t the current thread 
90.      * @param firstValue value for the initial entry of the map 
91.      * @param map the map to store. 
92.      */  
93.     void createMap(Thread t, T firstValue) {  
94.         t.threadLocals = new ThreadLocalMap(this, firstValue);  
95.     }  

96.     .......  

97.     /** 
98.      * ThreadLocalMap is a customized hash map suitable only for 
99.      * maintaining thread local values. No operations are exported 
100.      * outside of the ThreadLocal class. The class is package private to 
101.      * allow declaration of fields in class Thread.  To help deal with 
102.      * very large and long-lived usages, the hash table entries use 
103.      * WeakReferences for keys. However, since reference queues are not 
104.      * used, stale entries are guaranteed to be removed only when 
105.      * the table starts running out of space. 
106.      */  
107.     static class ThreadLocalMap {  

108.     ........  

109.     }  

110. }  

可以看到ThreadLocal类中的变量只有这3个int型： 

Java代码  

![0](https://note.youdao.com/yws/res/4975/CBF9BC3ECAC94268957F6A5505A719B9)

1. private final int threadLocalHashCode = nextHashCode();  
2. private static int nextHashCode = 0;  
3. private static final int HASH_INCREMENT = 0x61c88647;  

而作为ThreadLocal实例的变量只有 threadLocalHashCode 这一个，nextHashCode 和HASH_INCREMENT 是ThreadLocal类的静态变量，实际上HASH_INCREMENT是一个常量，表示了连续分配的两个ThreadLocal实例的threadLocalHashCode值的增量，而nextHashCode 的表示了即将分配的下一个ThreadLocal实例的threadLocalHashCode 的值。 

可以来看一下创建一个ThreadLocal实例即new ThreadLocal()时做了哪些操作，从上面看到构造函数ThreadLocal()里什么操作都没有，唯一的操作是这句： 

Java代码  

![0](https://note.youdao.com/yws/res/4978/F0B8126F32604F4F92C52FFA17869569)

1. private final int threadLocalHashCode = nextHashCode();  

那么nextHashCode()做了什么呢： 

Java代码  

![0](https://note.youdao.com/yws/res/4982/39A8F73972BF4646A75ABD9132827427)

1. private static synchronized int nextHashCode() {  
2.     int h = nextHashCode;  
3.     nextHashCode = h + HASH_INCREMENT;  
4.     return h;  
5. }  

就是将ThreadLocal类的下一个hashCode值即nextHashCode的值赋给实例的threadLocalHashCode，然后nextHashCode的值增加HASH_INCREMENT这个值。 

因此ThreadLocal实例的变量只有这个threadLocalHashCode，而且是final的，用来区分不同的ThreadLocal实例，ThreadLocal类主要是作为工具类来使用，那么ThreadLocal.set()进去的对象是放在哪儿的呢？ 

看一下上面的set()方法，两句合并一下成为 

Java代码  

![0](https://note.youdao.com/yws/res/4980/6AB6C7716A7640F3954172C3E6B63FC0)

1. ThreadLocalMap map = Thread.currentThread().threadLocals;  

这个ThreadLocalMap 类是ThreadLocal中定义的内部类，但是它的实例却用在Thread类中： 

Java代码  

![0](https://note.youdao.com/yws/res/4979/47B82A5F1AE14A8AA02325F3FE3070B8)

1. public class Thread implements Runnable {  
2.     ......  

3.     /* ThreadLocal values pertaining to this thread. This map is maintained 
4.      * by the ThreadLocal class. */  
5.     ThreadLocal.ThreadLocalMap threadLocals = null;    
6.     ......  
7. }  

再看这句： 

Java代码  

![0](https://note.youdao.com/yws/res/4977/DC9FF621A1A34F85B5235284F9F70877)

1. if (map != null)  
2.     map.set(this, value);  

也就是将该ThreadLocal实例作为key，要保持的对象作为值，设置到当前线程的ThreadLocalMap 中，get()方法同样大家看了代码也就明白了，ThreadLocalMap 类的代码太多了，我就不帖了，自己去看源码吧。 

写了这么多，也不知讲明白了没有，有什么不当的地方还请大家指出来。

来源： [http://www.iteye.com/topic/103804](http://www.iteye.com/topic/103804)