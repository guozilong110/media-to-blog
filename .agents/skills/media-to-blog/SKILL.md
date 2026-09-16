---
name: media-to-blog
description: |
  Turn an audio or video source into a published HTML blog post. Use when the user
  gives a podcast, video, recording, URL, or an existing transcript and wants a
  summary, article, or notes from it, or wants the result published to their
  GitHub Pages archive. Covers transcription with transcribe.py, handling truncated
  or misrecognized transcripts, writing the HTML, and publishing to
  guozilong110/transcripts. Always composes with the diagram-design and humanizer
  skills when drafting the page.
license: MIT
metadata:
  version: "1.1.0"
---

# 音视频转博客

把一段音频、视频或已有转录，整理成一篇可发布的 HTML 文章，并推到 GitHub Pages 归档站。

四个阶段：转录 → 读稿 → 写页面 → 发布。用户只要求其中一部分时，只做那一部分。

## 必须配合的两个 skill

这个 skill 不单独完成阶段三。写页面时读取并执行另外两个：

| skill | 何时用 | 位置 |
|---|---|---|
| `diagram-design` | 起草章节时判断哪些内容该出图，然后生成图 | `.agents/skills/diagram-design/SKILL.md` |
| `humanizer` | 正文写完后逐段自查，改完再定稿 | `.agents/skills/humanizer/SKILL.md` |

两者都不是可选项。跳过 `diagram-design` 会得到一篇只有表格和段落的页面；跳过 `humanizer` 会留下一堆「不是 X 而是 Y」和一句话金句收尾。阶段三的检查清单里各有一条对应，两条都过不了不要进入发布。

它们和本 skill 的分工：本 skill 决定页面有哪些章节、哪些事实能写；`diagram-design` 决定其中哪几处变成图、图长什么样；`humanizer` 只管措辞，不碰事实和结构。

## 阶段一：转录

已有转录文本就跳过这一步。

```bash
source .venv/bin/activate
python transcribe.py <URL 或本地路径> --language Chinese
```

输出写到当前目录的 `transcript.txt` 并同时打印。要点：

- URL 直接传，脚本会自己下载；M4A/MP4/WebM 等格式需要 `ffmpeg`，缺了就 `brew install ffmpeg`。
- 视频文件先抽音轨再转，省时间：`ffmpeg -i video.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav`。
- 长音频耗时可能到几十分钟，用足够长的 timeout，不要中途打断重跑。
- 默认模型是 0.6B，可用 `--model` 或 `QWEN3_ASR_MODEL` 指向本地 1.7B-8bit 目录换更准的版本。

## 阶段二：读稿

完整读一遍再动笔。ASR 输出是连续口语流，没有段落和标点结构，需要先自己判断这三件事。

**内容是否完整。** 检查文件末尾是否停在半句话上。转录中断很常见（模型上下文、音频截断、下载不全）。若中断，只总结已有内容，并在页面里说明缺失部分，不要靠推测补写。

**哪些词是识别错误。** 同音错字和专业术语错误要按上下文纠正，并在交付时告诉用户改了什么。已知例子：「皮质醇」常被写成「皮脂醇」「皮质唇」「皮脂纯」。

**哪些说法本身不准确。** 说话人自己讲错的专业内容，用规范说法并明确告知用户。比如原话说皮质醇由「肾上腺皮质疏松带」合成，规范名称是束状带。不确定的不要擅自改。

同时记下：主播/讲者是谁、节目名、核心论点、内容的天然结构（这决定页面的章节划分）。

## 阶段三：写页面

### 内容原则

- **不加事实。** 数字、研究、机构名、结论都只能来自转录。转录没说的就不写。
- **保留讲者的第一人称经历。** 「我自己空腹有氧坚持了近一年」这类内容是文章的价值所在，用「主播」指代，不要抹成通用建议。
- **保留讲者明确的免责和纠正。** 例如「内分泌学会不承认肾上腺疲劳是正规诊断」「本期提到补剂但不是广告」。
- **口语转书面。** 删掉「话不多说」「掰开了揉碎了」「大家可以听听就行」这类填充语，但保留讲者的判断和态度。

### 结构选择

按内容自身逻辑分章，不要套模板。常见几种：

- 知识科普 → 是什么 / 正常状态 / 影响因素 / 异常表现 / 怎么办
- 访谈对话 → 按话题分段，保留双方观点差异
- 教程 → 按步骤

用对形式：并列的类型或人群用表格，正反对照用双列卡片，有先后轻重的建议用分级块，其余用正文段落。不要因为「看起来丰富」而堆组件。

### 配图（走 diagram-design）

分好章节后，先判断哪些内容出图比留文字强，再读 `.agents/skills/diagram-design/SKILL.md` 生成。判断标准就是那个 skill 的 §2：读者从图里学到的比从段落或表格里更多才出图，单纯的清单、简单前后对比、一个方框的「图」都不出。

转录内容常见的对应关系：

| 转录里的内容 | 图表类型 |
|---|---|
| 多步骤通路、含反馈环的机制 | 架构图；有回写就用 loop |
| 一天/一年之内的数值起伏 | 折线图 |
| 按两个维度划分的人群或类型 | 象限图，或带表头的对比矩阵 |
| 有优先级的建议 | 金字塔 |
| 判断分支、走向不同结论 | 流程图 |
| 时间顺序的事件 | 时间线 |
| 多方对话、各自负责的环节 | 泳道图 |

