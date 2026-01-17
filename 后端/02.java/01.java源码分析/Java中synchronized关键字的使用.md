Java 中 synchronized 关键字的使用

对于关键字 synchronized，研究起来，发现还是有许多让自己模糊的地方，网上也有很多篇博客对 synchronized 关键字的使用讲解的相当好，自己也受益匪浅。自己之所以还写一篇博客来介绍 synchronized 的目的只有一个：加深自己对 synchronized 的理解。

写博客有时候确实是一个好的东西，往往研究某个知识点的时候，自己觉得弄懂了，但是过几天查不多就忘了模糊了，而写博客可以增加对知识点的理解和加深知识的记忆。

synchronized 关键字是解决多线程并发同步的方法之一。

synchronized 可以修饰如下几个方面。

1、修饰一个代码块，作用的对象是调用这个代码块的对象

2、修饰一个方法，作用的对象是调用这个方法的对象

3、修饰一个静态方法，作用的对象是静态方法所属的类的所有对象

4、修饰一个类，作用的对象是该类的所用对象。

下面一一进行介绍

1、synchronized 修饰一个代码块

1.1 一个线程访问一个对象 obj 中的 synchronize(this) 同步代码块时，其它线程试图访问该对象 obj 的 synchronize(this) 同步块时将会被阻塞。

看下面这个例子

Demo1

   class MyThread implements Runnable{

       private static final int NUM = 3;

       @Override

       public void run() {

           synchronized(this){

               for(int i =0;i

                   System.out.println(Thread.currentThread().getName()+" running .....");

                   try {

                       Thread.sleep(100);

                  } catch (InterruptedException e) {

                       e.printStackTrace();

                  }

              }

          }

      }

  }

测试代码如下：

   public class SyncCodeBlock {

       public static void main(String[] args) {

           MyThread mt = new MyThread();

           new Thread(mt,"Thread1").start();

           new Thread(mt,"Thread2").start();

      }

  }

运行结果：

Thread2 running ..... Thread2 running ..... Thread2 running ..... Thread1 running ..... Thread1 running ..... Thread1 running .....

这里，名字为 Thread1、Thread2 的两个线程都想访问对象 mt 的同步块 synchronized(this),由于只有一个锁，谁拿到的这个锁就该谁访问，也就是说，在任一时刻只能有一个线程访问这一同步代码块。例如，当 Thread1 线程拿到锁正在执行 run 里面的代码时，名字为 Thread2 的线程也想访问同一对象 mt 的同步块 synchroized(this) 的同步块将会被阻塞，只有等 Thread1 访问结束之后释放该对象锁 Thread2 拿到该对象锁才能访问。

如果我们将测试代码该为如下：

   public static void main(String[] args){

       MyThread mt = new MyThread();

       MyThread mt2 = new MyThread();

       new Thread(mt,"Thread1").start();

       new Thread(mt2,"Thread2").start();

  }

结果如下：

Thread2 running ..... Thread1 running ..... Thread2 running ..... Thread1 running ..... Thread2 running ..... Thread1 running .....

这里，和上面的第一种测试代码不同，这里有两个不同的 MyThread 对象，分别对应着两把锁，因此线程 Thread1 访问同步块是去拿对象 mt 的锁，而线程 Thread2 访问同步块是去拿对象 mt2 的锁，而这两个锁是没有任何关系的，即线程 Thread1 执行的是对象 mt 的中的 synchronized 代码块，而线程 Thread2 执行的是对象 mt2 中的 synchronized 代码块，两者互不相关，因此这两个线程就可以同时进行。

小结：当一个线程访问一个对象 obj 中的 synchronized(this) 同步块时，其它线程访问这个对象 obj 的 synchronize(this) 就会阻塞

1.2 当一个线程访问一个对象 obj 中的 synchronized(this) 同步代码块时，其它的线程可以同时访问该对象 obj 中的非 synchronize(this) 代码块

看一个例子

