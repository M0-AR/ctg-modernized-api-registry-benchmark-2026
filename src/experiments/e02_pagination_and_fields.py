"""Experiment E02: pagination contract + field selection + pageSize clamp.
Verified live 2026-10-05:
  - countTotal=605599 (matches /stats/size totalStudies=605599)
  - pageSize=1001 -> 1000 rows, 200 OK (silent clamp, no error)
  - termination = missing nextPageToken; empty query -> {"studies":[]} 200 OK
"""
import json, os
from src.ctg_client import get_json, paginate

def main():
    first = get_json("/studies", {"format": "json", "pageSize": "1", "countTotal": "true", "fields": "NCTId"})
    total = first.get("totalCount")
    print("totalCount:", total, "hasToken:", "nextPageToken" in first)

    clamped = get_json("/studies", {"format": "json", "pageSize": "1001", "fields": "NCTId"})
    print("clamp 1001 ->", len(clamped.get("studies", [])))
    assert len(clamped.get("studies", [])) == 1000, "clamp behavior changed!"

    # narrow query pagination: recruiting interventional, verified totalCount=47118 on 2026-10-05
    narrow = get_json("/studies", {
        "format": "json", "pageSize": "5", "fields": "NCTId",
        "filter.overallStatus": "RECRUITING",
        "query.term": "AREA[StudyType]INTERVENTIONAL",
        "countTotal": "true",
    })
    print("recruiting_interventional totalCount:", narrow.get("totalCount"))

    rows = paginate({"format": "json", "fields": "NCTId,BriefTitle,OverallStatus",
                     "filter.overallStatus": "RECRUITING",
                     "query.term": "AREA[StudyType]INTERVENTIONAL"}, max_pages=2, page_size=10)
    print("paginated rows:", len(rows))

    os.makedirs("results", exist_ok=True)
    with open("results/e02_pagination.json", "w") as f:
        json.dump({"totalCount": total, "clamp1001": len(clamped.get("studies", [])),
                   "recruiting_interventional": narrow.get("totalCount"),
                   "paginated_sample": len(rows)}, f, indent=2)
    assert total and total > 600_000, f"registry unexpectedly small: {total}"
    print("E02 PASS")

if __name__ == "__main__":
    main()
