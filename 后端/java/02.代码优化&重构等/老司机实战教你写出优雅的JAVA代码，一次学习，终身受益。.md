作者：xiaoniu

链接：https://zhuanlan.zhihu.com/p/33383648

来源：知乎

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

本文将以一个大家业务开发常见的场景，来教大家写出一手优雅的代码。

业务场景如下：

1. 充值话费，不同的充值方式享受不同的折扣（类似此需求的有很多，比如商品结算页面，不同的扣费渠道折扣不同等等）
2. 业务系统需要接入多个第三方渠道，不同的渠道处理不同的业务逻辑（这也是一个常见的业务需求）
3. 一套系统需要处理多个不同类型的业务（诸如可以提供多种形式的文件下载，可以选择下载excel，也可以选择下载word等等）
4. 诸如此类...

注：本文将涉及工厂模式 和策略模式，以及自定义注解。（自定义注解的目的是配置不同的渠道路由，除了使用注解，还可以使用xml配置文件等方式处理，各位具体可以自行定夺）

我们今天的需求就是页面选择不同的付款渠道，计算不同的折扣，进行扣款。需求界面如下：

![](assets/老司机实战教你写出优雅的JAVA代码，一次学习，终身受益。/file-20251128173533016.png)

选择不同的付款渠道，根据该渠道的优惠信息进行扣款。

很多新手在遇到诸如此类的需求的时候，想到的会是，很简单，if else 判段下就可以了嘛，if else 确实可以解决我们的问题，但是弊端也很明显：

- 代码冗长
- 维护不便，后面维护的人增加渠道，维护成本很大

---

OK.我们言简意赅（废话真多）进入正题，让我们一起来使用代码实战，一起写出优雅的业务代码。

1.构造一个策略接口

```java
package com.luffy.strategy;

/**
 * Created by jameslau on 2017/10/24.
 */
public interface Strategy {
    /**
     * 根据金额进行结算
     * @param charge 金额
     * @return
     */
    public Double calRecharge(Double charge);
}
```

2-1.多个结算渠道具体的结算实现类，实现类的数量视自己业务而定

```java
package com.luffy.pay.impls;

import com.luffy.pay.Calc;
import com.luffy.pay.PayTypeEnum;
import com.luffy.pay.Pays;

/**
 * Created by jameslau on 2017/11/16.
 */
@Pays(PayTypeEnum.CMBC)
public class CMBCPay implements Calc {

    /**工商银行的结算实现类
     * 这边就是具体业务代码的实现方法
     * 5元手续费
     * @return
     */
    public Double doCalculate(Double money) {

        return money+5;
    }
}
```

2-2多渠道实现类之浦发银行

```java
package com.luffy.pay.impls;

import com.luffy.pay.Calc;
import com.luffy.pay.PayTypeEnum;
import com.luffy.pay.Pays;

/**
 * Created by jameslau on 2017/11/16.
 */
@Pays(PayTypeEnum.ABC)
public class ABCPay implements Calc {

    /* 农业银行的结算实现类
     * 这边就是具体业务代码的实现方法
     * 优惠98折元折扣
     * @return
     */
    public Double doCalculate(Double money) {
        return money*0.98;
    }
}
```

2-N 具体有多少业务实现类，视自身业务而定

3.自定义注解，用来提供路由的类型

```java
package com.luffy.strategy;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Created by jameslau on 2017/11/2.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Pay {
    int value();
}
```

4.策略上下文

```java
package com.luffy.strategy;

/**
 * 策略上下文，这里就是根据类型路由到具体的实现类
 * Created by jameslau on 2017/10/24.
 */
public class Context {

    private Strategy strategy;

    public Double calRecharge(Double charge, Integer type) {

        try{
            strategy= StrategyFactory.getInstance().creator(type);
           }catch (Exception e){
            //log
        }

        return strategy.calRecharge(charge);
    }


    public Strategy getStrategy() {
        return strategy;
    }

    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }
}
```
5.工厂类，根据类型，把具体的实现类创建出来

```java
package com.luffy.strategy;

import com.luffy.common.RechargeTypeEnum;
import com.luffy.strategy.impl.*;
import org.dom4j.Document;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by jameslau on 2017/10/24.
 */
public class StrategyFactory {
    //生成我们的工厂对象
    private static StrategyFactory factory = new StrategyFactory();

    public StrategyFactory() {
    }

    public static HashMap<Integer, String> source_map = new HashMap<Integer, String>();
    static {
        //通过注解加载到map
        source_map= (HashMap<Integer, String>) ClassUtil.getClasses("com.luffy.strategy.impl");

    }


    //创建我们要的对象
    public Strategy creator(int type)throws  Exception{

        String clazz=source_map.get(type);
        Class clazz_= Class.forName(clazz);
        return  (Strategy)clazz_.newInstance();

    }

    //返回工厂对象
    public static StrategyFactory getInstance(){
        return factory;
    }
}
```

