import subprocess
from pathlib import Path
import shutil
import tempfile

ROOT_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = ROOT_DIR / "mayoiga"
SUBTITLE_DIR = ROOT_DIR / "subtitles"
OUTPUT_DIR = ROOT_DIR / "compressed_videos"
OUTPUT_DIR.mkdir(exist_ok=True)

def burn_and_compress(video_path: Path, subtitle_path: Path, output_path: Path):
    # 使用临时目录解决路径字符兼容问题
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        tmp_video = tmpdir_path / "temp.mkv"
        tmp_srt = tmpdir_path / "temp.srt"

        shutil.copy(video_path, tmp_video)
        shutil.copy(subtitle_path, tmp_srt)

        cmd = [
            "ffmpeg",
            "-i", str(tmp_video),
            "-vf", "subtitles=temp.srt:force_style='FontName=Noto Sans,FontSize=36'",
            "-s", "1280x720",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "28",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            str(output_path)
        ]

        try:
            print(f"Burning subtitles into: {video_path.name}")
            subprocess.run(cmd, check=True, cwd=tmpdir)
            print(f"→ Output saved to {output_path.name}")
        except subprocess.CalledProcessError:
            print(f"[WARN] Failed: {video_path.name}")

def main():
    for video_file in sorted(VIDEO_DIR.glob("*.mkv")):
        srt_file = SUBTITLE_DIR / f"{video_file.stem}.srt"
        if not srt_file.exists():
            print(f"[SKIP] No subtitle found for {video_file.name}")
            continue
        output_file = OUTPUT_DIR / f"{video_file.stem}.720p.burned.mp4"
        burn_and_compress(video_file, srt_file, output_file)

if __name__ == "__main__":
    main()
