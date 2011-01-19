
bin_SCRIPTS = tomb tomb-open

bin_PROGRAMS = tomb-status tomb-askpass

tomb_status_SOURCES = tomb-status.c
tomb_status_LDADD = @GTK2_LIBS@ @NOTIFY_LIBS@
tomb_status_CFLAGS = @GTK2_CFLAGS@ @NOTIFY_CFLAGS@

tomb_askpass_SOURCES = tomb-askpass.c
tomb_askpass_LDADD = @GTK2_LIBS@
tomb_askpass_CFLAGS = @GTK2_CFLAGS@

EXTRA_DIST = monmort.xpm
pixmapdir = $(prefix)/share/pixmaps
pixmap_DATA = monmort.xpm
