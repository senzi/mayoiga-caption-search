import re
import json
import subprocess
from pathlib import Path
from datetime import timedelta
from typing import List
from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = ROOT_DIR / "compressed_videos"
SUB_DIR = ROOT_DIR / "subtitles"
OUT_DIR = ROOT_DIR / "screenshots"

def parse_srt(srt_path: Path) -> List[dict]:
    """解析 .srt 字幕文件"""
    entries = []
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r"\n\s*\n", content.strip())
    for idx, block in enumerate(blocks, 1):
        lines = block.strip().splitlines()
        if len(lines) >= 3:
            timestamp = lines[1]
            text = " ".join(lines[2:]).strip().replace("\n", " ")
            start = timestamp.split(" --> ")[0].replace(",", ".")
            entries.append({
                "index": idx,
                "start": start,
                "text": text
            })
    return entries

def timestamp_plus_one(ts: str) -> str:
    """给时间戳加1秒"""
    h, m, s = ts.split(":")
    sec, ms = s.split(".")
    t = timedelta(hours=int(h), minutes=int(m), seconds=int(sec), milliseconds=int(ms))
    t += timedelta(seconds=1)
    return str(t)[:-3]  # 截掉微秒部分，保留到两位小数

def sanitize_filename(text: str, max_len=30) -> str:
    """移除非法字符，限制长度"""
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    return text[:max_len].strip().replace(" ", "_")

def extract_frame(video_path: Path, timestamp: str, out_path: Path):
    cmd = [
        "ffmpeg",
        "-ss", timestamp,
        "-i", str(video_path),
        "-frames:v", "1",
        "-q:v", "2",  # JPEG质量（1最好）
        str(out_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_episode(episode_name: str):
    video_file = VIDEO_DIR / f"{episode_name}.720p.burned.mp4"
    srt_file = SUB_DIR / f"{episode_name}.srt"
    out_folder = OUT_DIR / episode_name
    out_folder.mkdir(parents=True, exist_ok=True)

    entries = parse_srt(srt_file)
    index_data = {}

    for entry in tqdm(entries, desc=episode_name):
        ts = timestamp_plus_one(entry["start"])
        filename = f"{entry['index']:04d}_{sanitize_filename(entry['text'])}.jpg"
        out_path = out_folder / filename
        extract_frame(video_file, ts, out_path)
        index_data[filename] = {
            "time": ts,
            "text": entry["text"]
        }

    with open(out_folder / "index.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {episode_name}: {len(entries)} screenshots saved.")

def main():
    for video_file in sorted(VIDEO_DIR.glob("Mayoiga_S01E*.mp4")):
        ep_name = video_file.stem.replace(".720p.burned", "")
        process_episode(ep_name)

if __name__ == "__main__":
    main()
