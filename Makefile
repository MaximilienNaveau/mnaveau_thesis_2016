FILENAME=16-thesis-defense-mnaveau
PDFFILE=$(FILENAME).pdf
TEXFILE=$(FILENAME).tex

OUTFOLDER=./build
REVERSE_OUTFOLDER=..

all: ${PDFFILE}

RM:=rm -f
PDFLATEX:= cd src/ ; pdflatex --output-directory=../build $(TEXFILE) ; cd ..
BIBTEX:= cd ./build ; bibtex $(FILENAME).aux ; cd ..

${PDFFILE}: ./src/$(TEXFILE)
	if [ ! -d "build" ]; then mkdir build; fi
	cd build ; ln -fs  ../src/$(FILENAME).bib $(FILENAME).bib ; cd ..
	cd build ; ln -fs  ../src/header/beamerouterthememysmoothbars.sty beamerouterthememysmoothbars.sty ; cd ..
	cd build ; ln -fs  ../videos videos ; cd ..
	$(PDFLATEX) 
	$(BIBTEX)
	$(PDFLATEX)
	$(PDFLATEX)

pdf:
	$(PDFLATEX) 

bibtex:
	$(BIBTEX)

install: 
	if [ ! -d "bin" ]; then mkdir bin; fi
	cp build/$(PDFFILE) bin/
	cd bin ; ln -fs  ../videos videos ; cd ..

clean:
	rm -f ./build/*

# dummy targets
.PHONY: clean
