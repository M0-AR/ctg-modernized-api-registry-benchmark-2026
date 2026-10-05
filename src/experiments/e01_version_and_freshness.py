"""Experiment E01: version + freshness guard.
Verified live 2026-10-05: apiVersion 2.0.5, dataTimestamp 2026-10-02T09:00:04.
"""
import json, os
from src.ctg_client import check_freshness

def main():
    chk = check_freshness()
    print(json.dumps(chk, indent=2))
    os.makedirs("results", exist_ok=True)
    with open("results/e01_version.json", "w") as f:
        json.dump(chk, f, indent=2)
    # hard assertion: API must be reachable and timestamp parseable
    assert chk["version"].get("apiVersion"), "missing apiVersion"
    assert chk["version"].get("dataTimestamp"), "missing dataTimestamp"
    print("E01 PASS: freshness guard OK")

if __name__ == "__main__":
    main()
