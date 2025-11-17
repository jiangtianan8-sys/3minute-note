**Linux `cd` 命令** 可以说是 Linux 中最基本的命令语句，其他的命令语句要进行操作，都是建立在使用 `cd` 命令上的。

所以，学习 Linux 常用命令，首先就要学好 `cd` 命令的使用方法技巧。

## 1. 命令格式：

`cd` [目录名]

## 2. 命令功能：

切换当前目录至 `dirName`

## 3. 常用范例

#### 例一：进入系统根目录

### 命令：

`cd /`

### 输出：

`` [root@localhost ~]# `cd /` ``

### 说明：

进入系统根目录, 上面命令执行完后拿 `ls` 命令看一下，当前目录已经到系统根目录了。

### 命令：

`cd ..` 或者 `cd ..//`

### 输出：

``1 [root@localhost soft]# `pwd` 2 /opt/soft 3 [root@localhost soft]# `cd ..` 4 [root@localhost opt]# `cd ..//` 5 [root@localhost /]# `pwd` 6 /``

### 说明：

进入系统根目录可以使用 `cd ..` 一直退，就可以到达根目录。

### 命令：

`cd ../.. //`

### 输出：

``1 [root@localhost soft]# `pwd` 2 /opt/soft 3 [root@localhost soft]# `cd ../.. //` 4 [root@localhost /]# `pwd` 5 / 6 [root@localhost /]#``

### 说明：

使用 `cd` 命令实现进入当前目录的父目录的父目录。

#### 例 2：使用 `cd` 命令进入当前用户主目录

“当前用户主目录”和“系统根目录”是两个不同的概念。进入当前用户主目录有两个方法。

命令 1：

`cd`

### 输出：

``1 [root@localhost soft]# `pwd` 2 /opt/soft 3 [root@localhost soft]# `cd` 4 [root@localhost ~]# `pwd` 5 /root``

命令 2：

`cd ~`

### 输出：

``1 [root@localhost ~]# `cd /opt/soft/` 2 [root@localhost soft]# `pwd` 3 /opt/soft``

---