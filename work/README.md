# work/ — 转录产物归档

每一期转录放一个子目录，目录名用小写英文短横线（内容主题，非文件名）。

约定的文件名：

| 文件 | 说明 |
|---|---|
| `transcript.txt` | 转录文字稿（`transcribe.py` 输出） |
| `audio.wav` / `audio.m4a` | 音频源（媒体文件不入库，见 `.gitignore`） |
| `video.mp4` | 视频源（不入库） |
| `*.html` | 整理成文的博客/摘要页（可选） |

媒体文件（wav/mp4/m4a 等）被 `.gitignore` 挡住，只有文本产物进版本库。
如需重新拿到媒体，用 `yt-dlp` 按原始 URL 重下即可。

## 现有归档

- `cortisol/` — 万物生长FM 皮质醇那期
- `bilibili-early-retirement/` — B站「提前退休可行性计划」（哥白）
