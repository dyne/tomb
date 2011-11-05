dnl ==============================================================
dnl Process this file with autoconf to produce a configure script.
dnl ==============================================================

AC_PREREQ([2.60])

AC_INIT([Tomb],[1.2],[jaromil@dyne.org],[Tomb])
AC_CONFIG_MACRO_DIR([m4])

AC_CANONICAL_HOST

dnl backwards compatibility for autoconf >= 2.64
dnl PACKAGE_URL should be the fifth argument of AC_INIT
m4_define([AC_PACKAGE_URL], [http://tomb.dyne.org])
dnl AC_DEFINE(PACKAGE_URL, "AC_PACKAGE_URL", [Package URL])
AC_SUBST(PACKAGE_URL, AC_PACKAGE_URL)

dnl ==============================================================
dnl Get the operating system and version number...
dnl ==============================================================
AC_MSG_CHECKING([for which platform we are setting up])

case "$host_os" in
  *linux*)
    AC_MSG_RESULT([Linux])
    have_linux=yes

    if test x$have_x86_64 = xyes; then
        have_64bit=yes
    fi

    if test x$have_x86_32 = xyes; then
        have_32bit=yes
    fi
  ;;

  *darwin*)
    AC_MSG_RESULT([Darwin/OSX])
    have_darwin=yes
  ;;

  *freebsd*)
    AC_MSG_RESULT([FreeBSD])
    have_freebsd=yes
  ;;

  *)
    AC_MSG_RESULT([$host_os?!])
    AC_MSG_ERROR([[
[!] Your system architecture is not supported by Tomb.
]], 0)
  ;;
esac


dnl ==============================================================
dnl Setup for automake
dnl ==============================================================

AM_INIT_AUTOMAKE([dist-bzip2 subdir-objects -Wno-portability])
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_CONFIG_SRCDIR([src/tomb])

dnl Checks for reguired programs.
AC_PROG_CC
AC_PROG_INSTALL

dnl translation infrastructure
dnl waiting for translations..
dnl AM_GNU_GETTEXT
dnl AM_GNU_GETTEXT_VERSION(0.12)

dnl ---------------------------------------------------------------
dnl Checks for external programs.

dnl none of these will fail with error if missing since technically
dnl these are not *build* dependencies, but *runtime* dependencies.

dnl Mandatory
AC_CHECK_PROG(have_zsh,zsh,yes,no)
AC_CHECK_PROG(have_cryptsetup,cryptsetup,yes,no)
AC_CHECK_PROG(have_pinentry,pinentry,yes,no)
AC_CHECK_PROG(have_sudo,sudo,yes,no)
dnl Optional
AC_CHECK_PROG(have_wipe,wipe,yes,no)
AC_CHECK_PROG(have_dcfldd,dcfldd,yes,no)
dnl ---------------------------------------------------------------

PKG_CHECK_MODULES(GTK2, [gtk+-2.0 >= 2.16], :,
  AC_MSG_ERROR([*** Gtk+2 >=2.16 development files not found!]))
AC_SUBST([GTK2_CFLAGS])
AC_SUBST([GTK2_LIBS])

PKG_CHECK_MODULES(NOTIFY, libnotify, :,
  AC_MSG_ERROR([*** libnotify development files not found!]))
AC_SUBST([NOTIFY_CFLAGS])
AC_SUBST([NOTIFY_LIBS])
REALCFLAGS="$CFLAGS"
REALLIBS="$LIBS"
CFLAGS="$NOTIFY_CFLAGS $CFLAGS"
LIBS="$NOTIFY_LIBS $LIBS"
AC_CHECK_FUNCS([notify_notification_new_with_status_icon])
CFLAGS="$REALCFLAGS"
LIBS="$REALLIBS"

dnl compile with full warnings and debugging symbols
AC_ARG_ENABLE(debug,
    AS_HELP_STRING([--enable-debug],[compile with debug symbols (no)]),
    [enable_debug=$enableval],
    [enable_debug=no])
AC_MSG_CHECKING([if compiling with debug symbols])
if test x$enable_debug = xyes; then
    AC_MSG_RESULT([yes])
    CFLAGS="$CFLAGS -Wall -g -ggdb"
else
    AC_MSG_RESULT([no])
fi
AC_SUBST(CFLAGS)


PACKAGE_DATA_DIR='${prefix}/share/tomb'
AC_SUBST(PACKAGE_DATA_DIR)
# mime TODO see http://www.freedesktop.org/wiki/Specifications/AddingMIMETutor
XDG_DATA_DIR='${prefix}/share/mime/packages'
AC_SUBST(XDG_DATA_DIR)


dnl alphabetic order on dir/subdir, but Makefile sorts before everything
AC_CONFIG_FILES([
Makefile
src/Makefile
doc/Makefile
share/Makefile
])
AC_OUTPUT

dnl function to print verbose configure options only if V=1 is passed to
dnl configure
AC_DEFUN([VRB],
         AS_IF([test x"$V" == x1], INFO([$1])))

dnl autoconf < 2.63 compatibility
m4_ifndef([AS_VAR_APPEND],
          AC_DEFUN([AS_VAR_APPEND], $1=$$1$2))

dnl convenience function so that INFO messages go to config.log and to stdout,
dnl useful when debugging user problems only config.log is needed
AC_DEFUN([INFO],
         AS_ECHO(["$1"]) >&AS_MESSAGE_LOG_FD
         AS_ECHO(["$1"]) >&AS_MESSAGE_FD)

dnl as above, but no newline at the end
AC_DEFUN([INFO_N],
         AS_ECHO_N(["$1"]) >&AS_MESSAGE_LOG_FD
         AS_ECHO_N(["$1"]) >&AS_MESSAGE_FD)
