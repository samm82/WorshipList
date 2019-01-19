PY = python
PYFLAGS = 
#DOC = doxygen
#DOCFLAGS = 
#DOCCONFIG = docConfig

SRC = WorshipList.py

.PHONY: all test clean

test: 
	$(PY) $(PYFLAGS) $(SRC)

#doc: 
#    $(DOC) $(DOCFLAGS) $(DOCCONFIG)
#    cd latex && $(MAKE)

all: test #doc

clean:
	rm output.docx
