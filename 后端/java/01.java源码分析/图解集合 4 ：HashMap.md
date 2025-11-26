**初识 HashMap**

之前的 List，讲了 ArrayList、LinkedList，最后讲到了 CopyOnWriteArrayList，就前两者而言，反映的是两种思想：

（1）ArrayList 以数组形式实现，顺序插入、查找快，插入、删除较慢

（2）LinkedList 以链表形式实现，顺序插入、查找较慢，插入、删除方便

那么是否有一种数据结构能够结合上面两种的优点呢？有，答案就是 HashMap。

HashMap 是一种非常常见、方便和有用的集合，是一种键值对（K-V）形式的存储结构，下面将还是用图示的方式解读 HashMap 的实现原理，

**四个关注点在 HashMap 上的答案**

|   |   |
|---|---|
|**关  注  点**|**结      论**|
|HashMap 是否允许空|Key 和 Value 都允许为空|
|HashMap 是否允许重复数据|Key 重复会覆盖、Value 允许重复|
|HashMap 是否有序|无序，特别说明这个无序指的是**遍历 HashMap 的时候，得到的元素的顺序基本不可能是 put 的顺序**|
|HashMap 是否线程安全|非线程安全|

**添加数据**

首先看一下 HashMap 的一个存储单元 Entry：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

static class Entry<K,V> implements Map.Entry<K,V> {

    final K key;

    V value;

    Entry<K,V> next;

    int hash;

    …

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

之前一篇写 LinkedList 的文章，里面写到 LinkedList 是一个双向链表，从 HashMap 的 Entry 看得出，Entry 组成的是一个**单向链表**，因为里面只有 Entry 的后继 Entry，而没有 Entry 的前驱 Entry。用图表示应该是这么一个数据结构：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151208204904136-1453407209.png)

接下来，假设我有这么一段代码：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

1 public static void main(String[] args)

