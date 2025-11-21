所有业务代码提交 release 分支时，如不符合 commit message 规范，将被拒绝 push。

commit message 规范：

- 首行必须为:
- “TAPD ID:”前缀 + 对应需求 ID（该 ID 从 TAPD 平台获取），且该 ID 必须在本周的发布范围内。
- “RM ID:”前缀 + 对应需求 ID（该 ID 从 Redmine 平台获取），且该 ID 必须在本周的发布范围内 (即 Redmine 中的目标版本)。

示例：

TAPD ID: 56496974

RM ID: 734

该项由 git hooks: pre-receive 强制检测，意味着一次 push 中包含的若干个 commit，只要有一个不符合则全部 push 失败。

PS：前缀中的“:”为英文半角，多个 TAPD ID 使用英文半角逗号 "," 分割。

- 第二行起简述本次修改的类别、内容、范围等。

该项为建议项，不作强制检测。

commit message 修改：

- 执行 git rebase -i [commit id]

其中 commit id 为需要修改的 commit message 的前一个 commit

- 在后续的编辑框中会分行依次显示以 commit 之后的所有 commit message

将需要修改的 commit message 之前的 "pick" 改为 "reword"，保存退出

- 再次出现编辑框，此时修改 commit message 的内容，保存退出
