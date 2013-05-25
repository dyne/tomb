# {{{ - Install
# install mime-types, bells and whistles for the desktop
# see http://developers.sun.com/solaris/articles/integrating_gnome.html
# and freedesktop specs
install_tomb() {

# TODO: distro package deps (for binary)
# debian: zsh, cryptsetup, sudo
    _message "updating mimetypes..."
    cat <<EOF > /tmp/dyne-tomb.xml
<?xml version="1.0"?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="application/x-tomb-volume">
    <comment>Tomb crypto volume</comment>
    <glob pattern="*.tomb"/>
  </mime-type>
  <mime-type type="application/x-tomb-key">
    <comment>Tomb crypto key</comment>
    <glob pattern="*.tomb.key"/>
  </mime-type>
</mime-info>
EOF
    xdg-mime install /tmp/dyne-tomb.xml
    xdg-icon-resource install --context mimetypes --size 32 monmort.xpm monmort
    xdg-icon-resource install --size 32 monmort.xpm dyne-monmort

    rm /tmp/dyne-tomb.xml

    _message "updating desktop..."
    cat <<EOF > /usr/share/applications/tomb.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Tomb crypto undertaker
GenericName=Crypto undertaker
Comment=Keep your bones safe
Exec="${TOMBOPENEXEC}" %U
TryExec=tomb-open
Icon=monmort.xpm
Terminal=true
Categories=Utility;Security;Archiving;Filesystem;
MimeType=application/x-tomb-volume;
X-AppInstall-Package=tomb
EOF
    update-desktop-database

    _message "updating menus..."
    cat <<EOF > /etc/menu/tomb
?package(tomb):command="tomb" icon="/usr/share/pixmaps/monmort.xpm" needs="text" \
	section="Applications/Accessories" title="Tomb" hints="Crypto" \
	hotkey="Tomb"
EOF
    update-menus

    _message "updating mime info..."
    cat <<EOF > /usr/share/mime-info/tomb.keys
# actions for encrypted tomb storage
application/x-tomb-volume:
	open="${TOMBOPENEXEC}" %f
	view=tomb-open %f
	icon-filename=monmort.xpm
	short_list_application_ids_for_novice_user_level=tomb
EOF
    cat <<EOF > /usr/share/mime-info/tomb.mime
# mime type for encrypted tomb storage
application/x-tomb-volume
	ext: tomb

application/x-tomb-key
	ext: tomb.key
EOF
    cat <<EOF > /usr/lib/mime/packages/tomb
application/x-tomb-volume; tomb-open '%s'; priority=8
EOF
    update-mime

    _message "updating application entry..."

    cat <<EOF > /usr/share/application-registry/tomb.applications
tomb
	 command=tomb-open
	 name=Tomb - Crypto Undertaker
	 can_open_multiple_files=false
	 expects_uris=false
	 requires_terminal=true
	 mime-types=application/x-tomb-volume,application/x-tomb-key
EOF
    _message "Tomb is now installed."
}
# }}}
