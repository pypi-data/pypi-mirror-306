SRC=$(wildcard *.txt)
HTMLFRAGMENT=$(addsuffix .html, $(basename $(SRC)))

.SUFFIXES:

.PHONY: all clean

all: html

html: $(HTMLFRAGMENT)

%.html: %.txt    
	./rst2html.py --stylesheet ./style.css $< > $@

clean:
	rm -f *.html
	rm -f *.txt
	
