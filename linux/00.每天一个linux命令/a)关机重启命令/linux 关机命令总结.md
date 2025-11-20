linux 下常用的关机命令有：shutdown、halt、poweroff、init；重启命令有：reboot。下面本文就主要介绍一些常用的关机命令以及各种关机命令之间的区别和具体用法。

首先来看一下 linux 下比较常用的一些关机命令

关机命令：

1、halt   立刻关机 2、poweroff  立刻关机 3、shutdown -h now 立刻关机 (root 用户使用) 4、shutdown -h 10 10 分钟后自动关机 如果是通过 shutdown 命令设置关机的话，可以用 shutdown -c 命令取消重启

重启命令：

1、reboot 2、shutdown -r now 立刻重启 (root 用户使用) 3、shutdown -r 10 过 10 分钟自动重启 (root 用户使用)  4、shutdown -r 20:35 在时间为 20:35 时候重启 (root 用户使用) 如果是通过 shutdown 命令设置重启的话，可以用 shutdown -c 命令取消重启

下面我们来看看 linux 的这些具体的关机命令之间的区别和各自的用法

1.shutdown 安全的关机命令

对于 shutdown 命令，它是大家都推荐的一个安全的命令，通过参数 -h 或 -r 的配合来完成关机或重启。不过在 linux 系统中只有拥有 root 权限才可以使用这个命令。所以，虽然大家都推荐用这个命令，但是这个命令用起来真的不太方便：想要用这个命令吗？先去获得 root 权限吧。shutdown 执行关机，是送信号给 init，要求它改变运行级别，以此来关机。关机或重启实际上是运行级别的调整，所以我们也可以用 init 直接调整运行级别来进行关机或重启。使用这个命令时，机器立即关机或重启。它也需要 root 权限。

那么为什么说 shutdown 命令是安全地将系统关机呢？

实际中有些用户会使用直接断掉电源的方式来关闭 linux，这是十分危险的。因为 [linux](http://www.phpernote.com/linux/) 与 [windows](http://www.phpernote.com/windows-7/) 不同，其后台运行着许多进程，所以强制关机可能会导致进程的数据丢失使系统处于不稳定的状态。甚至在有的系统中会损坏硬件设备。而在系统关机前使用 shutdown 命令，系统管理员会通知所有登录的用户系统将要关闭。并且 login 指令会被冻结，即新的用户不能再登录。直接关机或者延迟一定的时间才关机都是可能的，还有可能是重启。这是由所有进程〔process〕都会收到系统所送达的信号〔signal〕决定的。

shutdown 执行它的工作是送信号〔signal〕给 init 程序，要求它改变 runlevel。runlevel 0 被用来停机〔halt〕，runlevel 6 是用来重新激活〔reboot〕系统，而 runlevel 1 则是被用来让系统进入管理工作可以进行的状态，这是预设的。假定没有 -h 也没有 -r 参数给 shutdown。要想了解在停机〔halt〕或者重新开机〔reboot〕过程中做了哪些动作？你可以在这个文件/etc/inittab 里看到这些 runlevels 相关的资料。

shutdown 参数说明:

[-t] 在改变到其它 runlevel 之前，告诉 init 多久以后关机。 [-r] 重启计算器。 [-k] 并不真正关机，只是送警告信号给每位登录者〔login〕。 [-h] 关机后关闭电源〔halt〕。 [-n] 不用 init 而是自己来关机。不鼓励使用这个选项，而且该选项所产生的后果往往不总是你所预期得到的。 [-c] cancel current process 取消目前正在执行的关机程序。所以这个选项当然没有时间参数，但是可以输入一个用来解释的讯息，而这信息将会送到每位使用者。 [-f] 在重启计算器〔reboot〕时忽略 fsck。   [-F] 在重启计算器〔reboot〕时强迫 fsck。 [-time] 设定关机〔shutdown〕前的时间。 　　 　　 2.halt 最简单的关机命令

用 halt 命令来关机时，实际调用的是 shutdown -h。halt 执行时将杀死应用进程，执行 sync 系统调用文件系统写操作完成后就会停止内核。

halt 参数说明:

[-n] 防止 sync 系统调用，它用在用 fsck 修补根分区之后，以阻止内核用老版本的超级块〔superblock〕覆盖修补过的超级块。 [-w] 并不是真正的重启或关机，只是写 wtmp〔/var/log/wtmp〕纪录。 [-d] 不写 wtmp 纪录〔已包含在选项 [-n] 中〕。 [-f] 没有调用 shutdown 而强制关机或重启。 [-i] 关机〔或重启〕前关掉所有的网络接口。 [-p] 该选项为缺省选项。就是关机时调用 poweroff。

3.poweroff 常用的关机命令

对于 poweroff，网上说它是 halt 命令的链接，基本用法和 halt 差不多，这里就不多说了。

4.init

init 是所有进程的祖先，他是 Linux 系统操作中不可缺少的程序之一。它的进程号始终为 1，所以发送 TERM 信号给 init 会终止所有的用户进程，守护进程等。shutdown 就是使用这种机制。init 定义了 8 个运行级别 (runlevel)，init 0 为关机，init 1 为重启。

5.reboot 重启命令

reboot 的工作过程差不多跟 halt 一样。不过它是引发主机重启，而 halt 是关机。它的参数与 halt 相差不多。
