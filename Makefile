PY = python
PYFLAGS = -u
DOC = doxygen
DOCFLAGS = 
DOCCONFIG = 

MAIN = src/Main.py
DIST_SRC = dist/src

.PHONY: all test doc clean

run: 
	$(PY) $(PYFLAGS) $(MAIN)

compile: $(MAIN)
	pyinstaller --onefile $^ #-w
	mkdir $(DIST_SRC)
	cp -R src/songs $(DIST_SRC)
	cp src/Settings.txt $(DIST_SRC)

doc: 
	$(DOC) $(DOCFLAGS) $(DOCCONFIG)
	cd latex && $(MAKE)

lint:
	flake8 --ignore=E402,F403,F405,N802,N806,N813,N815,W504 .

all: compile lint doc

clean:
# Compilation files
	rm -rf build/*
	rm -rf dist/*
# Continues execution if Main.spec not found
	rm Main.spec || true

# Documentation files
	rm -rf html/*
	rm -rf latex/*
	
