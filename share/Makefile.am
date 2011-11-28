
EXTRA_DIST = tomb.desktop tomb.applications tomb.keys tomb.mime tomb	\
             monmort.png gtkrc.in tomb.mimepkg dyne-tomb.xml

Applicationsdir = $(datadir)/applications
Applications_DATA = tomb.desktop

AppRegdir = $(datadir)/application-registry
AppReg_DATA = tomb.applications

MimeInfodir = $(datadir)/mime-info
MimeInfo_DATA = tomb.keys tomb.mime

Menudir = $(datadir)/menu
Menu_DATA = tomb

Iconsdir = $(datadir)/pixmaps
Icons_DATA = monmort.png

AppInstIcondir = $(datadir)/app-install/icons
AppInstIcon_DATA = monmort.png

AppInstDeskdir = $(datadir)/app-install/desktop
AppInstDesk_DATA = tomb.desktop

gtkrc:
	sed -e 's@\%prefix\%@'"$(datadir)"'@' $(top_srcdir)/share/gtkrc.in > \
					      $(top_builddir)/share/gtkrc

GtkRcdir = $(datadir)/themes/tomb/gtk-2.0-key
GtkRc_DATA = gtkrc

MimePkgdir = $(DESTDIR)/$(prefix)/lib/mime/packages/tomb
MimePkg = tomb.mimepkg

install-data-hook:
	@echo "installing mime type"
	@install -D $(top_srcdir)/share/dyne-tomb.xml $(DESTDIR)/$(datadir)/mime/packages/dyne-tomb.xml
	@if ! [ -n `which xdg-mime` ]; then xdg-mime install dyne-tomb.xml; fi
	@if ! [ -n `which update-desktop-database` ]; then echo update-desktop-database; update-desktop-database; fi
	@if ! [ -n `which update-menus` ]; then echo update-menus;  update-menus; fi
	@if ! [ -n `which update-mime` ]; then echo update-mime; update-mime; fi
	@echo "installing icons";
	@if ! [ -n `which xdg-icon-resource` ]; then \
		xdg-icon-resource install --context mimetypes --size 32 \
			$(top_srcdir)/src/monmort.xpm monmort; \
		xdg-icon-resource install --size 32 $(top_srcdir)/src/monmort.xpm monmort; fi
	@mkdir -p $(DESTDIR)/$(datadir)/icons/hicolor/32x32/mimetypes; \
	 ln -sf $(AppInstIcondir)/monmort.png \
	 	$(DESTDIR)/$(datadir)/icons/hicolor/32x32/mimetypes/application-x-tomb-volume.png
	 ln -sf $(AppInstIcondir)/monmort.png \
		$(DESTDIR)/$(datadir)/icons/hicolor/32x32/mimetypes/application-x-tomb-key.png
	@if ! [ -n `which update-icon-caches` ]; then \
		update-icon-caches $(DESTDIR)/$(datadir)/icons/hicolor; fi
	install $(top_builddir)/share/gtkrc $(DESTDIR)/$(GtkRcdir)/
distclean:
	unlink gtkrc
	unlink Makefile
