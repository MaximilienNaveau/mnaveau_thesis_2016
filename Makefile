FILENAME=16-thesis-mnaveau
PDFFILE=$(FILENAME).pdf
TEXFILE=$(FILENAME).tex
BEAMERNAME=16-thesis-defense-mnaveau
PDFFILE=$(FILENAME).pdf
TEXFILE=$(FILENAME).tex
PWD=./src/Documents/writtings/16-thesis-mnaveau

SOURCEDIR=./src
REVERSE_SRCDIR=..

OUTPUTDIR=./bin
BUILDDIR=./build

RM:=rm -f
LATEXMK:= cd $(SOURCEDIR) ; latexmk -pdf -jobname=$(REVERSE_SRCDIR)/$(BUILDDIR) $(TEXFILE) ; cd $(REVERSE_SRCDIR)
PDFLATEX:= cd $(SOURCEDIR) ; pdflatex --output-directory=$(REVERSE_SRCDIR)/$(BUILDDIR) $(TEXFILE) ; cd $(REVERSE_SRCDIR)
PDFLATEXBEAMER:= cd $(REVIEWDIR) ; pdflatex --output-directory=$(REVERSE_REVIEWDIR)/$(BUILDDIR) $(BEAMERNAME).tex ; cd $(REVERSE_REVIEWDIR)
BIBTEX:= cd ./build ; bibtex $(FILENAME).aux ; cd ../
BEAMERBIBTEX:= cd ./build ; bibtex bu1.aux 

define prepare_build
	$(bash export TEXINPUTS=$(pwd)/:$(TEXINPUTS))
	if [ ! -d "build" ]; then mkdir build; fi
	if [ ! -d "bin" ]; then mkdir bin; fi
	ln -fs ../$(SOURCEDIR)/$(FILENAME)-short.bib ./build/
# 	create a link to the log file for texmaker
	ln -sf ../$(BUILDDIR)/$(FILENAME).log $(SOURCEDIR)/
	ln -sf ../src/texmf/tex/latex/modele-these/StyleThese.bst $(BUILDDIR)/
	ln -sf ../src/texmf/tex/latex/modele-these/StyleThese.cls $(BUILDDIR)/
	ln -sf ../src/texmf/tex/latex/modele-these/formatAndDefs.tex $(BUILDDIR)/
	ln -sf ../src/texmf/tex/latex/modele-these/formatAndDefs.aux $(BUILDDIR)/
	ln -sf ../src/texmf/tex/latex/modele-these/tlsflyleaf.sty $(BUILDDIR)/
	ln -sf ../src/texmf/tex/latex/modele-these/tlsflyleaf $(SOURCEDIR)/
endef

define end_build
# 	create a link to the log file for texmaker
	ln -sf ../$(BUILDDIR)/$(FILENAME).log $(SOURCEDIR)/
endef

define pdf_latex
	cd $(SOURCEDIR) ; pdflatex --output-directory=$(REVERSE_SRCDIR)/$(BUILDDIR) $(1).tex ; cd $(REVERSE_SRCDIR)
endef

define build
	$(call pdf_latex,$(1))
	cd ./build ; bibtex $(1).aux ; cd ../
	$(call pdf_latex,$(1))
	$(call pdf_latex,$(1))
endef



all:
	$(call prepare_build)
	$(call build,$(FILENAME))
	$(call end_build)

stateoftheart:
	$(call prepare_build)
	$(call build,Chapter-StateOfTheArt)
	$(call end_build)


introduction:
	$(call prepare_build)
	$(call build,Introduction)
	$(call end_build)

nmpc:
	$(call prepare_build)
	$(call build,Chapter-NMPCWalkgen)
	$(call end_build)

multicontact:
	$(call prepare_build)
	$(call build,Chapter-Multicontact)
	$(call end_build)

application:
	$(call prepare_build)
	$(call build,Chapter-Application)
	$(call end_build)

conclusion:
	$(call prepare_build)
	$(call build,Conclusion)
	$(call end_build)

annexe:
	$(call prepare_build)
	$(call build,Annexe1)
	$(call end_build)

resume:
	$(call prepare_build)
	$(call build,Resume)
	$(call end_build)


latexmk :
	${LATEXMK}

pdf:
	$(PDFLATEX)

install :
	cp $(BUILDDIR)/$(PDFFILE) $(OUTPUTDIR)/$(PDFFILE) # copy the results in a binary directory.


synthesis:
	cd figures/tikz/ ; pdflatex --output-directory=../../$(BUILDDIR) synthesis.tex ; cd ../../
	cp $(BUILDDIR)/synthesis.pdf ./figures/synthesis.pdf

bibtex:
	${BIBTEX}

beamerbitex:
	${BEAMERBIBTEX}

clean:
	$(RM) ./build/*
	$(RM) ./bin/*
#	$(RM) *.dvi *.ps *.log *.out *.aux *.blg *.bbl *.gz *.nav *.snm *.toc $(PDFFILE) $(PSFILE)

# dummy targets
.PHONY: clean
