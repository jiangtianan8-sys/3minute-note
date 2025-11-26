《Java 源码分析》：HashMap

看过很多次 HashMap 的源码了，但是，每次都没有做记录，因此，每次记忆都不太深，今天在看别人博客时提到 Hashtable 是线程安全的，Hashtable 中的方法都用了 synchronized 进行了同步，于是就看了下 Hashtable 的源码，在看的过程中，写了篇博客，现在 2016 年 7 月 20 日 22:03:53，还在教研室，感觉回寝室还早，因此，决定再看下 HashMap 的源码，也随便以写博客的形式做点笔记。

Hashtable 的源码分析在这里：[http://blog.csdn.net/u010412719/article/details/51972602](http://blog.csdn.net/u010412719/article/details/51972602)

还是很看其他类的源码一样，先看构造函数，然后看一些比较常见的一些方法是如何实现的。

HashMap 和 Hashtable 一样，底层都是基于“数组和链表”来实现的

1、HashMap 的继承结构

   public class HashMap extends AbstractMap

       implements Map, Cloneable, Serializable

1

2

HashMap 继承了 AbstractMap 及实现了 Map、Cloneable 和 Serializable 接口。

HashMap 与 Hashtable 的第一个区别在于此，HashMap 继承了 AbstractMap，而 Hashtable 继承的是 Dictionary 抽象类

看过源码的人可能都有这样一个疑问：AbstractMap 也实现了 Map 接口，为什么 HashMap 既继承 AbstractMap 抽象类还需要实现 Map 接口吗？？？

从功能上来说：HashMap 实现 Map 是没有任何作用的。

从结构上来说：由于我们一般是面对接口编程，为了维护结构清晰和完整，是需要实现 Map 接口的。

而 HashMap 继承 AbstractMap 的作用为：AbstractMap 提供 Map 接口的骨干实现，以最大限度地减少实现此接口所需的工作。 

2、HashMap 的构造函数

   /*

      产生 HashMap 对象，其它的构造函数都是调用此构造函数来实现的

      参数的说明：

      initialCapacity：分配数组的大小，默认大小为 16，且只能是 2 的幂次方

      loadFactor: 加载因子，作用为：当数组中存储的数据大于了分配空间的总长度 *loadFactor 之后就进行扩容

  */

   public HashMap(int initialCapacity, float loadFactor) {

       if (initialCapacity < 0)

           throw new IllegalArgumentException("Illegal initial capacity: " +

                                              initialCapacity);

       if (initialCapacity > MAXIMUM_CAPACITY)

           initialCapacity = MAXIMUM_CAPACITY;

       if (loadFactor <= 0 || Float.isNaN(loadFactor))

           throw new IllegalArgumentException("Illegal load factor: " +

                                              loadFactor);

       this.loadFactor = loadFactor;

       this.threshold = tableSizeFor(initialCapacity);

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

其中，此构造函数中调用的 tableSizeFor 函数是将我们输入的任意值转化为大于等于此值的 2 的幂次方。

  static final int tableSizeFor(int cap) {

       int n = cap - 1;

       n |= n >>> 1;

       n |= n >>> 2;

       n |= n >>> 4;

       n |= n >>> 8;

       n |= n >>> 16;

       return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;

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

在看了 Hashtable 源码的构造函数之后，来看 HashMap 的构造函数，有点不一样，哪里不一样呢？？

Hashtable 的构造函数中对数组 table 进行了空间的分配，即在构造函数中直接使用了 table = new Entry[initialCapacity];。而在 HashMap 中却不是在构造函数中分配的。

仔细分析了下，如果不在构造函数中进行数组 table 空间的配，则一定是在第一次使用 put 函数存储数据时分配，追踪了下源码，发现 HashMap 确实是这样实现的。

下面我们就一起来看看 HashMap 中的 put 方法。

3、HashMap 中常见的方法

1）put(K key, V value)

   public V put(K key, V value) {

       return putVal(hash(key), key, value, false, true);

  }

1

2

3

4

put 方法直接是调用的 putVal 方法。因此，我们直接看 putVal 方法即可。

2）putVal(int hash, K key, V value, boolean onlyIfAbsent, 

boolean evict)

此方法的思想为：首先根据 key 得到 hashcode，根据 hashcode 得到要存储的位置 i=hash&(n-1),其中 n 为数组的长度 (只有 n 为 2 的幂次方时，这句话才与 hash%n 等价，这就解释了为什么了 HashMap 的容量必须为 2 的幂次方)。

得到存储位置 i 之后，检查此位置是否已经有元素，如果没有，则直接存储在该位置即可，如果有，则在位置的所有节点中遍历是否含有该 key，如果已经有了该 key，则更新其 value 即可，如果没有该 key，则在该链表的末尾加入该新节点即可。

源码如下：（加入了一定的注释）

   final V putVal(int hash, K key, V value, boolean onlyIfAbsent,

                  boolean evict) {

       Node[] tab; Node p; int n, i;

       if ((tab = table) == null || (n = tab.length) == 0)

           n = (tab = resize()).length;//重新开辟一个 Node 的数组

       /*

      根据 key 的 hash 值找到要存储的位置，

      如果该位置还没有存储元素，则直接在该位置保存值即可

      */

       if ((p = tab[i = (n - 1) & hash]) == null)

           tab[i] = newNode(hash, key, value, null);

       else {

           Node e; K k;

           /*

          检查在位置的链表中是否有了该 key,

          在下面的代码中，是先检查头结点是否为该 key，如果不等于，则在剩余的节点中寻找

          */

           if (p.hash == hash &&

              ((k = p.key) == key || (key != null && key.equals(k))))

               e = p;

           else if (p instanceof TreeNode)

               e = ((TreeNode)p).putTreeVal(this, tab, hash, key, value);

           else {

               /*

              在剩余的节点中寻找 key 的位置

              将节点 (key,value) 加到链表的末尾

              */

               for (int binCount = 0; ; ++binCount) {

                   if ((e = p.next) == null) {

                       p.next = newNode(hash, key, value, null);

                       if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st

                           treeifyBin(tab, hash);

                       break;

                  }

                   if (e.hash == hash &&

                      ((k = e.key) == key || (key != null && key.equals(k))))

                       break;

                   p = e;

              }

          }

           //如果 e 为空，则说明是添加的新节点，如果 e 不为空，则说明该 key 已经存在，只需要更新 value

           if (e != null) { // existing mapping for key

               V oldValue = e.value;

               if (!onlyIfAbsent || oldValue == null)

                   e.value = value;

               afterNodeAccess(e);

               return oldValue;

          }

      }

       ++modCount;

       //检查看是否需要扩容

       if (++size > threshold)

           resize();

       afterNodeInsertion(evict);

       return null;

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

上面调用了 resize 方法来进行扩容，前面提到，在 HashMap 所有的构造函数中，都没有对数组 table 分配存储空间。而是将这一步放入到了在 put 方法中进行 table 检测，如果为空，则调用 resize 方法进行扩容 (或者说是为了给其开辟空间)。

下面我们就具体的来看下这个函数

3、resize() 方法

此方法实现的思想为：

处理了一下两种情况

1）原 table 为 null 的情况，如果为空，则开辟默认大小的空间

2）原 table 不为空的情况，则开辟原来空间的 2 倍。由于可能 oldCap*2 会大于最大容量，因此也对其这种溢出情况进行了处理。

分配空间之后，然后将原数组中的元素拷贝到新数组中即可。

源码如下：（添加了一些注释）

   final Node[] resize() {

       Node[] oldTab = table;

       int oldCap = (oldTab == null) ? 0 : oldTab.length;

       int oldThr = threshold;

       int newCap, newThr = 0;

       /*

          如果数组 table 是有长度的，即不是第一次使用，则会进行扩容处理

      */

       if (oldCap > 0) {

           if (oldCap >= MAXIMUM_CAPACITY) {

               threshold = Integer.MAX_VALUE;

               return oldTab;

          }

           else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&

                    oldCap >= DEFAULT_INITIAL_CAPACITY)

               newThr = oldThr << 1; // double threshold

      }

       /*

      下面的就是 table 第一次使用

      （第一种是指定了 threshold，第二种是什么都没事指定，这个使用哪个构造函数得到 HashMap 对象有关）

      */

       else if (oldThr > 0) // initial capacity was placed in threshold

           newCap = oldThr;

       else {               // zero initial threshold signifies using defaults

           newCap = DEFAULT_INITIAL_CAPACITY;

           newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);

      }

       if (newThr == 0) {

           float ft = (float)newCap * loadFactor;

           newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?

                    (int)ft : Integer.MAX_VALUE);

      }

       threshold = newThr;

       @SuppressWarnings({"rawtypes","unchecked"})

           Node[] newTab = (Node[])new Node[newCap];

       table = newTab;

       //进行拷贝

       if (oldTab != null) {

           for (int j = 0; j < oldCap; ++j) {

               Node e;

               if ((e = oldTab[j]) != null) {

                   oldTab[j] = null;

                   if (e.next == null)

                       newTab[e.hash & (newCap - 1)] = e;

                   else if (e instanceof TreeNode)

                      ((TreeNode)e).split(this, newTab, j, oldCap);

                   else { // preserve order

                       Node loHead = null, loTail = null;

                       Node hiHead = null, hiTail = null;

                       Node next;

                       do {

                           next = e.next;

                           if ((e.hash & oldCap) == 0) {

                               if (loTail == null)

                                   loHead = e;

                               else

                                   loTail.next = e;

                               loTail = e;

                          }

                           else {

                               if (hiTail == null)

                                   hiHead = e;

                               else

                                   hiTail.next = e;

                               hiTail = e;

                          }

                      } while ((e = next) != null);

                       if (loTail != null) {

                           loTail.next = null;

                           newTab[j] = loHead;

                      }

                       if (hiTail != null) {

                           hiTail.next = null;

                           newTab[j + oldCap] = hiHead;

                      }

                  }

              }

          }

      }

       return newTab;

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

78

79

80

81

82

4、get 方法

该方法的实现思想为：首先根据 key 得到 hashcode，然后根据 hashcode 得到该 key 在数组 table 的存储位置，接着在该位置寻找 key 值和 hashcode 值一致的节点即可，如果没有找到，返回 null。

   public V get(Object key) {

       Node e;

       return (e = getNode(hash(key), key)) == null ? null : e.value;

  }

   final Node getNode(int hash, Object key) {

       Node[] tab; Node first, e; int n; K k;

       if ((tab = table) != null && (n = tab.length) > 0 &&

          (first = tab[(n - 1) & hash]) != null) {

           if (first.hash == hash && // always check first node

              ((k = first.key) == key || (key != null && key.equals(k))))

               return first;

           if ((e = first.next) != null) {

               if (first instanceof TreeNode)

                   return ((TreeNode)first).getTreeNode(hash, key);

               do {

                   if (e.hash == hash &&

                      ((k = e.key) == key || (key != null && key.equals(k))))

                       return e;

              } while ((e = e.next) != null);

          }

      }

       return null;

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

在我们了解了 put、get 方法的工作原理之后，在我们编程中使用的一些其它方法的源码也是比较好理解的，例如：

当我们在使用已存在的 map 来构建一个新的 Map 对象 map2 时，Map map2 = new HashMap(map);

从源码的角度来分析会进行哪些操作：

   public HashMap(Map m) {

       this.loadFactor = DEFAULT_LOAD_FACTOR;

       putMapEntries(m, false);

  }

   /*

      这个方法首先对 table 进行了检查，

      如果 table 为 null，则算出 threshold，为第一次调用 putVal 方法时为 table 分配空间

      如果 table 不为空，检查是否需要扩容。

      最后将需要添加的数据集合一个一个借助于 putVal 方法的加入到数组 table 中

  */

   final void putMapEntries(Map m, boolean evict) {

       int s = m.size();

       if (s > 0) {

           if (table == null) { // pre-size

               float ft = ((float)s / loadFactor) + 1.0F;

               int t = ((ft < (float)MAXIMUM_CAPACITY) ?

                        (int)ft : MAXIMUM_CAPACITY);

               if (t > threshold)

                   threshold = tableSizeFor(t);

          }

           else if (s > threshold)//如果 table 不为空，且添加的 map 的长度大于门限，则进行扩容

               resize();

           for (Map.Entry e : m.entrySet()) {

               K key = e.getKey();

               V value = e.getValue();

               putVal(hash(key), key, value, false, evict);

          }

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

而我们比较常用的 containsKey 方法也是借助于前面介绍的 getNode 方法来实现的。

   public boolean containsKey(Object key) {

       return getNode(hash(key), key) != null;

  }

1

2

3

5、remove(Object key)

remove 方法直接调用的是 removeNode 方法，而 removeNode 方法的思想为：先根据 key 的 hash 值找到 table 的位置 i，然后在该位置下的链表寻找 key 和 hash 均满足条件的节点。删除节点和链表删除节点方法一致。

   public V remove(Object key) {

       Node e;

       return (e = removeNode(hash(key), key, null, false, true)) == null ?

           null : e.value;

  }

   final Node removeNode(int hash, Object key, Object value,

                              boolean matchValue, boolean movable) {

       Node[] tab; Node p; int n, index;

       if ((tab = table) != null && (n = tab.length) > 0 &&

          (p = tab[index = (n - 1) & hash]) != null) {//该 table[i] 有元素

           Node node = null, e; K k; V v;

           /*

          先检查头结点是否是我们要找的节点，

          如果不是，则在此位置的链表中继续寻找

          */

           if (p.hash == hash &&

              ((k = p.key) == key || (key != null && key.equals(k))))

               node = p;

           else if ((e = p.next) != null) {

               if (p instanceof TreeNode)

                   node = ((TreeNode)p).getTreeNode(hash, key);

               else {

                   do {

                       if (e.hash == hash &&

                          ((k = e.key) == key ||

                            (key != null && key.equals(k)))) {

                           node = e;

                           break;

                      }

                       p = e;

                  } while ((e = e.next) != null);

              }

          }

           if (node != null && (!matchValue || (v = node.value) == value ||

                                (value != null && value.equals(v)))) {

               if (node instanceof TreeNode)

                  ((TreeNode)node).removeTreeNode(this, tab, movable);

               else if (node == p)//如果第一个节点就是我们要找的节点

                   tab[index] = node.next;

               else

                   p.next = node.next;

               ++modCount;

               --size;

               afterNodeRemoval(node);

               return node;

          }

      }

       return null;

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

HashMap 和 Hashtable 的几点区别

1、继承类不一样

HashMap 继承的是 AbstractMap，Hashtable 继承的是 Dictionary。实现的接口一致 (Map、Cloneable 和 Serializable)

2、初始容量不一样

HashMap 默认容量为 16，且容量只能是 2 的幂次方；Hashtable 默认容量为 11，容量并没有 2 的幂次方的限制，增加的方式是 oldCap*2+1。

3、HashMap 是线程不安全的，Hashtable 是线程安全的

默认情况下，HashMap 类中的方法并没有进行同步，而 Hashtable 中的方法均使用 synchronized 进行了同步。因此，在多线程并发时，Hashtable 可以直接使用，HashMap 需要我们加入额外的同步操作。

4、使用的 hashcode 不一样

Hashtable 是直接使用的 key 的 hashcode(key.hashcode())。而 HashMap 的 key 的 hashcode 是另外计算的。hashMap 独立了 hash 算法，并且算法是通过 key value 多次算出来的，减少了重复性

5、HashMap 允许有一个 key 为 null，多个 value 为 null。而 Hashtable 不允许 key 和 value 为 null。

6、HashMap 和 Hashtable 内部遍历方式的实现不一样

Hashtable、HashMap 都使用了 Iterator。而由于历史原因，Hashtable 还使用了 Enumeration 的方式 。
