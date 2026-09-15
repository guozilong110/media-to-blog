# Qwen3-ASR 0.6B MLX 本地转写

在 Apple Silicon（M1/M2/M3/M4/M5）上使用 PyTorch MPS 运行 Qwen3-ASR。首次运行会从 Hugging Face 下载模型并缓存到本机；也可以把 `--model` 指向已经下载好的 8bit 模型目录。

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
