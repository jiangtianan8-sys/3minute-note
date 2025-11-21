通常在发布软件的时候打一个 tag，tag 会记录版本的 commit 号，方便后期回溯。

列出已有的 tag

git tag

显示 tag

加上 -l 命令可以使用通配符来过滤 tag

tag 显示过滤

新建 tag

使用 git tag 命令跟上 tag 名字，直接创建一个 tag。

<span style="color:red">git tag v1.0</span>

上面创建一个名为 v1.0 的 tag。使用 git tag 命令可以看到新增加的 tag。

创建 tag

还可以加上 -a 参数来创建一个带备注的 tag，备注信息由 -m 指定。如果你未传入 -m 则创建过程系统会自动为你打开编辑器让你填写备注信息。

git tag -a tagName -m "my tag"

创建有备注信息的 tag

查看 tag 详细信息

git show 命令可以查看 tag 的详细信息，包括 commit 号等。

git show tagName

查看 v1.0tag 的详细信息

查看带备注的 v1.1 的详细信息

tag 最重要的是有 git commit 号，后期我们可以根据这个 commit 号来回溯代码。

给指定的某个 commit 号加 tag

打 tag 不必要在 head 之上，也可在之前的版本上打，这需要你知道某个提交对象的校验和（通过 git log 获取，取校验和的前几位数字即可）。

git tag -a v1.2 9fceb02 -m "my tag"

将 tag 同步到远程服务器

同提交代码后，使用 git push 来推送到远程服务器一样，tag 也需要进行推送才能到远端服务器。

使用 git push origin [tagName] 推送单个分支。

<span style="color:red">git push origin v1.0</span>

推送本地所有 tag，使用 git push origin --tags。

切换到某个 tag

跟分支一样，可以直接切换到某个 tag 去。这个时候不位于任何分支，处于游离状态，可以考虑基于这个 tag 创建一个分支。

删除某个 tag

本地删除

<span style="color:red">git tag -d v0.1.2</span>

远端删除

git push origin :refs/tags/

<span style="color:red">git push origin :refs/tags/v0.1.2</span>

作者：清风流苏

链接：https://www.jianshu.com/p/cdd80dd15593

来源：简书

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
