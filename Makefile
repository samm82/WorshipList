PY = py
PYFLAGS = -u
INSTALL = PyInstaller

DOC = doxygen
DOCFLAGS = 
DOCCONFIG = 

MAIN = src/Main.py
DIST_PATH = dist
DIST_SRC = dist/src

.PHONY: all test doc clean

run: 
	$(PY) $(PYFLAGS) $(MAIN)

compile: $(MAIN)
	$(PY) -m $(INSTALL) --onefile $^ -n WorshipList -i src/icon.ico #-w
# Continues execution if WorshipList.spec does not exist
	rm WorshipList.spec || true
# Continues execution if dist/ exists
	mkdir $(DIST_SRC) || true
	cp -R src/songs $(DIST_SRC)
	cp Settings.json $(DIST_PATH)
	cp src/COMPILED_README.md $(DIST_PATH)
	mv $(DIST_PATH)/COMPILED_README.md $(DIST_PATH)/README.md
	sed -i -- "s@COMPILE_DATE@$$(date "+%-m/%-d/%Y")@g" $(DIST_PATH)/README.md

build: compile

doc: 
	$(DOC) $(DOCFLAGS) $(DOCCONFIG)
	cd latex && $(MAKE)

lint:
	flake8 --ignore=E266,E402,E722,F403,F405,N802,N806,N813,N815,W504 --max-line-length=130 src/

all: compile lint doc

clean:
# Compilation files
	rm -rf build/*
	rm -rf $(DIST_PATH)/*

# Documentation files
	rm -rf html/*
	rm -rf latex/*

rebuild: clean compile

recompile: rebuild
