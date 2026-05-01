# Top-level Makefile for the statistical-eval-tutorial repo.
#
#   make           # build the paper, the workbook, and (if missing) the figures
#   make figures   # regenerate every figure in paper/figs/ from a fresh seeded run
#   make paper     # compile paper/stateval.pdf (and re-run bibtex)
#   make workbook  # compile appendix/student-appendix.pdf
#   make clean     # remove LaTeX build artifacts (keeps PDFs and figures)
#   make distclean # also remove generated PDFs and figures (full rebuild needed)

.PHONY: all figures paper workbook clean distclean

all: paper workbook

# ---- figures --------------------------------------------------------------

figures:
	python code/figures.py

# ---- main paper -----------------------------------------------------------

paper:
	cd paper && pdflatex -interaction=nonstopmode stateval.tex > /dev/null
	cd paper && bibtex stateval > /dev/null || true
	cd paper && pdflatex -interaction=nonstopmode stateval.tex > /dev/null
	cd paper && pdflatex -interaction=nonstopmode stateval.tex > /dev/null
	@echo "Built paper/stateval.pdf"

# ---- workbook -------------------------------------------------------------
# Builds twice so xr cross-references to the paper resolve. Requires
# paper/stateval.aux to exist; build the paper first if you have not.

workbook: paper/stateval.aux
	cd appendix && pdflatex -interaction=nonstopmode student-appendix.tex > /dev/null
	cd appendix && pdflatex -interaction=nonstopmode student-appendix.tex > /dev/null
	@echo "Built appendix/student-appendix.pdf"

paper/stateval.aux: paper
	@:

# ---- cleanup --------------------------------------------------------------

clean:
	rm -f paper/*.aux paper/*.log paper/*.out paper/*.bbl paper/*.blg paper/*.toc
	rm -f appendix/*.aux appendix/*.log appendix/*.out appendix/*.toc

distclean: clean
	rm -f paper/stateval.pdf appendix/student-appendix.pdf
	rm -f paper/figs/*.pdf
