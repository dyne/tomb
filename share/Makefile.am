Applicationsdir = $(datadir)/applications
Applications_DATA = tomb.desktop

AppRegdir = $(datadir)/application-registry
AppReg_DATA = tomb.applications

MimeInfodir = $(datadir)/mime-info
MimeInfo_DATA = tomb.keys tomb.mime

Menudir = $(datadir)/menu
Menu_DATA = tomb

Iconsdir = $(datadir)/icons
Icons_DATA = monmort.png
 
AppInstIcondir = $(datadir)/app-install/icons
AppInstIcon_DATA = monmort.png

AppInstDeskdir = $(datadir)/app-install/desktop
AppInstDesk_DATA = tomb.desktop

install-data-hook:
	@echo "installing mime type"; xdg-mime install dyne-tomb.xml
	@mkdir -p $(prefix)/lib/mime/packages
	@echo "application/x-tomb-volume; tomb-open '%s'; priority=8" > $(prefix)/lib/mime/packages/tomb
	@echo "installing icons";
	@xdg-icon-resource install --context mimetypes --size 32 ../src/monmort.xpm monmort
	@xdg-icon-resource install --size 32 ../src/monmort.xpm dyne-monmort
	@echo "updating dekstop database"; update-desktop-database
	@if ! [ -n `which update-menus` ]; then echo update-menus;  update-menus; fi
	update-mime
