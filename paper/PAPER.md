# From registry audit to PhD paper: three publishable threads

This companion note turns the README benchmark into submittable manuscripts.
All premises are live-verified (see `results/VERIFICATION.md`); do not cite without re-running.

## Thread A — Results-reporting survival at full-registry scale
**Question.** What predicts time-to-results, and did the 2017 Final Rule shift the hazard?
**Design.** HLACT/ACT filter (FDAAA algorithm per PMID cohorts) × Kaplan–Meier + Cox
(sponsor class, phase, funding, enrollment) + regression discontinuity at Jan-2017.
**Benchmark hook.** Our H1 (86.73% without results; COMPLETED 330,931 vs true 80,361) is the
denominator; PMID 38831158/41240399/42082083 are the priors.
**Contribution.** First full-registry (605k) survival with Final-Rule HR replication.

## Thread B — UNKNOWN as a stale-record vital sign
**Question.** Can we predict which records go UNKNOWN and prioritize curation?
**Design.** Logistic/GBM on last-update lag, sponsor class, location completeness, phase missingness;
validate against Woo 2026 atlas snapshot (2026-03-29) → our 2026-10-02 delta.
**Benchmark hook.** H2 (98,141 UNKNOWN, 16.21%) + H3 (OTHER 71.6%).
**Contribution.** Registry-integrity triage score + curation queue.

## Thread C — The translational valley (PHASE2→PHASE3)
**Question.** Which Phase-2 trials ever reach Phase-3, and what blocks the rest?
**Design.** Intervention-normalized linkage (NCT + lead sponsor + condition) → transition graph;
competing-risks (termination/withdrawal vs progression) by sponsor × enrollment/site burden
(Brøgger-Mikkelsen priors: duration 13→18 mo, sites 43→64).
**Benchmark hook.** H4 (PHASE2 90,442 > PHASE3 49,967; NA 238,061; 143,573 missing phase).
**Contribution.** Valley quantification + sponsor-stratified efficiency frontier.

## Methods boilerplate (reuse)
Base `https://clinicaltrials.gov/api/v2`; `User-Agent` pinned; `check_freshness()` guard;
cursor pagination terminating on missing `nextPageToken`; `pageSize` clamp 1000;
`markupFormat` pinned; Essie `AREA[]` queries; `filter.*` for stratification.
Report `apiVersion`, `dataTimestamp`, `totalCount`, and `results/*.json` hashes.

## Ethics & data
Public registry, no key, no login. Aggregate city/country only; no contact PII.
Report the 86.7% gap without shaming individual sponsors; UNKNOWN prediction is for
curation, not compliance accusation. Pre-register hypotheses; publish code + Docker image.
