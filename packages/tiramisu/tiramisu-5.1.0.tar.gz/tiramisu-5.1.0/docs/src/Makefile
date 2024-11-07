SRC=$(wildcard *.py)
HTMLFRAGMENT=$(addsuffix .html, $(basename $(SRC)))

.SUFFIXES:

.PHONY: all clean

all: html
#	make -C ./build all

html: $(HTMLFRAGMENT)

%.html: %.py
	pygmentize -f html -O full,bg=white,style=bw, -o ../en/_build/html/_modules/$@ $<

clean:
#	make -C ./build clean

