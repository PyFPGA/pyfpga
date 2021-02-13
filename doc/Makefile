CP=cp

# Sphinx options.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees -T -D language=en $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

all: pyfpga.info

#---

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man

#---

html:
	PYTHONPATH=$(shell pwd)/.. $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

#---

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex

#---

texi: pyfpga.texi
pyfpga.texi:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	$(CP) $(BUILDDIR)/texinfo/PyFPGA.texi $@

info: pyfpga.info
pyfpga.info: pyfpga.texi
	makeinfo -o $@ $<

dvi: pyfpga.dvi
pyfpga.dvi: pyfpga.texi
	texi2dvi $<

pyfpga.ps: pyfpga.dvi
	dvips $<

pdf: pyfpga.pdf
pyfpga.pdf: pyfpga.dvi
	dvipdf $<

#---

clean:
	$(RM) *~ *.dvi *.info *.aux *.cp *.fn *.ky *.log
	$(RM) *.pdf *.pg *.toc *.tp *.vr *.texi
	$(RM) -rf _build