Demo2：多个线程访问 synchronized 和非 synchronized 代码块

   class MyThread implements Runnable{

       private static final int NUM = 3;

       @Override

       public void run() {

           String name = Thread.currentThread().getName();

           if(name.equals("Thread1")){

               synMethod();

          }

           else if(name.equals("Thread2")){

               notSynMethod();

          }

      }

       public void synMethod(){

           synchronized(this){

               for(int i=0;i

                   System.out.println(Thread.currentThread().getName()+"running ....");

                   try {

                       Thread.sleep(100);

                  } catch (InterruptedException e) {

                       e.printStackTrace();

                  }

              }

          }

      }

       public void notSynMethod(){

           for(int i=0;i

               System.out.println(Thread.currentThread().getName()+"running ....");

               try {

                   Thread.sleep(100);

              } catch (InterruptedException e) {

                   e.printStackTrace();

              }

          }

      }

  }

测试代码：

   public static void main(String[] args) {

       MyThread mt = new MyThread();

       new Thread(mt,"Thread1").start();

       new Thread(mt,"Thread2").start();

  }

运行结果：

Thread1 running .... Thread2 running .... Thread1 running .... Thread2 running .... Thread1 running .... Thread2 running ....

分析：

上面的代码中，有一个使用 synchronize(this) 同步的方法 synMethod，有一个没有使用关键字 synchronize(this) 同步的方法 notSynMethod.

由于线程 Thread1 和 Thread2 没有同时访问对象 mt 的 synchronized(this) 同步代码块，而是只有 Thread1 访问，Thread2 访问的是对象 mt 非 synchronized(this) 代码块。因此这两个线程是可以同时进行的。

注意：这里的“访问对象 mt 的非 synchronized(this) 代码块”并不是单单指对象 mt 中没有用关键字 synchronized 修饰的代码块，而是还包括对象 mt 中其它使用类似 synchronized(otherRef) 修饰的代码块,其中 otherRef 为不等于 this 的其它引用对象。

看下面的例子，将上例 Demo2 中的 notSynMethod 方法用 synchronized(otherRefe) 来同步

   private int [] value = new int[0];

   public void notSynMethod(){

       synchronized(value){

           for(int i=0;i

               System.out.println(Thread.currentThread().getName()+" running ....");

               try {

                   Thread.sleep(100);

              } catch (InterruptedException e) {

                   e.printStackTrace();

              }

          }

      }

  }

改成这样，线程 Thread1、Thead2 依然可以同时工作，这是因为他们所需要的锁不一样。

小结：当一个线程访问对象 obj 的 synchronized(this) 代码块时，其它线程是可以同时访问该对象 obj 的非 synchronized(this) 的代码块

1.3、当多线程并发时，一个线程访问对象 obj 的 synchronized(this) 代码块时，其它线程对对象 obj 中所有其他 synchronized(this) 同步代码块的访问将被阻塞

看一个例子：MyThread5 类中的两个方法都使用了 synchronized(this) 来进行修饰.

   class MyThread5 implements Runnable{

       private static final int NUM = 3;

       @Override

       public void run() {

           String name = Thread.currentThread().getName();

           if(name.equals("Thread1")){

               synMethod();

          }

           else if(name.equals("Thread2")){

               synMethod2();

          }

      }

       public void synMethod(){

           synchronized(this){

               for(int i=0;i

                   System.out.println(Thread.currentThread().getName()+" running ....");

                   try {

                       Thread.sleep(100);

                  } catch (InterruptedException e) {

                       e.printStackTrace();

                  }

              }

          }

      }

       public void synMethod2(){

           synchronized(this){

               for(int i=0;i

                   System.out.println(Thread.currentThread().getName()+" running ...." + i);

                   try {

                       Thread.sleep(10);

                  } catch (InterruptedException e) {

                       e.printStackTrace();

                  }

              }

          }

      }

  }

测试方法为：

   public static void main(String[] args) {

       MyThread5 mt = new MyThread5();

       new Thread(mt,"Thread1").start();

       new Thread(mt,"Thread2").start();

  }

