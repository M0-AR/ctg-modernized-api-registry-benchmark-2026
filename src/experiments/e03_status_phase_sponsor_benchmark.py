"""Experiment E03: status / phase / sponsor benchmark (stats endpoints).
All values below were read LIVE on 2026-10-05 and asserted as regression floor.
  totalStudies=605599, avgSize=17301 bytes
  OverallStatus: COMPLETED 330931, UNKNOWN 98141, RECRUITING 64494, TERMINATED 34429, ...
  Phase: NA 238061, PHASE2 90442, PHASE1 65890, PHASE3 49967, PHASE4 35897, EARLY_PHASE1 6494, missing 143573
  LeadSponsorClass: OTHER 433502, INDUSTRY 132769, OTHER_GOV 16138, NIH 11577, NETWORK 5036, FED 4941
  StudyType: INTERVENTIONAL 462154, OBSERVATIONAL 141397, EXPANDED_ACCESS 1068
  HasResults: false 525238 (86.73%), true 80361 (13.27%)
"""
import json, os
from src.ctg_client import get_json

def main():
    size = get_json("/stats/size")
    ov = get_json("/stats/field/values", {"fields": "OverallStatus"})[0]
    ph = get_json("/stats/field/values", {"fields": "Phase"})[0]
    sp = get_json("/stats/field/values", {"fields": "LeadSponsorClass"})[0]
    ty = get_json("/stats/field/values", {"fields": "StudyType"})[0]
    hr = get_json("/stats/field/values", {"fields": "HasResults"})[0]

    out = {"size": {"totalStudies": size.get("totalStudies"), "averageSizeBytes": size.get("averageSizeBytes"),
                    "ranges_head": size.get("ranges", [])[:5]},
           "overallStatus": ov, "phase": ph, "sponsor": sp, "studyType": ty, "hasResults": hr}
    os.makedirs("results", exist_ok=True)
    with open("results/e03_distributions.json", "w") as f:
        json.dump(out, f, indent=2)

    # regression guards (lower bounds, not exact — registry only grows)
    assert size["totalStudies"] >= 600_000, size
    top_ov = {x["value"]: x["studiesCount"] for x in ov["topValues"]}
    assert top_ov["COMPLETED"] >= 325_000 and top_ov["UNKNOWN"] >= 90_000, top_ov
    assert top_ov["RECRUITING"] >= 60_000, top_ov
    false_c, true_c = hr["falseCount"], hr["trueCount"]
    assert false_c / (false_c + true_c) > 0.80, "results gap closed unexpectedly — re-examine!"
    print(f"E03 PASS: total={size['totalStudies']} results_gap={false_c/(false_c+true_c):.3f}")
    print(json.dumps({"total": size["totalStudies"], "completed": top_ov["COMPLETED"],
                       "unknown": top_ov["UNKNOWN"], "hasResults_true": true_c}, indent=2))

if __name__ == "__main__":
    main()
