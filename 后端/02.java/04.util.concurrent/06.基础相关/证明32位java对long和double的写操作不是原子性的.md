public class Test {     protected long l = -1l;     public static void main(String[] args) {         System.out.println(toBinary(-1l));         System.out.println(toBinary(1l));         Test t = new Test();         Worker w1 = new Worker(t);         Worker2 w2 = new Worker2(t);         w1.setDaemon(true);         w2.setDaemon(true);         w1.start();         w2.start();         while (true) {             if (t.l != -1l && t.l != 1l) {                 System.out.println(toBinary(t.l));                 System.out.println("l的写不是原子操作");                 break;             }         }     }     private static String toBinary(long l) {         StringBuilder sb = new StringBuilder(Long.toBinaryString(l));         while (sb.length() < 64) {             sb.insert(0, "0");         }         return sb.toString();     } } class Worker extends Thread {     public Worker(Test t) {         this.t = t;     }     private Test t;     public void run() {         while (true) {             t.l = -1l;         }     } } class Worker2 extends Thread {     public Worker2(Test t) {         this.t = t;     }     private Test t;     public void run() {         while (true) {             t.l = 1l;         }     } }

线程1和2不停的将l变量的值设置为 -1 和 1 ，结果，l的值既不等于1，也不等于-1

上面代码有误、修正

while (true) { long temp = t.l; String str = toBinary(temp); if (!str.equals("0000000000000000000000000000000000000000000000000000000000000001") && !str.equals("1111111111111111111111111111111111111111111111111111111111111111")) { System.out.println("l的写不是原子操作"); System.out.println(temp); System.out.println(str); break; } }

感谢楼下网友指正。if( xxx && xxx) 确实分两次读了一个值，有可能出现 if( -1!= 1 && 1!=-1) 的情况。修改一下，先把值用一个临时变量存起来。然后再比较。

有人问写这个干啥。没什么，就是做个实验而已。这个只在32位上是这样的，加上volatile之后就可以避免

For the purposes of the Java programming language memory model, a single write to a non-volatile long or double value is treated as two separate writes: one to each 32-bit half. This can result in a situation where a thread sees the first 32 bits of a 64-bit value from one write, and the second 32 bits from another write.

Writes and reads of volatile long and double values are always atomic.

Writes to and reads of references are always atomic, regardless of whether they are implemented as 32-bit or 64-bit values.

来源： [https://my.oschina.net/u/1047640/blog/510397](https://my.oschina.net/u/1047640/blog/510397)