**初识 LinkedHashMap**

上两篇文章讲了 HashMap 和 HashMap 在多线程下引发的问题，说明了，HashMap 是一种非常常见、非常有用的集合，并且在多线程情况下使用不当会有线程安全问题。

大多数情况下，只要不涉及线程安全问题，Map 基本都可以使用 HashMap，不过 HashMap 有一个问题，就是**迭代 HashMap 的顺序并不是 HashMap 放置的顺序**，也就是无序。HashMap 的这一缺点往往会带来困扰，因为有些场景，我们期待一个有序的 Map。

这个时候，LinkedHashMap 就闪亮登场了，它虽然增加了时间和空间上的开销，但是**通过维护一个运行于所有条目的双向链表，LinkedHashMap 保证了元素迭代的顺序**。

**四个关注点在 LinkedHashMap 上的答案**

|   |   |
|---|---|
|**关  注  点**|**结      论**|
|LinkedHashMap 是否允许键值对为空|Key 和 Value 都允许空|
|LinkedHashMap 是否允许重复数据|Key 重复会覆盖、Value 允许重复|
|LinkedHashMap 是否有序|有序|
|LinkedHashMap 是否线程安全|非线程安全|

**LinkedHashMap 基本数据结构**

关于 LinkedHashMap，先提两点：

1、LinkedHashMap 可以认为是**HashMap+LinkedList**，即它既使用 HashMap 操作数据结构，又使用 LinkedList 维护插入元素的先后顺序

2、LinkedHashMap 的基本实现思想就是 ----**多态**。可以说，理解多态，再去理解 LinkedHashMap 原理会事半功倍；反之也是，对于 LinkedHashMap 原理的学习，也可以促进和加深对于多态的理解。

为什么可以这么说，首先看一下，LinkedHashMap 的定义：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

public class LinkedHashMap<K,V>

    extends HashMap<K,V>

    implements Map<K,V>

{

    …

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

看到，LinkedHashMap 是 HashMap 的子类，自然 LinkedHashMap 也就继承了 HashMap 中所有非 private 的方法。再看一下 LinkedHashMap 中本身的方法：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151216205748224-1556969372.png)

看到 LinkedHashMap 中并没有什么操作数据结构的方法，也就是说 LinkedHashMap 操作数据结构（比如 put 一个数据），和 HashMap 操作数据的方法完全一样，无非就是细节上有一些的不同罢了。

LinkedHashMap 和 HashMap 的区别在于它们的基本数据结构上，看一下 LinkedHashMap 的基本数据结构，也就是 Entry：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

private static class Entry<K,V> extends HashMap.Entry<K,V> {

    // These fields comprise the doubly linked list used for iteration.

    Entry<K,V> before, after;

Entry(int hash, K key, V value, HashMap.Entry<K,V> next) {

        super(hash, key, value, next);

    }

    …

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

列一下 Entry 里面有的一些属性吧：

- **K key**
- **V value**
- **Entry<K, V> next**
- **int hash**
- **Entry<K, V> before**
- **Entry<K, V> after**

其中前面四个，也就是红色部分是从 HashMap.Entry 中继承过来的；后面两个，也就是蓝色部分是 LinkedHashMap 独有的。不要搞错了 next 和 before、After，**next 是用于维护 HashMap 指定 table 位置上连接的 Entry 的顺序的，before、After 是用于维护 Entry 插入的先后顺序的**。

还是用图表示一下，列一下属性而已：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151216211941693-590937713.png)

**初始化 LinkedHashMap**

假如有这么一段代码：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

1 public static void main(String[] args)

