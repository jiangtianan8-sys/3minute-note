**初识 LinkedList**

上一篇中讲解了 ArrayList，本篇文章讲解一下 LinkedList 的实现。

LinkedList 是基于链表实现的，所以先讲解一下什么是链表。链表原先是 C/C++ 的概念，是一种线性的存储结构，意思是将要存储的数据存在一个存储单元里面，这个存储单元里面除了存放有待存储的数据以外，还存储有其下一个存储单元的地址（下一个存储单元的地址是必要的，有些存储结构还存放有其前一个存储单元的地址），每次查找数据的时候，通过某个存储单元中的下一个存储单元的地址寻找其后面的那个存储单元。

这么讲可能有点抽象，先提一句，LinkedList 是一种双向链表，双向链表我认为有两点含义：

1、链表中任意一个存储单元都可以通过向前或者向后寻址的方式获取到其前一个存储单元和其后一个存储单元

2、链表的尾节点的后一个节点是链表的头结点，链表的头结点的前一个节点是链表的尾节点

LinkedList 既然是一种双向链表，必然有一个存储单元，看一下 LinkedList 的基本存储单元，它是 LinkedList 中的一个内部类：

> private static class Entry<E> {
>
>     E element;
>
>     Entry<E> next;
>
>     Entry<E> previous;
>
>     …
>
> }

看到 LinkedList 的 Entry 中的”E element”，就是它真正存储的数据。”Entry<E> next”和”Entry<E> previous”表示的就是这个存储单元的前一个存储单元的引用地址和后一个存储单元的引用地址。用图表示就是：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qia3bdcMyfqyo5NzhV8RNCfmibalhN37NzGHmtgFTicsjssdiaolMXUnKkyg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

**四个关注点在 LinkedList 上的答案**

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qia3dKd71vQI9DgbbiaZnsjhDgfv1mEZlibiaibmyiaQgXCq8InYlp7G4uLX5g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1 "QQ20170610-112449@2x")

**添加元素**

首先看下 LinkedList 添加一个元素是怎么做的，假如我有一段代码：

> public static void main(String[] args)
>
> {
>
>      List<String> list = new LinkedList<String>();
>
>      list.add("111");
>
>      list.add("222");
>
> }

逐行分析 main 函数中的三行代码是如何执行的，首先是第 3 行，看一下 LinkedList 的源码：

> public class LinkedList<E>
>
>     extends AbstractSequentialList<E>
>
>     implements List<E>, Deque<E>, Cloneable, java.io.Serializable
>
> {
>
>     private transient Entry<E> header = new Entry<E>(null, null, null);
>
>     private transient int size = 0;
>
>     /**
>
>      * Constructs an empty list.
>
>      */
>
>     public LinkedList() {
>
>         header.next = header.previous = header;
>
>     }
>
>     …
>
> }

看到，new 了一个 Entry 出来名为 header，Entry 里面的 previous、element、next 都为 null，执行构造函数的时候，将 previous 和 next 的值都设置为 header 的引用地址，还是用画图的方式表示。32 位 JDK 的字长为 4 个字节，而目前 64 位的 JDK 一般采用的也是 4 字长，所以就以 4 个字长为单位。header 引用地址的字长就是 4 个字节，假设是 0×00000000，那么执行完”List<String> list = new LinkedList<String>()”之后可以这么表示：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qiaaIGOgTujibuIrQic3goroVgCp60Bzhe1AWaMlQDPGdPIaGibeWTpnwh7Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2 "801753-20151201222221952-817374766")

接着看第 4 行 add 一个字符串”111″做了什么：

> public boolean add(E e) {
>
>      addBefore(e, header);
>
>      return true;
>
> }

> private Entry<E> addBefore(E e, Entry<E> entry) {
>
>     Entry<E> newEntry = new Entry<E>(e, entry, entry.previous);
>
>     newEntry.previous.next = newEntry;
>
>     newEntry.next.previous = newEntry;
>
>     size++;
>
>     modCount++;
>
>     return newEntry;
>
> }

第 2 行 new 了一个 Entry 出来，可能不太好理解，根据 Entry 的构造函数，我把这句话”翻译”一下，可能就好理解了：

1、newEntry.element = e;

2、newEntry.next = header.next;

3、newEntry.previous = header.previous;

