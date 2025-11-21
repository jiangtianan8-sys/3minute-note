一、前言

市面上有很多抓包工具，本文不会教大家如何使用抓包工具去 Crack，那是犯法的事儿，咱不做；本文使用抓包工具来分析一些应用的接口，例如：测试人员可以利用抓包工具来快速判断是前端请求问题，还是后端接口数据返回不对；再或者，我们发布了 App 到了市场，用户下载 / 更新 App 后，反馈 App 有 bug，虽然服务端可以查看海量日志，但我们利用抓包工具，根据用户的问题描述，来复现问题，也能够极快的定位问题，并寻找解决方案。

Windows 有很多抓包工具，例如：Fiddler，WirShark；而在 Mac 中，比较著名的就是 Charles，Charles 支持三个 Windows、Linux 和 Mac。目前，大多数服务端都支持 Https ，因此，大部分抓包出来的数据都是密文，那如何获取明文数据呢？

本篇文章是一篇小白文，告诉大家如何安装 Charles，如何通过『中间者』来代理请求，与服务端进行交互，获取明文数据。

二、中间者

中间者在网络中，通常用作数据截获，并窜改数据再发送，因此，可以用作一种网络攻击方式。『游戏外挂』就是中间者，它作为 Client / Server 之间的中间者，通过窜改 Client 发送到请求，再发送到 Server，来欺骗服务端达到一种数据窜改的效果。

抓包工具 Charles 就能作为中间者，当然，我们不是用来窜改数据来欺骗服务端造假，而是为了截获加密的数据，并明文展示出来。但是，这是有几点我们需要指出（因为中间者不是万能的，不是所有情况都能这么干，一定是有一定有 bug，我们才能使用这种方式）：

Server 端装有 Https 证书，而 Client 端没有，且 Client 端是完全信认 Server 端的，并且两者没有采用其它的数据加密方式，那么，我们可以使用中间者来进行两者之间的代理交互。

上面这个条件，或者说数据安全措施还是比较低的，所谓防君子不防小人，如果遇到：『Client 与 Server 之间的数据是加密传输的，那么我们就很难截获密文』。两端数据加密的方式就多种，例如：采用 AES（对称加密）、RSA （非对称加密）或是私有数据加密协议。

proxy.png

上图 1 是正常的 Client 与 Server 交互流程，采用了 HTTPS 数据加密；流程 2 加入了 Proxy（中间者），通过代理 Client 与 Server 之间的请求与返回，来达到数据截获：

对于 Client ，Proxy 相当于 Server，Client 将请求发送给 Proxy，Proxy 再转发给真正的 Server；

对于 Server，Proxy 相当于 Client，Proxy 将数据转发给 Server，Server 再将数据返回给 Proxy；

三、Charles 安装

3.1、安装

先到官网 https://www.charlesproxy.com/latest-release/download.do 下载对应的最新版本；

直接安装，然后去 https://www.charles.ren/ 该网站获取激活注册码（随意输入用户名，生成注册码）；

在 Charles 工具中完成注册激活即可；

启动 Charles ，软件会自动弹出对话框『是否根据系统自动完成配置』，选择『是』即可；

3.2、SSL 配置

选择『Proxy』-> 『SSL Proxying Settings』，如下图：

ssl-proxy-settings.png

添加 SSL 端口代理，如下图（点击 Location 下面的 Add 按钮，输入如下）：

ssl-proxying-settings.png

点击 OK 即完成设置，如下图（点击 OK）：

port.png

3.3、Proxy 配置

选择『Proxy』-> 『Proxy Settings』，如下图：

proxy-settings.png

如下图配置即可：

config.png

3.4、安装 PC 证书

pc-ssl.png

选择『Install Charles Root Certificate』，点击后可能有弹出对话框提示，也可能任何反应都没有，这时，我们要去 Mac 系统中的

key-app.png

钥匙串中，查找 Charles 证书，并设置为完全信认：

key-truth.png

双击该证书，选择『始终信认』即可：

full-truth.png

3.5、安装手机证书（以 iPhone 为例）

mobile-ssl.png

选择『Install Charles Root Certificate on a Mobile Device or Remote Browser』，Charles 会弹一个对话提示框：

tips.png

然后打开手机『设置』-> 『无线局域网』-> 选择当前连接的 WIFI，如下图操作步骤：

wifi-setting.png

再然后，打开手机浏览器，输入『chls.pro/ssl』，点击『前往』：

download-cer.png

允许下载配置描述文件，下载完后，打开手机『设置』，操作流程如下：

mob-operation.png

OK，至此，我们的 Charles、PC 证书、手机证书都安装完成了！

3.6、测试抓包（京东 APP 为例）

test-proxy.png

1 人点赞

日记本

作者：青叶小小

链接：https://www.jianshu.com/p/8b65cdd8cdc6

来源：简书

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
