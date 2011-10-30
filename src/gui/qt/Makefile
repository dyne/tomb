all: ui_create.py
test: ui_create.py
	python2 -3 create.py
ui_create.py: create.ui
	 pyuic4 create.ui -o ui_create.py

clean:
	rm ui_create.py

.PHONY: test clean