2 {

3     Map<String, String> map = new HashMap<String, String>();

4     map.put("111", "111");

5     map.put("222", "222");

6 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

看一下做了什么。首先从第 3 行开始，new 了一个 HashMap 出来：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

1 public HashMap() {

2     this.loadFactor = DEFAULT_LOAD_FACTOR;

3     threshold = (int)(DEFAULT_INITIAL_CAPACITY * DEFAULT_LOAD_FACTOR);

4     table = new Entry[DEFAULT_INITIAL_CAPACITY];

5 init();

6 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

注意一下第 5 行的 init() 是个空方法，它是 HashMap 的子类比如 LinkedHashMap 构造的时候使用的。DEFAULT_INITIAL_CAPACITY 为 16，也就是说，HashMap 在 new 的时候构造出了一个大小为 16 的 Entry 数组，Entry 内所有数据都取默认值，如图示为：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151212145239919-1445500983.png)

看到 new 出了一个大小为 16 的 Entry 数组来。接着第 4 行，put 了一个 Key 和 Value 同为 111 的字符串，看一下 put 的时候底层做了什么：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 public V put(K key, V value) { 2     if (key == null)

 3         return putForNullKey(value); 4     int hash = hash(key.hashCode()); 5     int i = indexFor(hash, table.length); 6     for (Entry<K,V> e = table[i]; e != null; e = e.next) { 7        Object k;

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

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

1 static int hash(int h) {

2     // This function ensures that hashCodes that differ only by

3     // constant multiples at each bit position have a bounded

4     // number of collisions (approximately 8 at default load factor).

5     h ^= (h >>> 20) ^ (h >>> 12);

6     return h ^ (h >>> 7) ^ (h >>> 4);

7 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 static int indexFor(int h, int length) { 2     return h & (length-1);

 3 }

看一下 put 方法的几个步骤：

1、第 2 行~第 3 行就是 HashMap 允许 Key 值为空的原因，空的 Key 会默认放在第 0 位的数组位置上

2、第 4 行拿到 Key 值的 HashCode，由于 HashCode 是 Object 的方法，因此每个对象都有一个 HashCode，对这个 HashCode 做一次 hash 计算。按照 JDK 源码注释的说法，这次 hash 的作用是根据给定的 HashCode 对它做一次打乱的操作，防止一些糟糕的 Hash 算法产生的糟糕的 Hash 值，至于为什么要防止糟糕的 Hash 值，HashMap 添加元素的最后会讲到

3、第 5 行根据重新计算的 HashCode，对 Entry 数组的大小取模得到一个 Entry 数组的位置。看到这里使用了&，移位加快一点代码运行效率。另外，这个取模操作的正确性依赖于 length 必须是 2 的 N 次幂，这个熟悉二进制的朋友一定理解，因此**注意 HashMap 构造函数中，如果你指定 HashMap 初始数组的大小 initialCapacity，如果 initialCapacity 不是 2 的 N 次幂，HashMap 会算出大于 initialCapacity 的最小 2 的 N 次幂的值，作为 Entry 数组的初始化大小**。这里为了讲解方便，我们假定字符串 111 和字符串 222 算出来的 i 都是 1

4、第 6 行~第 14 行会先判断一下原数据结构中是否存在相同的 Key 值，存在则覆盖并返回，不执行后面的代码。注意一下 recordAccess 这个方法，它也是 HashMap 的子类比如 LinkedHashMap 用的，HashMap 中这个方法为空。另外，注意一点，对比 Key 是否相同，是先比 HashCode 是否相同，HashCode 相同再判断 equals 是否为 true，这样大大增加了 HashMap 的效率，对 HashCode 不熟悉的朋友可以看一下我的这篇文章讲讲 [HashCode的作用](http://www.cnblogs.com/xrq730/p/4842028.html)

5、第 16 行的 modeCount++ 是用于 fail-fast 机制的，每次修改 HashMap 数据结构的时候都会自增一次这个值

然后就到了关键的 addEntry 方法了：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

void addEntry(int hash, K key, V value, int bucketIndex) {

    Entry<K,V> e = table[bucketIndex];

    table[bucketIndex] = new Entry<K,V>(hash, key, value, e);

    if (size++ >= threshold)

        resize(2 * table.length);

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

Entry(int h, K k, V v, Entry<K,V> n) {

    value = v;

    next = n;

    key = k;

    hash = h;

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

假设 new 出来的 Entry 地址为 0x00000001，那么，put("111", "111") 用图表示应该是这样的：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151212160210497-23750228.png)

每一个新增的 Entry 都位于 table[1] 上，另外，里面的 hash 是 rehash 之后的 hash 而不是 Key 最原始的 hash。看到 table[1] 上存放了 111---->111 这个键值对，它持有原 table[1] 的引用地址，因此可以寻址到原 table[1]，这就是单向链表。 再看一下 put("222", "222") 做了什么，一张图就可以理解了：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151212160243294-1319536937.png)

新的 Entry 再次占据 table[1] 的位置，并且持有原 table[1]，也就是 111---->111 这个键值对。

至此，HashMap 进行 put 数据的过程就呈现清楚了。不过还有一个问题，就是 HashMap 如何进行扩容，再看一下 addEntry 方法：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 void addEntry(int hash, K key, V value, int bucketIndex) { 2 Entry<K,V> e = table[bucketIndex]; 3     table[bucketIndex] = new Entry<K,V>(hash, key, value, e);

 4     if (size++ >= threshold) 5         resize(2 * table.length); 6 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

看到第 4 行~第 5 行，也就是说在每次放置完 Entry 之后都会判断是否需要扩容。这里不讲扩容是因为**HashMap 扩容在不正确的使用场景下将会导致死循环**，这是一个值得探讨的话题，也是我工作中实际遇到过的一个问题，因此下一篇文章将会详细说明为什么不正确地使用 HashMap 会导致死循环。

**删除数据**

有一段代码：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

1 public static void main(String[] args)

2 {

3     Map<String, String> map = new HashMap<String, String>();

4     map.put("111", "111");

5     map.put("222", "222");

6     map.remove("111");

7 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

第 6 行删除元素，看一下删除元素的时候做了什么，第 4 行~第 5 行添加了两个键值对就沿用上面的图，HashMap 删除指定键值对的源代码是：

 1 public V remove(Object key) { 2     Entry<K,V> e = removeEntryForKey(key); 3     return (e == null ? null : e.value); 4 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 final Entry<K,V> removeEntryForKey(Object key) { 2     int hash = (key == null) ? 0 : hash(key.hashCode()); 3     int i = indexFor(hash, table.length); 4     Entry<K,V> prev = table[i]; 5     Entry<K,V> e = prev; 6

 7     while (e != null) {

 8         Entry<K,V> next = e.next; 9 Object k;

10         if (e.hash == hash &&

11             ((k = e.key) == key || (key != null && key.equals(k)))) {

12             modCount++;

13             size--;

14             if (prev == e)

15                 table[i] = next;

16             else

17                 prev.next = next;

18             e.recordRemoval(this);

19             return e;

20 }

21         prev = e;

22         e = next;

23 }

24

25     return e;

26 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

分析一下 remove 元素的时候做了几步：

1、根据 key 的 hash 找到待删除的键值对位于 table 的哪个位置上

2、记录一个 prev 表示待删除的 Entry 的前一个位置 Entry，e 可以认为是当前位置

3、从 table[i] 开始遍历链表，假如找到了匹配的 Entry，要做一个判断，这个 Entry 是不是 table[i]：

（1）是的话，也就是第 14 行~第 15 行，table[i] 就直接是 table[i] 的下一个节点，后面的都不需要动

（2）不是的话，也就是第 16 行~第 17 行，e 的前一个 Entry 也就是 prev，prev 的 next 指向 e 的后一个节点，也就是 next，这样，e 所代表的 Entry 就被踢出了，e 的前后 Entry 就连起来了

remove("111") 用图表示就是：

![](https://images2015.cnblogs.com/blog/801753/201512/801753-20151212160519559-1676241073.png)

整个过程只需要修改一个节点的 next 的值即可，非常方便。

**修改数据**

修改元素也是 put，看一下源代码：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

 1 public V put(K key, V value) { 2     if (key == null)

 3         return putForNullKey(value); 4     int hash = hash(key.hashCode()); 5     int i = indexFor(hash, table.length); 6     for (Entry<K,V> e = table[i]; e != null; e = e.next) { 7         Object k;

 8         if (e.hash == hash && ((k = e.key) == key || key.equals(k))) { 9             V oldValue = e.value;

10             e.value = value;

11             e.recordAccess(this);

12             return oldValue;

13 }

14 }

15     modCount++;

16 addEntry(hash, key, value, i);

17     return null;

18 }

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

这个其实前面已经提到过了，第 6 行~第 14 行就是修改元素的逻辑，如果某个 Key 已经在数据结构中存在的话，那么就会覆盖原 value，也就是第 10 行的代码。

**插入数据**

所谓 " 插入元素 "，在我的理解里，一定是基于数据结构是**有序**的前提下的。像 ArrayList、LinkedList，再远点说就是数据库，一条一条都是有序的。

而 HashMap，它的顺序是基于 HashCode，HashCode 是一个随机性很强的数字，所以 HashMap 中的 Entry 完全是随机存放的。HashMap 又不像 LinkedHashMap 这样维护了插入元素的顺序，所以对 HashMap 这个数据结构谈插入元素是没有意义的。

所以，HashMap 并没有插入的概念。

**再谈 HashCode 的重要性**

前面讲到了，HashMap 中对 Key 的 HashCode 要做一次 rehash，防止一些糟糕的 Hash 算法生成的糟糕的 HashCode，那么为什么要防止糟糕的 HashCode？

**糟糕的 HashCode 意味着的是 Hash 冲突，即多个不同的 Key 可能得到的是同一个 HashCode**，糟糕的 Hash 算法意味着的就是 Hash 冲突的概率增大，这意味着 HashMap 的性能将下降，表现在两方面：

1、有 10 个 Key，可能 6 个 Key 的 HashCode 都相同，另外四个 Key 所在的 Entry 均匀分布在 table 的位置上，而某一个位置上却连接了 6 个 Entry。这就失去了 HashMap 的意义，HashMap 这种数据结构性高性能的前提是，**Entry 均匀地分布在 table 位置上**，但现在确是 1 1 1 1 6 的分布。所以，**我们要求 HashCode 有很强的随机性**，这样就尽可能地可以保证了 Entry 分布的随机性，提升了 HashMap 的效率。

2、HashMap 在一个某个 table 位置上遍历链表的时候的代码：

if (e.hash == hash && ((k = e.key) == key || key.equals(k)))

看到，由于采用了 "&&" 运算符，因此先比较 HashCode，HashCode 都不相同就直接 pass 了，不会再进行 equals 比较了。HashCode 因为是 int 值，比较速度非常快，而 equals 方法往往会对比一系列的内容，速度会慢一些。**Hash 冲突的概率大，意味着 equals 比较的次数势必增多**，必然降低了 HashMap 的效率了。

**HashMap 的 table 为什么是 transient 的**

一个非常细节的地方：

transient Entry[] table;

看到 table 用了 transient 修饰，也就是说 table 里面的内容全都不会被序列化，不知道大家有没有想过这么写的原因？

在我看来，这么写是非常必要的。因为 HashMap 是基于 HashCode 的，HashCode 作为 Object 的方法，是 native 的：

public native int hashCode();

这意味着的是：**HashCode 和底层实现相关，不同的虚拟机可能有不同的 HashCode 算法**。再进一步说得明白些就是，可能同一个 Key 在虚拟机 A 上的 HashCode=1，在虚拟机 B 上的 HashCode=2，在虚拟机 C 上的 HashCode=3。

这就有问题了，Java 自诞生以来，就以跨平台性作为最大卖点，好了，如果 table 不被 transient 修饰，在虚拟机 A 上可以用的程序到虚拟机 B 上可以用的程序就不能用了，失去了跨平台性，因为：

1、Key 在虚拟机 A 上的 HashCode=100，连在 table[4] 上

2、Key 在虚拟机 B 上的 HashCode=101，这样，就去 table[5] 上找 Key，明显找不到

整个代码就出问题了。因此，为了避免这一点，Java 采取了重写自己序列化 table 的方法，在 writeObject 选择将 key 和 value 追加到序列化的文件最后面：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

private void writeObject(java.io.ObjectOutputStream s)

        throws IOException

{

Iterator<Map.Entry<K,V>> i =

    (size > 0) ? entrySet0().iterator() : null;

// Write out the threshold, loadfactor, and any hidden stuff

s.defaultWriteObject();

// Write out number of buckets

s.writeInt(table.length);

// Write out size (number of Mappings)

s.writeInt(size);

    // Write out keys and values (alternating)

if (i != null) {

 while (i.hasNext()) {

    Map.Entry<K,V> e = i.next();

    s.writeObject(e.getKey());

    s.writeObject(e.getValue());

    }

    }

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

而在 readObject 的时候重构 HashMap 数据结构：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

private void readObject(java.io.ObjectInputStream s)

         throws IOException, ClassNotFoundException

{

// Read in the threshold, loadfactor, and any hidden stuff

s.defaultReadObject();

// Read in number of buckets and allocate the bucket array;

int numBuckets = s.readInt();

table = new Entry[numBuckets];

    init();  // Give subclass a chance to do its thing.

// Read in size (number of Mappings)

int size = s.readInt();

// Read the keys and values, and put the mappings in the HashMap

for (int i=0; i<size; i++) {

    K key = (K) s.readObject();

    V value = (V) s.readObject();

    putForCreate(key, value);

}

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

一种麻烦的方式，但却保证了跨平台性。

这个例子也告诉了我们：尽管使用的虚拟机大多数情况下都是 HotSpot，但是也不能对其它虚拟机不管不顾，有跨平台的思想是一件好事。

**HashMap 和 Hashtable 的区别**

HashMap 和 Hashtable 是一组相似的键值对集合，它们的区别也是面试常被问的问题之一，我这里简单总结一下 HashMap 和 Hashtable 的区别：

1、Hashtable 是线程安全的，Hashtable 所有对外提供的方法都使用了 synchronized，也就是同步，而 HashMap 则是线程非安全的

2、Hashtable 不允许空的 value，空的 value 将导致空指针异常，而 HashMap 则无所谓，没有这方面的限制

3、上面两个缺点是最主要的区别，另外一个区别无关紧要，我只是提一下，就是两个的 rehash 算法不同，Hashtable 的是：

private int hash(Object k) {

    // hashSeed will be zero if alternative hashing is disabled.

    return hashSeed ^ k.hashCode();

}

这个 hashSeed 是使用 sun.misc.Hashing 类的 randomHashSeed 方法产生的。HashMap 的 rehash 算法上面看过了，也就是：

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

static int hash(int h) {

    // This function ensures that hashCodes that differ only by

    // constant multiples at each bit position have a bounded

    // number of collisions (approximately 8 at default load factor).

    h ^= (h >>> 20) ^ (h >>> 12);

    return h ^ (h >>> 7) ^ (h >>> 4);

}

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void\(0\); "复制代码")

**==================================================================================**