运行结果：

Thread2 running ....0 Thread2 running ....1 Thread2 running ....2 Thread1 running .... Thread1 running .... Thread1 running ....

分析：

当线程 Thread1 访问对象 mt 的方法 synMethod 中的 synchronized(this) 同步代码块时，线程 Thread2 访问对象 mt 中另一个方法 synMethod2 中 synchronized(this) 同步代码块的访问将被阻塞。这是因为，线程 Thread1 访问 mt 的一个 synchronized(this) 同步代码块时，它就获得了这个 mt 的对象锁。结果，线程 Thread2 对该 mt 对象所有使用 synchronized(this) 的同步代码部分的访问都被暂时阻塞。

2、synchronized 修饰某个方法

synchronized 修饰某个方法，作用的对象为调用该方法的对象。

其实，

   public synchronized void method(){

       //to do something ....

  }

效果等同于：

   public void method(){

       synchronized(this){

           //to do something ....

      }

  }

因此，这里不再进行介绍。

不过，有两点需要注意的是

1、一般我们不建议同步整个方法，能同步方法中的某个代码块就同步代码块。同步安全往往是以性能为代价的。

2、synchronized 关键字同步的方法不能继承。虽然可以使用 synchronized 来修饰某个方法，但是 synchronized 并不属于方法定义的一部分，因此，synchronized 关键字不能被继承。如果在父类中的某个方法使用了 synchronized 关键字，而在子类中覆盖了这个方法，在子类中的这个方法默认情况下并不是同步的，而必须显式地在子类的这个方法中加上 synchronized 关键字才可以。

3.synchronized 关键字修饰静态代码块

synchronized 关键字修饰静态代码块，作用的是该类的所用对象。

Demo3:synchronized 关键字修饰静态代码块

   class MyThread2 implements Runnable{

       private static final int NUM = 3;

       @Override

       public void run() {

           print();

      }

       public synchronized static void print() {

           for(int i=0;i

               System.out.println(Thread.currentThread().getName()+" running... "+i);

               try {

                   Thread.sleep(100);

              } catch (InterruptedException e) {

                   e.printStackTrace();

              }

          }

      }

  }

测试代码：

   public static void main(String[] args) {

       MyThread2 mt = new MyThread2();

       MyThread2 mt2 = new MyThread2();

       new Thread(mt,"Thread1").start();

       new Thread(mt2,"Thread2").start();

  }

分析：

我们都知道静态方法是属于类的，不是属于对象的。

MyThread2 类中的静态方法 print 使用了 synchronized 修饰，尽管在测试代码中使用了两个不同的对象 mt/mt2,但是这里的锁不再是锁对象 mt/mt2.而是锁”类 MyThread2”这个对象，mt/mt2 都是属性类 MyThread 的，因此 mt/mt2 就相当于同一把锁。，因此，这两个线程在访问此静态方法 print 时就需要取得锁之后才能访问，访问完之后释放锁。

4、synchronized 修饰一个类

synchronized 修饰一个类，作用为该类的所用对象

   class MyThread3 implements Runnable{

       private static final int NUM = 3;

       @Override

       public void run() {

           synchronized(MyThread3.class){

               for(int i=0;i

                   System.out.println(Thread.currentThread().getName()+" running... "+i);

                   try {

                       Thread.sleep(100);

                  } catch (InterruptedException e) {

                       e.printStackTrace();

                  }

              }

          }

      }

  }

测试代码如下：

   public static void main(String[] args) {

       MyThread3 mt = new MyThread3();

       MyThread3 mt2 = new MyThread3();

       new Thread(mt,"Thread1").start();

       new Thread(mt2,"Thread2").start();

  }

1

2

3

4

5

6

运行结果如下：

Thread2 running... 0 Thread2 running... 1 Thread2 running... 2 Thread1 running... 0 Thread1 running... 1 Thread1 running... 2

