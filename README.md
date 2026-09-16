# 音视频转博客

把一段音频、视频或已有转录，整理成一篇可发布的 HTML 文章，并推到 GitHub Pages 归档站。你不需要自己跑任何命令，只要和 agent 对话就行。

## 怎么用

在 Kiro / pi 这类支持 skill 的 agent 里，调用 skill 再用一句话说需求：

```
/skill:media-to-blog
```

然后说你想做什么，例如：

- `/skill:media-to-blog 把 https://example.com/podcast.m4a 转录并整理成博客发布`
- `/skill:media-to-blog 这段视频 ./talk.mp4 帮我做成文章`
- `/skill:media-to-blog 用现有的 transcript.txt 写一篇总结，先别发布`

agent 会自己完成转录、读稿、写页面、发布这几步。转录用的是本地 Qwen3-ASR 模型（下面「实现说明」有细节），但你不用关心它怎么跑。

skill 分四个阶段：转录 → 读稿 → 写页面 → 发布。只要求其中一部分时（比如只转录、或只写不发），agent 就只做那一部分。写页面时会自动配合 `diagram-design`（判断哪些内容出图并生成配图）和 `humanizer`（正文去除 AI 腔）两个 skill。

发布后 agent 会告诉你线上链接、本地文件路径，以及它做的判断——纠正了哪些识别错误、改了哪些不准确的说法、转录是否中断、为哪些内容配了什么图。

skill 的完整说明见 `.agents/skills/media-to-blog/SKILL.md`。

## 实现说明（供参考，日常不需要）

转录由 `transcribe.py` 完成，在 Apple Silicon（M1/M2/M3/M4/M5）上用 PyTorch MPS 运行 Qwen3-ASR。首次运行会从 Hugging Face 下载模型并缓存到本机；也可以把 `--model` 指向已经下载好的 8bit 模型目录。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt

# URL
python transcribe.py 'https://media.xyzcdn.net/63524ea82a992d56e91e63f7/lgiUxlR1Fsg-3G-XZgpYDH-D_zbd.m4a'

# 本地音频
python transcribe.py ./audio.m4a --model /path/to/Qwen3-ASR-1.7B-8bit
```

也可以设置 `QWEN3_ASR_MODEL`，省略 `--model`。如果 MPS 上遇到算子兼容问题，可加 `--device cpu`。输出为纯文本，每个音频一行。
