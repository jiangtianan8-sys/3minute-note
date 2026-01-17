前言

LinkedList 内部是一个链表的实现，一个节点除了保持自身的数据外，还持有前，后两个节点的引用。所以就数据存储上来说，它相比使用数组作为底层数据结构的 ArrayList 来说，会更加耗费空间。但也正因为这个特性，它删除，插入节点很快！LinkedList 没有任何同步手段，所以多线程环境须慎重考虑，可以使用 Collections.synchronizedList(new LinkedList(…)); 保证线程安全。

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095131814.png)

友情链接：jdk1.8 ArrayList 源码全分析

LinkedList 结构

类关系

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095141872.png)

这里我们需要注意的是，相比于 ArrayList，它额外实现了双端队列接口 Deque，这个接口主要是声明了队头，队尾的一系列方法。

类成员

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095152053.png)

LinkedList 内部有两个引用，一个 first，一个 last，分别用于指向链表的头和尾，另外有一个 size，用于标识这个链表的长度，而它的接的引用类型是 Node,这是他的一个内部类：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095202794.png)

很容易理解，item 用于保存数据，而 prve 用于指向当前节点的前一个节点，next 用于指向当前节点的下一个节点。

源码解析

add(E e) 方法

```java
public boolean add(E e) {
    linkLast(e);
    return true;
}
```

这个方法直接调用 linkLast:

```java
void linkLast(E e) {
    final Node<E> l = last;
    final Node<E> newNode = new Node<>(l, e, null);
    last = newNode;
    if (l == null)
        first = newNode;
    else
        l.next = newNode;
    size++;
    modCount++;
}
```

我们用作图来解释下这个方法的执行过程，一开始，first 和 last 都为 null，此时链表什么都没有，当第一次调用该方法后，first 和 last 均指向了第一个新加的节点 E1：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095311636.png)

接着，第二次调用该方法，加入新节点 E2。首先，将 last 引用赋值给 l，接着 new 了一个新节点 E2，并且 E2 的 prve 指向 l，接着将新节点 E2 赋值为 last。现在结构如下：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095322912.png)

接着判断 l==null? 所以走的 else 语句，将 l 的 next 引用指向新节点 E2，现在数据结构如下：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095411852.png)

接着 size+1，modCount+1，退出该方法，局部变量 l 销毁，所以现在数据结构如下：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095424338.png)

这样就完成了链表新节点的构建。

add(int index, E element) 这个方法是在指定位置插入新元素

public void add(int index, E element) { checkPositionIndex(index); if (index == size) linkLast(element); else linkBefore(element, node(index)); }

1. index 位置检查（不能小于 0，大于 size）
2. 如果 index==size，直接在链表最后插入，相当于调用 add(E e) 方法
3. 小于 size，首先调用 node 方法将 index 位置的节点找出，接着调用 linkBefore

void linkBefore(E e, Node succ) { // assert succ != null; final Node pred = succ.prev; final Node newNode = new Node<>(pred, e, succ); succ.prev = newNode; if (pred == null) first = newNode; else pred.next = newNode; size++; modCount++; }

我们同样作图分析，假设现在链表中有三个节点，调用 node 方法后找到的第二个节点 E2，则进入方法后，结构如下：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095443430.png)

接着，将 succ 的 prev 赋值给 pred，并且构造新节点 E4，E4 的 prev 和 next 分别为 pred 和 suc，同时将新节点 E4 赋值为 succ 的 prev 引用，则现在结构如下：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095454928.png)

接着，将新节点赋值给 pred 节点的 next 引用，结构如下：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095519879.png)

最后，size+1，modCount+1，推出方法，本地变量 succ，pred 销毁，最后结构如下：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095602744.png)

这样新节点 E4 就插入在了第二个 E2 节点前面。新链表构建完成。从这个过程中我们可以知道，这里并没有大量移动移动以前的元素，所以效率非常高！

E get(int index) 获取指定节点数据

public E get(int index) { checkElementIndex(index); return node(index).item; }

直接调用 node 方法：

Node node(int index) { // assert isElementIndex(index); if (index < (size >> 1)) { Node x = first; for (int i = 0; i < index; i++) x = x.next; return x; } else { Node x = last; for (int i = size - 1; i > index; i--) x = x.prev; return x; } }

1. 判断 index 在链表的哪边。
2. 遍历查找 index 或者 size-index 次，找出对应节点。

这里我们知道，相比于数组的直接索引获取，遍历获取节点效率并不高。

E remove(int index) 移除指定节点

public E remove(int index) { checkElementIndex(index); return unlink(node(index)); }

1. 检查 index 位置
2. 调用 node 方法获取节点，接着调用 unlink(E e)

E unlink(Node x) { // assert x != null; final E element = x.item; final Node next = x.next; final Node prev = x.prev; if (prev == null) { first = next; } else { prev.next = next; x.prev = null; } if (next == null) { last = prev; } else { next.prev = prev; x.next = null; } x.item = null; size--; modCount++; return element; }

这个方法就不做分析了，其原理就是将当前节点 X 的前一个节点 P 的 next 直接指向 X 的下一个节点 D，这样 X 就不再关联任何引用，等待垃圾回收即可。

这里我们同样知道，相比于 ArrayList 的 copy 数组覆盖原来节点，效率同样更高！

到现在，我们关于链表的核心方法，增删改都分析完毕，最后介绍下它实现的队列 Deque 的各个方法：

![](assets/jdk1.8%20LinkedList源码全分析/file-20251126095623230.png)

- add(E e): 队尾插入新节点，如果队列空间不足，抛出异常；LinkedList 没有空间限制，所以可以无限添加。
- offer(E e): 队尾插入新节点，空间不足，返回 false，在 LinkedList 中和 add 方法同样效果。
- remove(): 移除队头节点，如果队列为空（没有节点，first 为 null），抛出异常。LinkedList 中就是 first 节点（链表头）
- poll()：同 remove，不同点：队列为空，返回 null
- element()：查询队头节点 (不移除)，如果队列为空，抛出异常。
- peek()：同 element，不同点：队列为空，返回 null。

总结

1. LinkedList 内部使用链表实现，相比于 ArrayList 更加耗费空间。
2. LinkedList 插入，删除节点不用大量 copy 原来元素，效率更高。
3. LinkedList 查找元素使用遍历，效率一般。
4. LinkedList 同时是双向队列的实现。
