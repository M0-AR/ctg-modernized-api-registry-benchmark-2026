.PHONY: up test fetch clean
up:
\tdocker compose up --build research
test:
\tpytest -v tests/
fetch:
\tpython scripts/run_all.py
clean:
\trm -rf results/*.json results/*.png data/*.json __pycache__
