sz 命令

用途说明：sz 命令是利用 ZModem 协议来从 Linux 服务器传送文件到本地，一次可以传送一个或多个文件。相对应的从本地上传文件到 Linux 服务器，可以使用 rz 命令。

常用参数

-a 以文本方式传输（ascii）。

-b 以二进制方式传输（binary）。

-e 对控制字符转义（escape），这可以保证文件传输正确。

如果能够确定所传输的文件是文本格式的，使用 sz -a files

如果是二进制文件，使用 sz -be files

rz 命令

-b 以二进制方式，默认为文本方式。（Binary (tell it like it is) file transfer override.）

-e 对所有控制字符转义。（Force sender to escape all control characters; normally XON, XOFF, DLE, [CR-@-CR](mailto:CR-@-CR), and Ctrl-X are escaped.）

如果要保证上传的文件内容在服务器端保存之后与原始文件一致，最好同时设置这两个标志，如下所示方式使用：

rz -be

此命令执行时，会弹出文件选择对话框，选择好需要上传的文件之后，点确定，就可以开始上传的过程了。上传的速度取决于当时网络的状况。

如果执行完毕显示“0 错误”，文件上传就成功了，其他显示则表示文件上传出现问题了。

rz，sz 是 Linux/Unix 同 Windows 进行 ZModem 文件传输的命令行工具。

优点就是不用再开一个 sftp 工具登录上去上传下载文件。

sz：将选定的文件发送（send）到本地机器

rz：运行该命令会弹出一个文件选择窗口，从本地选择文件上传到 Linux 服务器

安装命令：

yum install lrzsz

从服务端发送文件到客户端：

sz filename

从客户端上传文件到服务端：

rz

在弹出的框中选择文件，上传文件的用户和组是当前登录的用户

SecureCRT 设置默认路径：

Options -> Session Options -> Terminal -> Xmodem/Zmodem ->Directories

Xshell 设置默认路径：

右键会话 -> 属性 -> ZMODEM -> 接收文件夹

测试：

开发板接收文件：

1. 进入开发板要接收文件的目录
2. 开发板执行命令# rz
3. 在 minicom 下，按住 Ctrl+A 键不放，按下 Z 键
4. 按下 S 键选择发送文件
5. 选择 zmodem，用回车键确认
6. 用空格选择主机要发送的文件，用回车键确认
7. 传输完成后按任意键返回

开发板发送文件：

1. 进入开发板要发送文件的目录
2. 进入主机要接收文件的目录
3. 主机执行命令# rz
4. 开发板执行命令# sz filename

PS：同事和我说 SecureCRT 可以方便的上传下载文件，而 Xshell 没有。我上网一查原来用的是同一个 sz/rz 工具，Xshell 下没有菜单选择要输命令。
