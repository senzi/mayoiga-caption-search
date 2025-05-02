from flask import Flask, request, render_template, send_from_directory
from pathlib import Path
import json
import re



app = Flask(__name__)
ROOT_DIR = Path(__file__).resolve().parent
SCREENSHOT_ROOT = ROOT_DIR / "static" / "screenshots"
STATIC_ROOT = ROOT_DIR / "static" / "screenshots"

print("==== Flask App Starting ====")
print("Loading index.json files from:", SCREENSHOT_ROOT.resolve())

def load_indexes():
    result = []
    total = 0
    for index_file in SCREENSHOT_ROOT.glob("Mayoiga_S01E*/index.json"):
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)
            ep = index_file.parent.name
            count = len(index)
            print(f"[LOAD] {ep}: {count} entries from {index_file.name}")
            total += count
            for filename, meta in index.items():
                result.append({
                    "episode": ep,
                    "file": filename,
                    "text": meta["text"]
                })
    print(f"[INIT] Total captions loaded: {total}")
    return result


ALL_CAPTIONS = load_indexes()

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "").strip()
    matches = []
    print(f"\n[SEARCH] Query: '{q}'")

    if q:
        keywords = re.split(r"[,\s]+", q)
        print(f"[PARSE] Keywords: {keywords}")
        for item in ALL_CAPTIONS:
            text = item["text"]
            if all(k in text for k in keywords):
                matches.append(item)
                print(f"[MATCH] ✅ {item['episode']} - {item['file']} - {text}")
            else:
                print(f"[SKIP] ❌ {text}")
            if len(matches) >= 50:
                break
    else:
        print("[INFO] No query input.")

    print(f"[RESULT] {len(matches)} matched.")
    return render_template("index.html", query=q, results=matches)

@app.route("/screenshots/<ep>/<filename>")
def serve_image(ep, filename):
    resp = send_from_directory(STATIC_ROOT / ep, filename)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

if __name__ == "__main__":
    app.run(debug=True)