由于 mt/mt2 都是属于类 MyThread3 的，而 synchronized 修饰的是 MyThread3 这整个类，因此所有的 MyThread 访问此代码块都是互斥的，任一时刻都只能有一个线程能够访问。

不知道大家有没有这样的疑问，反正我是有的，既然 synchronized 修饰的静态方法和修饰的整个类都是作用与该类的全部对象，那么这两者是不是互斥的呢？？

上面的问题具体一点来描述：有一个 MyThread 类，MyThread 类中的一个方法中的代码块 Block1 用 synchronize(MyThread.class) 同步，MyThread 类中一个静态方法 method 用 synchronized 同步，有两个线程 Thread1、Thread2，Thread1 访问 Block1，Thread2 访问 method 是否可以同时进行？？？

答案是：可以的，这是因为虽然都作用与该类的所用对象，但是锁却不是同一个锁，因此不是互斥的，可以同时访问

看如下的例子

   class MyThread4 implements Runnable{

       private static final int NUM = 3;

       @Override

       public void run() {

           String name = Thread.currentThread().getName();

           if(name.equals("Thread1")){

               synClassMethod();

          }

           else if(name.equals("Thread2")){

               synStaticCodeBlock();

          }

      }

       public void synClassMethod(){

           synchronized(MyThread4.class){

               for(int i=0;i

                   System.out.println(Thread.currentThread().getName()+" running... "+i);

                   try {

                       Thread.sleep(100);

                  } catch (InterruptedException e) {

                       e.printStackTrace();

                  }

              }

          }

      }

       public static void synStaticCodeBlock(){    

           for(int i=0;i

               System.out.println(Thread.currentThread().getName()+" running... "+i);

               try {

                   Thread.sleep(100);

              } catch (InterruptedException e) {

                   e.printStackTrace();

              }

          }

      }

  }

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

测试代码如下：

   public static void main(String[] args) {

       MyThread4 mt = new MyThread4();

       MyThread4 mt2 = new MyThread4();

       new Thread(mt,"Thread1").start();

       new Thread(mt2,"Thread2").start();

  }

1

2

3

4

5

6

运行结果为：

Thread2 running... 0 Thread1 running... 0 Thread2 running... 1 Thread1 running... 1 Thread2 running... 2 Thread1 running... 2

总结

1、当两个线程 Thread1、Thread2 访问一个对象 obj 的 synchronized(this) 代码块时，每个时刻都只能有一个访问此代码块，当 Thread1 访问时，Thread2 只有在 Thread1 线程执行完这段代码块并释放锁后取得锁才能访问。

2、当两个线程并发时，一个线程访问对象 obj 的 synchronized(this) 代码块时，其它的线程可以访问对象 obj 的非 synchronized(this) 代码块。

3、当多线程并发时，一个线程访问对象 obj 的 synchronized(this) 代码块时，其它线程对对象 obj 中所有其他 synchronized(this) 同步代码块的访问将被阻塞。这是因为，当一个线程访问 obj 的一个 synchronized(this) 同步代码块时，它就获得了这个 obj 的对象锁。结果，其它线程对该 obj 对象所有同步代码部分的访问都被暂时阻塞。

4、第 3 个结论同样适用其它同步代码块。例如，如果一个线程访问对象 lock 的 synchronized(lock) 的同步代码块，其中 private int[] lock = new int[0]，则其它线程在在其它方法中出现的 

synchronized(lock) 的同步代码块的访问将被阻塞。

5、上面所有的结论都适用于其它对象锁。

参考资料

1、[http://blog.csdn.net/luoweifu/article/details/46613015](http://blog.csdn.net/luoweifu/article/details/46613015)

2、[http://www.cnblogs.com/GnagWang/archive/2011/02/27/1966606.html](http://www.cnblogs.com/GnagWang/archive/2011/02/27/1966606.html)

来源： [https://blog.csdn.net/u010412719/article/details/52040032](https://blog.csdn.net/u010412719/article/details/52040032)
