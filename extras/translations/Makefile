PREFIX ?= /usr/local
LOCALEDIR ?= ${PREFIX}/share/locale
TOMBFILE = LC_MESSAGES/tomb.mo

all:
	@rm -f tomb.pot
	@perl generate_translatable_strings.pl > tomb.pot
	@echo "Strings generated in tomb.pot"

.PHONY: install
install: de.mo es.mo fr.mo it.mo pt_BR.mo ru.mo sv.mo
	install -Dm644 de.mo ${DESTDIR}${LOCALEDIR}/de_DE/${TOMBFILE}
	install -Dm644 es.mo ${DESTDIR}${LOCALEDIR}/es_ES/${TOMBFILE}
	install -Dm644 fr.mo ${DESTDIR}${LOCALEDIR}/fr_FR/${TOMBFILE}
	install -Dm644 it.mo ${DESTDIR}${LOCALEDIR}/it_IT/${TOMBFILE}
	install -Dm644 pt_BR.mo ${DESTDIR}${LOCALEDIR}/pt_BR/${TOMBFILE}
	install -Dm644 ru.mo ${DESTDIR}${LOCALEDIR}/ru_RU/${TOMBFILE}
	install -Dm644 sv.mo ${DESTDIR}${LOCALEDIR}/sv_SV/${TOMBFILE}
	@echo "Translations installed."

%.mo: %.po
	msgfmt -o $@ $<

.PHONY: clean
clean:
	@rm -f *.mo
