下载MAC版的ngrok：https://ngrok.com/download

解压到指定目录：

$ unzip -n ngrok-stable-darwin-amd64.zip -d /tmp

进入到解压后的ngrok所在路径：

$ cd /tmp

开启服务：

$ ./ngrok http localhost:8080

![0](https://note.youdao.com/yws/res/17121/D7D993EEFCB8486F9B43FD39BC99E582)

![0](https://note.youdao.com/yws/res/17123/C3844FF3A5664CEE9DE90FC563102D2E)

![0](https://note.youdao.com/yws/res/17125/D54E9FEEFE4E4E3A9AA948340E29B9BF)

输入命令后会先出现图1，图2的情况，稍等片刻，等Session Status显示为online状态时即可使用外网访问。即：以前使用http://localhost:8080/testWeb访问，现在便可使用http://744fb6df.ngrok.io/testWeb进行访问，http://744fb6df.ngrok.io就是本地服务映射到外网的地址。其中744fb6df不是固定的，在每次开始ngrok服务的时候都会变更。

转自：http://blog.csdn.net/u011886447/article/details/73268407

作者：Melody_YM

链接：https://www.jianshu.com/p/5c9d77d7a8f9

来源：简书

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。