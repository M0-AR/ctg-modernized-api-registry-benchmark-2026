"""Experiment E05: modernized ingest — locations + geopoint.
Official notice: locations/geopoint now pull from a different geographic DB.
Verified live 2026-10-05:
  filter.geo=distance(39.0035707,-77.1013313,50mi) returns studies (e.g. NCT01181323, NCT00002359)
  with contactsLocationsModule.locations[].city/country populated.
This experiment asserts geo filter works and locations are present, and records
the new-DB behavior (city strings, no lat/lon in default fields).
"""
import json, os
from src.ctg_client import get_json

def main():
    j = get_json("/studies", {"format": "json", "pageSize": "2",
                              "fields": "NCTId,OverallStatus,LocationCity,LocationCountry",
                              "filter.geo": "distance(39.0035707,-77.1013313,50mi)"})
    studies = j.get("studies", [])
    locs = []
    for s in studies:
        for loc in s.get("protocolSection", {}).get("contactsLocationsModule", {}).get("locations", [])[:3]:
            locs.append(loc)
    print("geo hits:", len(studies), "sample locs:", json.dumps(locs[:3], indent=2)[:800])
    os.makedirs("results", exist_ok=True)
    with open("results/e05_geo.json", "w") as f:
        json.dump({"hits": len(studies),
                   "ncts": [s["protocolSection"]["identificationModule"]["nctId"] for s in studies],
                   "sample_locations": locs[:5]}, f, indent=2)
    assert len(studies) >= 1, "geo filter returned nothing — ingest or index changed"
    assert locs, "no locations in geo response"
    print("E05 PASS")

if __name__ == "__main__":
    main()
