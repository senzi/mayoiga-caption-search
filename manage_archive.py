import zipfile
import sys
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent
STATIC_SCREENSHOTS = BASE_DIR / "static" / "screenshots"
ZIP_PATH = BASE_DIR / "screenshots.zip"

def extract_zip():
    if not ZIP_PATH.exists():
        print(f"[ERROR] 未找到 {ZIP_PATH.name}")
        return
    if STATIC_SCREENSHOTS.exists():
        print(f"[INFO] 清理旧目录：{STATIC_SCREENSHOTS}")
        shutil.rmtree(STATIC_SCREENSHOTS)

    print(f"[INFO] 正在解压 {ZIP_PATH.name} → {STATIC_SCREENSHOTS}")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        zf.extractall(STATIC_SCREENSHOTS)
    print("[DONE] 解压完成")

def create_zip():
    if not STATIC_SCREENSHOTS.exists():
        print(f"[ERROR] 未找到目录 {STATIC_SCREENSHOTS}")
        return

    print(f"[INFO] 正在打包 {STATIC_SCREENSHOTS} → {ZIP_PATH.name}")
    with zipfile.ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for file in STATIC_SCREENSHOTS.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(BASE_DIR))
    print("[DONE] 打包完成")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        create_zip()
    else:
        extract_zip()
