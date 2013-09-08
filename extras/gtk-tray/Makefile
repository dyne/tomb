
all:
	gcc -I. `pkg-config --cflags libnotify gtk+-3.0` $(CFLAGS) -c tomb-gtk-tray.c
	gcc tomb-gtk-tray.o `pkg-config --libs  libnotify gtk+-3.0` -o tomb-gtk-tray

clean:
	rm *.o tomb-gtk-tray
