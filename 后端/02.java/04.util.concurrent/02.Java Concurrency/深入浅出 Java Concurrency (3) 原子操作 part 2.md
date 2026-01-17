在这一部分开始讨论数组原子操作和一些其他的原子操作。

AtomicIntegerArray/AtomicLongArray/AtomicReferenceArray的API类似，选择有代表性的AtomicIntegerArray来描述这些问题。

int get(int i)

获取位置 i 的当前值。很显然，由于这个是数组操作，就有索引越界的问题（IndexOutOfBoundsException异常）。

对于下面的API起始和AtomicInteger是类似的，这种通过方法、参数的名称就能够得到函数意义的写法是非常值得称赞的。在[《重构：改善既有代码的设计》](http://www.china-pub.com/12901)和[《代码整洁之道》](http://www.china-pub.com/196266)中都非常推崇这种做法。

void set(int i, int newValue)

void lazySet(int i, int newValue)

int getAndSet(int i, int newValue)

boolean compareAndSet(int i, int expect, int update)

boolean weakCompareAndSet(int i, int expect, int update)

int getAndIncrement(int i)

int getAndDecrement(int i)

int getAndAdd(int i, int delta)

int incrementAndGet(int i)

int decrementAndGet(int i)

int addAndGet(int i, int delta)

整体来说，数组的原子操作在理解上还是相对比较容易的，这些API就是有多使用才能体会到它们的好处，而不仅仅是停留在理论阶段。

现在关注字段的原子更新。

AtomicIntegerFieldUpdater/AtomicLongFieldUpdater/AtomicReferenceFieldUpdater是基于反射的原子更新字段的值。

相应的API也是非常简单的，但是也是有一些约束的。

（1）字段必须是volatile类型的！在后面的章节中会详细说明为什么必须是volatile，volatile到底是个什么东西。

（2）字段的描述类型（修饰符public/protected/default/private）是与调用者与操作对象字段的关系一致。也就是说调用者能够直接操作对象字段，那么就可以反射进行原子操作。但是对于父类的字段，子类是不能直接操作的，尽管子类可以访问父类的字段。

（3）只能是实例变量，不能是类变量，也就是说不能加static关键字。

（4）只能是可修改变量，不能使final变量，因为final的语义就是不可修改。实际上final的语义和volatile是有冲突的，这两个关键字不能同时存在。

（5）对于AtomicIntegerFieldUpdater和AtomicLongFieldUpdater只能修改int/long类型的字段，不能修改其包装类型（Integer/Long）。如果要修改包装类型就需要使用AtomicReferenceFieldUpdater。

在下面的例子中描述了操作的方法。

![0](https://note.youdao.com/yws/res/5169/B5EE6F1C8C1244F4BDBDC27F74C45C9C)

package xylz.study.concurrency.atomic; 

![0](https://note.youdao.com/yws/res/5169/B5EE6F1C8C1244F4BDBDC27F74C45C9C)

![0](https://note.youdao.com/yws/res/5169/B5EE6F1C8C1244F4BDBDC27F74C45C9C)

import java.util.concurrent.atomic.AtomicIntegerFieldUpdater; 

![0](https://note.youdao.com/yws/res/5169/B5EE6F1C8C1244F4BDBDC27F74C45C9C)

![0](https://note.youdao.com/yws/res/5168/78CE4C631DC44A3788C90D4899421E1F)

public class AtomicIntegerFieldUpdaterDemo { 

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

![0](https://note.youdao.com/yws/res/5167/F0EEFD02BBE247BABB25A9F10E021743)

   class DemoData{

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

       public volatile int value1 = 1;

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

       volatile int value2 = 2;

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

       protected volatile int value3 = 3;

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

       private volatile int value4 = 4;

![0](https://note.youdao.com/yws/res/5165/15B0F518CCF74FB3A6F16CE81342D85A)

   }

![0](https://note.youdao.com/yws/res/5167/F0EEFD02BBE247BABB25A9F10E021743)

    AtomicIntegerFieldUpdater getUpdater(String fieldName) {

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        return AtomicIntegerFieldUpdater.newUpdater(DemoData.class, fieldName);

![0](https://note.youdao.com/yws/res/5165/15B0F518CCF74FB3A6F16CE81342D85A)

    }

![0](https://note.youdao.com/yws/res/5167/F0EEFD02BBE247BABB25A9F10E021743)

    void doit() {

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        DemoData data = new DemoData();

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        System.out.println("1 ==> "+getUpdater("value1").getAndSet(data, 10));

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        System.out.println("3 ==> "+getUpdater("value2").incrementAndGet(data));

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        System.out.println("2 ==> "+getUpdater("value3").decrementAndGet(data));

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        System.out.println("true ==> "+getUpdater("value4").compareAndSet(data, 4, 5));

![0](https://note.youdao.com/yws/res/5165/15B0F518CCF74FB3A6F16CE81342D85A)

    }

![0](https://note.youdao.com/yws/res/5167/F0EEFD02BBE247BABB25A9F10E021743)

    public static void main(String[] args) {

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        AtomicIntegerFieldUpdaterDemo demo = new AtomicIntegerFieldUpdaterDemo();

![0](https://note.youdao.com/yws/res/5166/A3B4DCB21CF44F2891C90A07F553D443)

        demo.doit();

![0](https://note.youdao.com/yws/res/5165/15B0F518CCF74FB3A6F16CE81342D85A)

    }

![0](https://note.youdao.com/yws/res/5170/1A308F323BA246D2B3BD2539F0350166)

} 

![0](https://note.youdao.com/yws/res/5169/B5EE6F1C8C1244F4BDBDC27F74C45C9C)

![0](https://note.youdao.com/yws/res/5169/B5EE6F1C8C1244F4BDBDC27F74C45C9C)

在上面的例子中DemoData的字段value3/value4对于AtomicIntegerFieldUpdaterDemo类是不可见的，因此通过反射是不能直接修改其值的。

AtomicMarkableReference类描述的一个的对，可以原子的修改Object或者Boolean的值，这种数据结构在一些缓存或者状态描述中比较有用。这种结构在单个或者同时修改Object/Boolean的时候能够有效的提高吞吐量。

AtomicStampedReference类维护带有整数“标志”的对象引用，可以用原子方式对其进行更新。对比AtomicMarkableReference类的，AtomicStampedReference维护的是一种类似的数据结构，其实就是对对象（引用）的一个并发计数。但是与AtomicInteger不同的是，此数据结构可以携带一个对象引用（Object），并且能够对此对象和计数同时进行原子操作。

在后面的章节中会提到“ABA问题”，而AtomicMarkableReference/AtomicStampedReference在解决“ABA问题”上很有用。

原子操作的使用大概就是这么多，大体来说还算是比较清晰的，在下一个章节中，将对象原子操作进行总结，重点介绍下原子操作的原理和设计思想。