PREFIX ?= /usr/local
LOCALEDIR ?= ${PREFIX}/share/locale
TOMBFILE = LC_MESSAGES/tomb.mo

all:
	@rm -f tomb.pot
	@./generate_translatable_strings.sh > tomb.pot
	@echo "Strings generated in tomb.pot"

.PHONY: install
install: es.mo ru.mo fr.mo de.mo
	install -Dm644 es.mo ${DESTDIR}${LOCALEDIR}/es_ES/${TOMBFILE}
	install -Dm644 ru.mo ${DESTDIR}${LOCALEDIR}/ru_RU/${TOMBFILE}
	install -Dm644 fr.mo ${DESTDIR}${LOCALEDIR}/fr_FR/${TOMBFILE}
	install -Dm644 de.mo ${DESTDIR}${LOCALEDIR}/de_DE/${TOMBFILE}
	@echo "Translations installed."

%.mo: %.po
	msgfmt -o $@ $<

.PHONY: clean
clean:
	@rm -f *.mo
