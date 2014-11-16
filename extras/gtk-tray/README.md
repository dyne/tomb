# Gtk2 tray icon for Tomb
## by Jaromil

If you like to see our nifty little skull on the upper right corner of
your desktop, then compile and install this little auxiliary program.

Use by launching `tomb-gtk-tray` followed by the name of your tomb as
reported by `tomb list`. For instance if your tomb is `secrets.tomb`:

```
 $ tomb-gtk-tray secrets
```

The tray offers a drop-down menu with three options:
 + `explore` will launch your desktop configured filemanager
 + `close` will try to close the tomb (fails if in use)
 + `slam` will slam the tomb killing all applications using it

Please note you need to launch this program for each tomb you want it
to administer, then you will have a skull visible for each tomb open.

By mouse-over the skull tells the name of the tomb it is open for.

Enjoy!