header.next 和 header.previous 上图中已经看到了，都是 0×00000000，那么假设 new 出来的这个 Entry 的地址是 0×00000001，继续画图表示：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qiaEBcX1wh2I1Rvd0etdJOBTZah4wb5aOL1Of0BTK2aRmvtVbpXaM0iakw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3 "801753-20151201224247562-1626808729")

一共五步，每一步的操作步骤都用数字表示出来了：

1、新的 entry 的 element 赋值为 111;

2、新的 entry 的 next 是 header 的 next，header 的 next 是 0×00000000，所以新的 entry 的 next 即 0×00000000;

3、新的 entry 的 previous 是 header 的 previous，header 的 previous 是 0×00000000，所以新的 entry 的 next 即 0×00000000;

4、”newEntry.previous.next = newEntry”，首先是 newEntry 的 previous，由于 newEntry 的 previous 为 0×00000000，所以 newEntry.previous 表示的是 header，header 的 next 为 newEntry，即 header 的 next 为 0×00000001;

5、”newEntry.next.previous = newEntry”，和 4 一样，把 header 的 previous 设置为 0×00000001;

为什么要这么做？还记得双向链表的两个特点吗，一是任意节点都可以向前和向后寻址，二是整个链表头的 previous 表示的是链表的尾 Entry，链表尾的 next 表示的是链表的头 Entry。现在链表头就是 0×00000000 这个 Entry，链表尾就是 0×00000001，可以自己看图观察、思考一下是否符合这两个条件。

最后看一下 add 了一个字符串”222″做了什么，假设新 new 出来的 Entry 的地址是 0×00000002，画图表示：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qiaTDadTictEca7aVzfsfX6TEyibhl4P97myfoNNgicRRZvzX9zXLEjl3lgg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4 "801753-20151202201132252-1734941093")

还是执行的那 5 步，图中每一步都标注出来了，只要想清楚 previous、next 各自表示的是哪个节点就不会出问题了。

至此，往一个 LinkedList 里面添加一个字符串”111″和一个字符串”222″就完成了。从这张图中应该理解双向链表比较容易：

1、中间的那个 Entry，previous 的值为 0×00000000，即 header；next 的值为 0×00000002，即 tail，这就是任意一个 Entry 既可以向前查找 Entry，也可以向后查找 Entry

2、头 Entry 的 previous 的值为 0×00000002，即 tail，这就是双向链表中头 Entry 的 previous 指向的是尾 Entry

3、尾 Entry 的 next 的值为 0×00000000，即 header，这就是双向链表中尾 Entry 的 next 指向的是头 Entry 

**查看元素**

看一下 LinkedList 的代码是怎么写的：

> public E get(int index) {
>
>     return entry(index).element;
>
> }

> private Entry<E> entry(int index) {
>
>     if (index < 0 || index >= size)
>
>         throw new IndexOutOfBoundsException("Index: "+index+
>
>                                             ", Size: "+size);
>
>     Entry<E> e = header;
>
>     if (index < (size >> 1)) {
>
>         for (int i = 0; i <= index; i++)
>
>             e = e.next;
>
>     } else {
>
>         for (int i = size; i > index; i--)
>
>             e = e.previous;
>
>     }
>
>     return e;
>
> }

这段代码就体现出了双向链表的好处了。双向链表增加了一点点的空间消耗（每个 Entry 里面还要维护它的前置 Entry 的引用），同时也增加了一定的编程复杂度，却大大提升了效率。

由于 LinkedList 是双向链表，所以 LinkedList 既可以向前查找，也可以向后查找，第 6 行~第 12 行的作用就是：当 index 小于数组大小的一半的时候（size >> 1 表示 size / 2，使用移位运算提升代码运行效率），向后查找；否则，向前查找。

这样，在我的数据结构里面有 10000 个元素，刚巧查找的又是第 10000 个元素的时候，就不需要从头遍历 10000 次了，向后遍历即可，一次就能找到我要的元素。

**删除元素**

看完了添加元素，我们看一下如何删除一个元素。和 ArrayList 一样，LinkedList 支持按元素删除和按下标删除，前者会删除从头开始匹配的第一个元素。用按下标删除举个例子好了，比方说有这么一段代码：

> public static void main(String[] args)
>
> {
>
>     List<String> list = new LinkedList<String>();
>
>     list.add("111");
>
>     list.add("222");
>
>     list.remove(0);
>
> }

