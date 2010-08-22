dnl ==============================================================
dnl Process this file with autoconf to produce a configure script.
dnl ==============================================================

dnl require autoconf 2.62 (AS_ECHO/AS_ECHO_N)
AC_PREREQ([2.60])

AC_INIT([Tomb],[0.8.0],[jaromil@dyne.org],[tomb])
AC_CONFIG_MACRO_DIR([m4])

AC_CANONICAL_HOST

dnl backwards compatibility for autoconf >= 2.64
dnl PACKAGE_URL should be the fifth argument of AC_INIT
m4_define([AC_PACKAGE_URL], [http://crypto.dyne.org])
AC_DEFINE(PACKAGE_URL, "AC_PACKAGE_URL", [Package URL])
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
[!] Your system architecture is not supported by AutOrg.
]], 0)
  ;;
esac


dnl ==============================================================
dnl Setup for automake
dnl ==============================================================

AM_INIT_AUTOMAKE([dist-bzip2 subdir-objects -Wno-portability])
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_CONFIG_SRCDIR([src/tomb])

dnl Checks for programs.
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MAKE_SET

dnl compatibility with older libtool
dnl m4_ifndef([LT_INIT], [AC_PROG_RANLIB])


dnl versioning info for libtool
DYNE_CURRENT=0
DYNE_REVISION=0
DYNE_AGE=0
DYNE_VERSION_INFO="$DYNE_CURRENT:$DYNE_REVISION:$DYNE_AGE"
dnl Note this is the ABI version which is not the same as our actual
dnl library version
AC_SUBST(DYNE_VERSION_INFO)


dnl ###########################################################################
dnl ###### now about compile time paths
AC_MSG_CHECKING([which installation prefix to use])
if test "x${prefix}" = "xNONE"; then
   prefix=`pwd`
fi
AC_MSG_RESULT([${prefix}])
TOMB_PATH="${prefix}"
AC_SUBST(TOMB_PATH)



dnl alphabetic order on dir/subdir, but Makefile sorts before everything
AC_CONFIG_FILES([
Makefile
src/Makefile
])

AC_OUTPUT


dnl autoconf < 2.63 compatibility
m4_ifndef([AS_VAR_APPEND],
          AC_DEFUN([AS_VAR_APPEND], $1=$$1$2))

dnl convenience function so that INFO messages go to config.log and to stdout,
dnl useful when debugging user problems only config.log is needed

dnl as above, but no newline at the end

