
bin_SCRIPTS = tomb

bin_PROGRAMS = tomb-gtk tomb-notify

tomb_gtk_SOURCES = tomb-gtk.cpp
tomb_gtk_LDADD = @GTK2_LIBS@ @NOTIFY_LIBS@
tomb_gtk_CXXFLAGS = @GTK2_CFLAGS@ @NOTIFY_CFLAGS@

tomb_notify_SOURCES = tomb-notify.cpp
tomb_notify_LDADD = @NOTIFY_LIBS@
tomb_notify_CXXFLAGS = @NOTIFY_CFLAGS@