也就是我想删除”111″这个元素。看一下第 6 行是如何执行的：

> public E remove(int index) {
>
>      return remove(entry(index));
>
> }

> private E remove(Entry<E> e) {
>
> if (e == header)
>
>     throw new NoSuchElementException();
>
>         E result = e.element;
>
> e.previous.next = e.next;
>
> e.next.previous = e.previous;
>
>        e.next = e.previous = null;
>
>        e.element = null;
>
> size--;
>
> modCount++;
>
>        return result;
>
> }

当然，首先是找到元素在哪里，这和 get 是一样的。接着，用画图的方式来说明比较简单：

![图片](http://mmbiz.qpic.cn/mmbiz_png/eZzl4LXykQypLx0HCkPgu5K8OA2jp9qialzXibHj1FfDiadEPI2kbMCRZLAXic4gMdiab9V0O3DesBzc27JwGCjq2TQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5 "801753-20151202201557814-1924398895")

比较简单，只要找对引用地址就好了，每一步的操作也都详细标注在图上了。

这里我提一点，第 3 步、第 4 步、第 5 步将待删除的 Entry 的 previous、element、next 都设置为了 null，这三步的作用是让虚拟机可以回收这个 Entry。

但是，这个问题我稍微扩展深入一点：按照 Java 虚拟机 HotSpot 采用的垃圾回收检测算法—- 根节点搜索算法来说，即使 previous、element、next 不设置为 null 也是可以回收这个 Entry 的，因为此时这个 Entry 已经没有任何地方会指向它了，tail 的 previous 与 header 的 next 都已经变掉了，所以这块 Entry 会被当做”垃圾”对待。之所以还要将 previous、element、next 设置为 null，我认为可能是为了兼容另外一种垃圾回收检测算法—- 引用计数法，这种垃圾回收检测算法，只要对象之间存在相互引用，那么这块内存就不会被当作”垃圾”对待。

**插入元素**

插入元素就不细讲了，看一下删除元素的源代码：

> public void add(int index, E element) {
>
>     addBefore(element, (index==size ? header : entry(index)));
>
> }

> private Entry<E> addBefore(E e, Entry<E> entry) {
>
>     Entry<E> newEntry = new Entry<E>(e, entry, entry.previous);
>
>     newEntry.previous.next = newEntry;
>
>     newEntry.next.previous = newEntry;
>
>     size++;
>
>     modCount++;
>
>    return newEntry;
>
> }

如果朋友们理解了前面的内容，我认为这两个方法对你来说，应该是很容易看懂的。 

**LinkedList 和 ArrayList 的对比**

老生常谈的问题了，这里我尝试以自己的理解尽量说清楚这个问题，顺便在这里就把 LinkedList 的优缺点也给讲了。

1、顺序插入速度 ArrayList 会比较快，因为 ArrayList 是基于数组实现的，数组是事先 new 好的，只要往指定位置塞一个数据就好了；LinkedList 则不同，每次顺序插入的时候 LinkedList 将 new 一个对象出来，如果对象比较大，那么 new 的时间势必会长一点，再加上一些引用赋值的操作，所以顺序插入 LinkedList 必然慢于 ArrayList

2、基于上一点，因为 LinkedList 里面不仅维护了待插入的元素，还维护了 Entry 的前置 Entry 和后继 Entry，如果一个 LinkedList 中的 Entry 非常多，那么 LinkedList 将比 ArrayList 更耗费一些内存

3、数据遍历的速度，看最后一部分，这里就不细讲了，结论是：使用各自遍历效率最高的方式，ArrayList 的遍历效率会比 LinkedList 的遍历效率高一些

4、有些说法认为 LinkedList 做插入和删除更快，这种说法其实是不准确的：

（1）LinkedList 做插入、删除的时候，慢在寻址，快在只需要改变前后 Entry 的引用地址

（2）ArrayList 做插入、删除的时候，慢在数组元素的批量 copy，快在寻址

所以，如果待插入、删除的元素是在数据结构的前半段尤其是非常靠前的位置的时候，LinkedList 的效率将大大快过 ArrayList，因为 ArrayList 将批量 copy 大量的元素；越往后，对于 LinkedList 来说，因为它是双向链表，所以在第 2 个元素后面插入一个数据和在倒数第 2 个元素后面插入一个元素在效率上基本没有差别，但是 ArrayList 由于要批量 copy 的元素越来越少，操作速度必然追上乃至超过 LinkedList。

从这个分析看出，如果你十分确定你插入、删除的元素是在前半段，那么就使用 LinkedList；如果你十分确定你删除、删除的元素在比较靠后的位置，那么可以考虑使用 ArrayList。如果你不能确定你要做的插入、删除是在哪儿呢？那还是建议你使用 LinkedList 吧，因为一来 LinkedList 整体插入、删除的执行效率比较稳定，没有 ArrayList 这种越往后越快的情况；二来插入元素的时候，弄得不好 ArrayList 就要进行一次扩容，记住，ArrayList 底层数组扩容是一个既消耗时间又消耗空间的操作，在我的文章 Java 代码优化中，第 9 点有详细的解读。

最后一点，一切都是纸上谈兵，在选择了 List 后，有条件的最好可以做一些性能测试，比如在你的代码上下文记录 List 操作的时间消耗。

**对 LinkedList 以及 ArrayList 的迭代**

在我的 Java 代码优化一文中，第 19 点，专门提到过，ArrayList 使用最普通的 for 循环遍历，LinkedList 使用 foreach 循环比较快，看一下两个 List 的定义：

> public class ArrayList<E> extends AbstractList<E>
>
>         implements List<E>, RandomAccess, Cloneable, java.io.Serializable

> public class LinkedList<E>
>
>     extends AbstractSequentialList<E>
>
>     implements List<E>, Deque<E>, Cloneable, java.io.Serializable

注意到 ArrayList 是实现了 RandomAccess 接口而 LinkedList 则没有实现这个接口，关于 RandomAccess 这个接口的作用，看一下 JDK API 上的说法：

> public interface RamdomAcess

为此，我写一段代码证明一下这一点，注意，虽然上面的例子用的 Iterator，但是做 foreach 循环的时候，编译器默认会使用这个集合的 Iterator，具体可参见 foreach 循环原理。测试代码如下：

> public class TestMain
>
> {
>
>     private static int SIZE = 111111;
>
>     private static void loopList(List<Integer> list)
>
>     {
>
>         long startTime = System.currentTimeMillis();
>
>         for (int i = 0; i < list.size(); i++)
>
>         {
>
>             list.get(i);
>
>         }
>
>         System.out.println(list.getClass().getSimpleName() + " 使用普通 for 循环遍历时间为 " + 
>
>                 (System.currentTimeMillis() - startTime) + "ms");
>
>         startTime = System.currentTimeMillis();
>
>         for (Integer i : list)
>
>         {
>
>         }
>
>         System.out.println(list.getClass().getSimpleName() + " 使用 foreach 循环遍历时间为 " + 
>
>                 (System.currentTimeMillis() - startTime) + "ms");
>
>     }
>
>     public static void main(String[] args)
>
>     {
>
>         List<Integer> arrayList = new ArrayList<Integer>(SIZE);
>
>         List<Integer> linkedList = new LinkedList<Integer>();
>
>         for (int i = 0; i < SIZE; i++)
>
>         {
>
>             arrayList.add(i);
>
>             linkedList.add(i);
>
>         }
>
>         loopList(arrayList);
>
>         loopList(linkedList);
>
>         System.out.println();
>
>     }
>
> }

我截取三次运行结果：

> ArrayList 使用普通 for 循环遍历时间为 6ms
>
> ArrayList 使用 foreach 循环遍历时间为 12ms
>
> LinkedList 使用普通 for 循环遍历时间为 38482ms
>
> LinkedList 使用 foreach 循环遍历时间为 11ms

> ArrayList 使用普通 for 循环遍历时间为 5ms
>
> ArrayList 使用 foreach 循环遍历时间为 12ms
>
> LinkedList 使用普通 for 循环遍历时间为 43287ms
>
> LinkedList 使用 foreach 循环遍历时间为 9ms

> ArrayList 使用普通 for 循环遍历时间为 4ms
>
> ArrayList 使用 foreach 循环遍历时间为 12ms
>
> LinkedList 使用普通 for 循环遍历时间为 22370ms
>
> LinkedList 使用 foreach 循环遍历时间为 5ms

有了 JDK API 的解释，这个结果并不让人感到意外，最最想要提出的一点是：如果使用普通 for 循环遍历 LinkedList，其遍历速度将慢得令人发指。
