PYTHON ?= python3
.PHONY: all data figures verify clean
all: main.pdf
data:
	$(PYTHON) reproduction/scripts/analyze.py
	$(PYTHON) reproduction/scripts/analyze_survey.py
	$(PYTHON) reproduction/scripts/analyze_speculation.py
figures: data
	uv run --with matplotlib==3.10.8 python reproduction/scripts/plot.py
verify:
	$(PYTHON) reproduction/scripts/verify.py
references.bib: research/sources.json research/build_bibliography.py
	$(PYTHON) research/build_bibliography.py
main.pdf: main.tex references.bib arxiv.sty generated/numbers.tex generated/survey.tex generated/concurrency_rows.tex generated/speculation.tex figures/dense.pdf figures/prefill.pdf figures/mtp.pdf figures/concurrency.pdf
	@if command -v tectonic >/dev/null 2>&1; then tectonic --keep-logs main.tex; else pdflatex -interaction=nonstopmode -halt-on-error main.tex && bibtex main && pdflatex -interaction=nonstopmode -halt-on-error main.tex && pdflatex -interaction=nonstopmode -halt-on-error main.tex; fi
clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.toc main.fls main.fdb_latexmk main.synctex.gz