2 {

3     LinkedHashMap<String, String> linkedHashMap =

4             new LinkedHashMap<String, String>();

5     linkedHashMap.put("111", "111");

6     linkedHashMap.put("222", "222");

7 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

首先是第 3 行~第 4 行，new 一个 LinkedHashMap 出来，看一下做了什么：

 1 public LinkedHashMap() { 2 super();

 3     accessOrder = false;

 4 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

1 public HashMap() {

2     this.loadFactor = DEFAULT_LOAD_FACTOR;

3     threshold = (int)(DEFAULT_INITIAL_CAPACITY * DEFAULT_LOAD_FACTOR);

4     table = new Entry[DEFAULT_INITIAL_CAPACITY];

5 init();

6 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 void init() { 2     header = new Entry<K,V>(-1, null, null, null);

 3     header.before = header.after = header; 4 }

/**

 * The head of the doubly linked list.
 */
private transient Entry<K,V> header;

这里出现了第一个多态：init() 方法。尽管 init() 方法定义在 HashMap 中，但是由于：

1、LinkedHashMap 重写了 init 方法

2、实例化出来的是 LinkedHashMap

因此实际调用的 init 方法是 LinkedHashMap 重写的 init 方法。假设 header 的地址是 0x00000000，那么初始化完毕，实际上是这样的：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151216221839084-1702294835.png)

**LinkedHashMap 添加元素**

继续看 LinkedHashMap 添加元素，也就是 put("111","111") 做了什么，首先当然是调用 HashMap 的 put 方法：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 public V put(K key, V value) { 2     if (key == null)

 3         return putForNullKey(value); 4     int hash = hash(key.hashCode()); 5     int i = indexFor(hash, table.length); 6     for (Entry<K,V> e = table[i]; e != null; e = e.next) { 7         Object k;

 8         if (e.hash == hash && ((k = e.key) == key || key.equals(k))) { 9             V oldValue = e.value;

10             e.value = value;

11             e.recordAccess(this);

12             return oldValue;

13 }

14 }

15

16     modCount++;

17 addEntry(hash, key, value, i);

18     return null;

19 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

第 17 行又是一个多态，因为 LinkedHashMap 重写了 addEntry 方法，因此 addEntry 调用的是 LinkedHashMap 重写了的方法：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 void addEntry(int hash, K key, V value, int bucketIndex) { 2     createEntry(hash, key, value, bucketIndex);

 3

 4     // Remove eldest entry if instructed, else grow capacity if appropriate

 5     Entry<K,V> eldest = header.after; 6     if (removeEldestEntry(eldest)) { 7         removeEntryForKey(eldest.key);

 8     } else { 9         if (size >= threshold)

10             resize(2 * table.length);

11 }

12 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

因为 LinkedHashMap 由于其本身维护了插入的先后顺序，因此 LinkedHashMap 可以用来做缓存，第 5 行~第 7 行是用来支持 FIFO 算法的，这里暂时不用去关心它。看一下 createEntry 方法：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

1 void createEntry(int hash, K key, V value, int bucketIndex) {

2     HashMap.Entry<K,V> old = table[bucketIndex];

3     Entry<K,V> e = new Entry<K,V>(hash, key, value, old);

4     table[bucketIndex] = e;

5 e.addBefore(header);

6     size++;

7 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

private void addBefore(Entry<K,V> existingEntry) {

    after  = existingEntry;

    before = existingEntry.before;

    before.after = this;

    after.before = this;

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

第 2 行~第 4 行的代码和 HashMap 没有什么不同，新添加的元素放在 table[i] 上，差别在于 LinkedHashMap 还做了 addBefore 操作，这四行代码的意思就是让新的 Entry 和原链表生成一个双向链表。假设字符串 111 放在位置 table[1] 上，生成的 Entry 地址为 0x00000001，那么用图表示是这样的：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151218213242287-1993160354.png)

如果熟悉 LinkedList 的源码应该不难理解，还是解释一下，注意下 existingEntry 表示的是 header：

1、after=existingEntry，即新增的 Entry 的 after=header 地址，即 after=0x00000000

2、before=existingEntry.before，即新增的 Entry 的 before 是 header 的 before 的地址，header 的 before 此时是 0x00000000，因此新增的 Entry 的 before=0x00000000

3、before.after=this，新增的 Entry 的 before 此时为 0x00000000 即 header，header 的 after=this，即 header 的 after=0x00000001

4、after.before=this，新增的 Entry 的 after 此时为 0x00000000 即 header，header 的 before=this，即 header 的 before=0x00000001

这样，header 与新增的 Entry 的一个双向链表就形成了。再看，新增了字符串 222 之后是什么样的，假设新增的 Entry 的地址为 0x00000002，生成到 table[2] 上，用图表示是这样的：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151218214705677-401310205.png)

就不细解释了，只要 before、after 清除地知道代表的是哪个 Entry 的就不会有什么问题。

总得来看，再说明一遍，LinkedHashMap 的实现就是 HashMap+LinkedList 的实现方式，以 HashMap 维护数据结构，以 LinkList 的方式维护数据插入顺序。

**利用 LinkedHashMap 实现 LRU 算法缓存**

前面讲了 LinkedHashMap 添加元素，删除、修改元素就不说了，比较简单，和 HashMap+LinkedList 的删除、修改元素大同小异，下面讲一个新的内容。

LinkedHashMap 可以用来作缓存，比方说 LRUCache，看一下这个类的代码，很简单，就十几行而已：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

public class LRUCache extends LinkedHashMap

{

    public LRUCache(int maxSize)

    {

        super(maxSize, 0.75F, true);

        maxElements = maxSize;

    }

    protected boolean removeEldestEntry(java.util.Map.Entry eldest)
    {
        return size() > maxElements;
    }

    private static final long serialVersionUID = 1L;
    protected int maxElements;

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

顾名思义，LRUCache 就是基于 LRU 算法的 Cache（缓存），这个类继承自 LinkedHashMap，而类中看到没有什么特别的方法，这说明 LRUCache 实现缓存 LRU 功能都是源自 LinkedHashMap 的。LinkedHashMap 可以实现 LRU 算法的缓存基于两点：

1、LinkedList 首先它是一个 Map，Map 是基于 K-V 的，和缓存一致

2、LinkedList 提供了一个 boolean 值可以让用户指定是否实现 LRU

那么，首先我们了解一下什么是 LRU：**LRU 即 Least Recently Used，最近最少使用，也就是说，当缓存满了，会优先淘汰那些最近最不常访问的数据**。比方说数据 a，1 天前访问了；数据 b，2 天前访问了，缓存满了，优先会淘汰数据 b。

我们看一下 LinkedList 带 boolean 型参数的构造方法：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

public LinkedHashMap(int initialCapacity,

         float loadFactor,

                     boolean accessOrder) {

    super(initialCapacity, loadFactor);

    this.accessOrder = accessOrder;

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

就是这个 accessOrder，它表示：

（1）false，所有的 Entry 按照插入的顺序排列

（2）true，所有的 Entry 按照访问的顺序排列

第二点的意思就是，如果有 1 2 3 这 3 个 Entry，那么访问了 1，就把 1 移到尾部去，即 2 3 1。每次访问都把访问的那个数据移到双向队列的尾部去，那么每次要淘汰数据的时候，双向队列最头的那个数据不就是最不常访问的那个数据了吗？换句话说，双向链表最头的那个数据就是要淘汰的数据。

" 访问 "，这个词有两层意思：

1、根据 Key 拿到 Value，也就是 get 方法

2、修改 Key 对应的 Value，也就是 put 方法

首先看一下 get 方法，它在 LinkedHashMap 中被重写：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

public V get(Object key) {

    Entry<K,V> e = (Entry<K,V>)getEntry(key);

    if (e == null)

        return null;

    e.recordAccess(this);

    return e.value;

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

然后是 put 方法，沿用父类 HashMap 的：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 public V put(K key, V value) { 2     if (key == null)

 3         return putForNullKey(value); 4     int hash = hash(key.hashCode()); 5     int i = indexFor(hash, table.length); 6     for (Entry<K,V> e = table[i]; e != null; e = e.next) { 7         Object k;

 8         if (e.hash == hash && ((k = e.key) == key || key.equals(k))) { 9             V oldValue = e.value;

10             e.value = value;

11             e.recordAccess(this);

12             return oldValue;

13 }

14 }

15

16     modCount++;

17 addEntry(hash, key, value, i);

18     return null;

19 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

修改数据也就是第 6 行~第 14 行的代码。看到两端代码都有一个共同点：**都调用了 recordAccess 方法**，且这个方法是 Entry 中的方法，也就是说每次的 recordAccess 操作的都是某一个固定的 Entry。

recordAccess，顾名思义，记录访问，也就是说你这次访问了双向链表，我就把你记录下来，怎么记录？**把你访问的 Entry 移到尾部去**。这个方法在 HashMap 中是一个空方法，就是用来给子类记录访问用的，看一下 LinkedHashMap 中的实现：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

void recordAccess(HashMap<K,V> m) {

    LinkedHashMap<K,V> lm = (LinkedHashMap<K,V>)m;

    if (lm.accessOrder) {

        lm.modCount++;

        remove();

        addBefore(lm.header);

    }

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

private void remove() {

    before.after = after;

    after.before = before;

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

private void addBefore(Entry<K,V> existingEntry) {

    after  = existingEntry;

    before = existingEntry.before;

    before.after = this;

    after.before = this;

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

看到每次 recordAccess 的时候做了两件事情：

1、把待移动的 Entry 的前后 Entry 相连

2、把待移动的 Entry 移动到尾部

当然，这一切都是基于 accessOrder=true 的情况下。最后用一张图表示一下整个 recordAccess 的过程吧：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151219212410991-1819031365.png)

**代码演示 LinkedHashMap 按照访问顺序排序的效果**

最后代码演示一下 LinkedList 按照访问顺序排序的效果，验证一下上一部分 LinkedHashMap 的 LRU 功能：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

public static void main(String[] args)

{

    LinkedHashMap<String, String> linkedHashMap =

            new LinkedHashMap<String, String>(16, 0.75f, true);

    linkedHashMap.put("111", "111");

    linkedHashMap.put("222", "222");

    linkedHashMap.put("333", "333");

    linkedHashMap.put("444", "444");

    loopLinkedHashMap(linkedHashMap);

    linkedHashMap.get("111");

    loopLinkedHashMap(linkedHashMap);

    linkedHashMap.put("222", "2222");

    loopLinkedHashMap(linkedHashMap);

}

public static void loopLinkedHashMap(LinkedHashMap<String, String> linkedHashMap)

{

    Set<Map.Entry<String, String>> set = inkedHashMap.entrySet();

    Iterator<Map.Entry<String, String>> iterator = set.iterator();

    
    while (iterator.hasNext())
    {
        System.out.print(iterator.next() + "\t");
    }
    System.out.println();

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

注意这里的构造方法要用三个参数那个且最后的要传入 true，这样才表示按照访问顺序排序。看一下代码运行结果：

111=111    222=222    333=333    444=444

222=222    333=333    444=444    111=111

333=333    444=444    111=111    222=2222

代码运行结果证明了两点：

1、LinkedList 是有序的

2、每次访问一个元素（get 或 put），被访问的元素都被提到最后面去了

**==================================================================================**
