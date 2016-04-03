# Makefile for Sphinx documentation
#

all: html

HAVE_SPHINXBUILD_3 := $(shell command -v sphinx-build-3)
HAVE_SPHINXAUTOBUILD_3 := $(shell command -v sphinx-autobuild-3)

# You can set these variables from the command line.
SPHINXOPTS    =
ifdef HAVE_SPHINXBUILD_3
	SPHINXBUILD   = sphinx-build-3
else
	SPHINXBUILD   = sphinx-build
endif
ifdef HAVE_SPHINXAUTOBUILD_3
	SPHINXAUTOBUILD   = sphinx-autobuild-3
else
	SPHINXAUTOBUILD   = sphinx-autobuild
endif
BUILDDIR      = _build
PORT          = 8008

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  serve      to run a server"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  gettext    to make PO message catalogs"
	@echo "  linkcheck  to check all external links for integrity"

clean:
	rm -rf $(BUILDDIR)/*

serve: html
	sphinx-autobuild-3 -b html -p 8008 $(ALLSPHINXOPTS) $(BUILDDIR)/html

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

gettext:
	$(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."
