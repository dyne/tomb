
man_MANS = tomb.1

EXTRA_DIST = Luks_on_disk_format.pdf New_methods_in_HD_encryption.pdf TKS1-draft.pdf

install-data-hook:
	ln -sf $(mandir)/man1/tomb.1 $(mandir)/man1/tomb-open.1
	ln -sf $(mandir)/man1/tomb.1 $(mandir)/man1/tomb-status.1
	ln -sf $(mandir)/man1/tomb.1 $(mandir)/man1/tomb-askpass.1