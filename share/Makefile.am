Applicationsdir = $(datadir)/applications $(datadir)/app-install/desktop
Applications_DATA = tomb.desktop

AppRegdir = $(datadir)/application-registry
AppReg_DATA = tomb.applications

MimeInfodir = $(datadir)/mime-info
MimeInfo_DATA = tomb.keys tomb.mime

Menudir = $(datadir)/menu
Menu_DATA = tomb

Iconsdir = $(datadir)/icons $(datadir)/app-install/icons
Icons_DATA = monmort.png

install-data-hook:
	xdg-mime install dyne-tomb.xml
	xdg-icon-resource install --context mimetypes --size 32 ../src/monmort.xpm monmort
	xdg-icon-resource install --size 32 ../src/monmort.xpm dyne-monmort
	mkdir -p $(prefix)/lib/mime/packages
	echo "application/x-tomb-volume; tomb-open '%s'; priority=8" > $(prefix)/lib/mime/packages/tomb
	update-desktop-database
	update-menus
	update-mime
