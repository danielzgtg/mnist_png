#!/bin/bash
# Written during https://bugs.ghostscript.com/show_bug.cgi?id=708123#c6
set -e
set -x
if [ ! -d mnist_png ]; then
  tar xzvf mnist_png.tar.gz
fi
rm -rf atlas
mkdir atlas
./atlas.py
cd atlas
convert *.png mnist.pdf
time gs -dQUIET -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=ghostscript.pdf mnist.pdf
time qpdf --recompress-flate --compression-level=9 ghostscript.pdf qpdf.pdf
pdfimages -list ghostscript.pdf
pdfimages -list qpdf.pdf
