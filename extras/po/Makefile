PREFIX ?= /usr/local
LOCALEDIR ?= ${PREFIX}/share/locale
TOMBFILE = LC_MESSAGES/tomb.mo

all:
	@rm -f tomb.pot
	@perl generate_translatable_strings.pl > tomb.pot
	@echo "Strings generated in tomb.pot"

.PHONY: install
install: es.mo ru.mo fr.mo de.mo sv.mo it.mo
	install -Dm644 es.mo ${DESTDIR}${LOCALEDIR}/es_ES/${TOMBFILE}
	install -Dm644 ru.mo ${DESTDIR}${LOCALEDIR}/ru_RU/${TOMBFILE}
	install -Dm644 fr.mo ${DESTDIR}${LOCALEDIR}/fr_FR/${TOMBFILE}
	install -Dm644 de.mo ${DESTDIR}${LOCALEDIR}/de_DE/${TOMBFILE}
	install -Dm644 sv.mo ${DESTDIR}${LOCALEDIR}/sv_SV/${TOMBFILE}
	install -Dm644 it.mo ${DESTDIR}${LOCALEDIR}/it_IT/${TOMBFILE}
	@echo "Translations installed."

%.mo: %.po
	msgfmt -o $@ $<

.PHONY: clean
clean:
	@rm -f *.mo
