"""Experiment E04: modernized ingest — markup fields (markdown vs legacy).
Official notice (verified on live docs 2026-10-05): as of 2025-08-26, markup fields
in legacy 'chintzy' HTML subset no longer byte-identical to classic pipeline.
Verified live on NCT04852770 DetailedDescription:
  markdown: plain paragraphs, no CR/LF wrapping
  legacy:   same text with \\r\\n hard wraps (~80 cols), classic PRS compatible
This experiment asserts the two formats differ but normalize equal.
"""
import json, os
from src.ctg_client import get_json

NCT = "NCT04852770"

def main():
    md = get_json(f"/studies/{NCT}", {"format": "json", "markupFormat": "markdown", "fields": "DetailedDescription"})
    lg = get_json(f"/studies/{NCT}", {"format": "json", "markupFormat": "legacy", "fields": "DetailedDescription"})
    t_md = md["protocolSection"]["descriptionModule"]["detailedDescription"]
    t_lg = lg["protocolSection"]["descriptionModule"]["detailedDescription"]
    norm = lambda s: " ".join(s.replace("\\r", " ").replace("\\n", " ").split())
    print("markdown len:", len(t_md), "legacy len:", len(t_lg))
    print("raw equal:", t_md == t_lg, "normalized equal:", norm(t_md) == norm(t_lg))
    os.makedirs("results", exist_ok=True)
    with open("results/e04_markup.json", "w") as f:
        json.dump({"nct": NCT, "markdown_len": len(t_md), "legacy_len": len(t_lg),
                   "raw_equal": t_md == t_lg, "normalized_equal": norm(t_md) == norm(t_lg),
                   "markdown_head": t_md[:300], "legacy_head": t_lg[:300]}, f, indent=2)
    assert t_md != t_lg, "formats unexpectedly identical — ingest may have changed"
    assert norm(t_md) == norm(t_lg), "semantic drift between formats!"
    print("E04 PASS: markdown vs legacy differ in whitespace only, as documented")

if __name__ == "__main__":
    main()
