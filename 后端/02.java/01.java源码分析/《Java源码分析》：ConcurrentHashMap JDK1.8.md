《Java 源码分析》：ConcurrentHashMap JDK1.8

最近一直在看关于 J.U.C 中的源码，了解原子操作，了解锁机制，了解多线程并发等等。但是 ConcurrentHashMap 一直拖着到今天才算告一段落。

也要感谢 ConcurrentHashMap 这个类，刚开始就是想弄懂里面的工作原理，但是，无奈看了网上关于介绍 ConcurrentHashMap 这个类的资料或博客都是基于 JDK1.8 以前的，而刚好此类在 JDK1.8 之后有很大的变化。因此，由于里面涉及到关于原子操作 CAS，自己以前并不知道是什么，于是就开始对原子操作进行了解，看了 java.util.concurrent.atom 包下相关类源码对其有了一定的了解。接着为了了解锁机制，看了 java.util.concurrent.lock 包下相关的类库，对锁机制有了大概的了解之后，看了线程池相关的类，对线程池也有了一定的了解。

关于阻塞队列相关的类，自己也大致看了下，但是并没有形成相应的博文，以后有时间重新来了解他们的时候才记录吧。整个过程大概花费了我将近一个来月的时间，虽然对看过的类库的内部实现都只是一个大致的了解，但是确实收获还是挺多的。让我们更好的明白在多线程并发中他们是如何来工作的。

回到正题，刚好借着今天星期天，花了将近一天的时间来看 ConcurrentHashMap 的实现原理，总算看了一个大概，有了一个大致的了解。也就有了这篇博文。

ConcurrentHashMap 在 JDK1.8 版本以前的实现原理

既然本篇博文的标题明确的标出了是基于 JDK1.8 版本的，也就暗示了这个版本和以前的版本关于 ConcurrentHashMap 有些许的不同，对吧。x

下面我们就先借助网上的资料来看下以前版本的 ConcurrentHashMap 的实现思路。

我们都知道 HashMap 是线程不安全的。Hashtable 是线程安全的。看过 Hashtable 源码的我们都知道 Hashtable 的线程安全是采用在每个方法来添加了 synchronized 关键字来修饰，即 Hashtable 是针对整个 table 的锁定，这样就导致 HashTable 容器在竞争激烈的并发环境下表现出效率低下。

效率低下的原因说的更详细点：是因为所有访问 HashTable 的线程都必须竞争同一把锁。当一个线程访问 HashTable 的同步方法时，其他线程访问 HashTable 的同步方法时，可能会进入阻塞或轮询状态。如线程 1 使用 put 进行添加元素，线程 2 不但不能使用 put 方法添加元素，并且也不能使用 get 方法来获取元素，所以竞争越激烈效率越低。

基于 Hashtable 的缺点，人们就开始思考，假如容器里有多把锁，每一把锁用于锁容器其中一部分数据，那么当多线程访问容器里不同数据段的数据时，线程间就不会存在锁竞争，从而可以有效的提高并发访问效率呢？？这就是我们的“锁分离”技术，这也是 ConcurrentHashMap 实现的基础。

ConcurrentHashMap 使用的就是锁分段技术，ConcurrentHashMap 由多个 Segment 组成 (Segment 下包含很多 Node，也就是我们的键值对了)，每个 Segment 都有把锁来实现线程安全，当一个线程占用锁访问其中一个段数据的时候，其他段的数据也能被其他线程访问。

因此，关于 ConcurrentHashMap 就转化为了对 Segment 的研究。这是因为，ConcurrentHashMap 的 get、put 操作是直接委托给 Segment 的 get、put 方法，但是自己上手上的 JDK1.8 的具体实现确不想网上这些博文所介绍的。因此，就有了本篇博文的介绍。

推荐几个 JDK1.8 以前版本的关于 ConcurrentHashMap 的原理分析，方便大家比较。

