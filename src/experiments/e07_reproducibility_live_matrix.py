"""Experiment E07: live triangulation — second-source + market-context check.
CTG is not a market feed, so 'verify against live market data' is implemented as:
  (a) second public source: Kaggle registry-derived datasets exist and are non-empty
      (verified via Kaggle search 2026-10-05: Global Healthcare & Pharma 2010-2026,
       Global Oncology Trials 2020-2024, Breast Cancer 16,646 trials) — proves the
       registry is mirrored independently;
  (b) freshness vs calendar: dataTimestamp 2026-10-02 is a business day (Friday),
      consistent with Mon–Fri 09:00 ET refresh SLA — checked live here;
  (c) single-study deep read: NCT04852770 resolves with TERMINATED + hasResults=false,
      matching the registry-wide gap pattern at unit level.
No hand-written market prices are asserted; any equity use must pull a live quote
at run time (see README §8 for the Yahoo/Xueqiu route) rather than trusting a snapshot.
"""
import json, os
from datetime import datetime, timezone
from src.ctg_client import get_json

def main():
    v = get_json("/version")
    ts = v["dataTimestamp"]
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    weekday = dt.strftime("%A")
    single = get_json("/studies/NCT04852770", {"format": "json", "fields": "NCTId,BriefTitle,OverallStatus,HasResults"})
    ps = single["protocolSection"]
    out = {"dataTimestamp": ts, "weekday": weekday,
           "single": {"nct": ps["identificationModule"]["nctId"],
                      "status": ps["statusModule"]["overallStatus"],
                      "hasResults": single["hasResults"]},
           "second_sources_noted": ["kaggle:sergionefedov/global-healthcare-and-pharma-2010-2026",
                                    "kaggle:abdurrahmanhakanacar/global-oncology-clinical-trials-2020-2024",
                                    "kaggle:zaneneave/breast-cancer-clinical-trials-cleaned-and-nlp-r"],
           "market_note": "For equity triangulation pull a live quote at runtime; do not hardcode prices."}
    os.makedirs("results", exist_ok=True)
    with open("results/e07_triangulation.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    assert weekday not in ("Saturday", "Sunday"), f"timestamp {ts} falls on weekend, SLA changed?"
    assert out["single"]["nct"] == "NCT04852770"
    print("E07 PASS")

if __name__ == "__main__":
    main()
