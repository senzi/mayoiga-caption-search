import re
from pathlib import Path
import shutil

ROOT_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = ROOT_DIR / "mayoiga"
SUB_DIR = ROOT_DIR / "subtitles"

episode_re = re.compile(r"S01E(\d{2})")

def rename_files(folder: Path, ext: str):
    for file in sorted(folder.glob(f"*.{ext}")):
        match = episode_re.search(file.name)
        if not match:
            print(f"[SKIP] No episode info found in {file.name}")
            continue
        ep_num = match.group(1)
        new_name = f"Mayoiga_S01E{ep_num}.{ext}"
        target = folder / new_name
        shutil.move(str(file), str(target))
        print(f"{file.name} → {new_name}")

def main():
    print("Renaming video files...")
    rename_files(VIDEO_DIR, "mkv")

    print("Renaming subtitle files...")
    rename_files(SUB_DIR, "srt")

if __name__ == "__main__":
    main()
