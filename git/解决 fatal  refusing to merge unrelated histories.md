Git 的报错

![](assets/解决%20fatal%20%20refusing%20to%20merge%20unrelated%20histories/file-20251121113427981.png)

一、fatal: refusing to merge unrelated histories

新建了一个仓库之后，把本地仓库进行关联提交、拉取的时候，出现了如下错误：

ankobot@DESKTOP-9IUDMKP MINGW64 /e/workspace/firmware_upload/firmware_upload (master) $ git pull fatal: refusing to merge unrelated histories

二、解决方案

在你操作命令后面加 --allow-unrelated-histories

例如：

git merge master --allow-unrelated-histories

$ git pull --allow-unrelated-histories CONFLICT (add/add): Merge conflict in .gitignore Auto-merging .gitignore Automatic merge failed; fix conflicts and then commit the result.

我这里由于使用了官方的 .gitignore 自动合并失败，需要手动合并之后再进行 add、commit 即可

如果你是 git pull 或者 git push 报 fatal: refusing to merge unrelated histories

同理：

git pull origin master --allow-unrelated-histories / git pull --allow-unrelated-histories

等等，就是这样完美的解决！
