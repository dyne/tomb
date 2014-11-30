PREFIX ?= /usr/local

all:
	$(CC) -I. `pkg-config --cflags libnotify gtk+-2.0` $(CFLAGS) -c tomb-gtk-tray.c
	$(CC) tomb-gtk-tray.o `pkg-config --libs  libnotify gtk+-2.0` -o tomb-gtk-tray

install:
	install -Dm666 gtkrc-2.0 ${DESTDIR}${PREFIX}/share/themes/tomb/gtk-2.0-key/gtkrc
	install -Dm666 monmort.xpm ${DESTDIR}${PREFIX}/share/themes/tomb/gtk-2.0-key/monmort.xpm

clean:
	rm -f *.o tomb-gtk-tray
