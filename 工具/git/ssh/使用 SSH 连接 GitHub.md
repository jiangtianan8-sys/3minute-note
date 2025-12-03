一、生成 SSH 密钥
打开终端（命令行）并输入：

ssh-keygen -t rsa -b 4096 -C "你的GitHub邮箱"
智能体编程
bash
1
会提示保存路径，一般按回车即可（默认路径是 ~/.ssh/id_rsa）。
会让你输入密码，可以留空（或设置一把密码保护）。
生成成功后，会看到：

Your identification has been saved in /home/you/.ssh/id_rsa.
Your public key has been saved in /home/you/.ssh/id_rsa.pub.
智能体编程
text
1
2
📋 二、复制公钥
复制公钥内容（id_rsa.pub 文件）：

cat ~/.ssh/id_rsa.pub
智能体编程
bash
1
复制输出的那一整行内容（以 ssh-rsa 开头）。

三、添加 SSH 公钥到 GitHub
登录 GitHub官网。

点击右上角头像 → Settings。

左侧导航栏选择 SSH and GPG keys。

点击 “New SSH key”。

输入标题（比如 “My Laptop”），并粘贴刚才复制的公钥内容。

点击 “Add SSH key”。

四、测试 SSH 是否成功连接
在终端中运行：

ssh -T git@github.com
智能体编程
bash
1
第一次会问是否继续连接，输入 yes。

成功的话会显示：

Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
智能体编程
text
1
五、使用 SSH 克隆仓库
用 SSH 地址而不是 HTTPS 地址：

git clone git@github.com:你的用户名/你的仓库名.git
智能体编程
bash
1
比如：

git clone git@github.com:johnsmith/my-private-repo.git
智能体编程
bash
1
六、切换已存在仓库为 SSH 方式（可选）
如果你一开始用了 HTTPS，可以这样切换为 SSH：

cd 仓库目录
git remote set-url origin git@github.com:你的用户名/你的仓库名.git
智能体编程
bash
1
2
七、后续上传（无需再输入用户名密码）
以后提交代码时只需：

git add .
git commit -m "更新说明"
git push
智能体编程
bash
1
2
3
不会再要求输入用户名或密码。

异常
git push -u origin develop
fatal: unable to access ‘https://github.com/xxx.git/’: OpenSSL SSL_read: Connection was reset, errno 10054

表明 Git 在通过 HTTPS 方式连接 GitHub 时连接被重置。这个通常是由以下原因造成的：

✅ 建议改用 SSH（最推荐）
如果你已经配置过 SSH（参见上一步的 SSH 教程），直接改 remote 为 SSH 地址，问题通常就解决了：
git remote set-url origin git@github.com:xxx/xxx.git
智能体编程
bash
1
然后再执行：

git push -u origin develop
智能体编程
bash
1
ssh -T git@github.com
git@github.com: Permission denied (publickey).

说明你的 Git 正在尝试使用 SSH 连接 GitHub，但 GitHub 没有找到匹配的 SSH 公钥。

一、确认是否生成了 SSH 密钥
执行以下命令，检查密钥是否存在：

ls ~/.ssh
智能体编程
bash
1
你应该能看到如下文件：

id_rsa       # 私钥
id_rsa.pub   # 公钥
智能体编程
nginx
1
2
如果没有，就生成一对：

ssh-keygen -t rsa -b 4096 -C "你的GitHub邮箱"
智能体编程
bash
1
一路回车即可。

二、将公钥添加到 GitHub
<span style="color:rgb(255, 0, 0)">三、确认 SSH Agent 正常运行并加载密钥（Linux/macOS）<br>eval "$(ssh-agent -s)"<br>ssh-add ~/.ssh/id_rsa</span>
智能体编程
bash
1
2
如果是 Windows Git Bash，也可以运行上面这两行。

四、测试是否成功连接
ssh -T git@github.com
智能体编程
bash
1
如果配置正确，会显示：

Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
智能体编程
vbnet
1
五、如果你用了多个密钥（高级）
你可以创建 ~/.ssh/config 文件指定 GitHub 使用哪个密钥：

nano ~/.ssh/config   # 或用你喜欢的编辑器
智能体编程
bash
1
添加以下内容：

Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa
智能体编程
bash
1
2
3
4
保存后，再次测试连接。

最后一步：确认远程仓库使用的是 SSH 地址

git remote set-url origin git@github.com:你的用户名/你的仓库名.git
智能体编程
bash
1
git push
fatal: The current branch develop has no upstream branch.
To push the current branch and set the remote as upstream, use
git push --set-upstream origin develop

这个提示是因为你当前的 develop 分支 还没有关联远程分支，所以 Git 不知道要把它推到哪里。

解决方法
运行下面这条命令即可设置 origin 为 develop 分支的上游：

git push --set-upstream origin develop
智能体编程
bash
1
之后你就可以直接使用：

git push
智能体编程
bash
1
来提交了，无需再加任何参数。

背景解释
git push 其实是这样理解的：

如果你第一次推送某个新分支（如 develop），Git 不知道它应该对应远程的哪个分支。

所以你要用 --set-upstream 明确告诉 Git：这个分支的“上游”就是 origin/develop。

一旦设置后，Git 会记住，以后 git pull 和 git push 就默认用这个远程分支了。

小提示：你也可以用简写命令

git push -u origin develop
智能体编程
bash
1
-u 等价于 --set-upstream。
————————————————
版权声明：本文为CSDN博主「強云」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_42577742/article/details/149270517