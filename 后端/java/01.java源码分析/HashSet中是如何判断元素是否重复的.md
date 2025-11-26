HashSet不能添加重复的元素，当调用add（Object）方法时候，

首先会调用Object的hashCode方法判hashCode是否已经存在，如不存在则直接插入元素；

如果已存在则调用Object对象的equals方法判断是否返回true，如果为true则说明元素已经存在，如为false则插入元素。

以下转载自：http://www.hijava.org/2010/02/how-to-judge-object-repeated-for-hashset/

查看了JDK源码，发现HashSet竟然是借助HashMap来实现的，利用HashMap中Key的唯一性，来保证HashSet中不出现重复值。具体参见代码：

```java

```





由此可见，HashSet中的元素实际上是作为HashMap中的Key存放在HashMap中的。下面是HashMap类中的put方法：

![0](https://note.youdao.com/yws/res/17567/C090B2C4AE1341C090ABE667A68EFFB4)

public V put(K key, V value) { if (key == null) return putForNullKey(value); int hash = hash(key.hashCode()); int i = indexFor(hash, table.length); for (Entry e = table[i]; e != null; e = e.next) { Object k; if (e.hash == hash && ((k = e.key) == key || key.equals(k))) { V oldValue = e.value; e.value = value; e.recordAccess(this); return oldValue; } } }

![0](https://note.youdao.com/yws/res/17567/C090B2C4AE1341C090ABE667A68EFFB4)

从这段代码中可以看出，HashMap中的Key是根据对象的hashCode() 和 euqals()来判断是否唯一的。

结论：为了保证HashSet中的对象不会出现重复值，在被存放元素的类中必须要重写hashCode()和equals()这两个方法。