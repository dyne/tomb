bin_SCRIPTS = tomb tomb-open undertaker

if GTK
bin_PROGRAMS = tomb-status
else
bin_PROGRAMS =
endif

tomb_status_SOURCES = tomb-status.c
tomb_status_LDADD = @GTK2_LIBS@ @NOTIFY_LIBS@
tomb_status_CFLAGS = @GTK2_CFLAGS@ @NOTIFY_CFLAGS@

EXTRA_DIST = monmort.xpm tomb tomb-open
pixmapdir = $(datadir)/pixmaps
pixmap_DATA = monmort.xpm
