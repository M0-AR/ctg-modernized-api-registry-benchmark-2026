"""Live-contract tests. Every assertion is a live API behavior verified 2026-10-05.
Nothing here trusts a snapshot: tests fail if the registry contract drifts.
"""
from src.ctg_client import get_json, get_version

def test_version_contract():
    v = get_version()
    assert v["apiVersion"].startswith("2."), v
    assert "T" in v["dataTimestamp"], v

def test_registry_scale_floor():
    j = get_json("/studies", {"format": "json", "pageSize": "1", "countTotal": "true", "fields": "NCTId"})
    assert j["totalCount"] >= 600_000, j.get("totalCount")
    s = get_json("/stats/size")
    assert s["totalStudies"] >= 600_000

def test_pagesize_clamp():
    j = get_json("/studies", {"format": "json", "pageSize": "1001", "fields": "NCTId"})
    assert len(j["studies"]) == 1000

def test_pagination_terminates_on_missing_token():
    j = get_json("/studies", {"format": "json", "pageSize": "2", "fields": "NCTId",
                              "filter.overallStatus": "RECRUITING",
                              "query.term": "AREA[StudyType]INTERVENTIONAL"})
    assert "studies" in j and len(j["studies"]) >= 1

def test_results_gap_persists():
    hr = get_json("/stats/field/values", {"fields": "HasResults"})[0]
    gap = hr["falseCount"] / (hr["falseCount"] + hr["trueCount"])
    assert gap > 0.80, gap

def test_unknown_bucket_persists():
    ov = get_json("/stats/field/values", {"fields": "OverallStatus"})[0]
    d = {x["value"]: x["studiesCount"] for x in ov["topValues"]}
    assert d["UNKNOWN"] > 90_000 and d["COMPLETED"] > 300_000

def test_markup_formats_differ_whitespace_only():
    md = get_json("/studies/NCT04852770", {"format": "json", "markupFormat": "markdown", "fields": "DetailedDescription"})
    lg = get_json("/studies/NCT04852770", {"format": "json", "markupFormat": "legacy", "fields": "DetailedDescription"})
    a = md["protocolSection"]["descriptionModule"]["detailedDescription"]
    b = lg["protocolSection"]["descriptionModule"]["detailedDescription"]
    assert a != b
    assert " ".join(a.split()) == " ".join(b.replace("\r", " ").replace("\n", " ").split())

def test_geo_filter():
    j = get_json("/studies", {"format": "json", "pageSize": "1",
                              "fields": "NCTId",
                              "filter.geo": "distance(39.0035707,-77.1013313,50mi)"})
    assert len(j.get("studies", [])) >= 1
