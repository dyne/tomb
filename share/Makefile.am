Applicationsdir = $(DESTDIR)/$(datadir)/applications
Applications_DATA = tomb.desktop

AppRegdir = $(DESTDIR)/$(datadir)/application-registry
AppReg_DATA = tomb.applications

MimeInfodir = $(DESTDIR)/$(datadir)/mime-info
MimeInfo_DATA = tomb.keys tomb.mime

Menudir = $(DESTDIR)/$(datadir)/menu
Menu_DATA = tomb

Iconsdir = $(DESTDIR)/$(datadir)/icons
Icons_DATA = monmort.png
 
AppInstIcondir = $(DESTDIR)/$(datadir)/app-install/icons
AppInstIcon_DATA = monmort.png

AppInstDeskdir = $(DESTDIR)/$(datadir)/app-install/desktop
AppInstDesk_DATA = tomb.desktop

gtkrc:
	sed -e 's@\%prefix\%@'"$(datadir)"'@' gtkrc.in > gtkrc

GtkRcdir = $(DESTDIR)/$(datadir)/themes/tomb/gtk-2.0-key
GtkRc_DATA = gtkrc

MimePkgdir = $(DESTDIR)/$(prefix)/lib/mime/packages/tomb
MimePkg = tomb.mimepkg

install-data-hook:
	@echo "installing mime type"
	@install -D dyne-tomb.xml $(DESTDIR)/$(datadir)/mime/packages
	@if ! [ -n `which xdg-mime` ]; then xdg-mime install dyne-tomb.xml; fi
	@echo "installing icons";
	@install -D monmort.png $(DESTDIR)/$(datadir)/pixmaps
	@if ! [ -n `which xdg-icon-resource` ]; then \
		xdg-icon-resource install --context mimetypes --size 32 ../src/monmort.xpm monmort; \
		xdg-icon-resource install --size 32 ../src/monmort.xpm dyne-monmort; fi
	@if ! [ -n `which update-desktop-database` ]; then echo update-desktop-database; update-desktop-database; fi
	@if ! [ -n `which update-menus` ]; then echo update-menus;  update-menus; fi
	@if ! [ -n `which update-mime` ]; then echo update-mime; update-mime; fi
