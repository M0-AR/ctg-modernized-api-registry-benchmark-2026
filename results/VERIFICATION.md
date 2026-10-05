# VERIFICATION — live evidence ledger (2026-10-05 UTC)

All commands ran with `User-Agent: ctg-benchmark-2026/1.0` against `https://clinicaltrials.gov/api/v2`.
Re-run: `pytest -v tests/` (8 tests) + `python scripts/run_all.py` (E01–E07).

| # | Claim in README | Endpoint + params | Observed | Artifact |
|---|---|---|---|---|
| V01 | apiVersion + timestamp | `GET /version` | `2.0.5`, `2026-10-05T09:00:05` (Monday, SLA ✓) | `results/e01_version.json`, age 3.2h fresh=true |
| V02 | scale 605,819 | `GET /studies?countTotal=true&pageSize=1&fields=NCTId` + `GET /stats/size` | `totalCount=605819`, `totalStudies=605819`, avg 17301 B | `results/e02_pagination.json`, `e03_distributions.json` |
| V03 | clamp 1001→1000 | `GET /studies?pageSize=1001&fields=NCTId` | 200 OK, 1000 rows | test_pagesize_clamp PASS |
| V04 | termination rule | narrow query + `paginate()` 2×10 | 20 rows, token-chained; `recruiting_interventional=47150` | `e02_pagination.json` |
| V05 | status distribution | `GET /stats/field/values?fields=OverallStatus` | COMPLETED 331052, UNKNOWN 98113, RECRUITING 64541, … 14 values | `e03_distributions.json` |
| V06 | phase/sponsor/type/results | `...?fields=Phase/LeadSponsorClass/StudyType/HasResults` | NA 238061; OTHER 433502/INDUSTRY 132769; INT 462154; false 525442/true 80377 | same |
| V07 | markup divergence | `GET /studies/NCT04852770?markupFormat=markdown vs legacy&fields=DetailedDescription` | 1629 vs 1647 chars, raw≠, normalized= | `e04_markup.json` |
| V08 | geo new-DB | `GET /studies?filter.geo=distance(39.0035707,-77.1013313,50mi)&pageSize=2` | NCT01181323, NCT00002359 + city/country locs | `e05_geo.json` |
| V09 | hidden ratios | derived | gap 86.73%, unknown 16.20% | `e06_hidden_patterns.json` |
| V10 | triangulation | `GET /version` weekday + `GET /studies/NCT04852770` + Kaggle search | Monday; TERMINATED/false; 3 Kaggle mirrors noted | `e07_triangulation.json` |
| V11 | contract suite | `pytest -v tests/` | **8 passed in 23.02s (re-run 2026-10-05)** | console log |
| V12 | end-to-end | `python scripts/run_all.py` + `figures.py` | ALL EXPERIMENTS PASS + `fig_status_top8.png` 61 kB | `results/` |

Online voting (sequential, distinct keywords): websearch, searxng (unreachable → fallback noted),
openresearch web/openalex/news/hackernews/europepmc/stackoverflow, paper-search arxiv/unified/pubmed,
duckduckgo, agent-reach, gitmcp (no-hit), kaggle, wiki, gsd_websearch, superpowers — see README §2.

Docker: `docker compose config` validates; `docker compose up --build research` builds
`python:3.12-slim` + pip install (needs ~3 min first pull; timed out at 120s in sandbox, config OK,
local pytest green).
