使用 Beyond Compare 来进行文件对比及操作是提高生产力的最佳实践之一，请支持正版。

今天在使用 Beyond Compare 的时候发现。密钥被吊销了。于是我就想办法解决。以下是解决方法（我使用的系统是 mac）

# [#](https://shenzhiyong.com.cn/misc/BeyondCompare/#%E4%B8%80%E3%80%81%E8%AE%BF%E9%97%AEbeyond-compare%E6%96%87%E4%BB%B6%E5%A4%B9) 一、访问 Beyond Compare 文件夹

mac 用户 ~/Library/Application Support/Beyond Compare

win 用户 C:\Users\Admin\AppData\Roaming\Scooter Software\Beyond Compare 4

mac 用户，请按住 `command ⌘ + shift⇧ + g`，在弹出的对话框里面输入上面的路径。回车即可！

![](https://cdn.nlark.com/yuque/0/2025/png/35478707/1758251678951-2548a480-cccd-491b-b00b-6c3928ba050e.png)

# [#](https://shenzhiyong.com.cn/misc/BeyondCompare/#%E4%BA%8C%E3%80%81%E4%BF%AE%E6%94%B9bcstate-xml%E6%96%87%E4%BB%B6) 二、修改 BCState.xml 文件

打开 BCState.xml 文件，替换 TCheckForUpdatesState 标签。删除标签下面的所有内容，仅保留一项

```
<TCheckForUpdatesState>
    <Build Value="24545"/> 
</TCheckForUpdatesState>
```

# [#](https://shenzhiyong.com.cn/misc/BeyondCompare/#%E4%B8%89%E3%80%81%E4%BF%AE%E6%94%B9bcsessions-xml%E6%96%87%E4%BB%B6) 三、修改 BCSessions.xml 文件

打开 BCSessions.xml 文件,删除标签下面的所有内容。仅保留 `Version`, `MinVersion` 属性

```
<BCSessions Version="1" MinVersion="1">
</BCSessions>
```

本文仅为学习用，请支持正版，如有侵权请联系站长删除。
