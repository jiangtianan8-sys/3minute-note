如果不小心 commit 了一个不需要 commit 的文件，可以对其进行撤销。

先使用

|   |   |
|---|---|
|1|git log|

日志信息显示如下：

|     |                                                 |
| --- | ----------------------------------------------- |
| 1   | WARNING: terminal is not fully functional       |
| 2   | commit 197634d80f1aca2fefd4bb93ffb64bbf2af5bc1e |
| 3   | Author: /****hidden****EHOLDER}**/                        |
| 4   | Date:   Thu Jun 27 14:23:52 2013 +0800          |
| 6   | 新增 PHP 框架模块，此处采用 yii 框架                           |
| 8   | commit f093b6ed512f761a346e2e5c0f00230e448c217c |
| 9   | Author: /**hidden**EHOLDER}**/                        |
| 10  | Date:   Thu Jun 27 14:05:23 2013 +0800          |
| 12  | 创建 master，以生成 HEAD 仓                            |

本次由于添加了错误的 yii 框架版本，因此需要将第二次的提交强制撤销。

找到需要回退的那次 commit 的 哈希值，

|   |   |
|---|---|
|1|f093b6ed512f761a346e2e5c0f00230e448c217c|

执行

|   |   |
|---|---|
|1|git reset --hard f093b6ed512f761a346e2e5c0f00230e448c217c|

使用上面的命令进行回退

上述命令执行成功之后，会彻底返回到回退到的版本状态，新发生的变更将会丢失。

对于部分发生了变更，但是变更部分的文件夹存在未提交的文件可能导致目录非空而删除失败，此时需要自行处置

完成之后，使用 –force 或 -f 参数强制 push（本地分支和远程分支都是 develop）

|   |   |
|---|---|
|1|git push develop develop --force|

如果你使用 TortiseGit 工具的话，它应该是不具备 reset 支持的，至少我没找到。所以 reset 操作只能在命令行模式下进行。

如果你工作在 SSH 的公钥模式下，命令行操作可能比较麻烦，我暂时不知道如何将公钥带进来提交，因为我的 gitolite 服务不允许密码的，呵呵

查找了一些疑似文档，可能需要将自己的公钥添加到用户目录下的.ssh 的认证文件中，未测试~~~

此时可以使用 TortiseGit 工具选择 push，并在弹出的窗口选择 force 的复选框，提交对应的分支或者全部提交，如下图：

以下是豆瓣的

苍炎的日记 

起因: 不小新把记录了公司服务器 IP,账号,密码的文件提交到了 git

方法:

|   |   |
|---|---|
|1|git reset --hard|

|   |   |
|---|---|
|2||

|     |                              |
| --- | ---------------------------- |
| 3   | git push origin HEAD --force |

其他:

根据–soft –mixed –hard，会对 working tree 和 index 和 HEAD 进行重置:

git reset –mixed：此为默认方式，不带任何参数的 git reset，即时这种方式，它回退到某个版本，只保留源码，回退 commit 和 index 信息

git reset –soft：回退到某个版本，只回退了 commit 的信息，不会恢复到 index file 一级。如果还要提交，直接 commit 即可

git reset –hard：彻底回退到某个版本，本地的源码也会变为上一个版本的内容

HEAD 最近一个提交

HEAD^ 上一次

每次 commit 的 SHA1 值. 可以用 git log 看到,也可以在页面上 commit 标签页里找到
