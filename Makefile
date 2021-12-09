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
	pyinstaller --onefile $^ -n WorshipList #-w
	rm WorshipList.spec || true
# Continues execution if dist/ exists
	mkdir $(DIST_SRC) || true
	cp -R src/songs $(DIST_SRC)
	cp src/Settings.txt $(DIST_SRC)
	cp src/COMPILED_README.md dist
	mv dist/COMPILED_README.md dist/README.md
	sed -i -- "s@COMPILE_DATE@$$(date "+%-m/%-d/%Y")@g" dist/README.md

build: compile

doc: 
	$(DOC) $(DOCFLAGS) $(DOCCONFIG)
	cd latex && $(MAKE)

lint:
	flake8 --ignore=E266,E402,E722,F403,F405,N802,N806,N813,N815,W504 .

all: compile lint doc

clean:
# Compilation files
	rm -rf build/*
	rm -rf dist/*

# Documentation files
	rm -rf html/*
	rm -rf latex/*
	
