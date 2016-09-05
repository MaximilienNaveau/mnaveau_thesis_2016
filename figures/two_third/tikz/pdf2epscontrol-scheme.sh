#!/bin/bash
pdfcrop control-scheme.pdf
pdftops -f 1 -l 1 -eps control-scheme-crop.pdf
