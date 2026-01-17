从这一节开始介绍锁里面的最后一个工具：读写锁(ReadWriteLock)。

ReentrantLock 实现了标准的互斥操作，也就是一次只能有一个线程持有锁，也即所谓独占锁的概念。前面的章节中一直在强调这个特点。显然这个特点在一定程度上面减低了吞吐量，实际上独占锁是一种保守的锁策略，在这种情况下任何“读/读”，“写/读”，“写/写”操作都不能同时发生。但是同样需要强调的一个概念是，锁是有一定的开销的，当并发比较大的时候，锁的开销就比较客观了。所以如果可能的话就尽量少用锁，非要用锁的话就尝试看能否改造为读写锁。

ReadWriteLock描述的是：一个资源能够被多个读线程访问，或者被一个写线程访问，但是不能同时存在读写线程。也就是说读写锁使用的场合是一个共享资源被大量读取操作，而只有少量的写操作（修改数据）。清单1描述了ReadWriteLock的API。

 清单1 ReadWriteLock 接口

public interface ReadWriteLock {

    Lock readLock();

    Lock writeLock();

}

清单1描述的ReadWriteLock结构，这里需要说明的是ReadWriteLock并不是Lock的子接口，只不过ReadWriteLock借助Lock来实现读写两个视角。在ReadWriteLock中每次读取共享数据就需要读取锁，当需要修改共享数据时就需要写入锁。看起来好像是两个锁，但其实不尽然，在下一节中的分析中会解释这点奥秘。

在JDK 6里面ReadWriteLock的实现是ReentrantReadWriteLock。

清单2 SimpleConcurrentMap

package xylz.study.concurrency.lock;

import java.util.ArrayList;

import java.util.Collection;

import java.util.HashSet;

import java.util.Map;

import java.util.Set;

import java.util.concurrent.locks.Lock;

import java.util.concurrent.locks.ReadWriteLock;

import java.util.concurrent.locks.ReentrantReadWriteLock;

public class SimpleConcurrentMap implements Map {

    final ReadWriteLock lock = new ReentrantReadWriteLock();

    final Lock r = lock.readLock();

    final Lock w = lock.writeLock();

    final Map map;

    public SimpleConcurrentMap(Map map) {

        this.map = map;

        if (map == null) throw new NullPointerException();

    }

    public void clear() {

        w.lock();

        try {

            map.clear();

        } finally {

            w.unlock();

        }

    }

    public boolean containsKey(Object key) {

        r.lock();

        try {

            return map.containsKey(key);

        } finally {

            r.unlock();

        }

    }

    public boolean containsValue(Object value) {

        r.lock();

        try {

            return map.containsValue(value);

        } finally {

            r.unlock();

        }

    }

    public Set> entrySet() {

        throw new UnsupportedOperationException();

    }

    public V get(Object key) {

        r.lock();

        try {

            return map.get(key);

        } finally {

            r.unlock();

        }

    }

    public boolean isEmpty() {

        r.lock();

        try {

            return map.isEmpty();

        } finally {

            r.unlock();

        }

    }

    public Set keySet() {

        r.lock();

        try {

            return new HashSet(map.keySet());

        } finally {

            r.unlock();

        }

    }

    public V put(K key, V value) {

        w.lock();

        try {

            return map.put(key, value);

        } finally {

            w.unlock();

        }

    }

    public void putAll(Map m) {

        w.lock();

        try {

            map.putAll(m);

        } finally {

            w.unlock();

        }

    }

    public V remove(Object key) {

        w.lock();

        try {

            return map.remove(key);

        } finally {

            w.unlock();

        }

    }

    public int size() {

        r.lock();

        try {

            return map.size();

        } finally {

            r.unlock();

        }

    }

    public Collection values() {

        r.lock();

        try {

            return new ArrayList(map.values());

        } finally {

            r.unlock();

        }

    }

}

清单2描述的是用读写锁实现的一个线程安全的Map。其中需要特别说明的是并没有实现entrySet()方法，这是因为实现这个方法比较复杂，在后面章节中讲到ConcurrentHashMap的时候会具体谈这些细节。另外这里keySet()和values()也没有直接返回Map的视图，而是一个映射原有元素的新视图，其实这个entrySet()一样，是为了保护原始Map的数据逻辑，防止不正确的修改导致原始Map发生数据错误。特别说明的是在没有特别需求的情况下没有必要按照清单2写一个线程安全的Map实现，因为ConcurrentHashMap已经完成了此操作。

ReadWriteLock需要严格区分读写操作，如果读操作使用了写入锁，那么降低读操作的吞吐量，如果写操作使用了读取锁，那么就可能发生数据错误。

另外ReentrantReadWriteLock还有以下几个特性：

- 公平性

- 非公平锁（默认） 这个和独占锁的非公平性一样，由于读线程之间没有锁竞争，所以读操作没有公平性和非公平性，写操作时，由于写操作可能立即获取到锁，所以会推迟一个或多个读操作或者写操作。因此非公平锁的吞吐量要高于公平锁。
- 公平锁 利用AQS的CLH队列，释放当前保持的锁（读锁或者写锁）时，优先为等待时间最长的那个写线程分配写入锁，当前前提是写线程的等待时间要比所有读线程的等待时间要长。同样一个线程持有写入锁或者有一个写线程已经在等待了，那么试图获取公平锁的（非重入）所有线程（包括读写线程）都将被阻塞，直到最先的写线程释放锁。如果读线程的等待时间比写线程的等待时间还有长，那么一旦上一个写线程释放锁，这一组读线程将获取锁。

- 重入性

- 读写锁允许读线程和写线程按照请求锁的顺序重新获取读取锁或者写入锁。当然了只有写线程释放了锁，读线程才能获取重入锁。
- 写线程获取写入锁后可以再次获取读取锁，但是读线程获取读取锁后却不能获取写入锁。
- 另外读写锁最多支持65535个递归写入锁和65535个递归读取锁。

- 锁降级

- 写线程获取写入锁后可以获取读取锁，然后释放写入锁，这样就从写入锁变成了读取锁，从而实现锁降级的特性。

- 锁升级

- 读取锁是不能直接升级为写入锁的。因为获取一个写入锁需要释放所有读取锁，所以如果有两个读取锁视图获取写入锁而都不释放读取锁时就会发生死锁。

- 锁获取中断

- 读取锁和写入锁都支持获取锁期间被中断。这个和独占锁一致。

- 条件变量

- 写入锁提供了条件变量(Condition)的支持，这个和独占锁一致，但是读取锁却不允许获取条件变量，将得到一个UnsupportedOperationException异常。

- 重入数

- 读取锁和写入锁的数量最大分别只能是65535（包括重入数）。这在下节中有介绍。

上面几个特性对读写锁的理解很有帮助，而且也是必要的，另外在下一节中讲ReadWriteLock的实现会用到这些知识的。