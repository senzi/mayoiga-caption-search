from pathlib import Path
import re

SUBTITLE_DIR = Path(__file__).resolve().parent.parent / "subtitles"

def count_srt_entries(srt_path: Path) -> int:
    """统计.srt文件中的字幕条目数"""
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = re.findall(r"\d+\s*\n\d{2}:\d{2}:\d{2},\d{3}", content)
    return len(entries)

def estimate_storage(num_images: int, avg_size_kb: int) -> float:
    """估算图像存储大小（MB）"""
    return round(num_images * avg_size_kb / 1024, 2)

def main():
    AVG_PNG_KB = 400
    AVG_JPG_KB = 100

    total_images = 0
    print(f"{'Episode':<15} {'Images':<10} {'PNG(MB)':<10} {'JPG(MB)'}")
    print("-" * 45)
    for srt in sorted(SUBTITLE_DIR.glob("*.srt")):
        count = count_srt_entries(srt)
        total_images += count
        png_mb = estimate_storage(count, AVG_PNG_KB)
        jpg_mb = estimate_storage(count, AVG_JPG_KB)
        print(f"{srt.stem:<15} {count:<10} {png_mb:<10} {jpg_mb}")

    print("-" * 45)
    print(f"{'TOTAL':<15} {total_images:<10} {estimate_storage(total_images, AVG_PNG_KB):<10} {estimate_storage(total_images, AVG_JPG_KB)}")

if __name__ == "__main__":
    main()
