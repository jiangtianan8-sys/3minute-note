对于做运维的同学来说，给两台 UNIX/Linux 机器建立 ssh 信任关系是再经常不过的事情了。

不知道大家之前建立信任关系是采用什么方法，反正我是纯手工创建。

如果需要“machineA 机器的 nameA 账号”建立到“machineB 机器的 nameB 账号”的 ssh 信任关系，达到无需输密码即可登陆的目的，那么我一般是这样做的：

1 将 machineA 机器的/home/nameA/.ssh/id_rsa.pub 文件的内容拷贝出来 2 登陆到 machineB 机器的/home/nameB/.ssh 中，如果不存在则创建 authorized_keys 文件， 将第 1 步中的内容追加到文件尾部。 3 检查 authorized_keys 文件的权限，确保其 group/other 位没有 w 权限 4 登陆到 machineA 机器，测试 ssh 信任关系是否建好

其实上面的添加机器信任关系的方法很不友好，需要全手工操作，而且要两台机器之间来来回回切换，且操作正确性完全由人保证，很容易出现问题和错误。

现在，隆重推出“SSH 信任关系自动化建立工具”：ssh-copy-id。（这是一个划时代的时刻，让我学会了使用工具^_^）

【五分钟学会 ssh-copy-id】

在不建立 ssh 信任关系的情况下，从 machineA 机器的 nameA 登陆到 machineB 机器的 nameB，可以看出是需要输入密码的：

[nameA@machineA]$ ssh nameB@machineB -p 22000 nameB@machineB's password:

我们现在就用新学到的命令建立信任关系，但是却提示“没有找到标识”，这是因为我们的 nameA 账号还没有自己的公钥私钥：

[nameA@machineA]$ ssh-copy-id nameB@machineB /usr/bin/ssh-copy-id: ERROR: No identities found

我们需要现为 nameA 账号建立自己的公钥私钥，建立好之后，会在/home/nameA/.ssh 里多出 id_rsa（私钥）和 id_rsa.pub（公钥）两个文件：

[nameA@machineA]$ ssh-keygen -t rsa Generating public/private rsa key pair. Enter file in which to save the key (/home/nameA/.ssh/id_rsa): Enter passphrase (empty for no passphrase): Enter same passphrase again: Your identification has been saved in /home/nameA/.ssh/id_rsa. Your public key has been saved in /home/nameA/.ssh/id_rsa.pub. The key fingerprint is: bb:3b:14:be:5d:45:ab:72:27:ec:93:21:c6:a3:7d:77 nameA@machineA The key's randomart image is: +--[ RSA 2048]----+ | | | | | | | . . | | .X. o . | | .o. + | | .*+.o | | +++C+o E | | . +C++ . | +-----------------+

好了，准备工作就绪，我们开始建立信任关系：

[nameA@machineA]$ ssh-copy-id nameB@machineB ssh: connect to host machineB port 22: Connection refused

悲剧，新的错误提示又来了，原来我们的 B 机器的 sshd 的服务端口不是 22，而是 22000，但是 ssh-copy-id 命令却不知道这个信息。这可如何是好。

我们试试加个 -p 参数设置下端口：

[nameA@machineA]$ ssh-copy-id nameB@machineB -p 22000 ssh: connect to host machineB port 22: Connection refused

还是不好使，-p 参数完全没有被 ssh-copy-id 命令识别。

如果你 man ssh-copy-id 就可以看到它根本就没有这个选项的。

好吧，不卖关子了，其实解决办法一点也不复杂，只是用了一个小技巧，那就是：

[nameA@machineA]ssh-copy-id "-p 22000 nameB@machineB" nameB@machineB's password: [nameB@machineB]

大功告成，终于可以无密码登陆了：

[nameA@machineA]$ ssh nameB@machineB -p 22000 [nameB@machineB]$

其实 ssh-copy-id 是一个普普通通的脚本文件：

[nameA@machineA]$ which ssh-copy-id /usr/bin/ssh-copy-id [nameA@machineA]$ file /usr/bin/ssh-copy-id /usr/bin/ssh-copy-id: POSIX shell script text executable

如果你有兴趣，可以读一读这个脚本，只有短短 50 行，不过里面却有不少 shell 编程技巧可以学习。

谢谢！
