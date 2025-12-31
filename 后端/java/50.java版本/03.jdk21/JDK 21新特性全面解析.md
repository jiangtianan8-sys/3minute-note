Java Development Kit (JDK) 21作为Oracle长期支持(LTS)版本，于2023年9月正式发布，带来了多项令人振奋的新特性和改进。本文将全面介绍JDK 21中的主要更新，帮助开发者了解如何利用这些新功能提升开发效率和代码质量。

# 一、虚拟线程(Virtual Threads)正式发布
虚拟线程是JDK 21中最引人注目的特性之一，它从预览阶段(JDK 19和20)正式转正。

```java
// 创建虚拟线程的简单示例
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        });
    });
}
```

核心优势：

轻量级线程，可创建数百万个而不会耗尽系统资源
简化高吞吐量并发应用程序的编写
与现有Java代码无缝兼容，使用相同的Thread API
显著减少编写、维护和观察高吞吐量并发应用程序的工作量

# 二、序列集合(Sequenced Collections)
JDK 21引入了一套新的接口来表示具有定义顺序的集合：

```java
interface SequencedCollection<E> extends Collection<E> {
    // 新增方法
    SequencedCollection<E> reversed();
    void addFirst(E);
    void addLast(E);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}
```

具体实现：

SequencedCollection - 有序集合(如List)
SequencedSet - 有序且不重复的集合(如LinkedHashSet)
SequencedMap - 有序映射(如LinkedHashMap)
使用示例：

```java
List<Integer> list = new ArrayList<>(List.of(1, 2, 3));

// 新方法
list.getFirst(); // 1
list.getLast();  // 3

var reversed = list.reversed(); // [3, 2, 1]
```


# 三、分代ZGC(Generational ZGC)
JDK 21对Z垃圾收集器进行了重大改进，引入了分代收集：

主要改进：

通过区分年轻代和老年代对象提高垃圾收集效率
减少垃圾收集的开销，特别是对于分配率高的应用程序
保持ZGC的低延迟特性(暂停时间通常小于1毫秒)
可通过-XX:+ZGenerational标志启用

# 四、模式匹配的增强
1. 记录模式(Record Patterns)正式发布
```java
record Point(int x, int y) {}

static void printSum(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.println(x + y);
    }
}
```


2. switch模式匹配增强

```java
static String formatterPatternSwitch(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case Double d  -> String.format("double %f", d);
        case String s  -> String.format("String %s", s);
        default        -> obj.toString();
    };
}
```

# 五、字符串模板(预览特性)
JDK 21引入了字符串模板(预览)，简化字符串插值和复杂字符串的构建：

```java
String name = "Joan";
String info = STR."My name is \{name}";
// 结果: "My name is Joan"

// 复杂示例
String title = "My Web Page";
String text  = "Hello, world";
String html = STR."""
    <html>
      <head>
        <title>\{title}</title>
      </head>
      <body>
        <p>\{text}</p>
      </body>
    </html>
    """;
```


# 六、外部函数与内存API(正式发布)
替代JNI的更安全、更高效的方式：

```java
// 1. 在Java代码中链接到C库函数
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();
MethodHandle strlen = linker.downcallHandle(
    stdlib.lookup("strlen").get(),
    FunctionDescriptor.of(JAVA_LONG, ADDRESS)
);

// 2. 使用try-with-resources管理原生内存
try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateUtf8String("Hello");
    long len = (long) strlen.invoke(str);
    System.out.println(len); // 5
}
```


# 七、未命名模式和变量(预览)
简化模式匹配并减少不必要的变量命名：

```java
// 旧方式
if (obj instanceof Point p) {
    System.out.println(p.x());
}

// 新方式 - 不需要命名变量
if (obj instanceof Point(_, int y)) {
    System.out.println("y=" + y);
}

// 未命名变量示例
try {
    int res = calculate();
} catch (Exception _) {  // 忽略异常细节
    System.out.println("计算出错");
}
```


# 八、未命名类和实例main方法(预览)
简化入门程序编写：

```java
// 传统方式
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// 新方式(预览)
void main() {
    System.out.println("Hello, World!");
}
```


# 九、作用域值(Scoped Values)预览
替代线程局部变量的更好选择：

```java
final static ScopedValue<...> V = ScopedValue.newInstance();

// 在作用域内设置值
ScopedValue.where(V, <value>)
           .run(() -> { ... V.get() ... });
```

优势：

不可变，更安全
生命周期有限，仅限于动态范围
子线程自动继承
# 十、其他重要改进
密钥封装机制API：用于安全密钥交换的加密功能
准备禁止动态加载代理：为未来版本默认禁止动态加载代理做准备
性能改进：包括G1垃圾收集器的优化和向量API的增强
Linux/RISC-V移植：正式支持RISC-V架构
总结
JDK 21作为长期支持版本，为Java开发者带来了众多强大的新特性和改进。从革命性的虚拟线程到实用的序列集合，从模式匹配的增强到字符串模板的引入，这些特性共同推动Java平台向前迈进了一大步。

对于开发者而言，现在是时候开始探索这些新特性，评估它们如何能够提升现有应用程序的性能和开发效率。特别是虚拟线程和分代ZGC等特性，有望显著改善高并发应用程序的性能和可维护性。

随着Java的持续演进，JDK 21再次证明了Java平台在现代软件开发中的活力和创新精神。
————————————————
版权声明：本文为CSDN博主「Bruk.Liu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_46054799/article/details/148028826