# Raw data policy

- No bulk dumps are committed. The registry is 605,599 studies × ~17 kB avg (~10 GB full-fidelity).
- Experiments use the live API with tight `fields=` projections and `pageSize ≤ 1000`.
- To keep a local sample: `python scripts/run_all.py` writes only aggregate `results/*.json`.
- For full-registry work, use the official bulk XML snapshot or AACT, then join NCT IDs from `results/`.
- Never commit contact PII (`centralContacts`, `overallOfficials`, location contacts). City/country aggregates only.
