搜索快捷键

      在编辑文档中，cmd+f 开始搜索 cmd + r 搜索替换

    在project中，按下cmd + shift + f(r) 即是在当前目前下递归查找或替换,搜索出来后，要全部替换，按下alt + a

    alt + F7      搜索对象被引用的地方

    cmd + F7   搜索对象在当前文件被引用的地方 

    cmd + n     查找类

    shift + cmd + n  查找文件

<mark style="background: #FF5582A6;">    双击shift      全局搜文件</mark>

    cmd + F12     查看类中所有的方法名 （Fn换出F12）

查看代码快捷键

     cmd + p                  查询某方法的参数信息

     cmd + b                  跳到调用方法的定义处

     option + cmd + b          跳到方法的实现处

     ctrl + up/down           跳到上/下一方法

     alt + cmd + left/right   跳到上/下一次光标查看处

     cmd + g                  跳到指定行

     cmd + shift + h          显示方法的层级结构

     alt + cmd + h            调用层级结构

View     

     cmd + [                  back

     cmd + ]                  forward

同样单词之间跳转:在Eclipse中的快捷键是ctrl+k，这个挺好用的，在IntelliJ中也不缺这个功能，但是在Mac OSX 10.5+的键位绑定中默认为空。据说Windows的默认绑定中是有绑定的，自己可以查询下，我自己绑定了一个⌘+ctrl+k (Find Word at Caret)，没有的需要自己绑定一个，然后还能结合其他的键位实现上一个⌘+G (Find Next)下一个⌘+Shift+G (Find Previous)的功能.很是实用。

实用快捷键:

Ctrl+/ 或 Ctrl+Shift+/ 注释（// 或者/*...*/ ）

Ctrl+D 复制行

Ctrl+X 删除行

快速修复 alt+enter (modify/cast)

代码提示 alt+/

ctr+G 定位某一行

Shift+F6 重构-重命名

Ctrl+R 替换文本

Ctrl+F 查找文本

Ctrl+E 最近打开的文件

Ctrl+J 自动代码

组织导入 ctr+alt+O

格式化代码 ctr+alt+L

大小写转化 ctr+shift+U

--------------------------

IntelliJ Idea 常用快捷键列表

Alt+回车 导入包,自动修正

Ctrl+N   查找类

Ctrl+Shift+N 查找文件

Ctrl+Alt+L  格式化代码

Ctrl+Alt+O 优化导入的类和包

Alt+Insert 生成代码(如get,set方法,构造函数等)

Ctrl+E或者Alt+Shift+C  最近更改的代码

Ctrl+R 替换文本

Ctrl+F 查找文本

Ctrl+Shift+Space 自动补全代码

Ctrl+空格 代码提示

Ctrl+Alt+Space 类名或接口名提示

Ctrl+P 方法参数提示

Ctrl+Shift+Alt+N 查找类中的方法或变量

Alt+Shift+C 对比最近修改的代码

Shift+F6  重构-重命名

Ctrl+Shift+先上键

Ctrl+X 删除行

Ctrl+D 复制行

Ctrl+/ 或 Ctrl+Shift+/  注释（// 或者/*...*/ ）

Ctrl+J  自动代码

Ctrl+E 最近打开的文件

Ctrl+H 显示类结构图

Ctrl+Q 显示注释文档

Alt+F1 查找代码所在位置

Alt+1 快速打开或隐藏工程面板

Ctrl+Alt+ left/right 返回至上次浏览的位置

Alt+ left/right 切换代码视图

Alt+ Up/Down 在方法间快速移动定位

Ctrl+Shift+Up/Down 代码向上/下移动。

F2 或Shift+F2 高亮错误或警告快速定位

代码标签输入完成后，按Tab，生成代码。

选中文本，按Ctrl+Shift+F7 ，高亮显示所有该文本，按Esc高亮消失。

Ctrl+W 选中代码，连续按会有其他效果

选中文本，按Alt+F3 ，逐个往下查找相同文本，并高亮显示。

Ctrl+Up/Down 光标跳转到第一行或最后一行下

Ctrl+B 快速打开光标处的类或方法 

------------------------------------------------------------------------------------------------------------

1. IDEA内存优化

因机器本身的配置而配置：

\IntelliJ IDEA 8\bin\idea.exe.vmoptions  

-----------------------------------------  

-Xms64m  

-Xmx256m  

-XX:MaxPermSize=92m  

-ea  

-server  

-Dsun.awt.keepWorkingSetOnMinimize=true

2. 查询快捷键

CTRL+N   查找类 

CTRL+SHIFT+N  查找文件 

CTRL+SHIFT+ALT+N 查找类中的方法或变量 

CIRL+B   找变量的来源 

CTRL+ALT+B  找所有的子类 

CTRL+SHIFT+B  找变量的类 

CTRL+G   定位行 

CTRL+F   在当前窗口查找文本 

CTRL+SHIFT+F  在指定窗口查找文本 

CTRL+R   在 当前窗口替换文本 

CTRL+SHIFT+R  在指定窗口替换文本 

ALT+SHIFT+C  查找修改的文件 

CTRL+E   最近打开的文件 

F3   向下查找关键字出现位置 

SHIFT+F3  向上一个关键字出现位置 

F4   查找变量来源 

CTRL+ALT+F7  选中的字符查找工程出现的地方 

CTRL+SHIFT+O  弹出显示查找内容

3. 自动代码

ALT+回车  导入包,自动修正 

CTRL+ALT+L  格式化代码 

CTRL+ALT+I  自动缩进 

CTRL+ALT+O  优化导入的类和包 

ALT+INSERT  生成代码(如GET,SET方法,构造函数等) 

CTRL+E 最近更改的代码 

CTRL+SHIFT+SPACE 自动补全代码 

CTRL+空格  代码提示 

CTRL+ALT+SPACE  类名或接口名提示 

CTRL+P   方法参数提示 

CTRL+J   自动代码 

CTRL+ALT+T  把选中的代码放在 TRY{} IF{} ELSE{} 里

4. 复制快捷方式

CTRL+D   复制行 

CTRL+X   剪切,删除行  

5. 其他快捷方式

CIRL+U   大小写切换 

CTRL+Z   倒退 

CTRL+SHIFT+Z  向前 

CTRL+ALT+F12  资源管理器打开文件夹 

ALT+F1   查找文件所在目录位置 

SHIFT+ALT+INSERT 竖编辑模式 

CTRL+/   注释//   

CTRL+SHIFT+/  注释/*...*/ 

CTRL+W   选中代码，连续按会有其他效果 

CTRL+B   快速打开光标处的类或方法 

ALT+ ←/→  切换代码视图 

CTRL+ALT ←/→  返回上次编辑的位置 

ALT+ ↑/↓  在方法间快速移动定位 

SHIFT+F6  重构-重命名 

CTRL+H   显示类结构图 

CTRL+Q   显示注释文档 

ALT+1   快速打开或隐藏工程面板 

CTRL+SHIFT+UP/DOWN 代码向上/下移动。 

CTRL+UP/DOWN  光标跳转到第一行或最后一行下 

ESC   光标返回编辑框 

SHIFT+ESC  光标返回编辑框,关闭无用的窗口 

F1   帮助千万别按,很卡! 

CTRL+F4   非常重要下班都用

------------------------------------------------------------------------------------------------------------

来源： [https://www.cnblogs.com/bluestorm/archive/2013/05/20/3087889.html](https://www.cnblogs.com/bluestorm/archive/2013/05/20/3087889.html)