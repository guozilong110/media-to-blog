#!/usr/bin/env python3
"""Local MLX Qwen3-ASR transcription on Apple Silicon.

Examples:
  python transcribe.py https://example.com/audio.m4a
  python transcribe.py ./audio.wav --model /path/to/Qwen3-ASR-1.7B-8bit
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def audio_for_qwen(audio: str):
    """Convert formats unsupported by soundfile (notably M4A/AAC) to WAV."""
    suffix = Path(audio.split("?", 1)[0]).suffix.lower()
    if suffix not in {".m4a", ".mp4", ".aac", ".webm", ".opus"}:
        yield audio
        return

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            f"音频格式 {suffix} 需要 ffmpeg 转换，但未找到 ffmpeg。"
            "请安装：brew install ffmpeg"
        )
    with tempfile.TemporaryDirectory(prefix="qwen-asr-") as tmp:
        wav = os.path.join(tmp, "audio.wav")
        cmd = [ffmpeg, "-nostdin", "-loglevel", "error", "-i", audio,
               "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"ffmpeg 无法解码音频：{audio}") from exc
        yield wav


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe audio with MLX Qwen3-ASR.")
    parser.add_argument("audio", help="Local audio path or http(s) URL")
    parser.add_argument(
        "--model", default=os.environ.get("QWEN3_ASR_MODEL", "mlx-community/Qwen3-ASR-0.6B-6bit"),
        help="MLX model ID or local directory",
    )
    parser.add_argument("--language", default=None, help="Optional language, e.g. Chinese or English")
    parser.add_argument(
        "--max-tokens", type=int, default=200_000,
        help=("生成 token 总预算，所有音频分块共享。"
              "上游默认仅 8192，长音频会被中途截断，故这里显式放大。"),
    )
    parser.add_argument("--output", default="transcript.txt", help="输出文件路径（默认 transcript.txt）")
    parser.add_argument("--device", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        import mlx_audio  # noqa: F401
    except ImportError as exc:
        print("缺少依赖，请先执行: python -m pip install -r requirements.txt", file=sys.stderr)
        print(f"详细信息: {exc}", file=sys.stderr)
        return 2

    try:
        with audio_for_qwen(args.audio) as normalized_audio:
            output_path = Path(args.output).expanduser().resolve()
            # mlx_audio 的 save_as_* 会自行追加 .{format}，所以传入不带扩展名的 stem
            stem = output_path.with_suffix("") if output_path.suffix == ".txt" else output_path
            written = Path(f"{stem}.txt")
            cmd = [sys.executable, "-m", "mlx_audio.stt.generate", "--model", args.model,
                   "--audio", normalized_audio, "--output-path", str(stem), "--format", "txt",
                   "--max-tokens", str(args.max_tokens)]
            if args.language:
                cmd += ["--language", args.language]
            subprocess.run(cmd, check=True)
            if written.exists():
                print(written.read_text(encoding="utf-8"), end="")
                print(f"\n已保存到: {written}", file=sys.stderr)
            else:
                raise RuntimeError(f"模型未生成输出文件: {written}")
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
