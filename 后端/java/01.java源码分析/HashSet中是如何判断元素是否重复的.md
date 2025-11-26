HashSet 不能添加重复的元素，当调用 add（Object）方法时候，

首先会调用 Object 的 hashCode 方法判 hashCode 是否已经存在，如不存在则直接插入元素；

如果已存在则调用 Object 对象的 equals 方法判断是否返回 true，如果为 true 则说明元素已经存在，如为 false 则插入元素。

以下转载自：http://www.hijava.org/2010/02/how-to-judge-object-repeated-for-hashset/

查看了 JDK 源码，发现 HashSet 竟然是借助 HashMap 来实现的，利用 HashMap 中 Key 的唯一性，来保证 HashSet 中不出现重复值。具体参见代码：

```java
public class HashSet<E>
    extends AbstractSet<E>
    implements Set<E>, Cloneable, java.io.Serializable
{
    private transient HashMap<E,Object> map;

    // Dummy value to associate with an Object in the backing Map
    private static final Object PRESENT = new Object();

    public HashSet() {
    map = new HashMap<E,Object>();
    }

    public boolean contains(Object o) {
    return map.containsKey(o);
    }

    public boolean add(E e) {
    return map.put(e, PRESENT)==null;
    }
}
```

由此可见，HashSet 中的元素实际上是作为 HashMap 中的 Key 存放在 HashMap 中的。下面是 HashMap 类中的 put 方法：

```java
public V put(K key, V value) {
    if (key == null)
        return putForNullKey(value);
    int hash = hash(key.hashCode());
    int i = indexFor(hash, table.length);
    for (Entry<K,V> e = table[i]; e != null; e = e.next) {
        Object k;
        if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
        V oldValue = e.value;
        e.value = value;
        e.recordAccess(this);
        return oldValue;
        }
    }
}
```

从这段代码中可以看出，HashMap 中的 Key 是根据对象的 hashCode() 和 euqals() 来判断是否唯一的。

结论：为了保证 HashSet 中的对象不会出现重复值，在被存放元素的类中必须要重写 hashCode() 和 equals() 这两个方法。
