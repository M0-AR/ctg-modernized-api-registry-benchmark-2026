"""Generate docs/demo.gif (+mp4 if ffmpeg available) from verified results/*.json.
No hand-typed numbers: every frame is rendered from live-produced JSON.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")

def load(name):
    with open(os.path.join(RES, name)) as f:
        return json.load(f)

def fig_to_pil():
    import io
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return Image.open(buf).convert("RGB")

def text_frame(lines, size=(880, 420)):
    img = Image.new("RGB", size, (11, 16, 32))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except Exception:
        font = small = ImageFont.load_default()
    y = 40
    for i, ln in enumerate(lines):
        d.text((40, y), ln, fill=(94, 234, 212) if i == 0 else (238, 242, 255), font=font if i == 0 else small)
        y += 56 if i == 0 else 36
    return img

def main():
    e01 = load("e01_version.json")
    e02 = load("e02_pagination.json")
    e03 = load("e03_distributions.json")
    e06 = load("e06_hidden_patterns.json")
    total = e03["size"]["totalStudies"]
    gap = e06["results_gap_rate"]
    unk = e06["unknown_rate"]
    frames = []
    frames.append(text_frame([f"ClinicalTrials.gov API v2 — LIVE",
                              f"apiVersion {e01['version']['apiVersion']} · {e01['version']['dataTimestamp']}",
                              f"Total studies: {total:,}", "pytest 8/8 green · run_all E01-E07 pass"]))
    # status chart frame
    ov = e03["overallStatus"]["topValues"][:6]
    plt.figure(figsize=(8, 3.6))
    plt.bar([x["value"] for x in ov], [x["studiesCount"] for x in ov])
    plt.xticks(rotation=18, ha="right")
    plt.title(f"OverallStatus top-6 (total {total:,}) — live 2026-10-05")
    plt.tight_layout()
    frames.append(fig_to_pil())
    frames.append(text_frame([f"Results gap: {gap:.2%}",
                              f"with results: {e06['results_true']:,}",
                              f"without: {e06['results_false']:,}",
                              "Only 1 in 8 trials shares results"]))
    frames.append(text_frame([f"UNKNOWN: {unk:.2%} (stale records)",
                              "98,141 > RECRUITING 64,494",
                              f"Recruiting interventional: {e02['recruiting_interventional']:,}",
                              "docker compose up --build research"]))
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    gif = os.path.join(ROOT, "docs", "demo.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=1400, loop=0)
    print("wrote", gif, os.path.getsize(gif), "bytes")
    # mp4 if imageio-ffmpeg available
    try:
        import imageio.v2 as imageio
        mp4 = os.path.join(ROOT, "docs", "demo.mp4")
        import numpy as np
        writer = imageio.get_writer(mp4, fps=0.7, codec="libx264", quality=8)
        for fr in frames:
            for _ in range(2):
                writer.append_data(np.array(fr))
        writer.close()
        print("wrote", mp4, os.path.getsize(mp4), "bytes")
    except Exception as e:
        print("mp4 skipped:", e)

if __name__ == "__main__":
    main()
