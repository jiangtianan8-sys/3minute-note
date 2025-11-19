
> `cd` 命令是 Linux 入门必学的命令之一，是切换目录的基础。

---

# 1. 命令格式

```bash
cd [目录名]
```

---

# 2. 命令功能

- 切换当前目录至指定目录（dirName）

---

# 3. 常用范例

## 例一：进入系统根目录

- 命令：

```bash
cd /
```

- 输出：

```shell
[root@localhost ~]# cd /
```

- 说明：进入系统根目录，执行 ls 可查看当前目录确实到了根目录。

---

## 进入上级目录

- 命令：

```bash
cd ..
# 或者
cd ..//
```

- 输出：

```shell
[root@localhost soft]# pwd
/opt/soft
[root@localhost soft]# cd ..
[root@localhost opt]# cd ..//
[root@localhost /]# pwd
/
```

- 说明：一直使用 cd .. 可以逐步退回根目录。

---

## 进入上上级目录

- 命令：

```bash
cd ../..
```

- 输出：

```shell
[root@localhost soft]# pwd
/opt/soft
[root@localhost soft]# cd ../..
[root@localhost /]# pwd
/
```

- 说明：进入父目录的父目录。

---

## 例二：进入当前用户主目录

“当前用户主目录”和“系统根目录”不同。

- 方法 1：
    - 命令：

```bash
cd
```

    - 输出：

```shell
[root@localhost soft]# pwd
/opt/soft
[root@localhost soft]# cd
[root@localhost ~]# pwd
/root
```

- 方法 2：
    - 命令：

```bash
cd ~
```

    - 输出：

```shell
[root@localhost ~]# cd /opt/soft/
[root@localhost soft]# pwd
/opt/soft
```

---

> 更多 Linux 技巧敬请关注。
