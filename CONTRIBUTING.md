

# 第一次参与开源

万事起头难。特别是和其他人合作时，犯错格外令人不舒服。不过，开源的本质就是和其他人合作。我们希望为初学者带来一个简单的方法去学 xi 及参与开源项目。

阅读文章和观看教程会有所帮助。不过，有什么方法能比实际动手做更好？本项目旨在指导初学者及简化初学者参与开源的方式。记住：过程越轻松，学 xi 效益越高。如果你想要做出第一次贡献，只需按照以下简单步骤操作即可。我们答应你，这将很好玩 :)

<img align="right" width="300" src="https://raw.githubusercontent.com/firstcontributions/first-contributions/master//assets/fork.png" alt="fork this repository" />

## 准备

### 账号

首先，你需要准备一个 GitHub 账号。由于本项目特殊性，**您需要一个不包括您真实信息的账号**。

绑定境外邮箱比如谷歌，不要用国区苹果账号，腾讯，163，阿里的邮箱，也不要让境外邮箱转发到境内邮箱。

如果您已经申请有github账号，而且它不包括你真实个人信息，没有使用国内邮箱进行过绑定，同时知道你身份和github账号的人都可靠，直接使用就行。不过以后需要在github从事其他项目开发，要看具体情况，是否新建github账号

如果包括个人信息，请重新申请一个github账号专门提交这个项目有关的代码。

### git 环境

如果您想只通过网页修改，可以不准备这个。但是您需要确认网络环境稳定。现在中国大陆访问GitHub非常不稳定，为了确保更改不丢失，请最好使用某些稳定的工具。

如果您想先在本地修改，你的电脑上尚未安装 git, 请按照这个[ 安装指引 ](https://help.github.com/articles/set-up-git/)进行安装。

## Fork（复制）本代码仓库

点击仓库右上角的一个按钮去 Fork 这个代码仓库。
这个操作会将代码仓库复制一个到你的账户名下。

## 只通过网页修改

只通过网页修改，在你的账户名下 Fork 的仓库内随意修改，点击浏览某个文件，然后点击笔图标编辑就行。记得点击页面底部绿色commit按钮保存。也可以新建文件，记得添加文件名。不能新建空文件夹。

一次只能修改一个文件，但是您可以这样修改多个文件之后再进行下一步操作

## 提pr Pull Request

前往 Github 你的代码仓库，你会在仓库标题下看到一个 `pull requests` 的标签。点击该按钮。

接着再点击 `new pull request` 按钮，正式提交 pull request,写好说明。

不久之后，我便会把你所有的变化合并到这个项目的主分支。更改合并后，你会收到电子邮件通知。

# 贡献什么

###### 你喜欢写作吗？

- 编写并改进项目的文档
- 编写项目的教程

###### 你喜欢组织吗？

- 链接到重复的问题，并建议新的问题标签，以保持组织有序
- 通过开放性问题并建议关闭旧问题
- 询问有关最近开放的问题的澄清问题，以推进讨论

###### 你喜欢编码吗？

- 找一个待解决的公开问题
- 询问您是否可以帮助编写新功能
- 自动化项目设置
- 改进工具和测试

###### 你喜欢帮助别人吗？

- 回答有关项目的问题
- 回答有关未解决问题的人的问题
- 帮助调节讨论板或对话渠道

###### 你喜欢帮助别人代码吗？

- 查看其他人提交的代码
- 编写有关如何使用项目的教程
- 提供指导另一个贡献者，

## 本地修改操作：

## Clone（克隆）代码仓库

<img align="right" width="300" src="https://raw.githubusercontent.com/firstcontributions/first-contributions/master/assets/clone.png" alt="clone this repository" />

接下来，将复制后的代码仓库克隆到你的电脑上。点击图示中的绿色按钮，接着点击复制到剪切板按钮（将代码仓库地址复制下来）

随后打开命令行窗口，敲入如下 git 命令：

```
git clone "刚才复制的 url 链接"
```

"刚才复制的 url 链接"（去掉双引号）就是复制到你账户名下的代码仓库地址。获取这链接地址的方法请见上一步。

<img align="right" width="300" src="https://raw.githubusercontent.com/firstcontributions/first-contributions/master/assets/copy-to-clipboard.png" alt="copy URL to clipboard" />

譬如：

```
git clone https://github.com/你的Github用户名/first-contributions.git
```

'你的 Github 用户名' 指的就是你的 Github 用户名。这一步，你将复制到你账户名下的 first-contributions 这个代码仓库克隆到本地电脑上。

## 新建一个分支

下面的命令能在命令行窗口中，把目录切换到 first-contributions

```
cd first-contributions
```

接下来使用 `git checkout` 命令新建一个代码分支

```
git checkout -b <新分支的名称>
```

譬如：

```
git checkout -b add-myname
```

(新分支的名称不一定需要有* add *。然而，在新分支的名称加入* add *是一件合理的事情，因为这个分支的目的是将你的名字添加到列表中。)

## 对代码进行修改，而後 Commit (提交) 修改

打开 `Contributors.md` 这个文件，更新文件内容，将你的名字加上去，保存修改。`git status` 这命令会列出被改动的文件。接着 `git add` 这命令则可以添加你的改动，就像如下这条命令。

<img align="right" width="450" src="https://raw.githubusercontent.com/firstcontributions/first-contributions/master/assets/git-status.png" alt="git status" />

```
git add Contributors.md
```

现在就可以使用 `git commit` 命令 commit 你的修改了。

```
git commit -m "Add <你的名字> to Contributors list"
```

将 `<你的名字>` 替换为你的名字

## 将改动 Push（发布）到 GitHub

使用 `git push` 命令发布代码

```
git push origin <分支的名称>
```

将 `<分支的名称>` 替换为之前新建的分支名称。

## 提出 Pull Request 将你的修改供他人审阅

前往 Github 你的代码仓库，你会看到一个 `Compare & pull request` 的按钮。点击该按钮。

<img style="float: right;" src="https://raw.githubusercontent.com/firstcontributions/first-contributions/master/assets/compare-and-pull.png" alt="create a pull request" />

接着再点击 `Create pull request` 按钮，正式提交 pull request。

<img style="float: right;" src="https://raw.githubusercontent.com/firstcontributions/first-contributions/master/assets/submit-pull-request.png" alt="submit pull request" />

不久之后，我便会把你所有的变化合并到这个项目的主分支。更改合并后，你会收到电子邮件通知。

### [ 更多资料 ](../additional-material/git_workflow_scenarios/additional-material.md)





