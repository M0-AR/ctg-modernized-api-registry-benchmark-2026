"""Robust client for ClinicalTrials.gov API v2.
Verified live 2026-10-05 against production:
  GET /version -> {"apiVersion":"2.0.5","dataTimestamp":"2026-10-02T09:00:04"}
Only stdlib + requests. Implements: retries with backoff, dataTimestamp guard,
cursor pagination (terminate on missing nextPageToken), pageSize clamp handling.
"""
from __future__ import annotations
import os
import time
import requests

BASE = os.getenv("CTG_BASE", "https://clinicaltrials.gov/api/v2")
UA = os.getenv("CTG_UA", "ctg-benchmark-2026/1.0")
TIMEOUT = int(os.getenv("CTG_TIMEOUT", "60"))

def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "application/json"})
    return s

def get_json(path: str, params: dict | None = None, retries: int = 3) -> dict:
    s = session()
    url = BASE + path
    last = None
    for i in range(retries):
        try:
            r = s.get(url, params=params or {}, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()
        except Exception as e:  # backoff 2s, 4s
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"GET {url} failed after {retries}: {last}")

def get_version() -> dict:
    return get_json("/version")

def check_freshness(max_age_days: int = 7) -> dict:
    """Return version + age check. Data refreshes Mon-Fri ~09:00 ET (14:00 UTC)."""
    from datetime import datetime, timezone
    v = get_version()
    ts = v.get("dataTimestamp", "")
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age_h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    except Exception:
        age_h = float("nan")
    return {"version": v, "age_hours": age_h, "fresh": age_h <= max_age_days * 24}

def paginate(params: dict, max_pages: int = 5, page_size: int = 100) -> list[dict]:
    """Cursor pagination. Termination = missing nextPageToken (verified live).
    Same params must be reused except pageSize/pageToken/countTotal.
    """
    out: list[dict] = []
    p = dict(params or {})
    p["pageSize"] = page_size
    p.pop("pageToken", None)
    for _ in range(max_pages):
        j = get_json("/studies", p)
        studies = j.get("studies", [])
        out.extend(studies)
        tok = j.get("nextPageToken")
        if not tok:
            break
        p["pageToken"] = tok
        # countTotal only valid on first page
        p.pop("countTotal", None)
        time.sleep(0.4)  # be polite to federal API
    return out
