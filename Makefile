PY = python
PYFLAGS = 
DOC = doxygen
DOCFLAGS = 
DOCCONFIG = 

SRC = src/WorshipList.py

.PHONY: all test gui doc clean

test: 
	$(PY) $(PYFLAGS) $(SRC) false

gui: 
	$(PY) $(PYFLAGS) $(SRC) true

doc: 
	$(DOC) $(DOCFLAGS) $(DOCCONFIG)
	cd latex && $(MAKE)

all: test doc

clean:
	rm output.docx
