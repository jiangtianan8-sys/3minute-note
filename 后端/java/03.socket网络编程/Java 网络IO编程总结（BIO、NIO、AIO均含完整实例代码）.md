1、BIO编程

    1.1、传统的BIO编程

    网络编程的基本模型是C/S模型，即两个进程间的通信。

    服务端提供IP和监听端口，客户端通过连接操作想服务端监听的地址发起连接请求，通过三次握手连接，如果连接成功建立，双方就可以通过套接字进行通信。

    传统的同步阻塞模型开发中，ServerSocket负责绑定IP地址，启动监听端口；Socket负责发起连接操作。连接成功后，双方通过输入和输出流进行同步阻塞式通信。 

    简单的描述一下BIO的服务端通信模型：采用BIO通信模型的服务端，通常由一个独立的Acceptor线程负责监听客户端的连接，它接收到客户端连接请求之后为每个客户端创建一个新的线程进行链路处理没处理完成后，通过输出流返回应答给客户端，线程销毁。即典型的一请求一应答通宵模型。

    传统BIO通信模型图：

![0](https://note.youdao.com/yws/res/5236/402DE098F63849A8B6CFFE4AD7E977B8)

    该模型最大的问题就是缺乏弹性伸缩能力，当客户端并发访问量增加后，服务端的线程个数和客户端并发访问数呈1:1的正比关系，[Java](http://lib.csdn.net/base/javase)中的线程也是比较宝贵的系统资源，线程数量快速膨胀后，系统的性能将急剧下降，随着访问量的继续增大，系统最终就死-掉-了。

    同步阻塞式I/O创建的Server源码：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5270/633F5653C08249C4BCF22415AF16A90E)

![0](https://note.youdao.com/yws/res/5254/A49B08EC23064104BC8CC7B6D04FCBD5)

1. package com.anxpp.io.calculator.bio;  
2. import java.io.IOException;  
3. import java.net.ServerSocket;  
4. import java.net.Socket;  
5. /** 
6.  * BIO服务端源码 
7.  * @author yangtao__anxpp.com 
8.  * @version 1.0 
9.  */  
10. public final class ServerNormal {  
11.     //默认的端口号  
12.     private static int DEFAULT_PORT = 12345;  
13.     //单例的ServerSocket  
14.     private static ServerSocket server;  
15.     //根据传入参数设置监听端口，如果没有参数调用以下方法并使用默认值  
16.     public static void start() throws IOException{  
17.         //使用默认值  
18.         start(DEFAULT_PORT);  
19.     }  
20.     //这个方法不会被大量并发访问，不太需要考虑效率，直接进行方法同步就行了  
21.     public synchronized static void start(int port) throws IOException{  
22.         if(server != null) return;  
23.         try{  
24.             //通过构造函数创建ServerSocket  
25.             //如果端口合法且空闲，服务端就监听成功  
26.             server = new ServerSocket(port);  
27.             System.out.println("服务器已启动，端口号：" + port);  
28.             Socket socket;  
29.             //通过无线循环监听客户端连接  
30.             //如果没有客户端接入，将阻塞在accept操作上。  
31.             while(true){  
32.                 socket = server.accept();  
33.                 //当有新的客户端接入时，会执行下面的代码  
34.                 //然后创建一个新的线程处理这条Socket链路  
35.                 new Thread(new ServerHandler(socket)).start();  
36.             }  
37.         }finally{  
38.             //一些必要的清理工作  
39.             if(server != null){  
40.                 System.out.println("服务器已关闭。");  
41.                 server.close();  
42.                 server = null;  
43.             }  
44.         }  
45.     }  
46. }  

    客户端消息处理线程ServerHandler源码：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5262/9C2E3CAD8A4D45BCBB162772CF849DDA)

![0](https://note.youdao.com/yws/res/5250/8DF20CD385D94CFC81874DBE13B82507)

1. package com.anxpp.io.calculator.bio;  
2. import java.io.BufferedReader;  
3. import java.io.IOException;  
4. import java.io.InputStreamReader;  
5. import java.io.PrintWriter;  
6. import java.net.Socket;  

7. import com.anxpp.io.utils.Calculator;  
8. /** 
9.  * 客户端线程 
10.  * @author yangtao__anxpp.com 
11.  * 用于处理一个客户端的Socket链路 
12.  */  
13. public class ServerHandler implements Runnable{  
14.     private Socket socket;  
15.     public ServerHandler(Socket socket) {  
16.         this.socket = socket;  
17.     }  
18.     @Override  
19.     public void run() {  
20.         BufferedReader in = null;  
21.         PrintWriter out = null;  
22.         try{  
23.             in = new BufferedReader(new InputStreamReader(socket.getInputStream()));  
24.             out = new PrintWriter(socket.getOutputStream(),true);  
25.             String expression;  
26.             String result;  
27.             while(true){  
28.                 //通过BufferedReader读取一行  
29.                 //如果已经读到输入流尾部，返回null,退出循环  
30.                 //如果得到非空值，就尝试计算结果并返回  
31.                 if((expression = in.readLine())==null) break;  
32.                 System.out.println("服务器收到消息：" + expression);  
33.                 try{  
34.                     result = Calculator.cal(expression).toString();  
35.                 }catch(Exception e){  
36.                     result = "计算错误：" + e.getMessage();  
37.                 }  
38.                 out.println(result);  
39.             }  
40.         }catch(Exception e){  
41.             e.printStackTrace();  
42.         }finally{  
43.             //一些必要的清理工作  
44.             if(in != null){  
45.                 try {  
46.                     in.close();  
47.                 } catch (IOException e) {  
48.                     e.printStackTrace();  
49.                 }  
50.                 in = null;  
51.             }  
52.             if(out != null){  
53.                 out.close();  
54.                 out = null;  
55.             }  
56.             if(socket != null){  
57.                 try {  
58.                     socket.close();  
59.                 } catch (IOException e) {  
60.                     e.printStackTrace();  
61.                 }  
62.                 socket = null;  
63.             }  
64.         }  
65.     }  
66. }  

    同步阻塞式I/O创建的Client源码：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5271/45E717E2FCC640259AA4FF5F8FCCA2D7)

![0](https://note.youdao.com/yws/res/5253/1328F149A14E4874BDA9D7AC15C7A164)

1. package com.anxpp.io.calculator.bio;  
2. import java.io.BufferedReader;  
3. import java.io.IOException;  
4. import java.io.InputStreamReader;  
5. import java.io.PrintWriter;  
6. import java.net.Socket;  
7. /** 
8.  * 阻塞式I/O创建的客户端 
9.  * @author yangtao__anxpp.com 
10.  * @version 1.0 
11.  */  
12. public class Client {  
13.     //默认的端口号  
14.     private static int DEFAULT_SERVER_PORT = 12345;  
15.     private static String DEFAULT_SERVER_IP = "127.0.0.1";  
16.     public static void send(String expression){  
17.         send(DEFAULT_SERVER_PORT,expression);  
18.     }  
19.     public static void send(int port,String expression){  
20.         System.out.println("算术表达式为：" + expression);  
21.         Socket socket = null;  
22.         BufferedReader in = null;  
23.         PrintWriter out = null;  
24.         try{  
25.             socket = new Socket(DEFAULT_SERVER_IP,port);  
26.             in = new BufferedReader(new InputStreamReader(socket.getInputStream()));  
27.             out = new PrintWriter(socket.getOutputStream(),true);  
28.             out.println(expression);  
29.             System.out.println("___结果为：" + in.readLine());  
30.         }catch(Exception e){  
31.             e.printStackTrace();  
32.         }finally{  
33.             //一下必要的清理工作  
34.             if(in != null){  
35.                 try {  
36.                     in.close();  
37.                 } catch (IOException e) {  
38.                     e.printStackTrace();  
39.                 }  
40.                 in = null;  
41.             }  
42.             if(out != null){  
43.                 out.close();  
44.                 out = null;  
45.             }  
46.             if(socket != null){  
47.                 try {  
48.                     socket.close();  
49.                 } catch (IOException e) {  
50.                     e.printStackTrace();  
51.                 }  
52.                 socket = null;  
53.             }  
54.         }  
55.     }  
56. }  

    [测试](http://lib.csdn.net/base/softwaretest)代码，为了方便在控制台看输出结果，放到同一个程序（jvm）中运行：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5274/3283B85E690545D981CC0F522652C886)

![0](https://note.youdao.com/yws/res/5240/D92007EA000B4707A675344AE413A62B)

1. package com.anxpp.io.calculator.bio;  
2. import java.io.IOException;  
3. import java.util.Random;  
4. /** 
5.  * 测试方法 
6.  * @author yangtao__anxpp.com 
7.  * @version 1.0 
8.  */  
9. public class Test {  
10.     //测试主方法  
11.     public static void main(String[] args) throws InterruptedException {  
12.         //运行服务器  
13.         new Thread(new Runnable() {  
14.             @Override  
15.             public void run() {  
16.                 try {  
17.                     ServerBetter.start();  
18.                 } catch (IOException e) {  
19.                     e.printStackTrace();  
20.                 }  
21.             }  
22.         }).start();  
23.         //避免客户端先于服务器启动前执行代码  
24.         Thread.sleep(100);  
25.         //运行客户端   
26.         char operators[] = {'+','-','*','/'};  
27.         Random random = new Random(System.currentTimeMillis());  
28.         new Thread(new Runnable() {  
29.             @SuppressWarnings("static-access")  
30.             @Override  
31.             public void run() {  
32.                 while(true){  
33.                     //随机产生算术表达式  
34.                     String expression = random.nextInt(10)+""+operators[random.nextInt(4)]+(random.nextInt(10)+1);  
35.                     Client.send(expression);  
36.                     try {  
37.                         Thread.currentThread().sleep(random.nextInt(1000));  
38.                     } catch (InterruptedException e) {  
39.                         e.printStackTrace();  
40.                     }  
41.                 }  
42.             }  
43.         }).start();  
44.     }  
45. }  

    其中一次的运行结果：

46. 服务器已启动，端口号：12345
47. 算术表达式为：4-2
48. 服务器收到消息：4-2
49. ___结果为：2
50. 算术表达式为：5-10
51. 服务器收到消息：5-10
52. ___结果为：-5
53. 算术表达式为：0-9
54. 服务器收到消息：0-9
55. ___结果为：-9
56. 算术表达式为：0+6
57. 服务器收到消息：0+6
58. ___结果为：6
59. 算术表达式为：1/6
60. 服务器收到消息：1/6
61. ___结果为：0.16666666666666666
62. ...

    从以上代码，很容易看出，BIO主要的问题在于每当有一个新的客户端请求接入时，服务端必须创建一个新的线程来处理这条链路，在需要满足高性能、高并发的场景是没法应用的（大量创建新的线程会严重影响服务器性能，甚至罢工）。

    1.2、伪异步I/O编程

    为了改进这种一连接一线程的模型，我们可以使用线程池来管理这些线程（需要了解更多请参考前面提供的文章），实现1个或多个线程处理N个客户端的模型（但是底层还是使用的同步阻塞I/O），通常被称为“伪异步I/O模型“。

    伪异步I/O模型图：

![0](https://note.youdao.com/yws/res/5243/ADC55573A7C246199638B63086145E67)

    实现很简单，我们只需要将新建线程的地方，交给线程池管理即可，只需要改动刚刚的Server代码即可：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5272/5507EBF3808C4C80853463B8DD37CAFF)

![0](https://note.youdao.com/yws/res/5252/21899B7A94394C539840580E11504F5F)

1. package com.anxpp.io.calculator.bio;  
2. import java.io.IOException;  
3. import java.net.ServerSocket;  
4. import java.net.Socket;  
5. import java.util.concurrent.ExecutorService;  
6. import java.util.concurrent.Executors;  
7. /** 
8.  * BIO服务端源码__伪异步I/O 
9.  * @author yangtao__anxpp.com 
10.  * @version 1.0 
11.  */  
12. public final class ServerBetter {  
13.     //默认的端口号  
14.     private static int DEFAULT_PORT = 12345;  
15.     //单例的ServerSocket  
16.     private static ServerSocket server;  
17.     //线程池 懒汉式的单例  
18.     private static ExecutorService executorService = Executors.newFixedThreadPool(60);  
19.     //根据传入参数设置监听端口，如果没有参数调用以下方法并使用默认值  
20.     public static void start() throws IOException{  
21.         //使用默认值  
22.         start(DEFAULT_PORT);  
23.     }  
24.     //这个方法不会被大量并发访问，不太需要考虑效率，直接进行方法同步就行了  
25.     public synchronized static void start(int port) throws IOException{  
26.         if(server != null) return;  
27.         try{  
28.             //通过构造函数创建ServerSocket  
29.             //如果端口合法且空闲，服务端就监听成功  
30.             server = new ServerSocket(port);  
31.             System.out.println("服务器已启动，端口号：" + port);  
32.             Socket socket;  
33.             //通过无线循环监听客户端连接  
34.             //如果没有客户端接入，将阻塞在accept操作上。  
35.             while(true){  
36.                 socket = server.accept();  
37.                 //当有新的客户端接入时，会执行下面的代码  
38.                 //然后创建一个新的线程处理这条Socket链路  
39.                 executorService.execute(new ServerHandler(socket));  
40.             }  
41.         }finally{  
42.             //一些必要的清理工作  
43.             if(server != null){  
44.                 System.out.println("服务器已关闭。");  
45.                 server.close();  
46.                 server = null;  
47.             }  
48.         }  
49.     }  
50. }  

    测试运行结果是一样的。

    我们知道，如果使用CachedThreadPool线程池（不限制线程数量，如果不清楚请参考文首提供的文章），其实除了能自动帮我们管理线程（复用），看起来也就像是1:1的客户端：线程数模型，而使用FixedThreadPool我们就有效的控制了线程的最大数量，保证了系统有限的资源的控制，实现了N:M的伪异步I/O模型。

    但是，正因为限制了线程数量，如果发生大量并发请求，超过最大数量的线程就只能等待，直到线程池中的有空闲的线程可以被复用。而对Socket的输入流就行读取时，会一直阻塞，直到发生：

-     有数据可读
-     可用数据以及读取完毕
-     发生空指针或I/O异常

    所以在读取数据较慢时（比如数据量大、网络传输慢等），大量并发的情况下，其他接入的消息，只能一直等待，这就是最大的弊端。

    而后面即将介绍的NIO，就能解决这个难题。

2、NIO 编程

    JDK 1.4中的java.nio.*包中引入新的[Java](http://lib.csdn.net/base/java) I/O库，其目的是提高速度。实际上，“旧”的I/O包已经使用NIO重新实现过，即使我们不显式的使用NIO编程，也能从中受益。速度的提高在文件I/O和网络I/O中都可能会发生，但本文只讨论后者。

    2.1、简介

    NIO我们一般认为是New I/O（也是官方的叫法），因为它是相对于老的I/O类库新增的（其实在JDK 1.4中就已经被引入了，但这个名词还会继续用很久，即使它们在现在看来已经是“旧”的了，所以也提示我们在命名时，需要好好考虑），做了很大的改变。但民间跟多人称之为Non-block I/O，即非阻塞I/O，因为这样叫，更能体现它的特点。而下文中的NIO，不是指整个新的I/O库，而是非阻塞I/O。

    NIO提供了与传统BIO模型中的Socket和ServerSocket相对应的SocketChannel和ServerSocketChannel两种不同的套接字通道实现。

    新增的着两种通道都支持阻塞和非阻塞两种模式。

    阻塞模式使用就像传统中的支持一样，比较简单，但是性能和可靠性都不好；非阻塞模式正好与之相反。

    对于低负载、低并发的应用程序，可以使用同步阻塞I/O来提升开发速率和更好的维护性；对于高负载、高并发的（网络）应用，应使用NIO的非阻塞模式来开发。

    下面会先对基础知识进行介绍。

    2.2、缓冲区 Buffer

    Buffer是一个对象，包含一些要写入或者读出的数据。

    在NIO库中，所有数据都是用缓冲区处理的。在读取数据时，它是直接读到缓冲区中的；在写入数据时，也是写入到缓冲区中。任何时候访问NIO中的数据，都是通过缓冲区进行操作。

    缓冲区实际上是一个数组，并提供了对[数据结构](http://lib.csdn.net/base/datastructure)化访问以及维护读写位置等信息。

    具体的缓存区有这些：ByteBuffe、CharBuffer、 ShortBuffer、IntBuffer、LongBuffer、FloatBuffer、DoubleBuffer。他们实现了相同的接口：Buffer。

    2.3、通道 Channel

    我们对数据的读取和写入要通过Channel，它就像水管一样，是一个通道。通道不同于流的地方就是通道是双向的，可以用于读、写和同时读写操作。

    底层的[操作系统](http://lib.csdn.net/base/operatingsystem)的通道一般都是全双工的，所以全双工的Channel比流能更好的映射底层操作系统的API。

    Channel主要分两大类：

-     SelectableChannel：用户网络读写
-     FileChannel：用于文件操作

    后面代码会涉及的ServerSocketChannel和SocketChannel都是SelectableChannel的子类。

    2.4、多路复用器 Selector

    Selector是Java  NIO 编程的基础。

    Selector提供选择已经就绪的任务的能力：Selector会不断轮询注册在其上的Channel，如果某个Channel上面发生读或者写事件，这个Channel就处于就绪状态，会被Selector轮询出来，然后通过SelectionKey可以获取就绪Channel的集合，进行后续的I/O操作。

    一个Selector可以同时轮询多个Channel，因为JDK使用了epoll()代替传统的select实现，所以没有最大连接句柄1024/2048的限制。所以，只需要一个线程负责Selector的轮询，就可以接入成千上万的客户端。

    2.5、NIO服务端

    代码比传统的Socket编程看起来要复杂不少。

    直接贴代码吧，以注释的形式给出代码说明。

    NIO创建的Server源码：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5263/84EFD5154E3F477789D1B4CA3EC177B9)

![0](https://note.youdao.com/yws/res/5255/33EB24E44BA643599E4906DBDDE4DE8C)

1. package com.anxpp.io.calculator.nio;  
2. public class Server {  
3.     private static int DEFAULT_PORT = 12345;  
4.     private static ServerHandle serverHandle;  
5.     public static void start(){  
6.         start(DEFAULT_PORT);  
7.     }  
8.     public static synchronized void start(int port){  
9.         if(serverHandle!=null)  
10.             serverHandle.stop();  
11.         serverHandle = new ServerHandle(port);  
12.         new Thread(serverHandle,"Server").start();  
13.     }  
14.     public static void main(String[] args){  
15.         start();  
16.     }  
17. }  

    ServerHandle：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5273/38E6D895F7C3417E82A2B11E178014A3)

![0](https://note.youdao.com/yws/res/5256/08C578BCA91741D2B209AC745B925264)

1. package com.anxpp.io.calculator.nio;  
2. import java.io.IOException;  
3. import java.net.InetSocketAddress;  
4. import java.nio.ByteBuffer;  
5. import java.nio.channels.SelectionKey;  
6. import java.nio.channels.Selector;  
7. import java.nio.channels.ServerSocketChannel;  
8. import java.nio.channels.SocketChannel;  
9. import java.util.Iterator;  
10. import java.util.Set;  

11. import com.anxpp.io.utils.Calculator;  
12. /** 
13.  * NIO服务端 
14.  * @author yangtao__anxpp.com 
15.  * @version 1.0 
16.  */  
17. public class ServerHandle implements Runnable{  
18.     private Selector selector;  
19.     private ServerSocketChannel serverChannel;  
20.     private volatile boolean started;  
21.     /** 
22.      * 构造方法 
23.      * @param port 指定要监听的端口号 
24.      */  
25.     public ServerHandle(int port) {  
26.         try{  
27.             //创建选择器  
28.             selector = Selector.open();  
29.             //打开监听通道  
30.             serverChannel = ServerSocketChannel.open();  
31.             //如果为 true，则此通道将被置于阻塞模式；如果为 false，则此通道将被置于非阻塞模式  
32.             serverChannel.configureBlocking(false);//开启非阻塞模式  
33.             //绑定端口 backlog设为1024  
34.             serverChannel.socket().bind(new InetSocketAddress(port),1024);  
35.             //监听客户端连接请求  
36.             serverChannel.register(selector, SelectionKey.OP_ACCEPT);  
37.             //标记服务器已开启  
38.             started = true;  
39.             System.out.println("服务器已启动，端口号：" + port);  
40.         }catch(IOException e){  
41.             e.printStackTrace();  
42.             System.exit(1);  
43.         }  
44.     }  
45.     public void stop(){  
46.         started = false;  
47.     }  
48.     @Override  
49.     public void run() {  
50.         //循环遍历selector  
51.         while(started){  
52.             try{  
53.                 //无论是否有读写事件发生，selector每隔1s被唤醒一次  
54.                 selector.select(1000);  
55.                 //阻塞,只有当至少一个注册的事件发生的时候才会继续.  
56. //              selector.select();  
57.                 Set keys = selector.selectedKeys();  
58.                 Iterator it = keys.iterator();  
59.                 SelectionKey key = null;  
60.                 while(it.hasNext()){  
61.                     key = it.next();  
62.                     it.remove();  
63.                     try{  
64.                         handleInput(key);  
65.                     }catch(Exception e){  
66.                         if(key != null){  
67.                             key.cancel();  
68.                             if(key.channel() != null){  
69.                                 key.channel().close();  
70.                             }  
71.                         }  
72.                     }  
73.                 }  
74.             }catch(Throwable t){  
75.                 t.printStackTrace();  
76.             }  
77.         }  
78.         //selector关闭后会自动释放里面管理的资源  
79.         if(selector != null)  
80.             try{  
81.                 selector.close();  
82.             }catch (Exception e) {  
83.                 e.printStackTrace();  
84.             }  
85.     }  
86.     private void handleInput(SelectionKey key) throws IOException{  
87.         if(key.isValid()){  
88.             //处理新接入的请求消息  
89.             if(key.isAcceptable()){  
90.                 ServerSocketChannel ssc = (ServerSocketChannel) key.channel();  
91.                 //通过ServerSocketChannel的accept创建SocketChannel实例  
92.                 //完成该操作意味着完成TCP三次握手，TCP物理链路正式建立  
93.                 SocketChannel sc = ssc.accept();  
94.                 //设置为非阻塞的  
95.                 sc.configureBlocking(false);  
96.                 //注册为读  
97.                 sc.register(selector, SelectionKey.OP_READ);  
98.             }  
99.             //读消息  
100.             if(key.isReadable()){  
101.                 SocketChannel sc = (SocketChannel) key.channel();  
102.                 //创建ByteBuffer，并开辟一个1M的缓冲区  
103.                 ByteBuffer buffer = ByteBuffer.allocate(1024);  
104.                 //读取请求码流，返回读取到的字节数  
105.                 int readBytes = sc.read(buffer);  
106.                 //读取到字节，对字节进行编解码  
107.                 if(readBytes>0){  
108.                     //将缓冲区当前的limit设置为position=0，用于后续对缓冲区的读取操作  
109.                     buffer.flip();  
110.                     //根据缓冲区可读字节数创建字节数组  
111.                     byte[] bytes = new byte[buffer.remaining()];  
112.                     //将缓冲区可读字节数组复制到新建的数组中  
113.                     buffer.get(bytes);  
114.                     String expression = new String(bytes,"UTF-8");  
115.                     System.out.println("服务器收到消息：" + expression);  
116.                     //处理数据  
117.                     String result = null;  
118.                     try{  
119.                         result = Calculator.cal(expression).toString();  
120.                     }catch(Exception e){  
121.                         result = "计算错误：" + e.getMessage();  
122.                     }  
123.                     //发送应答消息  
124.                     doWrite(sc,result);  
125.                 }  
126.                 //没有读取到字节 忽略  
127. //              else if(readBytes==0);  
128.                 //链路已经关闭，释放资源  
129.                 else if(readBytes<0){  
130.                     key.cancel();  
131.                     sc.close();  
132.                 }  
133.             }  
134.         }  
135.     }  
136.     //异步发送应答消息  
137.     private void doWrite(SocketChannel channel,String response) throws IOException{  
138.         //将消息编码为字节数组  
139.         byte[] bytes = response.getBytes();  
140.         //根据数组容量创建ByteBuffer  
141.         ByteBuffer writeBuffer = ByteBuffer.allocate(bytes.length);  
142.         //将字节数组复制到缓冲区  
143.         writeBuffer.put(bytes);  
144.         //flip操作  
145.         writeBuffer.flip();  
146.         //发送缓冲区的字节数组  
147.         channel.write(writeBuffer);  
148.         //****此处不含处理“写半包”的代码  
149.     }  
150. }  

    可以看到，创建NIO服务端的主要步骤如下：

151.     打开ServerSocketChannel，监听客户端连接
152.     绑定监听端口，设置连接为非阻塞模式
153.     创建Reactor线程，创建多路复用器并启动线程
154.     将ServerSocketChannel注册到Reactor线程中的Selector上，监听ACCEPT事件
155.     Selector轮询准备就绪的key
156.     Selector监听到新的客户端接入，处理新的接入请求，完成TCP三次握手，简历物理链路
157.     设置客户端链路为非阻塞模式
158.     将新接入的客户端连接注册到Reactor线程的Selector上，监听读操作，读取客户端发送的网络消息
159.     异步读取客户端消息到缓冲区
160.     对Buffer编解码，处理半包消息，将解码成功的消息封装成Task
161.     将应答消息编码为Buffer，调用SocketChannel的write将消息异步发送给客户端

    因为应答消息的发送，SocketChannel也是异步非阻塞的，所以不能保证一次能吧需要发送的数据发送完，此时就会出现写半包的问题。我们需要注册写操作，不断轮询Selector将没有发送完的消息发送完毕，然后通过Buffer的hasRemain()方法判断消息是否发送完成。

    2.6、NIO客户端

    还是直接上代码吧，过程也不需要太多解释了，跟服务端代码有点类似。

    Client：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5260/C670EBA113B04136B7C901995DF7FD56)

![0](https://note.youdao.com/yws/res/5251/64848BCE4A764984B4F6CB6992FA134C)

1. package com.anxpp.io.calculator.nio;  
2. public class Client {  
3.     private static String DEFAULT_HOST = "127.0.0.1";  
4.     private static int DEFAULT_PORT = 12345;  
5.     private static ClientHandle clientHandle;  
6.     public static void start(){  
7.         start(DEFAULT_HOST,DEFAULT_PORT);  
8.     }  
9.     public static synchronized void start(String ip,int port){  
10.         if(clientHandle!=null)  
11.             clientHandle.stop();  
12.         clientHandle = new ClientHandle(ip,port);  
13.         new Thread(clientHandle,"Server").start();  
14.     }  
15.     //向服务器发送消息  
16.     public static boolean sendMsg(String msg) throws Exception{  
17.         if(msg.equals("q")) return false;  
18.         clientHandle.sendMsg(msg);  
19.         return true;  
20.     }  
21.     public static void main(String[] args){  
22.         start();  
23.     }  
24. }  

    ClientHandle：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5269/6FF36097154346798006F407C526BF6E)

![0](https://note.youdao.com/yws/res/5235/E7E507724AEA4EADAFC861DEA644DCD4)

1. package com.anxpp.io.calculator.nio;  
2. import java.io.IOException;  
3. import java.net.InetSocketAddress;  
4. import java.nio.ByteBuffer;  
5. import java.nio.channels.SelectionKey;  
6. import java.nio.channels.Selector;  
7. import java.nio.channels.SocketChannel;  
8. import java.util.Iterator;  
9. import java.util.Set;  
10. /** 
11.  * NIO客户端 
12.  * @author yangtao__anxpp.com 
13.  * @version 1.0 
14.  */  
15. public class ClientHandle implements Runnable{  
16.     private String host;  
17.     private int port;  
18.     private Selector selector;  
19.     private SocketChannel socketChannel;  
20.     private volatile boolean started;  

21.     public ClientHandle(String ip,int port) {  
22.         this.host = ip;  
23.         this.port = port;  
24.         try{  
25.             //创建选择器  
26.             selector = Selector.open();  
27.             //打开监听通道  
28.             socketChannel = SocketChannel.open();  
29.             //如果为 true，则此通道将被置于阻塞模式；如果为 false，则此通道将被置于非阻塞模式  
30.             socketChannel.configureBlocking(false);//开启非阻塞模式  
31.             started = true;  
32.         }catch(IOException e){  
33.             e.printStackTrace();  
34.             System.exit(1);  
35.         }  
36.     }  
37.     public void stop(){  
38.         started = false;  
39.     }  
40.     @Override  
41.     public void run() {  
42.         try{  
43.             doConnect();  
44.         }catch(IOException e){  
45.             e.printStackTrace();  
46.             System.exit(1);  
47.         }  
48.         //循环遍历selector  
49.         while(started){  
50.             try{  
51.                 //无论是否有读写事件发生，selector每隔1s被唤醒一次  
52.                 selector.select(1000);  
53.                 //阻塞,只有当至少一个注册的事件发生的时候才会继续.  
54. //              selector.select();  
55.                 Set keys = selector.selectedKeys();  
56.                 Iterator it = keys.iterator();  
57.                 SelectionKey key = null;  
58.                 while(it.hasNext()){  
59.                     key = it.next();  
60.                     it.remove();  
61.                     try{  
62.                         handleInput(key);  
63.                     }catch(Exception e){  
64.                         if(key != null){  
65.                             key.cancel();  
66.                             if(key.channel() != null){  
67.                                 key.channel().close();  
68.                             }  
69.                         }  
70.                     }  
71.                 }  
72.             }catch(Exception e){  
73.                 e.printStackTrace();  
74.                 System.exit(1);  
75.             }  
76.         }  
77.         //selector关闭后会自动释放里面管理的资源  
78.         if(selector != null)  
79.             try{  
80.                 selector.close();  
81.             }catch (Exception e) {  
82.                 e.printStackTrace();  
83.             }  
84.     }  
85.     private void handleInput(SelectionKey key) throws IOException{  
86.         if(key.isValid()){  
87.             SocketChannel sc = (SocketChannel) key.channel();  
88.             if(key.isConnectable()){  
89.                 if(sc.finishConnect());  
90.                 else System.exit(1);  
91.             }  
92.             //读消息  
93.             if(key.isReadable()){  
94.                 //创建ByteBuffer，并开辟一个1M的缓冲区  
95.                 ByteBuffer buffer = ByteBuffer.allocate(1024);  
96.                 //读取请求码流，返回读取到的字节数  
97.                 int readBytes = sc.read(buffer);  
98.                 //读取到字节，对字节进行编解码  
99.                 if(readBytes>0){  
100.                     //将缓冲区当前的limit设置为position=0，用于后续对缓冲区的读取操作  
101.                     buffer.flip();  
102.                     //根据缓冲区可读字节数创建字节数组  
103.                     byte[] bytes = new byte[buffer.remaining()];  
104.                     //将缓冲区可读字节数组复制到新建的数组中  
105.                     buffer.get(bytes);  
106.                     String result = new String(bytes,"UTF-8");  
107.                     System.out.println("客户端收到消息：" + result);  
108.                 }  
109.                 //没有读取到字节 忽略  
110. //              else if(readBytes==0);  
111.                 //链路已经关闭，释放资源  
112.                 else if(readBytes<0){  
113.                     key.cancel();  
114.                     sc.close();  
115.                 }  
116.             }  
117.         }  
118.     }  
119.     //异步发送消息  
120.     private void doWrite(SocketChannel channel,String request) throws IOException{  
121.         //将消息编码为字节数组  
122.         byte[] bytes = request.getBytes();  
123.         //根据数组容量创建ByteBuffer  
124.         ByteBuffer writeBuffer = ByteBuffer.allocate(bytes.length);  
125.         //将字节数组复制到缓冲区  
126.         writeBuffer.put(bytes);  
127.         //flip操作  
128.         writeBuffer.flip();  
129.         //发送缓冲区的字节数组  
130.         channel.write(writeBuffer);  
131.         //****此处不含处理“写半包”的代码  
132.     }  
133.     private void doConnect() throws IOException{  
134.         if(socketChannel.connect(new InetSocketAddress(host,port)));  
135.         else socketChannel.register(selector, SelectionKey.OP_CONNECT);  
136.     }  
137.     public void sendMsg(String msg) throws Exception{  
138.         socketChannel.register(selector, SelectionKey.OP_READ);  
139.         doWrite(socketChannel, msg);  
140.     }  
141. }  

    2.7、演示结果

    首先运行服务器，顺便也运行一个客户端：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5267/82FCB0785B26475883CBDCADEA0E1628)

![0](https://note.youdao.com/yws/res/5259/07F5133BFF594B04BAC5DB118EC2F25D)

1. package com.anxpp.io.calculator.nio;  
2. import java.util.Scanner;  
3. /** 
4.  * 测试方法 
5.  * @author yangtao__anxpp.com 
6.  * @version 1.0 
7.  */  
8. public class Test {  
9.     //测试主方法  
10.     @SuppressWarnings("resource")  
11.     public static void main(String[] args) throws Exception{  
12.         //运行服务器  
13.         Server.start();  
14.         //避免客户端先于服务器启动前执行代码  
15.         Thread.sleep(100);  
16.         //运行客户端   
17.         Client.start();  
18.         while(Client.sendMsg(new Scanner(System.in).nextLine()));  
19.     }  
20. }  

    我们也可以单独运行客户端，效果都是一样的。

    一次测试的结果：

1. 服务器已启动，端口号：12345
2. 1+2+3+4+5+6
3. 服务器收到消息：1+2+3+4+5+6
4. 客户端收到消息：21
5. 1*2/3-4+5*6/7-8
6. 服务器收到消息：1*2/3-4+5*6/7-8
7. 客户端收到消息：-7.0476190476190474

    运行多个客户端，都是没有问题的。

3、AIO编程

    NIO 2.0引入了新的异步通道的概念，并提供了异步文件通道和异步套接字通道的实现。

    异步的套接字通道时真正的异步非阻塞I/O，对应于UNIX网络编程中的事件驱动I/O（AIO）。他不需要过多的Selector对注册的通道进行轮询即可实现异步读写，从而简化了NIO的编程模型。

    直接上代码吧。

    3.1、Server端代码

    Server：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5266/80B8DEB263B1490FB0A51F0295978229)

![0](https://note.youdao.com/yws/res/5242/BD5FA8015A234972920739693FCA707B)

1. package com.anxpp.io.calculator.aio.server;  
2. /** 
3.  * AIO服务端 
4.  * @author yangtao__anxpp.com 
5.  * @version 1.0 
6.  */  
7. public class Server {  
8.     private static int DEFAULT_PORT = 12345;  
9.     private static AsyncServerHandler serverHandle;  
10.     public volatile static long clientCount = 0;  
11.     public static void start(){  
12.         start(DEFAULT_PORT);  
13.     }  
14.     public static synchronized void start(int port){  
15.         if(serverHandle!=null)  
16.             return;  
17.         serverHandle = new AsyncServerHandler(port);  
18.         new Thread(serverHandle,"Server").start();  
19.     }  
20.     public static void main(String[] args){  
21.         Server.start();  
22.     }  
23. }  

    AsyncServerHandler：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5268/81AB499B4DF24A509DBA70B70303E504)

![0](https://note.youdao.com/yws/res/5246/A6111BF291B6497A8221C40279695E37)

1. package com.anxpp.io.calculator.aio.server;  
2. import java.io.IOException;  
3. import java.net.InetSocketAddress;  
4. import java.nio.channels.AsynchronousServerSocketChannel;  
5. import java.util.concurrent.CountDownLatch;  
6. public class AsyncServerHandler implements Runnable {  
7.     public CountDownLatch latch;  
8.     public AsynchronousServerSocketChannel channel;  
9.     public AsyncServerHandler(int port) {  
10.         try {  
11.             //创建服务端通道  
12.             channel = AsynchronousServerSocketChannel.open();  
13.             //绑定端口  
14.             channel.bind(new InetSocketAddress(port));  
15.             System.out.println("服务器已启动，端口号：" + port);  
16.         } catch (IOException e) {  
17.             e.printStackTrace();  
18.         }  
19.     }  
20.     @Override  
21.     public void run() {  
22.         //CountDownLatch初始化  
23.         //它的作用：在完成一组正在执行的操作之前，允许当前的现场一直阻塞  
24.         //此处，让现场在此阻塞，防止服务端执行完成后退出  
25.         //也可以使用while(true)+sleep   
26.         //生成环境就不需要担心这个问题，以为服务端是不会退出的  
27.         latch = new CountDownLatch(1);  
28.         //用于接收客户端的连接  
29.         channel.accept(this,new AcceptHandler());  
30.         try {  
31.             latch.await();  
32.         } catch (InterruptedException e) {  
33.             e.printStackTrace();  
34.         }  
35.     }  
36. }  

    AcceptHandler：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5265/8A782EEA895048C1BAA48308903BD738)

![0](https://note.youdao.com/yws/res/5244/A30F30FB707A4A47BBD8B83C0D56CA2F)

1. package com.anxpp.io.calculator.aio.server;  
2. import java.nio.ByteBuffer;  
3. import java.nio.channels.AsynchronousSocketChannel;  
4. import java.nio.channels.CompletionHandler;  
5. //作为handler接收客户端连接  
6. public class AcceptHandler implements CompletionHandler {  
7.     @Override  
8.     public void completed(AsynchronousSocketChannel channel,AsyncServerHandler serverHandler) {  
9.         //继续接受其他客户端的请求  
10.         Server.clientCount++;  
11.         System.out.println("连接的客户端数：" + Server.clientCount);  
12.         serverHandler.channel.accept(serverHandler, this);  
13.         //创建新的Buffer  
14.         ByteBuffer buffer = ByteBuffer.allocate(1024);  
15.         //异步读  第三个参数为接收消息回调的业务Handler  
16.         channel.read(buffer, buffer, new ReadHandler(channel));  
17.     }  
18.     @Override  
19.     public void failed(Throwable exc, AsyncServerHandler serverHandler) {  
20.         exc.printStackTrace();  
21.         serverHandler.latch.countDown();  
22.     }  
23. }  

    ReadHandler：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5264/8420E517065441538EE9A7C2F6DE8F1E)

![0](https://note.youdao.com/yws/res/5245/B553396861484DBBA888FC5AC5EE8D13)

1. package com.anxpp.io.calculator.aio.server;  
2. import java.io.IOException;  
3. import java.io.UnsupportedEncodingException;  
4. import java.nio.ByteBuffer;  
5. import java.nio.channels.AsynchronousSocketChannel;  
6. import java.nio.channels.CompletionHandler;  
7. import com.anxpp.io.utils.Calculator;  
8. public class ReadHandler implements CompletionHandler {  
9.     //用于读取半包消息和发送应答  
10.     private AsynchronousSocketChannel channel;  
11.     public ReadHandler(AsynchronousSocketChannel channel) {  
12.             this.channel = channel;  
13.     }  
14.     //读取到消息后的处理  
15.     @Override  
16.     public void completed(Integer result, ByteBuffer attachment) {  
17.         //flip操作  
18.         attachment.flip();  
19.         //根据  
20.         byte[] message = new byte[attachment.remaining()];  
21.         attachment.get(message);  
22.         try {  
23.             String expression = new String(message, "UTF-8");  
24.             System.out.println("服务器收到消息: " + expression);  
25.             String calrResult = null;  
26.             try{  
27.                 calrResult = Calculator.cal(expression).toString();  
28.             }catch(Exception e){  
29.                 calrResult = "计算错误：" + e.getMessage();  
30.             }  
31.             //向客户端发送消息  
32.             doWrite(calrResult);  
33.         } catch (UnsupportedEncodingException e) {  
34.             e.printStackTrace();  
35.         }  
36.     }  
37.     //发送消息  
38.     private void doWrite(String result) {  
39.         byte[] bytes = result.getBytes();  
40.         ByteBuffer writeBuffer = ByteBuffer.allocate(bytes.length);  
41.         writeBuffer.put(bytes);  
42.         writeBuffer.flip();  
43.         //异步写数据 参数与前面的read一样  
44.         channel.write(writeBuffer, writeBuffer,new CompletionHandler() {  
45.             @Override  
46.             public void completed(Integer result, ByteBuffer buffer) {  
47.                 //如果没有发送完，就继续发送直到完成  
48.                 if (buffer.hasRemaining())  
49.                     channel.write(buffer, buffer, this);  
50.                 else{  
51.                     //创建新的Buffer  
52.                     ByteBuffer readBuffer = ByteBuffer.allocate(1024);  
53.                     //异步读  第三个参数为接收消息回调的业务Handler  
54.                     channel.read(readBuffer, readBuffer, new ReadHandler(channel));  
55.                 }  
56.             }  
57.             @Override  
58.             public void failed(Throwable exc, ByteBuffer attachment) {  
59.                 try {  
60.                     channel.close();  
61.                 } catch (IOException e) {  
62.                 }  
63.             }  
64.         });  
65.     }  
66.     @Override  
67.     public void failed(Throwable exc, ByteBuffer attachment) {  
68.         try {  
69.             this.channel.close();  
70.         } catch (IOException e) {  
71.             e.printStackTrace();  
72.         }  
73.     }  
74. }  

    OK，这样就已经完成了，其实说起来也简单，虽然代码感觉很多，但是API比NIO的使用起来真的简单多了，主要就是监听、读、写等各种CompletionHandler。此处本应有一个WriteHandler的，确实，我们在ReadHandler中，以一个匿名内部类实现了它。

    下面看客户端代码。

    3.2、Client端代码

    Client：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5275/1C799AF3F81148F8834C874572F6A654)

![0](https://note.youdao.com/yws/res/5249/40CA3B9120A54002996B8CC157E4F3E3)

1. package com.anxpp.io.calculator.aio.client;  
2. import java.util.Scanner;  
3. public class Client {  
4.     private static String DEFAULT_HOST = "127.0.0.1";  
5.     private static int DEFAULT_PORT = 12345;  
6.     private static AsyncClientHandler clientHandle;  
7.     public static void start(){  
8.         start(DEFAULT_HOST,DEFAULT_PORT);  
9.     }  
10.     public static synchronized void start(String ip,int port){  
11.         if(clientHandle!=null)  
12.             return;  
13.         clientHandle = new AsyncClientHandler(ip,port);  
14.         new Thread(clientHandle,"Client").start();  
15.     }  
16.     //向服务器发送消息  
17.     public static boolean sendMsg(String msg) throws Exception{  
18.         if(msg.equals("q")) return false;  
19.         clientHandle.sendMsg(msg);  
20.         return true;  
21.     }  
22.     @SuppressWarnings("resource")  
23.     public static void main(String[] args) throws Exception{  
24.         Client.start();  
25.         System.out.println("请输入请求消息：");  
26.         Scanner scanner = new Scanner(System.in);  
27.         while(Client.sendMsg(scanner.nextLine()));  
28.     }  
29. }  

    AsyncClientHandler：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5258/DAA00E8BA99D42EEAFF647C76F28167E)

![0](https://note.youdao.com/yws/res/5247/977DB79E8698495EAFD92AA282810BC6)

1. package com.anxpp.io.calculator.aio.client;  
2. import java.io.IOException;  
3. import java.net.InetSocketAddress;  
4. import java.nio.ByteBuffer;  
5. import java.nio.channels.AsynchronousSocketChannel;  
6. import java.nio.channels.CompletionHandler;  
7. import java.util.concurrent.CountDownLatch;  
8. public class AsyncClientHandler implements CompletionHandler, Runnable {  
9.     private AsynchronousSocketChannel clientChannel;  
10.     private String host;  
11.     private int port;  
12.     private CountDownLatch latch;  
13.     public AsyncClientHandler(String host, int port) {  
14.         this.host = host;  
15.         this.port = port;  
16.         try {  
17.             //创建异步的客户端通道  
18.             clientChannel = AsynchronousSocketChannel.open();  
19.         } catch (IOException e) {  
20.             e.printStackTrace();  
21.         }  
22.     }  
23.     @Override  
24.     public void run() {  
25.         //创建CountDownLatch等待  
26.         latch = new CountDownLatch(1);  
27.         //发起异步连接操作，回调参数就是这个类本身，如果连接成功会回调completed方法  
28.         clientChannel.connect(new InetSocketAddress(host, port), this, this);  
29.         try {  
30.             latch.await();  
31.         } catch (InterruptedException e1) {  
32.             e1.printStackTrace();  
33.         }  
34.         try {  
35.             clientChannel.close();  
36.         } catch (IOException e) {  
37.             e.printStackTrace();  
38.         }  
39.     }  
40.     //连接服务器成功  
41.     //意味着TCP三次握手完成  
42.     @Override  
43.     public void completed(Void result, AsyncClientHandler attachment) {  
44.         System.out.println("客户端成功连接到服务器...");  
45.     }  
46.     //连接服务器失败  
47.     @Override  
48.     public void failed(Throwable exc, AsyncClientHandler attachment) {  
49.         System.err.println("连接服务器失败...");  
50.         exc.printStackTrace();  
51.         try {  
52.             clientChannel.close();  
53.             latch.countDown();  
54.         } catch (IOException e) {  
55.             e.printStackTrace();  
56.         }  
57.     }  
58.     //向服务器发送消息  
59.     public void sendMsg(String msg){  
60.         byte[] req = msg.getBytes();  
61.         ByteBuffer writeBuffer = ByteBuffer.allocate(req.length);  
62.         writeBuffer.put(req);  
63.         writeBuffer.flip();  
64.         //异步写  
65.         clientChannel.write(writeBuffer, writeBuffer,new WriteHandler(clientChannel, latch));  
66.     }  
67. }  

    WriteHandler：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5276/2012A2ADB1B049F8926C53CE99055872)

![0](https://note.youdao.com/yws/res/5238/E2CD95258F00494A8591760E7FF71C6B)

1. package com.anxpp.io.calculator.aio.client;  
2. import java.io.IOException;  
3. import java.nio.ByteBuffer;  
4. import java.nio.channels.AsynchronousSocketChannel;  
5. import java.nio.channels.CompletionHandler;  
6. import java.util.concurrent.CountDownLatch;  
7. public class WriteHandler implements CompletionHandler {  
8.     private AsynchronousSocketChannel clientChannel;  
9.     private CountDownLatch latch;  
10.     public WriteHandler(AsynchronousSocketChannel clientChannel,CountDownLatch latch) {  
11.         this.clientChannel = clientChannel;  
12.         this.latch = latch;  
13.     }  
14.     @Override  
15.     public void completed(Integer result, ByteBuffer buffer) {  
16.         //完成全部数据的写入  
17.         if (buffer.hasRemaining()) {  
18.             clientChannel.write(buffer, buffer, this);  
19.         }  
20.         else {  
21.             //读取数据  
22.             ByteBuffer readBuffer = ByteBuffer.allocate(1024);  
23.             clientChannel.read(readBuffer,readBuffer,new ReadHandler(clientChannel, latch));  
24.         }  
25.     }  
26.     @Override  
27.     public void failed(Throwable exc, ByteBuffer attachment) {  
28.         System.err.println("数据发送失败...");  
29.         try {  
30.             clientChannel.close();  
31.             latch.countDown();  
32.         } catch (IOException e) {  
33.         }  
34.     }  
35. }  

    ReadHandler：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5261/916C8AF700EA4ECA9825C811A2D57910)

![0](https://note.youdao.com/yws/res/5241/B7AB043869A34BE9A521633C8C5FB88A)

1. package com.anxpp.io.calculator.aio.client;  
2. import java.io.IOException;  
3. import java.io.UnsupportedEncodingException;  
4. import java.nio.ByteBuffer;  
5. import java.nio.channels.AsynchronousSocketChannel;  
6. import java.nio.channels.CompletionHandler;  
7. import java.util.concurrent.CountDownLatch;  
8. public class ReadHandler implements CompletionHandler {  
9.     private AsynchronousSocketChannel clientChannel;  
10.     private CountDownLatch latch;  
11.     public ReadHandler(AsynchronousSocketChannel clientChannel,CountDownLatch latch) {  
12.         this.clientChannel = clientChannel;  
13.         this.latch = latch;  
14.     }  
15.     @Override  
16.     public void completed(Integer result,ByteBuffer buffer) {  
17.         buffer.flip();  
18.         byte[] bytes = new byte[buffer.remaining()];  
19.         buffer.get(bytes);  
20.         String body;  
21.         try {  
22.             body = new String(bytes,"UTF-8");  
23.             System.out.println("客户端收到结果:"+ body);  
24.         } catch (UnsupportedEncodingException e) {  
25.             e.printStackTrace();  
26.         }  
27.     }  
28.     @Override  
29.     public void failed(Throwable exc,ByteBuffer attachment) {  
30.         System.err.println("数据读取失败...");  
31.         try {  
32.             clientChannel.close();  
33.             latch.countDown();  
34.         } catch (IOException e) {  
35.         }  
36.     }  
37. }  

    这个API使用起来真的是很顺手。

    3.3、测试

    Test：

[java] [view plain](http://blog.csdn.net/anxpp/article/details/51512200#) [copy](http://blog.csdn.net/anxpp/article/details/51512200#)

 [print?](http://blog.csdn.net/anxpp/article/details/51512200#)

![0](https://note.youdao.com/yws/res/5257/CF2B87FC3284479DB65B2F73A39A27C4)

![0](https://note.youdao.com/yws/res/5248/9D145EDB5373400D83F7F4CCFAA616C2)

1. package com.anxpp.io.calculator.aio;  
2. import java.util.Scanner;  
3. import com.anxpp.io.calculator.aio.client.Client;  
4. import com.anxpp.io.calculator.aio.server.Server;  
5. /** 
6.  * 测试方法 
7.  * @author yangtao__anxpp.com 
8.  * @version 1.0 
9.  */  
10. public class Test {  
11.     //测试主方法  
12.     @SuppressWarnings("resource")  
13.     public static void main(String[] args) throws Exception{  
14.         //运行服务器  
15.         Server.start();  
16.         //避免客户端先于服务器启动前执行代码  
17.         Thread.sleep(100);  
18.         //运行客户端   
19.         Client.start();  
20.         System.out.println("请输入请求消息：");  
21.         Scanner scanner = new Scanner(System.in);  
22.         while(Client.sendMsg(scanner.nextLine()));  
23.     }  
24. }  

    我们可以在控制台输入我们需要计算的算数字符串，服务器就会返回结果，当然，我们也可以运行大量的客户端，都是没有问题的，以为此处设计为单例客户端，所以也就没有演示大量客户端并发。

    读者可以自己修改Client类，然后开辟大量线程，并使用构造方法创建很多的客户端测试。

    下面是其中一次参数的输出：

1. 服务器已启动，端口号：12345
2. 请输入请求消息：
3. 客户端成功连接到服务器...
4. 连接的客户端数：1
5. 123456+789+456
6. 服务器收到消息: 123456+789+456
7. 客户端收到结果:124701
8. 9526*56
9. 服务器收到消息: 9526*56
10. 客户端收到结果:533456
11. ...

    AIO是真正的异步非阻塞的，所以，在面对超级大量的客户端，更能得心应手。

    下面就比较一下，几种I/O编程的优缺点。

4、各种I/O的对比

    先以一张表来直观的对比一下：

![0](https://note.youdao.com/yws/res/5239/34932483E27B4EBEBBBF6A0079B33C4E)

    具体选择什么样的模型或者NIO框架，完全基于业务的实际应用场景和性能需求，如果客户端很少，服务器负荷不重，就没有必要选择开发起来相对不那么简单的NIO做服务端；相反，就应考虑使用NIO或者相关的框架了。

5、附录

    上文中服务端使用到的用于计算的工具类：

1. package com.anxpp.utils;

2. import javax.script.ScriptEngine;

3. import javax.script.ScriptEngineManager;

4. import javax.script.ScriptException;

5. public final class Calculator {

6. private final static ScriptEngine jse = new ScriptEngineManager().getEngineByName("JavaScript");

7. public static Object cal(String expression) throws ScriptException{

8. return jse.eval(expression);

9. }

10. }

    更多文章：

    [Java NIO框架Netty简单使用](http://blog.csdn.net/anxpp/article/details/52108238)

    后续会写一篇NIO框架Netty的教程，不过这段时间有一点小忙。

来源： [https://www.cnblogs.com/hujihon/p/6686363.html](https://www.cnblogs.com/hujihon/p/6686363.html)