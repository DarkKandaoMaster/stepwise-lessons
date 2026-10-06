# stepwise-lessons 技能：用户须知

这份文档写给使用者本人看。技能本身的说明见 `stepwise-lessons/SKILL.md`。

## 它做什么

stepwise-lessons 会把一个知识点、一篇论文或一段讲座视频，拆成一套循序渐进的课程，给初学者看。整个过程是：

1. 先写课程大纲，等你确认。
2. 然后一课写一个 Markdown 文件。
3. 每写完一课就停下来，等你看完、给反馈，再写下一课。

## 怎么叫它

只需要提供每次都不一样的那几项：

> 用 stepwise-lessons 讲解 xx。目标是 ___（例如看懂某篇论文 / 某段视频），我懂 ___，不懂 ___。课程放在 ___。

也可以直接输入 `/stepwise-lessons`，再补充上面这些信息。存放目录如果不写，默认放在学习材料旁边的 `lessons/` 文件夹里。

## 它会怎么写

- 每课只讲一件事，最多引入 2 个新概念，并且只用一个贯穿全课的比喻。
- 讲解顺序：先说为什么需要这个概念，再给比喻和配图，然后用手算的小数字例子演示，最后才给出公式，并把公式里的每个符号对应回例子。
- 文中的数字都经过 Python 验算。
- 插图用 matplotlib 画，放在 `img/` 文件夹里。二元函数一律画成 3D 立体图。
- 所有插图都由课程目录里的 `make_figures.py` 生成。想改图，告诉它改哪里就行。

## 怎么看

用 VS Code 的 Markdown Preview Enhanced 打开 `.md` 文件，就能看到渲染后的公式和插图。如果想要 HTML 文件，可以在预览里导出。

## 怎么反馈最有用

- 直接指出哪一段、哪张图没看懂。它会换一个比喻或换一个角度重写，不会把原话换个说法再说一遍。
- 对讲法的偏好（比如"以后都画 3D 图"）说一次就行，后面的课会一直照做。

## 安装

技能本体在 `D:\Release\DarkKandaoMaster-Skills\stepwise-lessons\stepwise-lessons\`。`C:\Users\Kandao\.claude\skills\stepwise-lessons` 是指向它的目录联接，所以修改本体后立即生效。

要换到另一台机器上用，把 `stepwise-lessons\stepwise-lessons` 整个文件夹复制到那台机器的 `~/.claude/skills/stepwise-lessons` 即可。
