PY = python
PYFLAGS = 
DOC = doxygen
DOCFLAGS = 
DOCCONFIG = 

SRC = src/WorshipList.py

.PHONY: all test gui doc clean

test: 
	$(PY) $(PYFLAGS) $(SRC)

gui: 
	$(PY) $(PYFLAGS) $(SRC) gui

doc: 
	$(DOC) $(DOCFLAGS) $(DOCCONFIG)
	cd latex && $(MAKE)

all: test doc

clean:
	rm output.docx
	rm -rf html/*
	rm -rf latex/*
