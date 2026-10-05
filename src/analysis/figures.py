"""Make benchmark figures from live results (matplotlib, no seaborn)."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load(p):
    with open(p) as f:
        return json.load(f)

def main():
    os.makedirs("results", exist_ok=True)
    d = load("results/e03_distributions.json")
    ov = d["overallStatus"]["topValues"][:8]
    labels = [x["value"] for x in ov]
    vals = [x["studiesCount"] for x in ov]
    plt.figure(figsize=(10, 5))
    plt.bar(labels, vals)
    plt.xticks(rotation=25, ha="right")
    plt.title(f"OverallStatus top-8 (total={d['size']['totalStudies']:,}, live 2026-10-05)")
    plt.tight_layout()
    plt.savefig("results/fig_status_top8.png", dpi=150)
    print("wrote results/fig_status_top8.png")

if __name__ == "__main__":
    main()
