import os
import subprocess
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent

# 原始视频所在目录
VIDEO_DIR = ROOT_DIR / "mayoiga"
# 输出字幕目录
OUTPUT_DIR = ROOT_DIR / "subtitles"
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_subtitle(mkv_path: Path, stream_index: int = 0):
    """
    提取指定字幕轨道（默认为0，即简体中文）为srt文件
    """
    episode_name = mkv_path.stem
    output_path = OUTPUT_DIR / f"{episode_name}.srt"

    cmd = [
        "ffmpeg",
        "-i", str(mkv_path),
        "-map", f"0:s:{stream_index}",
        "-c:s", "copy",
        str(output_path)
    ]

    try:
        print(f"Extracting subtitle from: {mkv_path.name}")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"→ Saved to {output_path.name}")
    except subprocess.CalledProcessError:
        print(f"[WARN] Failed to extract subtitles from {mkv_path.name}")

def main():
    if not VIDEO_DIR.exists():
        print(f"[ERROR] VIDEO_DIR not found: {VIDEO_DIR}")
        return

    for file in sorted(VIDEO_DIR.glob("*.mkv")):
        extract_subtitle(file)

if __name__ == "__main__":
    main()