三条硬约束：

- **图里的数字只能来自转录。** 讲者没给具体数值就画趋势和相对关系，不要编刻度。这条比 diagram-design 自己的美学规则优先。
- **嵌入文章的图删掉 Google Fonts 的 `<link>`。** 文章要求自包含不引外部资源，字体退到本地栈（见 style-guide 的「Blog embedding」）。单独作为文件存在的图可以保留 link。
- **图的 SVG 直接内联进文章的 `<section>`**，不要用 `<iframe>` 或 `<img>` 引外部文件。

配色已经对齐博客站点（`accent` 是站点的墨绿 `#0b6b5f`，`paper` 是 `#fafafa`），首次运行的品牌门禁不用走，diagram-design 若提出把当前 skin 存成 profile 也直接谢绝——profile 存在 `~/.diagram-design/`，属于全局配置，本项目刻意只在项目内安装。改了站点 CSS 就同步改 `diagram-design/references/style-guide.md` 的 token 表。

### 语言

图内标签用简体中文，跟正文一致。Han 字符要守 diagram-design 的三条规则：12px 下限、eyebrow 和箭头标签这类 7–8px 等宽槽位换成 12px 无衬线（不加字间距、不转大写）、端口和单位这类拉丁 sublabel 留在 Geist Mono 不翻译。宽度按每个全角字符 1em 估，全角标点 `（）「」，。：` 同样算 1em。

### HTML 模板

用 `templates/post.html` 起页面，它带完整的样式类：

```bash
cp .agents/skills/media-to-blog/templates/post.html \
   /Users/zilong/git/transcripts/posts/$(date +%Y-%m-%d)-<slug>.html
```

可用类：`.lead` 开篇结论块，`.cols` + `.card.good` / `.card.bad` 正反对照，`.note` 提示框，`.tier` + `<span>` 分级建议，`table` 表格，`footer` 来源与免责说明。

固定要求：`lang="zh-CN"`、`<meta charset="UTF-8">`、viewport 声明、单一 `<h1>`、章节用 `<h2>`。样式内联在 `<style>` 里，页面自包含，不引外部资源。

页脚必须写清三件事：内容是转录整理、转录若有中断则说明缺了什么、非医疗/法律/投资建议（涉及这些领域时）。

### 定稿前的检查

按顺序过，全过了才进入阶段四：

1. **事实核对。** 页面里每个数字、机构名、研究结论都能在转录里找到出处。图里的数字同样核。
2. **`humanizer` 自查。** 读 `.agents/skills/humanizer/SKILL.md`，按它的流程走一遍正文。它的 §1–5 见一次就要改；标 *weak alone* 的看有没有同伴。特别留它点出的五个最容易残留的：「不是 X 而是 Y」、一句话金句收尾、破折号、三连排比、加粗小标签。改措辞不要顺手改掉事实。
3. **HTML 校验。** 标签闭合平衡，`lang="zh-CN"`，单一 `<h1>`，无外部资源引用。
4. **图的检查。** 每张图跑一遍 diagram-design 的 taste gate；`accent` 每张图最多 1–2 个焦点。可用 `.agents/skills/diagram-design/scripts/self_check.py` 跑自动检查。

第 2 步和第 4 步是最容易被跳过的两步。它们跳过与否从产出上能直接看出来，不要报告说做了而实际没做。

## 阶段四：发布

归档仓库是 `guozilong110/transcripts`，本地在 `/Users/zilong/git/transcripts`，已开启 Pages，推到 `main` 自动发布。

```bash
cd /Users/zilong/git/transcripts
git pull

# 1. 文章放进 posts/，命名 YYYY-MM-DD-slug.html，slug 用小写英文短横线
# 2. 在 index.html 的 <ul class="posts"> 顶部加一个条目：
#    <li><a href="posts/FILE.html">标题</a>
#      <span class="date">YYYY-MM-DD · 来源</span>
#      <p class="desc">一两句摘要</p></li>

git add posts/<新文件> index.html
git commit -m "<中文说明>"
git push
```

提交前确认：文件名日期用 `date +%Y-%m-%d` 的真实结果，不要凭印象写；`index.html` 里的链接和实际文件名一致。

推送后验证两个页面都返回 200：

```bash
sleep 45
curl -s -o /dev/null -w "%{http_code}\n" https://guozilong110.github.io/transcripts/
curl -s -o /dev/null -w "%{http_code}\n" https://guozilong110.github.io/transcripts/posts/<文件名>
```

首次发布约需 1 分钟，之后更新更快。若返回 404，等 30 秒重试；持续 404 就查 `gh api repos/guozilong110/transcripts/pages/builds/latest`。

仓库是 public，Pages 免费版的要求。用户给的内容涉及隐私或不宜公开时，先问，不要直接推。

## 交付说明

告诉用户：线上链接、本地文件路径、以及你做的判断——纠正了哪些识别错误、改了哪些不准确的说法、转录是否中断以及缺了什么、为哪些内容配了什么图。这些是用户无法自己看出来的部分。
