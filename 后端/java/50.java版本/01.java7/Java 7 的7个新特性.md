1.对集合类的语言支持；

2.自动资源管理；

3.改进的通用实例创建类型推断；

4.数字字面量下划线支持；

5.switch中使用string；

6.二进制字面量；

7.简化可变参数方法调用。

======================  华丽丽的分割线  ======================

1.对集合类的语言支持

Java将包含对创建集合类的第一类语言支持。这意味着集合类的创建可以像Ruby和Perl那样了。

原本需要怎样：

![0](https://note.youdao.com/yws/res/4116/CBA791589821421EBD51A5A515FE6F78)

1         List list = new ArrayList();

2         list.add("item");

3         String item = list.get(0);

4  

5         Set set = new HashSet();

6         set.add("item");

7         Map map = new HashMap();

8         map.put("key", 1);

9         int value = map.get("key");

![0](https://note.youdao.com/yws/res/4116/CBA791589821421EBD51A5A515FE6F78)

现在只需这样：（这些集合是不可变的...）

![0](https://note.youdao.com/yws/res/4116/CBA791589821421EBD51A5A515FE6F78)

1         List list = ["item"];

2         String item = list[0];

3        

4         Set set = {"item"};

5        

6         Map map = {"key" : 1};

7         int value = map["key"];

![0](https://note.youdao.com/yws/res/4116/CBA791589821421EBD51A5A515FE6F78)

======================  华丽丽的分割线  ======================

 2.自动资源管理

Java中某些资源是需要手动关闭的，如InputStream，Writes，Sockets，Sql classes等。这个新的语言特性允许try语句本身申请更多的资源，这些资源作用于try代码块，并自动关闭。

以前的写法：

1         BufferedReader br = new BufferedReader(new FileReader(path));

2         try {

3         return br.readLine();

4               } finally {

5                   br.close();

6         }

现在可以：（有点像C#）

1         try (BufferedReader br = new BufferedReader(new FileReader(path)) {

2             return br.readLine();

3         }

======================  华丽丽的分割线  ======================

3.改进的通用实例创建类型推断；

类型推断是一个特殊的烦恼，如下面的代码：

1 Map> anagrams = new HashMap>();

通过类型推断后变成：

1 Map> anagrams = new HashMap<>();

注：这个<>被叫做diamond（钻石）运算符，Java 7后这个运算符从引用的声明中推断类型。

======================  华丽丽的分割线  ======================

4.数字字面量下划线支持

很长的数字可读性不好，在Java 7中可以使用下划线分隔长int以及long了。如：

int one_million = 1_000_000;

这样子还真看不惯。。。不过的确是可读性好了。

======================  华丽丽的分割线  ======================

5.switch中使用string

这个问题是我在Java中不喜欢用switch的原因之一，以前在switch中只能使用number或enum。现在可以使用string了，哈哈，不错，赞个！

![0](https://note.youdao.com/yws/res/4116/CBA791589821421EBD51A5A515FE6F78)

1         String s = ...

2         switch(s) {

3         case "quux":

4              processQuux(s);

5         // fall-through

6           case "foo":

7         case "bar":

8              processFooOrBar(s);

9         break;

10         case "baz":

11         processBaz(s);

12              // fall-through

13           default:

14              processDefault(s);

15         break;

16         }

![0](https://note.youdao.com/yws/res/4116/CBA791589821421EBD51A5A515FE6F78)

======================  华丽丽的分割线  ======================

6.二进制字面量

由于继承C语言，Java代码在传统上迫使程序员只能使用十进制，八进制或十六进制来表示数(numbers)。

由于很少的域是以bit导向的，这种限制可能导致错误。你现在可以使用0b前缀创建二进制字面量：

1 int binary = 0b1001_1001;

 现在，可以使用二进制字面量这种表示方式，并且使用非常简短的代码，可将二进制字符转换为数据类型，如在byte或short。

1 byte aByte = (byte)0b001;    

2  short aShort = (short)0b010;

======================  华丽丽的分割线  ======================

7.简化可变参数方法调用。

当程序员试图使用一个不可具体化的可变参数并调用一个*varargs* （可变）方法时，编辑器会生成一个“非安全操作”的警告。

JDK 7将警告从call转移到了方法声明(methord declaration)的过程中。这样API设计者就可以使用vararg，因为警告的数量大大减少了。