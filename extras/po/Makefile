LOCALEDIR ?= /usr/share/locale
TOMBFILE = LC_MESSAGES/tomb.mo

all:
	@rm -f tomb.pot
	@./generate_translatable_strings.sh > tomb.pot
	@echo "Strings generated in tomb.pot"

install: es.mo ru.mo fr.mo
	@install -Dm644 es.mo ${LOCALEDIR}/es/${TOMBFILE}
	@install -Dm644 ru.mo ${LOCALEDIR}/ru/${TOMBFILE}
	@install -Dm644 fr.mo ${LOCALEDIR}/fr/${TOMBFILE}

%.mo: %.po
	msgfmt -o $@ $<
