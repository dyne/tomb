TARGETS_OPEN=tombqt/ui_open_tombfile.py tombqt/ui_open_keymethod.py tombqt/ui_open_success.py
TARGETS=tombqt/ui_create.py $(TARGETS_OPEN)

all: $(TARGETS)
test_create: tombqt/ui_create.py
	python2 -3 tombqt/create.py
test_open: $(TARGETS_OPEN)
	python2 -3 tombqt/open.py


tombqt/ui_create.py: tombqt/create.ui
	 pyuic4 create.ui -o tombqt/ui_create.py
tombqt/ui_open_tombfile.py: tombqt/open_tombfile.ui
	pyuic4 tombqt/open_tombfile.ui -o tombqt/ui_open_tombfile.py
tombqt/ui_open_keymethod.py: tombqt/open_keymethod.ui
	pyuic4 tombqt/open_keymethod.ui -o tombqt/ui_open_keymethod.py
tombqt/ui_open_success.py: tombqt/open_success.ui
	pyuic4 tombqt/open_success.ui -o tombqt/ui_open_success.py

clean:
	rm $(TARGETS)

.PHONY: test clean
