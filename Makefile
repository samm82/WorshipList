PY = python
PYFLAGS = 
DOC = doxygen
DOCFLAGS = 
DOCCONFIG = 

SRC = src/Main.py

.PHONY: all test doc clean

test: 
	$(PY) $(PYFLAGS) $(SRC)

doc: 
	$(DOC) $(DOCFLAGS) $(DOCCONFIG)
	cd latex && $(MAKE)

all: test doc

clean:
	rm output.docx
	rm output.pdf
	rm -rf html/*
	rm -rf latex/*
