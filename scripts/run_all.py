import sys
sys.path.insert(0, ".")
from src.experiments import e01_version_and_freshness as e01
from src.experiments import e02_pagination_and_fields as e02
from src.experiments import e03_status_phase_sponsor_benchmark as e03
from src.experiments import e04_markup_modernized_ingest as e04
from src.experiments import e05_geo_modernized_ingest as e05
from src.experiments import e06_hidden_patterns_results_gap as e06
from src.experiments import e07_reproducibility_live_matrix as e07

if __name__ == "__main__":
    for i, m in enumerate([e01, e02, e03, e04, e05, e06, e07], start=1):
        print(f"\n===== E0{i} =====")
        m.main()
    print("\nALL EXPERIMENTS PASS")
