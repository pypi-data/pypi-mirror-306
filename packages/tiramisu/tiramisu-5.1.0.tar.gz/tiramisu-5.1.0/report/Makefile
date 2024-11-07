.SUFFIXES:

.PHONY: all clean

all: html

generate:
	python ./generate.py
	    		
html: generate
	make -C ./build all

clean: 
	make -C ./build clean
	
