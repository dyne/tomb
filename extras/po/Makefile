LOCALEDIR ?= /usr/share/locale
TOMBFILE = LC_MESSAGES/tomb.po

all:
	@rm -f tomb.pot
	@./generate_translatable_strings.sh > tomb.pot
	@echo "Strings generated in tomb.pot"

install: *.mo
	@install -Dm755 es.mo ${LOCALEDIR}/es/${TOMBFILE}

es.mo: es.po
	msgfmt -o $@ $<
