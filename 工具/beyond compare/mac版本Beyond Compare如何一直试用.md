 Beyond Compare4 比较好用，但是用过 30 天以后不让用了。网上各种找密钥，本来网上的密钥资料就不多，几乎试了个遍，都不行。然后卸载，重装，卸载重装，不行。快绝望了，买正版吧，60 美刀，吓死宝宝。然后就想到了修改时间的的思路，但是大都是 windows 版的，在 windows 上，删除 BCUnrar.dill 就可以了。但是在 mac 上删除哪个文件呢？找了半天，找到以下：

    https://blog.csdn.net/jia12216/article/details/53101554

    他上面说的比较详细，按照人家的来，基本没什么问题。

Beyond Compare 是一种码农经常使用的代码比较工具。通过不断删除 registry.dat 来达到永远在试用 Beyond Compare 的方式。 

注意只有安装 Beyond Compare 成功并且运行过一次才能看到 registry.dat。当它试用期到期了，重新找到 registry.dat，那么你又得到 30 天的试用期了，不断这样到期前或到期后，删除 registry.dat，达到永远在试用期的效果。 

点击 mac 电脑的桌面，选择菜单栏的前往 ->电脑.可以看到我磁盘。注意要显示隐藏文件生效。 

MAC 中显示隐藏文件有很多种方法，最简单的是通过在 Mac 终端输入命令。 

显示隐藏文件（注意空格和大小写）： 

defaults write com.apple.finder AppleShowAllFiles -bool true 

或 

defaults write com.apple.finder AppleShowAllFiles YES

不显示隐藏文件： 

defaults write com.apple.finder AppleShowAllFiles -bool false 

或 

defaults write com.apple.finder AppleShowAllFiles NO

输入完成后，单击 Enter 键，然后直接退出终端，重新启动 Finder 即可。 

重启 Finder：首先强制退出 Finder，再重新启动 Finder 即可。 

点击电脑磁盘 ->用户 ->用户名 ->资源库（隐藏文件夹）->Application Support->Beyond Compare->registry.dat。删除这个文件就可以了。过一段时间删除一次就可以一直使用了。你的试用期永远是 30 天了。 

点赞 1

————————————————

版权声明：本文为 CSDN 博主「愿化身孤岛做你的鲸」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。

原文链接：https://blog.csdn.net/qq_36091574/article/details/80390301
