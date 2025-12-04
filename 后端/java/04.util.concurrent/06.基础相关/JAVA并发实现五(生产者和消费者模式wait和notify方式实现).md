package com.subject01;

import java.util.PriorityQueue;

/**

 * 通过wait和notify 实现

 * 生产者-消费者模型：当队列满时，生产者需要等待队列有空间才能继续往里面放入商品，而在等待的期间内，

 *          生产者必须释放对临界资源（即队列）的占用权。因为生产者如果不释放对临界资源的占用权，

 *          那么消费者就无法消费队列中的商品，就不会让队列有空间，那么生产者就会一直无限等待下去。

 *          因此，一般情况下，当队列满时，会让生产者交出对临界资源的占用权，并进入挂起状态。

 *          然后等待消费者消费了商品，然后消费者通知生产者队列有空间了。

 *          同样地，当队列空时，消费者也必须等待，等待生产者通知它队列中有商品了。这种互相通信的过程就是线程间的协作。

 * com.subject01.CusAndPro.java

 * @author 孙涛

 * 2016年5月10日

 */

public class CusAndPro {

    private int queueSize = 10 ;

    private PriorityQueue queue = new PriorityQueue(queueSize);

    public static void main(String[] args) {

        CusAndPro cap = new CusAndPro();

        Consumer cus = cap.new Consumer();

        Producer pro = cap.new Producer();

        Thread cusT = new Thread(cus);

        Thread proT = new Thread(pro);

        proT.start();

        cusT.start();

    }

    /**

     * 消费者

     * com.subject01.CusAndPro.java

     * @author 孙涛

     * 2016年5月10日

     */

    class Consumer implements Runnable{

        @Override

        public void run() {

            cousume();

        }

        private void cousume() {

            while(true){

                synchronized (queue) {

                    while(queue.size() ==0){

                        try {

                            System.out.println("队列空，等待数据。。。");

                            queue.wait();

                        } catch (InterruptedException e) {

                            e.printStackTrace();

                            queue.notify();

                        }

                    }

                    queue.poll() ;

                    queue.notify();

                    System.out.println("从队列中取走一个元素，队列中剩余"+queue.size()+"个");

                }

            }

        }

    }

    /**

     * 生产者

     * com.subject01.CusAndPro.java

     * @author 孙涛

     * 2016年5月10日

     */

    class Producer implements Runnable{

        @Override

        public void run() {

            produce();

        }

        private void produce() {

            while(true){

                synchronized(queue){

                    while(queue.size() == queueSize){

                        try {

                            System.out.println("队列已满，等待空余的空间");

                            queue.wait();

                        } catch (InterruptedException e) {

                            e.printStackTrace();

                            queue.notify();

                        }

                    }

                    queue.offer(1);   // 每次插入一个元素

                    queue.notify();

                    System.out.println("向队列取中插入一个元素，队列剩余空间："+(queueSize-queue.size()));

                }

            }

        }

    }

}

来源： [http://www.cnblogs.com/xiaotao726/p/5476644.html](http://www.cnblogs.com/xiaotao726/p/5476644.html)