6.自定义注解加载

```java
package com.luffy.strategy;

import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.lang.annotation.Annotation;
import java.net.JarURLConnection;
import java.net.URL;
import java.net.URLDecoder;
import java.util.*;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

/**
 * Created by jameslau on 2017/11/2.
 */
public class ClassUtil {

    /**
     * 从包package中获取所有的Class
     * @param pack
     * @return
     */
    public static HashMap<Integer, String> getClasses(String pack) {

        //定义一个MAP用于存放type 和类路径的映射
        HashMap<Integer, String> map = new HashMap<Integer, String>();

        // 是否循环迭代
        boolean recursive = true;
        // 获取包的名字 并进行替换
        String packageName = pack;
        String packageDirName = packageName.replace('.', '/');
        // 定义一个枚举的集合 并进行循环来处理这个目录下的things
        Enumeration<URL> dirs;
        try {
            dirs = Thread.currentThread().getContextClassLoader().getResources(
                    packageDirName);
            // 循环迭代下去
            while (dirs.hasMoreElements()) {
                // 获取下一个元素
                URL url = dirs.nextElement();
                // 得到协议的名称
                String protocol = url.getProtocol();
                // 如果是以文件的形式保存在服务器上
                if ("file".equals(protocol)) {
                    System.err.println("file类型的扫描");
                    // 获取包的物理路径
                    String filePath = URLDecoder.decode(url.getFile(), "UTF-8");
                    // 以文件的方式扫描整个包下的文件 并添加到集合中
                    findAndAddClassesInPackageByFile(packageName, filePath,
                            recursive, map);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return map;
    }

    /**
     * 以文件的形式来获取包下的所有Class
     *
     * @param packageName
     * @param packagePath
     * @param recursive
     * @param
     */
    public static void findAndAddClassesInPackageByFile(String packageName,
                                                        String packagePath, final boolean recursive, Map<Integer, String> map) {
        // 获取此包的目录 建立一个File
        File dir = new File(packagePath);
        // 如果不存在或者 也不是目录就直接返回
        if (!dir.exists() || !dir.isDirectory()) {
            // log.warn("用户定义包名 " + packageName + " 下没有任何文件");
            return;
        }
        // 如果存在 就获取包下的所有文件 包括目录
        File[] dirfiles = dir.listFiles(new FileFilter() {
            // 自定义过滤规则 如果可以循环(包含子目录) 或则是以.class结尾的文件(编译好的java类文件)
            public boolean accept(File file) {
                return (recursive && file.isDirectory())
                        || (file.getName().endsWith(".class"));
            }
        });
        // 循环所有文件
        for (File file : dirfiles) {
            // 如果是目录 则继续扫描
            if (file.isDirectory()) {
                findAndAddClassesInPackageByFile(packageName + "."
                                + file.getName(), file.getAbsolutePath(), recursive,
                        map);
            } else {
                // 如果是java类文件 去掉后面的.class 只留下类名
                String className = file.getName().substring(0,
                        file.getName().length() - 6);
                try {

                    String fullPath= packageName + '.' + className;

                    //使用注解塞map
                    Class clazz = Class.forName(fullPath);
                    Annotation[] annotations= clazz.getAnnotations();
                    for(Annotation annotation:annotations){
                         //自行完善
                        Pay pay = (Pay) annotation;
                        map.put(pay.value(),  fullPath);
                    }
                } catch (ClassNotFoundException e) {
                    // log.error("添加用户自定义视图类错误 找不到此类的.class文件");
                    e.printStackTrace();
                }
            }
        }
    }
}
```

7.controller控制层负责接收类型，提供给策略模式进行路由

@RequestMapping("/pay") @ResponseBody public String doPay(Double charge, int type)throws Exception{ com.luffy.pay.Context context = new com.luffy.pay.Context(); Double actualAmount= context.doCalculate(type, 100d); return actualAmount+""; }

8.具体的页面代码，由于毫无审美，就不提供了。
```java
@RequestMapping("/pay")
    @ResponseBody
    public  String doPay(Double charge, int type)throws Exception{
       
        com.luffy.pay.Context context = new com.luffy.pay.Context();
        Double actualAmount= context.doCalculate(type, 100d);
        return actualAmount+"";
    }
```
结束语：至此我们业务就完成了，可能大家会觉得，设计模式的引入反而造成了类爆炸，还不如直接if else写在一个文件里的直观。但是，对于新增一个付款渠道，如果使用策略和自定义注解的方式将变得很简单，只要定义一个具体的实现类，上面加上渠道的注解就解决了，根本不需要去阅读之前别人写的其他支付渠道的代码，松耦合的目的就在于此。各位有没有觉得代码变得优雅了捏~

如果在编程道路上有什么困惑欢迎大家加入互联网技术交流圈，这里有一群爱分享的年轻人。