1、[http://www.iteye.com/topic/344876](http://www.iteye.com/topic/344876)

2、[http://ifeve.com/concurrenthashmap/](http://ifeve.com/concurrenthashmap/)

如需要更多，请自己网上搜索即可。

下面就开始 JDK1.8 版本中 ConcurrentHashMap 的介绍。

JDK1.8 版本中 ConcurrentHashMap 介绍 1、前言

首先要说明的几点：

1、JDK1.8 的 ConcurrentHashMap 中 Segment 虽保留，但已经简化属性，仅仅是为了兼容旧版本。

2、ConcurrentHashMap 的底层与 Java1.8 的 HashMap 有相通之处，底层依然由“数组”+ 链表 + 红黑树来实现的，底层结构存放的是 TreeBin 对象，而不是 TreeNode 对象；

3、ConcurrentHashMap 实现中借用了较多的 CAS 算法，unsafe.compareAndSwapInt(this, valueOffset, expect, update); CAS(Compare And Swap)，意思是如果 valueOffset 位置包含的值与 expect 值相同，则更新 valueOffset 位置的值为 update，并返回 true，否则不更新，返回 false。

ConcurrentHashMap 既然借助了 CAS 来实现非阻塞的无锁实现线程安全，那么是不是就没有用锁了呢？？答案：还是使用了 synchronized 关键字进行同步了的，在哪里使用了呢？在操作 hash 值相同的链表的头结点还是会 synchronized 上锁，这样才能保证线程安全。

看完 ConcurrentHashMap 整个类的源码，给自己的感觉就是和 HashMap 的实现基本一模一样，当有修改操作时借助了 synchronized 来对 table[i] 进行锁定保证了线程安全以及使用了 CAS 来保证原子性操作，其它的基本一致，例如：ConcurrentHashMap 的 get(int key) 方法的实现思路为：根据 key 的 hash 值找到其在 table 所对应的位置 i,然后在 table[i] 位置所存储的链表 (或者是树) 进行查找是否有键为 key 的节点，如果有，则返回节点对应的 value，否则返回 null。思路是不是很熟悉，是不是和 HashMap 中该方法的思路一样。所以，如果你也在看 ConcurrentHashMap 的源码，不要害怕，思路还是原来的思路，只是多了些许东西罢了。

2、ConcurrentHashMap 类中相关属性的介绍

为了方便介绍此类后面的实现，这里需要先将此类中的一些属性给介绍下。

sizeCtl 最重要的属性之一，看源码之前，这个属性表示什么意思，一定要记住。

0、private transient volatile int sizeCtl;//控制标识符

此属性在源码中给出的注释如下：

    /**

      * Table initialization and resizing control. When negative, the

      * table is being initialized or resized: -1 for initialization,

      * else -(1 + the number of active resizing threads). Otherwise,

      * when table is null, holds the initial table size to use upon

      * creation, or 0 for default. After initialization, holds the

      * next element count value upon which to resize the table.

      */

翻译如下：

sizeCtl 是控制标识符，不同的值表示不同的意义。

- 负数代表正在进行初始化或扩容操作 ,其中 -1 代表正在初始化 ,-N 表示有 N-1 个线程正在进行扩容操作
- 正数或 0 代表 hash 表还没有被初始化，这个数值表示初始化或下一次进行扩容的大小，类似于扩容阈值。它的值始终是当前 ConcurrentHashMap 容量的 0.75 倍，这与 loadfactor 是对应的。实际容量>=sizeCtl，则扩容。

1、 transient volatile Node[] table; 是一个容器数组，第一次插入数据的时候初始化，大小是 2 的幂次方。这就是我们所说的底层结构：”数组 + 链表（或树）”

2、private static final int MAXIMUM_CAPACITY = 1 << 30; // 最大容量

3、private static final intDEFAULT_CAPACITY = 16;

4、static final int MAX_ARRAY_SIZE = Integer.MAX_VALUE - 8; // MAX_VALUE=2^31-1=2147483647

5、private static finalint DEFAULT_CONCURRENCY_LEVEL = 16;

6、private static final float LOAD_FACTOR = 0.75f;

7、static final int TREEIFY_THRESHOLD = 8; // 链表转树的阀值，如果 table[i] 下面的链表长度大于 8 时就转化为数

8、static final int UNTREEIFY_THRESHOLD = 6; //树转链表的阀值，小于等于 6 是转为链表，仅在扩容 tranfer 时才可能树转链表

9、static final int MIN_TREEIFY_CAPACITY = 64;

10、private static final int MIN_TRANSFER_STRIDE = 16;

11、private static int RESIZE_STAMP_BITS = 16;

12、private static final int MAX_RESIZERS = (1 << (32 - RESIZE_STAMP_BITS)) - 1; // help resize 的最大线程数

13、private static final int RESIZE_STAMP_SHIFT = 32 - RESIZE_STAMP_BITS;

14、static final int MOVED = -1; // hash for forwarding nodes（forwarding nodes 的 hash 值）、标示位

15、static final int TREEBIN = -2; // hash for roots of trees（树根节点的 hash 值）

16、static final int RESERVED = -3; // hash for transient reservations（ReservationNode 的 hash 值）

3、ConcurrentHashMap 的构造函数

和往常一样，我们还是从类的构造函数开始说起。

  ```java

  /**

    * Creates a new, empty map with the default initial table size (16).

    */

   public ConcurrentHashMap() {

  }

   public ConcurrentHashMap(int initialCapacity) {

       if (initialCapacity < 0)

           throw new IllegalArgumentException();

       int cap = ((initialCapacity >= (MAXIMUM_CAPACITY >>> 1)) ?

                  MAXIMUM_CAPACITY :

                  tableSizeFor(initialCapacity + (initialCapacity >>> 1) + 1));

       this.sizeCtl = cap;

  }

   /*

    * Creates a new map with the same mappings as the given map.

    *

    */

   public ConcurrentHashMap(Map m) {

       this.sizeCtl = DEFAULT_CAPACITY;

       putAll(m);

  }

   public ConcurrentHashMap(int initialCapacity, float loadFactor) {

       this(initialCapacity, loadFactor, 1);

  }

   public ConcurrentHashMap(int initialCapacity,

                            float loadFactor, int concurrencyLevel) {

       if (!(loadFactor > 0.0f) || initialCapacity < 0 || concurrencyLevel <= 0)

           throw new IllegalArgumentException();

       if (initialCapacity < concurrencyLevel)   // Use at least as many bins

           initialCapacity = concurrencyLevel;   // as estimated threads

       long size = (long)(1.0 + (long)initialCapacity / loadFactor);

       int cap = (size >= (long)MAXIMUM_CAPACITY) ?

           MAXIMUM_CAPACITY : tableSizeFor((int)size);

       this.sizeCtl = cap;

  }

  ```

有过 HashMap 和 Hashtable 源码经历，看这些构造函数是不是相当 easy 哈。

上面的构造函数主要干了两件事：

1、参数的有效性检查

2、table 初始化的长度 (如果不指定默认情况下为 16)。

这里要说一个参数：concurrencyLevel，表示能够同时更新 ConccurentHashMap 且不产生锁竞争的最大线程数。默认值为 16，(即允许 16 个线程并发可能不会产生竞争)。为了保证并发的性能，我们要很好的估计出 concurrencyLevel 值，不然要么竞争相当厉害，从而导致线程试图写入当前锁定的段时阻塞。

ConcurrentHashMap 类中相关节点类：Node/TreeNode/TreeBin

1、Node 类

Node 类是 table 数组中的存储元素，即一个 Node 对象就代表一个键值对 (key,value) 存储在 table 中。

Node 类是没有提供修改入口的 (唯一的 setValue 方法抛异常)，因此只能用于只读遍历。

此类的具体代码如下：

   ```java

   /*

    *Node 类是没有提供修改入口的 (setValue 方法抛异常，供子类实现)，

    即是可读的。只能用于只读遍历。

    */

   static class Node implements Map.Entry {

       final int hash;

       final K key;

       volatile V val;//volatile，保证可见性

       volatile Node next;

       Node(int hash, K key, V val, Node next) {

           this.hash = hash;

           this.key = key;

           this.val = val;

           this.next = next;

      }

       public final K getKey()       { return key; }

       public final V getValue()     { return val; }

       /*

          HashMap 中 Node 类的 hashCode() 方法中的代码为：Objects.hashCode(key) ^ Objects.hashCode(value)

          而 Objects.hashCode(key) 最终也是调用了 key.hashCode()，因此，效果一样。写法不一样罢了

      */;

       public final int hashCode()   { return key.hashCode() ^ val.hashCode(); }

       public final String toString(){ return key + "=" + val; }

       public final V setValue(V value) { // 不允许修改 value 值，HashMap 允许

           throw new UnsupportedOperationException();

      }

       /*

            HashMap 使用 if (o == this)，且嵌套 if；ConcurrentHashMap 使用&&

            个人觉得 HashMap 格式的代码更好阅读和理解

      */

       public final boolean equals(Object o) {

           Object k, v, u; Map.Entry e;

           return ((o instanceof Map.Entry) &&

                  (k = (e = (Map.Entry)o).getKey()) != null &&

                  (v = e.getValue()) != null &&

                  (k == key || k.equals(key)) &&

                  (v == (u = val) || v.equals(u)));

      }

       /*

        * Virtualized support for map.get(); overridden in subclasses.

        * 增加 find 方法辅助 get 方法 ，HashMap 中的 Node 类中没有此方法

        */

       Node find(int h, Object k) {

           Node e = this;

           if (k != null) {

               do {

                   K ek;

                   if (e.hash == h &&

                      ((ek = e.key) == k || (ek != null && k.equals(ek))))

                       return e;

              } while ((e = e.next) != null);

          }

           return null;

      }

  }

   ```

我们在看这个类时，可以与 HashMap 中的 Node 类的具体代码进行比较，发现在具体的实现上，有一定的细微的区别。

例如：在 ConcurrentHashMap.Node 的 hashCode 的代码是这样的：

    public final int hashCode()   { return key.hashCode() ^ val.hashCode(); }

1

而 HashMap.Node 的 hashCode 的代码是这样的：

```java
public final int hashCode() {

               return Objects.hashCode(key) ^ Objects.hashCode(value);

          }
```

而 Objects.hashCode(key) 最终也是调用了 key.hashCode()，因此，两者的效果一样，写法不一样罢了。

除了 hashCode 方法有一点差别，Node 类中的 find 方法在两个类的实现中的写法也不一样。

2、TreeNode

 ```java

 /*

    * Nodes for use in TreeBins

    */

   static final class TreeNode extends Node {

       TreeNode parent;  // red-black tree links

       TreeNode left;

       TreeNode right;

       TreeNode prev;    // needed to unlink next upon deletion

       boolean red;

       TreeNode(int hash, K key, V val, Node next,

                TreeNode parent) {

           super(hash, key, val, next);

           this.parent = parent;

      }

       Node find(int h, Object k) {

           return findTreeNode(h, k, null);

      }

       /*

        * Returns the TreeNode (or null if not found) for the given key

        * starting at given root.

        * 根据给定的 key 值从 root 节点出发找出节点

        *

        */

       final TreeNode findTreeNode(int h, Object k, Class kc) {

           if (k != null) {//HashMap 没有非空判断

               TreeNode p = this;

               do {

                   int ph, dir; K pk; TreeNode q;

                   TreeNode pl = p.left, pr = p.right;

                   if ((ph = p.hash) > h)

                       p = pl;

                   else if (ph < h)

                       p = pr;

                   else if ((pk = p.key) == k || (pk != null && k.equals(pk)))

                       return p;

                   else if (pl == null)

                       p = pr;

                   else if (pr == null)

                       p = pl;

                   else if ((kc != null ||

                            (kc = comparableClassFor(k)) != null) &&

                            (dir = compareComparables(kc, k, pk)) != 0)

                       p = (dir < 0) ? pl : pr;

                   else if ((q = pr.findTreeNode(h, k, kc)) != null)

                       return q;

                   else

                       p = pl;

              } while (p != null);

          }

           return null;

      }

  }

 ```

和 HashMap 相比，这里的 TreeNode 相当简洁；ConcurrentHashMap 链表转树时，并不会直接转， 

正如注释（Nodes for use in TreeBins）所说，只是把这些节点包装成 TreeNode 放到 TreeBin 中， 

再由 TreeBin 来转化红黑树。红黑树不理解没关系，并不影响看 ConcurrentHashMap 的内部实现

3、TreeBins

TreeBin 用于封装维护 TreeNode，包含 putTreeVal、lookRoot、UNlookRoot、remove、balanceInsetion、balanceDeletion 等方法，当链表转树时，用于封装 TreeNode，也就是说，ConcurrentHashMap 的红黑树存放的时 TreeBin，而不是 treeNode。

TreeBins 类代码太长，截取部分代码如下：

```java
static final class TreeBin extends Node {

       TreeNode root;

       volatile TreeNode first;

       volatile Thread waiter;

       volatile int lockState;

       // values for lockState

       static final int WRITER = 1; // set while holding write lock

       static final int WAITER = 2; // set when waiting for write lock

       static final int READER = 4; // increment value for setting read lock

       /**

        * Creates bin with initial set of nodes headed by b.

        */

       TreeBin(TreeNode b) {

           super(TREEBIN, null, null, null);

           this.first = b;

           TreeNode r = null;

           for (TreeNode x = b, next; x != null; x = next) {

               next = (TreeNode)x.next;

               x.left = x.right = null;

               if (r == null) {

                   x.parent = null;

                   x.red = false;

                   r = x;

              }

               else {

                   K k = x.key;

                   int h = x.hash;

                   Class kc = null;

                   for (TreeNode p = r;;) {

                       int dir, ph;

                       K pk = p.key;

                       if ((ph = p.hash) > h)

                           dir = -1;

                       else if (ph < h)

                           dir = 1;

                       else if ((kc == null &&

                                (kc = comparableClassFor(k)) == null) ||

                                (dir = compareComparables(kc, k, pk)) == 0)

                           dir = tieBreakOrder(k, pk);

                           TreeNode xp = p;

                       if ((p = (dir <= 0) ? p.left : p.right) == null) {

                           x.parent = xp;

                           if (dir <= 0)

                               xp.left = x;

                           else

                               xp.right = x;

                           r = balanceInsertion(r, x);

                           break;

                      }

                  }

              }

          }

           this.root = r;

           assert checkInvariants(root);

      }

       //……..other methods

  }
```

5、ForwardingNode：在 transfer 操作中，将一个节点插入到桶中

```java
/*

    * A node inserted at head of bins during transfer operations.

    * 在 transfer 操作中，一个节点插入到 bins 中

    */

   static final class ForwardingNode extends Node {

       final Node[] nextTable;

       ForwardingNode(Node[] tab) {

           //Node(int hash, K key, V val, Node next) 是 Node 类的构造函数

           super(MOVED, null, null, null);

           this.nextTable = tab;

      }

       Node find(int h, Object k) {

           // loop to avoid arbitrarily deep recursion on forwarding nodes

           outer: for (Node[] tab = nextTable;;) {

               Node e; int n;

               if (k == null || tab == null || (n = tab.length) == 0 ||

                  (e = tabAt(tab, (n - 1) & h)) == null)

                   return null;

               for (;;) {

                   int eh; K ek;

                   if ((eh = e.hash) == h &&

                      ((ek = e.key) == k || (ek != null && k.equals(ek))))

                       return e;

                   if (eh < 0) {

                       if (e instanceof ForwardingNode) {

                           tab = ((ForwardingNode)e).nextTable;

                           continue outer;

                      }

                       else

                           return e.find(h, k);

                  }

                   if ((e = e.next) == null)

                       return null;

              }

          }

      }

  }
```

ConcurrentHashMap 类中的 put(K key, V value) 方法的原理分析

我们对 Node、TreeNode、TreeBin 有一点认识后，我们就可以看下 ConcurrentHashMap 类的 put 方法是如何来实现的了，这里给出一个建议，关于容器我们用的最多的就是 put、get 方法了，我们看源码的实现，我们核心要关注的就是 put、get 方法的实现，只要我们弄懂这两个方法实现，这个类的大概实现思想我们也就知道了哈

基于此，我们就先来看 ConcurrentHashMap 类的 put 方法

put(K key, V value) 方法的功能：将制定的键值对映射到 table 中，key/value 均不能为 null

put 方法的代码如下：

```java
public V put(K key, V value) {

       return putVal(key, value, false);

  }
```

由于直接是调用了 putVal(key, value, false) 方法，那就我们就继续看。

putVal(key, value, false) 方法的代码如下：

```java
/** Implementation for put and putIfAbsent */

   final V putVal(K key, V value, boolean onlyIfAbsent) {

       if (key == null || value == null) throw new NullPointerException();

       int hash = spread(key.hashCode());//计算 hash 值，两次 hash 操作

       int binCount = 0;

       for (Node[] tab = table;;) {//类似于 while(true)，死循环，直到插入成功

           Node f; int n, i, fh;

           if (tab == null || (n = tab.length) == 0)//检查是否初始化了，如果没有，则初始化

               tab = initTable();

               /*

                  i=(n-1)&hash 等价于 i=hash%n(前提是 n 为 2 的幂次方).即取出 table 中位置的节点用 f 表示。

                  有如下两种情况：

                  1、如果 table[i]==null(即该位置的节点为空，没有发生碰撞)，则利用 CAS 操作直接存储在该位置，

                      如果 CAS 操作成功则退出死循环。

                  2、如果 table[i]!=null(即该位置已经有其它节点，发生碰撞)

              */

           else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {

               if (casTabAt(tab, i, null,

                            new Node(hash, key, value, null)))

                   break;                   // no lock when adding to empty bin

          }

           else if ((fh = f.hash) == MOVED)//检查 table[i] 的节点的 hash 是否等于 MOVED，如果等于，则检测到正在扩容，则帮助其扩容

               tab = helpTransfer(tab, f);//帮助其扩容

           else {//运行到这里，说明 table[i] 的节点的 hash 值不等于 MOVED。

               V oldVal = null;

               synchronized (f) {//锁定,（hash 值相同的链表的头节点）

                   if (tabAt(tab, i) == f) {//避免多线程，需要重新检查

                       if (fh >= 0) {//链表节点

                           binCount = 1;

                           /*

                          下面的代码就是先查找链表中是否出现了此 key，如果出现，则更新 value，并跳出循环，

                          否则将节点加入到里阿尼报末尾并跳出循环

                          */

                           for (Node e = f;; ++binCount) {

                               K ek;

                               if (e.hash == hash &&

                                  ((ek = e.key) == key ||

                                    (ek != null && key.equals(ek)))) {

                                   oldVal = e.val;

                                   if (!onlyIfAbsent)//仅 putIfAbsent() 方法中 onlyIfAbsent 为 true

                                       e.val = value;//putIfAbsent() 包含 key 则返回 get，否则 put 并返回  

                                   break;

                              }

                               Node pred = e;

                               if ((e = e.next) == null) {//插入到链表末尾并跳出循环

                                   pred.next = new Node(hash, key,

                                                             value, null);

                                   break;

                              }

                          }

                      }

                       else if (f instanceof TreeBin) { //树节点，

                           Node p;

                           binCount = 2;

                           if ((p = ((TreeBin)f).putTreeVal(hash, key,

                                                          value)) != null) {//插入到树中

                               oldVal = p.val;

                               if (!onlyIfAbsent)

                                   p.val = value;

                          }

                      }

                  }

              }

               //插入成功后，如果插入的是链表节点，则要判断下该桶位是否要转化为树

               if (binCount != 0) {

                   if (binCount >= TREEIFY_THRESHOLD)//实则是>8,执行 else,说明该桶位本就有 Node

                       treeifyBin(tab, i);//若 length<64,直接 tryPresize,两倍 table.length; 不转树

                   if (oldVal != null)

                       return oldVal;

                   break;

              }

          }

      }

       addCount(1L, binCount);

       return null;

  }
```

代码比较长哈，但是不要怕，我刚开始看的时候，也被长度给吓住了，怎么可以有这么长的方法呢，HashMap 中 put 方法的长度就很短的么。

虽然很长，但是思路相当的简单。代码详细流程如下,在上面代码中也有详细的注释

/* putVal(K key, V value, boolean onlyIfAbsent) 方法干的工作如下： 1、检查 key/value 是否为空，如果为空，则抛异常，否则进行 2 2、进入 for 死循环，进行 3 3、检查 table 是否初始化了，如果没有，则调用 initTable() 进行初始化然后进行 2，否则进行 4 4、根据 key 的 hash 值计算出其应该在 table 中储存的位置 i，取出 table[i] 的节点用 f 表示。 根据 f 的不同有如下三种情况：1）如果 table[i]==null(即该位置的节点为空，没有发生碰撞)， 则利用 CAS 操作直接存储在该位置，如果 CAS 操作成功则退出死循环。 2）如果 table[i]!=null(即该位置已经有其它节点，发生碰撞)，碰撞处理也有两种情况 2.1）检查 table[i] 的节点的 hash 是否等于 MOVED，如果等于，则检测到正在扩容，则帮助其扩容 2.2）说明 table[i] 的节点的 hash 值不等于 MOVED，如果 table[i] 为链表节点，则将此节点插入链表中即可 如果 table[i] 为树节点，则将此节点插入树中即可。插入成功后，进行 5 5、如果 table[i] 的节点是链表节点，则检查 table 的第 i 个位置的链表是否需要转化为数，如果需要则调用 treeifyBin 函数进行转化 */

可能你觉得上面的详细流程也比较多哈，但是不要怕，用两句话来总结的话，是如下的两步：

1、第一步根据给定的 key 的 hash 值找到其在 table 中的位置 index。

2、找到位置 index 后，存储进行就好了。

只是这里的存储有三种情况罢了，第一种：table[index] 中没有任何其他元素，即此元素没有发生碰撞，这种情况直接存储就好了哈。第二种，table[i] 存储的是一个链表，如果链表不存在 key 则直接加入到链表尾部即可，如果存在 key 则更新其对应的 value。第三种，table[i] 存储的是一个树，则按照树添加节点的方法添加就好。

在 putVal 函数，出现了如下几个函数

1、casTabAt tabAt 等 CAS 操作

2、initTable 作用是初始化 table 数组

3、treeifyBin 作用是将 table[i] 的链表转化为树

下面将分别进行介绍。

这里给出第二个建议，当一个类的代码量相当大且复杂时，从我们感兴趣的方法出发，然后是遇到哪个方法就才解决哪个方法

3 个用的比较多的 CAS 操作：casTabAt tabAt setTabAt

```java
/*

      3 个用的比较多的 CAS 操作

  */

   @SuppressWarnings("unchecked") // ASHIFT 等均为 private static final  

   static final Node tabAt(Node[] tab, int i) { // 获取索引 i 处 Node  

       return (Node)U.getObjectVolatile(tab, ((long)i << ASHIFT) + ABASE);  

  }  

   // 利用 CAS 算法设置 i 位置上的 Node 节点（将 c 和 table[i] 比较，相同则插入 v）。  

   static final boolean casTabAt(Node[] tab, int i,  

                                       Node c, Node v) {  

       return U.compareAndSwapObject(tab, ((long)i << ASHIFT) + ABASE, c, v);  

  }  

   // 设置节点位置的值，仅在上锁区被调用  

   static final void setTabAt(Node[] tab, int i, Node v) {  

       U.putObjectVolatile(tab, ((long)i << ASHIFT) + ABASE, v);  

  }
```

initTable() terrifyBin 方法

在 putVal 方法中遇到的第一个扩容函数为：initTable，即初始化

代码如下，注释相当详细，这里就不再解释。

```java
/**

    * Initializes table, using the size recorded in sizeCtl.

    */

   private final Node[] initTable() {

       Node[] tab; int sc;

       while ((tab = table) == null || tab.length == 0) {

           if ((sc = sizeCtl) < 0)//如果 sizeCtl 为负数，则说明已经有其它线程正在进行扩容，即正在初始化或初始化完成

               Thread.yield(); // lost initialization race; just spin

               //如果 CAS 成功，则表示正在初始化，设置为 -1，否则说明其它线程已经对其正在初始化或是已经初始化完毕

           else if (U.compareAndSwapInt(this, SIZECTL, sc, -1)) {

               try {

                   if ((tab = table) == null || tab.length == 0) {//再一次检查确认是否还没有初始化

                       int n = (sc > 0) ? sc : DEFAULT_CAPACITY;

                       @SuppressWarnings("unchecked")

                       Node[] nt = (Node[])new Node[n];

                       table = tab = nt;

                       sc = n - (n >>> 2);//即 sc = 0.75n。

                  }

              } finally {

                   sizeCtl = sc;//sizeCtl = 0.75*Capacity,为扩容门限

              }

               break;

          }

      }

       return tab;

  }
```

treeifyBin 方法：将数组 tab 的第 index 位置的链表转化为 树

```java
/*

    * 链表转树：将将数组 tab 的第 index 位置的链表转化为 树

    */

   private final void treeifyBin(Node[] tab, int index) {

       Node b; int n, sc;

       if (tab != null) {

           if ((n = tab.length) < MIN_TREEIFY_CAPACITY)// 容量<64，则 table 两倍扩容，不转树了

               tryPresize(n << 1);

           else if ((b = tabAt(tab, index)) != null && b.hash >= 0) {

               synchronized (b) { // 读写锁  

                   if (tabAt(tab, index) == b) {

                       TreeNode hd = null, tl = null;

                       for (Node e = b; e != null; e = e.next) {

                           TreeNode p =

                               new TreeNode(e.hash, e.key, e.val,

                                                 null, null);

                           if ((p.prev = tl) == null)

                               hd = p;

                           else

                               tl.next = p;

                           tl = p;

                      }

                       setTabAt(tab, index, new TreeBin(hd));

                  }

              }

          }

      }

  }
```

treeifyBin 方法的思想也相当的简单，如下：

1、检查下 table 的长度是否大于等于 MIN_TREEIFY_CAPACITY（64），如果不大于，则调用 tryPresize 方法将 table 两倍扩容就可以了，就不降链表转化为树了。如果大于，则就将 table[i] 的链表转化为树。

tryPresize 方法

在 putVal 方法中遇到的第二个扩容函数为：tryPresize

```java
/*

      扩容相关

      tryPresize 在 putAll 以及 treeifyBin 中调用

  */

   private final void tryPresize(int size) {

       // 给定的容量若>=MAXIMUM_CAPACITY 的一半，直接扩容到允许的最大值，否则调用 tableSizeFor 函数扩容

       int c = (size >= (MAXIMUM_CAPACITY >>> 1)) ? MAXIMUM_CAPACITY :

           tableSizeFor(size + (size >>> 1) + 1);//tableSizeFor(count) 的作用是找到大于等于 count 的最小的 2 的幂次方

       int sc;

       while ((sc = sizeCtl) >= 0) {//只有大于等于 0 才表示该线程可以扩容，具体看 sizeCtl 的含义

           Node[] tab = table; int n;

           if (tab == null || (n = tab.length) == 0) {//没有被初始化

               n = (sc > c) ? sc : c;

               // 期间没有其他线程对表操作，则 CAS 将 SIZECTL 状态置为 -1，表示正在进行初始化  

               if (U.compareAndSwapInt(this, SIZECTL, sc, -1)) {

                   try {

                       if (table == tab) {//再一次检查

                           @SuppressWarnings("unchecked")

                           Node[] nt = (Node[])new Node[n];

                           table = nt;

                           sc = n - (n >>> 2);//无符号右移 2 位，此即 0.75*n

                      }

                  } finally {

                       sizeCtl = sc;// 更新扩容阀值  

                  }

              }

          }

           // 若欲扩容值不大于原阀值，或现有容量>=最值，什么都不用做了

           else if (c <= sc || n >= MAXIMUM_CAPACITY)

               break;

           else if (tab == table) { // table 不为空，且在此期间其他线程未修改 table  

               int rs = resizeStamp(n);

               if (sc < 0) {//这里的 sc 可能小于零么？？？不明白为什么会有此判断

                   Node[] nt;//RESIZE_STAMP_SHIFT=16,MAX_RESIZERS=2^15-1  

                   if ((sc >>> RESIZE_STAMP_SHIFT) != rs || sc == rs + 1 ||

                       sc == rs + MAX_RESIZERS || (nt = nextTable) == null ||

                       transferIndex <= 0)

                       break;

                   if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1))

                       transfer(tab, nt);

              }

               else if (U.compareAndSwapInt(this, SIZECTL, sc,

                                            (rs << RESIZE_STAMP_SHIFT) + 2))

                   transfer(tab, null);

          }

      }

  }

   /*

    Returns the stamp bits for resizing a table of size n.当扩容到 n 时，调用该函数返回一个标志位

    Must be negative when shifted left by RESIZE_STAMP_SHIFT.

    numberOfLeadingZeros 返回 n 对应 32 位二进制数左侧 0 的个数，如 9（1001）返回 28  

    RESIZE_STAMP_BITS=16,

    因此返回值为：(参数 n 的左侧 0 的个数)|(2^15)  

    */

   static final int resizeStamp(int n) {

       return Integer.numberOfLeadingZeros(n) | (1 << (RESIZE_STAMP_BITS - 1));

  }
```

既然是扩容，思路就比较简单哈，注释的相当详细，就不介绍了哈，在这个函数中调用 transfer 函数，transfer 方法的代码太长，这里不贴出。

在 transfer 方法中，用到了如下的属性

```java
private transient volatile Node[] nextTable;
```

仅仅在扩容使用，并且此时非空。

在扩容的过程中，还有一个辅助方法：helpTransfer 方法。

代码如下：

```java
/*

    * Helps transfer if a resize is in progress.

    * 在多线程情况下，如果发现其它线程正在扩容，则帮助转移元素。

    （只有这种情况会被调用）从某种程度上说，其“优先级”很高，只要检测到扩容，就会放下其他工作，先扩容。

    */

   final Node[] helpTransfer(Node[] tab, Node f) {// 调用之前，nextTable 一定已存在。

       Node[] nextTab; int sc;

       if (tab != null && (f instanceof ForwardingNode) &&

          (nextTab = ((ForwardingNode)f).nextTable) != null) {

           int rs = resizeStamp(tab.length);//标志位

           while (nextTab == nextTable && table == tab &&

                  (sc = sizeCtl) < 0) {

               if ((sc >>> RESIZE_STAMP_SHIFT) != rs || sc == rs + 1 ||

                   sc == rs + MAX_RESIZERS || transferIndex <= 0)

                   break;

               if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1)) {

                   transfer(tab, nextTab);//调用扩容方法，直接进入复制阶段  

                   break;

              }

          }

           return nextTab;

      }

       return table;

  }
```

以上就把跟 putVal 相关的函数都看了一篇哈，可能细节我们没有看懂，但是各个方法的思路我们都清楚了，继续往下面来看

分析 ConcurrentHashMap 类的 get(int key) 方法

看完了 ConcurrentHashMap 类的 put(int key ,int value) 方法的内部实现，接着看此类的 get(int key) 方法。

 ```java

 /*

    功能：根据 key 在 Map 中找出其对应的 value，如果不存在 key，则返回 null，

    其中 key 不允许为 null，否则抛异常

    */

   public V get(Object key) {

       Node[] tab; Node e, p; int n, eh; K ek;

       int h = spread(key.hashCode());//两次 hash 计算出 hash 值

       if ((tab = table) != null && (n = tab.length) > 0 &&//table 不能为 null，是吧

          (e = tabAt(tab, (n - 1) & h)) != null) {//table[i] 不能为空，是吧

           if ((eh = e.hash) == h) {//检查头结点

               if ((ek = e.key) == key || (ek != null && key.equals(ek)))

                   return e.val;

          }

           else if (eh < 0)//table[i] 为一颗树

               return (p = e.find(h, key)) != null ? p.val : null;

           while ((e = e.next) != null) {//链表，遍历寻找即可

               if (e.hash == h &&

                  ((ek = e.key) == key || (ek != null && key.equals(ek))))

                   return e.val;

          }

      }

       return null;

  }

 ```

get(int key) 方法代码实现流程如下：

1、根据 key 调用 spread 计算 hash 值；并根据计算出来的 hash 值计算出该 key 在 table 出现的位置 i.

2、检查 table 是否为空；如果为空，返回 null，否则进行 3

3、检查 table[i] 处桶位不为空；如果为空，则返回 null，否则进行 4

4、先检查 table[i] 的头结点的 key 是否满足条件，是则返回头结点的 value；否则分别根据树、链表查询。

get 方法的思想是不是也很简单哈，与 HashMap 的 get 方法一模一样，分析到这里，ConcurrentHashMap 类的源码的大概实现思路我们就基本清晰了哈，本着学习的精神，我们还是稍微看下其他的方法哈，例如：containsKey、remove、size 等等

分析 ConcurrentHashMap 类的 containsKey/containsValue 方法

看下 containsKey/containsValue 方法

```java
/*

    * Tests if the specified object is a key in this table.

    */

   public boolean containsKey(Object key) {

       return get(key) != null;//直接调用 get(int key) 方法即可，如果有返回值，则说明是包含 key 的

  }

   /*

    * 功能，检查在所有映射 (k,v) 中只要出现一次及以上的 v==value，返回 true

    * 注意：这个方法可能需要一个完全遍历 Map，因此比 containsKey 要慢的多

    */

   public boolean containsValue(Object value) {

       if (value == null)

           throw new NullPointerException();

       Node[] t;

       if ((t = table) != null) {

           Traverser it = new Traverser(t, t.length, 0, t.length);

           for (Node p; (p = it.advance()) != null; ) {

               V v;

               if ((v = p.val) == value || (v != null && value.equals(v)))

                   return true;

          }

      }

       return false;

  }
```

containsKey/containsValue 方法的内部实现也比较简单哈。这里也不再详细介绍。

分析 ConcurrentHashMap 类的 size() 方法

```java
// Original (since JDK1.2) Map methods

   public int size() {// 旧版本方法，和推荐的 mappingCount 返回的值基本无区别

       long n = sumCount();

       return ((n < 0L) ? 0 :

              (n > (long)Integer.MAX_VALUE) ? Integer.MAX_VALUE :

              (int)n);

  }
```

这个方法是从 JDK1.2 版本开始就有的方法了。而 ConcurrentHashMap 在 JDK1.8 版本中还提供了另外一种方法可以获取大小，这个方法就是 mappingCount。

代码如下：

```java
// ConcurrentHashMap-only methods

   /**

    * Returns the number of mappings. This method should be used

    * instead of {@link #size} because a ConcurrentHashMap may

    * contain more mappings than can be represented as an int. The

    * value returned is an estimate(估计); the actual count may differ if

    * there are concurrent insertions or removals.

    *

    * @return the number of mappings

    * @since 1.8

    */

   public long mappingCount() {

       long n = sumCount();

       return (n < 0L) ? 0L : n; // ignore transient negative values

  }
```

根据 mappingCount() 方法头上的注释，我们可以得到如下的信息：

1、这个应该用来代替 size() 方法被使用。这是因为 ConcurrentHashMap 可能比包含更多的映射结果，即超过 int 类型的最大值。

2、这个方法返回值是一个估计值，由于存在并发的插入和删除，因此返回值可能与实际值会有出入。

虽然注释这么才说使用 mappingCount 来代替 size() 方法，但是我们比较两个方法的源码你会发现这两个方法的源码基本一致。

在 size() 方法和 mappingCount 方法中都出现了 sumCount() 方法，因此，我们也顺便看一下。

 ```java

 /* ---------------- Counter support -------------- */

   /**

    * A padded cell for distributing counts. Adapted from LongAdder

    * and Striped64. See their internal docs for explanation.

    */

   @sun.misc.Contended static final class CounterCell {

       volatile long value;

       CounterCell(long x) { value = x; }

  }

   // Table of counter cells. When non-null, size is a power of 2

   private transient volatile CounterCell[] counterCells;

   //ConcurrentHashMap 中元素个数,基于 CAS 无锁更新,但返回的不一定是当前 Map 的真实元素个数。

   private transient volatile long baseCount;

   final long sumCount() {

       CounterCell[] as = counterCells; CounterCell a;

       long sum = baseCount;

       if (as != null) {

           for (int i = 0; i < as.length; ++i) {

               if ((a = as[i]) != null)

                   sum += a.value;

          }

      }

       return sum;

  }

 ```

最后看下，clear，remove 方法

remove 方法的代码如下;

 ```java

 /*

    * Removes the key (and its corresponding value) from this map.

    * This method does nothing if the key is not in the map.

    */

   public V remove(Object key) {

       return replaceNode(key, null, null);

  }

   /*

    * 如果 Map 中存在 (key,value) 节点，则用对象 cd 来代替，

    * 如果 value 为空，则删除此节点。

    */

   final V replaceNode(Object key, V value, Object cv) {

       int hash = spread(key.hashCode());//计算 hash 值

       for (Node[] tab = table;;) {//死循环，直到找到

           Node f; int n, i, fh;

           if (tab == null || (n = tab.length) == 0 ||

              (f = tabAt(tab, i = (n - 1) & hash)) == null)//如果为空，则立即返回

               break;

           else if ((fh = f.hash) == MOVED)//如果检测到其它线程正在扩容，则先帮助扩容，然后再来寻找，可见扩容的优先级之高

               tab = helpTransfer(tab, f);

           else {

               V oldVal = null;

               boolean validated = false;

               synchronized (f) {  //开始锁住这个桶，然后进行比对寻找满足 (key,value) 的节点

                   if (tabAt(tab, i) == f) { //重新检查，避免由于多线程的原因 table[i] 已经被修改

                       if (fh >= 0) {//链表节点

                           validated = true;

                           for (Node e = f, pred = null;;) {

                               K ek;

                               if (e.hash == hash &&

                                  ((ek = e.key) == key ||

                                    (ek != null && key.equals(ek)))) {//满足条件就是找到 key 出现的节点位置

                                   V ev = e.val;

                                   if (cv == null || cv == ev ||

                                      (ev != null && cv.equals(ev))) {

                                       oldVal = ev;

                                       if (value != null)//value 不为空，则更新值

                                           e.val = value;

                                       //value 为空，则删除此节点

                                       else if (pred != null)

                                           pred.next = e.next;

                                       else

                                           setTabAt(tab, i, e.next);//符合条件的节点 e 为头结点的情况

                                  }

                                   break;

                              }

                               //更改指向，继续向后循环

                               pred = e;

                               if ((e = e.next) == null)//如果为到链表末尾了，则直接退出即可

                                   break;

                          }

                      }

                       else if (f instanceof TreeBin) {//树节点

                           validated = true;

                           TreeBin t = (TreeBin)f;

                           TreeNode r, p;

                           if ((r = t.root) != null &&

                              (p = r.findTreeNode(hash, key, null)) != null) {

                               V pv = p.val;

                               if (cv == null || cv == pv ||

                                  (pv != null && cv.equals(pv))) {

                                   oldVal = pv;

                                   if (value != null)

                                       p.val = value;

                                   else if (t.removeTreeNode(p))

                                       setTabAt(tab, i, untreeify(t.first));

                              }

                          }

                      }

                  }

              }

               if (validated) {

                   if (oldVal != null) {

                       if (value == null)//如果删除了节点，则要减 1

                           addCount(-1L, -1);

                       return oldVal;

                  }

                   break;

              }

          }

      }

       return null;

  }

 ```

remove 方法的实现思路也比较简单。如下；

1、先根据 key 的 hash 值计算书其在 table 的位置 i。

2、检查 table[i] 是否为空，如果为空，则返回 null，否则进行 3

3、在 table[i] 存储的链表 (或树) 中开始遍历比对寻找，如果找到节点符合 key 的，则判断 value 是否为 null 来决定是否是更新 oldValue 还是删除该节点。

clear() 方法的源码如下，这里就不再进行分析了哈。

```java
/**

    * Removes all of the mappings from this map.

    */

   public void clear() {

       long delta = 0L; // negative number of deletions

       int i = 0;

       Node[] tab = table;

       while (tab != null && i < tab.length) {

           int fh;

           Node f = tabAt(tab, i);

           if (f == null)

               ++i;

           else if ((fh = f.hash) == MOVED) {

               tab = helpTransfer(tab, f);

               i = 0; // restart

          }

           else {

               synchronized (f) {

                   if (tabAt(tab, i) == f) {

                       Node p = (fh >= 0 ? f :

                                      (f instanceof TreeBin) ?

                                      ((TreeBin)f).first : null);

                       while (p != null) {

                           --delta;

                           p = p.next;

                      }

                       setTabAt(tab, i++, null);

                  }

              }

          }

      }

       if (delta != 0L)

           addCount(delta, -1);

  }
```

小结

以上就是关于 ConcurrentHashMap 的全部介绍，是不是比较简单哈。话虽这么说，但是还是需要我们花时间和精力来慢慢看和分析总结，这样我们才会有收获，本篇博文对链表和数的转化并没有过多的介绍，以及关于在树中插入节点和查找节点也没有过多的介绍哈

来源： [https://blog.csdn.net/u010412719/article/details/52145145](https://blog.csdn.net/u010412719/article/details/52145145)
