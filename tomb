#!/bin/zsh
#
# Tomb, the Crypto Undertaker
#
# A commandline tool to easily operate encryption of secret data
#

# {{{ License

# Copyright (C) 2007-2015 Dyne.org Foundation
#
# Tomb is designed, written and maintained by Denis Roio <jaromil@dyne.org>
#
# With contributions by Anathema, Boyska, Hellekin O. Wolf and GDrooid
#
# Gettext internationalization and Spanish translation is contributed by
# GDrooid, French translation by Hellekin, Russian translation by fsLeg,
# German translation by x3nu.
#
# Testing, reviews and documentation are contributed by Dreamer, Shining
# the Translucent, Mancausoft, Asbesto Molesto, Nignux, Vlax, The Grugq,
# Reiven, GDrooid, Alphazo, Brian May, TheJH, fsLeg, JoelMon and the
# Linux Action Show!
#
# Tomb's artwork is contributed by Jordi aka Mon Mort and Logan VanCuren.
#
# Cryptsetup was developed by Christophe Saout and Clemens Fruhwirth.

# This source code is free software; you can redistribute it and/or
# modify it under the terms of the GNU Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This source code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  Please refer
# to the GNU Public License for more details.
#
# You should have received a copy of the GNU Public License along with
# this source code; if not, write to: Free Software Foundation, Inc.,
# 675 Mass Ave, Cambridge, MA 02139, USA.

# }}} - License

# {{{ Global variables

typeset VERSION="2.1"
typeset DATE="Jul/2015"
typeset TOMBEXEC=$0
typeset TMPPREFIX=${TMPPREFIX:-/tmp}
# TODO: configure which tmp dir to use from a cli flag

# Tomb is using some global variables set by the shell:
# TMPPREFIX, UID, GID, PATH, TTY, USERNAME
# You can grep 'global variable' to see where they are used.

# Keep a reference of the original command line arguments
typeset -a OLDARGS
for arg in "${(@)argv}"; do OLDARGS+=("$arg"); done

# Special command requirements
typeset -a DD WIPE PINENTRY
DD=(dd)
WIPE=(rm -f)
PINENTRY=(pinentry)

# load zsh regex module
zmodload zsh/regex
zmodload zsh/mapfile
zmodload -F zsh/stat b:zstat

# make sure variables aren't exported
unsetopt allexport

# Flag optional commands if available (see _ensure_dependencies())
typeset -i KDF=1
typeset -i STEGHIDE=1
typeset -i RESIZER=1
typeset -i SWISH=1
typeset -i QRENCODE=1

# Default mount options
typeset      MOUNTOPTS="rw,noatime,nodev"

# Makes glob matching case insensitive
unsetopt CASE_MATCH

typeset -AH OPTS              # Command line options (see main())

# Command context (see _whoami())
typeset -H  _USER             # Running username
typeset -Hi _UID              # Running user identifier
typeset -Hi _GID              # Running user group identifier
typeset -H  _TTY              # Connected input terminal

# Tomb context (see _plot())
typeset -H TOMBPATH           # Full path to the tomb
typeset -H TOMBDIR            # Directory where the tomb is
typeset -H TOMBFILE           # File name of the tomb
typeset -H TOMBNAME           # Name of the tomb

# Tomb secrets
typeset -H TOMBKEY            # Encrypted key contents (see forge_key(), recover_key())
typeset -H TOMBKEYFILE        # Key file               (ditto)
typeset -H TOMBSECRET         # Raw deciphered key     (see forge_key(), gpg_decrypt())
typeset -H TOMBPASSWORD       # Raw tomb passphrase    (see gen_key(), ask_key_password())
typeset -H TOMBTMP            # Filename of secure temp just created (see _tmp_create())

typeset -aH TOMBTMPFILES      # Keep track of temporary files
typeset -aH TOMBLOOPDEVS      # Keep track of used loop devices

# Make sure sbin is in PATH (man zshparam)
path+=( /sbin /usr/sbin )

# For gettext
export TEXTDOMAIN=tomb

# }}}

# {{{ Safety functions

# Wrap sudo with a more visible message
_sudo() {
    local sudo_eng="[sudo] Enter password for user ::1 user:: to gain superuser privileges"
    local msg="$(gettext -s "$sudo_eng")"
    msg=${(S)msg//::1*::/$USER}
    sudo -p "
$msg

" ${@}
}

# Cleanup anything sensitive before exiting.
_endgame() {

    # Prepare some random material to overwrite vars
    local rr="$RANDOM"
    while [[ ${#rr} -lt 500 ]]; do
        rr+="$RANDOM"
    done

    # Ensure no information is left in unallocated memory
    TOMBPATH="$rr";      unset TOMBPATH
    TOMBDIR="$rr";       unset TOMBDIR
    TOMBFILE="$rr";      unset TOMBFILE
    TOMBNAME="$rr";      unset TOMBNAME
    TOMBKEY="$rr";       unset TOMBKEY
    TOMBKEYFILE="$rr";   unset TOMBKEYFILE
    TOMBSECRET="$rr";    unset TOMBSECRET
    TOMBPASSWORD="$rr";  unset TOMBPASSWORD

    # Clear temporary files
    for f in $TOMBTMPFILES; do
        ${=WIPE} "$f"
    done
    unset TOMBTMPFILES

    # Detach loop devices
    for l in $TOMBLOOPDEVS; do
        _sudo losetup -d "$l"
    done
    unset TOMBLOOPDEVS

}

# Trap functions for the _endgame event
TRAPINT()  { _endgame INT   }
TRAPEXIT() { _endgame EXIT  }
TRAPHUP()  { _endgame HUP   }
TRAPQUIT() { _endgame QUIT  }
TRAPABRT() { _endgame ABORT }
TRAPKILL() { _endgame KILL  }
TRAPPIPE() { _endgame PIPE  }
TRAPTERM() { _endgame TERM  }
TRAPSTOP() { _endgame STOP  }

_cat() { local -a _arr;
    # read file using mapfile, newline fix
    _arr=("${(f@)${mapfile[${1}]%$’\n’}}"); print "$_arr"
}

_is_found() {
    # returns 0 if binary if found in path
    [[ "$1" = "" ]] && return 1
    command -v "$1" 1>/dev/null 2>/dev/null
    return $?
}

# Identify the running user
# Set global variables _UID, _GID, _TTY, and _USER, either from the
# command line, -U, -G, -T, respectively, or from the environment.
# Also update USERNAME and HOME to maintain consistency.
_whoami() {

    # Set username from UID or environment
    _USER=$SUDO_USER
    [[ "$_USER" = "" ]] && { _USER=$USERNAME }
    [[ "$_USER" = "" ]] && { _USER=$(id -u)  }
    [[ "$_USER" = "" ]] && {
        _failure "Failing to identify the user who is calling us" }

    # Get GID from option -G or the environment
    option_is_set -G \
        && _GID=$(option_value -G) || _GID=$(id -g $_USER)

    # Get UID from option -U or the environment
    option_is_set -U \
        && _UID=$(option_value -U) || _UID=$(id -u $_USER)

    _verbose "Identified caller: ::1 username:: (::2 UID:::::3  GID::)" $_USER $_UID $_GID

    # Update USERNAME accordingly if we can
    [[ EUID == 0 && $_USER != $USERNAME ]] && {
        _verbose "Updating USERNAME from '::1 USERNAME::' to '::2 _USER::')" $USERNAME $_USER
        USERNAME=$_USER
    }

    # Force HOME to _USER's HOME if necessary
    local home=$(awk -F: "/^$_USER:/ { print \$6 }" /etc/passwd 2>/dev/null)
    [[ $home == $HOME ]] || {
        _verbose "Updating HOME to match user's: ::1 home:: (was ::2 HOME::)" \
            $home $HOME
        HOME=$home }

    # Get connecting TTY from option -T or the environment
    option_is_set -T && _TTY=$(option_value -T)
    [[ -z $_TTY ]]   && _TTY=$TTY

}

# Define sepulture's plot (setup tomb-related arguments)
# Synopsis: _plot /path/to/the.tomb
# Set TOMB{PATH,DIR,FILE,NAME}
_plot() {

    # We set global variables
    typeset -g TOMBPATH TOMBDIR TOMBFILE TOMBNAME

    TOMBPATH="$1"

    TOMBDIR=$(dirname $TOMBPATH)

    TOMBFILE=$(basename $TOMBPATH)

    # The tomb name is TOMBFILE without an extension.
    # It can start with dots: ..foo.tomb -> ..foo
    TOMBNAME="${TOMBFILE%\.[^\.]*}"
    [[ -z $TOMBNAME ]] && {
        _failure "Tomb won't work without a TOMBNAME." }

}

# Provide a random filename in shared memory
_tmp_create() {
    [[ -d "$TMPPREFIX" ]] || {
        # we create the tempdir with the sticky bit on
        _sudo mkdir -m 1777 "$TMPPREFIX"
        [[ $? == 0 ]] || _failure "Fatal error creating the temporary directory: ::1 temp dir::" "$TMPPREFIX"
    }

    # We're going to add one more $RANDOM for each time someone complain
    # about this being too weak of a random.
    tfile="${TMPPREFIX}/$RANDOM$RANDOM$RANDOM$RANDOM"   # Temporary file
    umask 066
    [[ $? == 0 ]] || {
        _failure "Fatal error setting the permission umask for temporary files" }

    [[ -r "$tfile" ]] && {
        _failure "Someone is messing up with us trying to hijack temporary files." }

    touch "$tfile"
    [[ $? == 0 ]] || {
        _failure "Fatal error creating a temporary file: ::1 temp file::" "$tfile" }

    _verbose "Created tempfile: ::1 temp file::" "$tfile"
    TOMBTMP="$tfile"
    TOMBTMPFILES+=("$tfile")

    return 0
}

# Check if a *block* device is encrypted
# Synopsis: _is_encrypted_block /path/to/block/device
# Return 0 if it is an encrypted block device
_is_encrypted_block() {
    local    b=$1 # Path to a block device
    local    s="" # lsblk option -s (if available)

    # Issue #163
    # lsblk --inverse appeared in util-linux 2.22
    # but --version is not consistent...
    lsblk --help | grep -Fq -- --inverse
    [[ $? -eq 0 ]] && s="--inverse"

    sudo lsblk $s -o type -n $b 2>/dev/null \
        | egrep -q '^crypt$'

    return $?
}

# Check if swap is activated
# Return 0 if NO swap is used, 1 if swap is used.
# Return 1 if any of the swaps is not encrypted.
# Return 2 if swap(s) is(are) used, but ALL encrypted.
# Use _check_swap in functions, that will call this function but will
# exit if unsafe swap is present.
_ensure_safe_swap() {

    local -i r=1    # Return code: 0 no swap, 1 unsafe swap, 2 encrypted
    local -a swaps  # List of swap partitions
    local    bone is_crypt

    swaps="$(awk '/^\// { print $1 }' /proc/swaps 2>/dev/null)"
    [[ -z "$swaps" ]] && return 0 # No swap partition is active

    _message "An active swap partition is detected..."
    for s in $=swaps; do
        { _is_encrypted_block $s } && { r=2 } || {
	    # We're dealing with unencrypted stuff.
	    # Maybe it lives on an encrypted filesystem anyway.
	    # @todo: verify it's actually on an encrypted FS (see #163 and !189)
	    # Well, no: bail out.
	    r=1; break
	}
    done

    if [[ $r -eq 2 ]]; then
        _success "All your swaps are belong to crypt.  Good."
    else
        _warning "This poses a security risk."
        _warning "You can deactivate all swap partitions using the command:"
        _warning " swapoff -a"
        _warning "[#163] I may not detect plain swaps on an encrypted volume."
        _warning "But if you want to proceed like this, use the -f (force) flag."
    fi
    return $r

}

# Wrapper to allow encrypted swap and remind the user about possible
# data leaks to disk if swap is on, and not to be ignored.  It could
# be run once in main(), but as swap evolves, it's better to run it
# whenever swap may be needed.
# Exit if unencrypted swap is active on the system.
_check_swap() {
    if ! option_is_set -f && ! option_is_set --ignore-swap; then
        _ensure_safe_swap
        case $? in
            0|2)     # No, or encrypted swap
                return 0
                ;;
            *)       # Unencrypted swap
                _failure "Operation aborted."
                ;;
        esac
    fi
}

# Ask user for a password
# Wraps around the pinentry command, from the GnuPG project, as it
# provides better security and conveniently use the right toolkit.
ask_password() {

    local description="$1"
    local title="${2:-Enter tomb password.}"
    local output
    local password
    local gtkrc
    local theme

    # Distributions have broken wrappers for pinentry: they do
    # implement fallback, but they disrupt the output somehow.  We are
    # better off relying on less intermediaries, so we implement our
    # own fallback mechanisms. Pinentry supported: curses, gtk-2, qt4
    # and x11.

    # make sure LANG is set, default to C
    LANG=${LANG:-C}

    _verbose "asking password with tty=$TTY lc-ctype=$LANG"

    if [[ "$DISPLAY" = "" ]]; then

        if _is_found "pinentry-curses"; then
            _verbose "using pinentry-curses"
            output=`cat <<EOF | pinentry-curses
OPTION ttyname=$TTY
OPTION lc-ctype=$LANG
SETTITLE $title
SETDESC $description
SETPROMPT Password:
GETPIN
EOF`
        else
            _failure "Cannot find pinentry-curses and no DISPLAY detected."
        fi

    else # a DISPLAY is found to be active

        # customized gtk2 dialog with a skull (if extras are installed)
        if _is_found "pinentry-gtk-2"; then
            _verbose "using pinentry-gtk2"

            gtkrc=""
            theme=/share/themes/tomb/gtk-2.0-key/gtkrc
            for i in /usr/local /usr; do
                [[ -r $i/$theme ]] && {
                    gtkrc="$i/$theme"
                    break
                }
            done
            [[ "$gtkrc" = "" ]] || {
                gtkrc_old="$GTK2_RC_FILES"
                export GTK2_RC_FILES="$gtkrc"
            }
            output=`cat <<EOF | pinentry-gtk-2
OPTION ttyname=$TTY
OPTION lc-ctype=$LANG
SETTITLE $title
SETDESC $description
SETPROMPT Password:
GETPIN
EOF`
            [[ "$gtkrc" = "" ]] || export GTK2_RC_FILES="$gtkrc_old"

            # TODO QT4 customization of dialog
        elif _is_found "pinentry-qt4"; then
            _verbose "using pinentry-qt4"

            output=`cat <<EOF | pinentry-qt4
OPTION ttyname=$TTY
OPTION lc-ctype=$LANG
SETTITLE $title
SETDESC $description
SETPROMPT Password:
GETPIN
EOF`

            # TODO X11 customization of dialog
        elif _is_found "pinentry-x11"; then
            _verbose "using pinentry-x11"

            output=`cat <<EOF | pinentry-x11
OPTION ttyname=$TTY
OPTION lc-ctype=$LANG
SETTITLE $title
SETDESC $description
SETPROMPT Password:
GETPIN
EOF`

        else

            if _is_found "pinentry-curses"; then
                _verbose "using pinentry-curses"

                _warning "Detected DISPLAY, but only pinentry-curses is found."
                output=`cat <<EOF | pinentry-curses
OPTION ttyname=$TTY
OPTION lc-ctype=$LANG
SETTITLE $title
SETDESC $description
SETPROMPT Password:
GETPIN
EOF`
            else
                _failure "Cannot find any pinentry: impossible to ask for password."
            fi

        fi

    fi # end of DISPLAY block

    # parse the pinentry output
    for i in ${(f)output}; do
        [[ "$i" =~ "^ERR.*" ]] && {
            _warning "Pinentry error: ::1 error::" ${i[(w)3]}
            print "canceled"
            return 1 }

        # here the password is found
        [[ "$i" =~ "^D .*" ]] && password="${i##D }"
    done

    [[ "$password" = "" ]] && {
        _warning "Empty password"
        print "empty"
        return 1 }

    print "$password"
    return 0
}



# Check if a filename is a valid tomb
is_valid_tomb() {
    _verbose "is_valid_tomb ::1 tomb file::" $1

    # First argument must be the path to a tomb
    [[ -z "$1" ]] && {
        _failure "Tomb file is missing from arguments." }

    _fail=0
    # Tomb file must be a readable, writable, not-empty regular file.
    [[ ! -w "$1" ]] && {
        _warning "Tomb file is not writable: ::1 tomb file::" $1
        _fail=1
    }
    [[ ! -f "$1" ]] && {
        _warning "Tomb file is not a regular file: ::1 tomb file::" $1
        _fail=1
    }
    [[ ! -s "$1" ]] && {
        _warning "Tomb file is empty (zero length): ::1 tomb file::" $1
        _fail=1
    }

    _uid="`zstat +uid $1`"
    [[ "$_uid"  = "$UID" ]] || {
        _user="`zstat -s +uid $1`"
        _warning "Tomb file is owned by another user: ::1 tomb owner::" $_user
    }
    [[ $_fail = 1 ]] && {
        _failure "Tomb command failed: ::1 command name::" $subcommand
    }

    # TODO: split the rest of that function out.
    # We already have a valid tomb, now we're checking
    # whether we can alter it.

    # Tomb file may be a LUKS FS (or we are creating it)
    [[ "`file $1`" =~ "luks encrypted file" ]] || {
        _warning "File is not yet a tomb: ::1 tomb file::" $1 }

    _plot $1     # Set TOMB{PATH,DIR,FILE,NAME}

    # Tomb cannot be already mounted (or we cannot alter it)
    [[ "`mount -l`" -regex-match "${TOMBFILE}.*\[$TOMBNAME\]$" ]] && {
        _failure "Tomb is currently in use: ::1 tomb name::" $TOMBNAME
    }

    _message "Valid tomb file found: ::1 tomb path::" $TOMBPATH

    return 0
}

# $1 is the tomb file to be lomounted
lo_mount() {
    tpath="$1"

    # check if we have support for loop mounting
    _nstloop=`_sudo losetup -f`
    [[ $? = 0 ]] || {
        _warning "Loop mount of volumes is not possible on this machine, this error"
        _warning "often occurs on VPS and kernels that don't provide the loop module."
        _warning "It is impossible to use Tomb on this machine at this conditions."
        _failure "Operation aborted."
    }

    _sudo losetup -f "$tpath" # allocates the next loopback for our file

    TOMBLOOPDEVS+=("$_nstloop") # add to array of lodevs used

    return 0
}

# print out latest loopback mounted
lo_new() { print - "${TOMBLOOPDEVS[${#TOMBLOOPDEVS}]}" }

# $1 is the path to the lodev to be preserved after quit
lo_preserve() {
    _verbose "lo_preserve on ::1 path::" $1
    # remove the lodev from the tomb_lodevs array
    TOMBLOOPDEVS=("${(@)TOMBLOOPDEVS:#$1}")
}

# eventually used for debugging
dump_secrets() {
    print "TOMBPATH: $TOMBPATH"
    print "TOMBNAME: $TOMBNAME"

    print "TOMBKEY len: ${#TOMBKEY}"
    print "TOMBKEYFILE: $TOMBKEYFILE"
    print "TOMBSECRET len: ${#TOMBSECRET}"
    print "TOMBPASSWORD: $TOMBPASSWORD"

    print "TOMBTMPFILES: ${(@)TOMBTMPFILES}"
    print "TOMBLOOPDEVS: ${(@)TOMBLOOPDEVS}"
}

# }}}

# {{{ Commandline interaction

usage() {
    _print "Syntax: tomb [options] command [arguments]"
    _print "\000"
    _print "Commands:"
    _print "\000"
    _print " // Creation:"
    _print " dig     create a new empty TOMB file of size -s in MB"
    _print " forge   create a new KEY file and set its password"
    _print " lock    installs a lock on a TOMB to use it with KEY"
    _print "\000"
    _print " // Operations on tombs:"
    _print " open    open an existing TOMB"
    _print " index   update the search indexes of tombs"
    _print " search  looks for filenames matching text patterns"
    _print " list    list of open TOMBs and information on them"
    _print " close   close a specific TOMB (or 'all')"
    _print " slam    slam a TOMB killing all programs using it"
    [[ $RESIZER == 1 ]] && {
        _print " resize  resize a TOMB to a new size -s (can only grow)"
    }
    _print "\000"
    _print " // Operations on keys:"
    _print " passwd  change the password of a KEY (needs old pass)"
    _print " setkey  change the KEY locking a TOMB (needs old key and pass)"
    _print "\000"
    [[ $QRENCODE == 1 ]] && {
        _print " // Backup on paper:"
        _print " engrave makes a QR code of a KEY to be saved on paper"
    }
    _print "\000"
    [[ $STEGHIDE == 1 ]] && {
        _print " // Steganography:"
        _print " bury    hide a KEY inside a JPEG image (for use with -k)"
        _print " exhume  extract a KEY from a JPEG image (prints to stdout)"
    }
    _print "\000"
    _print "Options:"
    _print "\000"
    _print " -s     size of the tomb file when creating/resizing one (in MB)"
    _print " -k     path to the key to be used ('-k -' to read from stdin)"
    _print " -n     don't process the hooks found in tomb"
    _print " -o     options passed to commands: open, lock, forge (see man)"
    _print " -f     force operation (i.e. even if swap is active)"
    [[ $KDF == 1 ]] && {
        _print " --kdf  forge keys armored against dictionary attacks"
    }

    _print "\000"
    _print " -h     print this help"
    _print " -v     print version, license and list of available ciphers"
    _print " -q     run quietly without printing informations"
    _print " -D     print debugging information at runtime"
    _print "\000"
    _print "For more informations on Tomb read the manual: man tomb"
    _print "Please report bugs on <http://github.com/dyne/tomb/issues>."
}


# Check whether a commandline option is set.
#
# Synopsis: option_is_set -flag [out]
#
# First argument is the commandline flag (e.g., "-s").
# If the second argument is present and set to 'out', print out the
# result: either 'set' or 'unset' (useful for if conditions).
#
# Return 0 if is set, 1 otherwise
option_is_set() {
    local -i r   # the return code (0 = set, 1 = unset)

    [[ -n ${(k)OPTS[$1]} ]];
    r=$?

    [[ $2 == "out" ]] && {
        [[ $r == 0 ]] && { print 'set' } || { print 'unset' }
    }

    return $r;
}

# Print the option value matching the given flag
# Unique argument is the commandline flag (e.g., "-s").
option_value() {
    print -n - "${OPTS[$1]}"
}

# Messaging function with pretty coloring
function _msg() {
    local msg="$2"
    command -v gettext 1>/dev/null 2>/dev/null && msg="$(gettext -s "$2")"
    for i in $(seq 3 ${#});
    do
        msg=${(S)msg//::$(($i - 2))*::/$*[$i]}
    done

    local command="print -P"
    local progname="$fg[magenta]${TOMBEXEC##*/}$reset_color"
    local message="$fg_bold[normal]$fg_no_bold[normal]$msg$reset_color"
    local -i returncode

    case "$1" in
        inline)
            command+=" -n"; pchars=" > "; pcolor="yellow"
            ;;
        message)
            pchars=" . "; pcolor="white"; message="$fg_no_bold[$pcolor]$msg$reset_color"
            ;;
        verbose)
            pchars="[D]"; pcolor="blue"
            ;;
        success)
            pchars="(*)"; pcolor="green"; message="$fg_no_bold[$pcolor]$msg$reset_color"
            ;;
        warning)
            pchars="[W]"; pcolor="yellow"; message="$fg_no_bold[$pcolor]$msg$reset_color"
            ;;
        failure)
            pchars="[E]"; pcolor="red"; message="$fg_no_bold[$pcolor]$msg$reset_color"
            returncode=1
            ;;
        print)
            progname=""
            ;;
        *)
            pchars="[F]"; pcolor="red"
            message="Developer oops!  Usage: _msg MESSAGE_TYPE \"MESSAGE_CONTENT\""
            returncode=127
            ;;
    esac
    ${=command} "${progname} $fg_bold[$pcolor]$pchars$reset_color ${message}$color[reset_color]" >&2
    return $returncode
}

function _message say() {
    local notice="message"
    [[ "$1" = "-n" ]] && shift && notice="inline"
    option_is_set -q || _msg "$notice" $@
    return 0
}

function _verbose xxx() {
    option_is_set -D && _msg verbose $@
    return 0
}

function _success yes() {
    option_is_set -q || _msg success $@
    return 0
}

function _warning  no() {
    option_is_set -q || _msg warning $@
    return 1
}

function _failure die() {
    typeset -i exitcode=${exitv:-1}
    option_is_set -q || _msg failure $@
    # be sure we forget the secrets we were told
    exit $exitcode
}

function _print() {
    option_is_set -q || _msg print $@
    return 0
}

_list_optional_tools() {
    typeset -a _deps
    _deps=(gettext dcfldd wipe steghide)
    _deps+=(resize2fs tomb-kdb-pbkdf2 qrencode swish-e unoconv)
    for d in $_deps; do
        _print "`which $d`"
    done
    return 0
}


# Check program dependencies
#
# Tomb depends on system utilities that must be present, and other
# functionality that can be provided by various programs according to
# what's available on the system.  If some required commands are
# missing, bail out.
_ensure_dependencies() {

    # Check for required programs
    for req in cryptsetup pinentry sudo gpg mkfs.ext4 e2fsck; do
        command -v $req 1>/dev/null 2>/dev/null || {
            _failure "Missing required dependency ::1 command::.  Please install it." $req }
    done

    # Ensure system binaries are available in the PATH
    path+=(/sbin /usr/sbin) # zsh magic

    # Which dd command to use
    command -v dcfldd 1>/dev/null 2>/dev/null && DD=(dcfldd statusinterval=1)

    # Which wipe command to use
    command -v wipe 1>/dev/null 2>/dev/null && WIPE=(wipe -f -s)

    # Check for steghide
    command -v steghide 1>/dev/null 2>/dev/null || STEGHIDE=0
    # Check for resize
    command -v resize2fs 1>/dev/null 2>/dev/null || RESIZER=0
    # Check for KDF auxiliary tools
    command -v tomb-kdb-pbkdf2 1>/dev/null 2>/dev/null || KDF=0
    # Check for Swish-E file content indexer
    command -v swish-e 1>/dev/null 2>/dev/null || SWISH=0
    # Check for QREncode for paper backups of keys
    command -v qrencode 1>/dev/null 2>/dev/null || QRENCODE=0
}

# }}} - Commandline interaction

# {{{ Key operations

# $1 is the encrypted key contents we are checking
is_valid_key() {
    local key="$1"       # Unique argument is an encrypted key to test

    _verbose "is_valid_key"

    [[ -z $key ]] && key=$TOMBKEY
    [[ "$key" = "cleartext" ]] && {
        { option_is_set --unsafe } || {
            _warning "cleartext key from stdin selected: this is unsafe."
            exitv=127 _failure "please use --unsafe if you really want to do this."
        }
        _warning "received key in cleartext from stdin (unsafe mode)"
        return 0 }

    [[ -z $key ]] && {
        _warning "is_valid_key() called without an argument."
        return 1
    }

    # If the key file is an image don't check file header
    [[ -r $TOMBKEYFILE ]] \
        && [[ $(file $TOMBKEYFILE) =~ "JP.G" ]] \
        && {
        _message "Key is an image, it might be valid."
        return 0 }

    [[ $key =~ "BEGIN PGP" ]] && {
        _message "Key is valid."
        return 0 }

    return 1
}

# $1 is a string containing an encrypted key
_tomb_key_recover recover_key() {
    local key="${1}"    # Unique argument is an encrypted key

    _warning "Attempting key recovery."

    _head="${key[(f)1]}" # take the first line

    TOMBKEY=""        # Reset global variable

    [[ $_head =~ "^_KDF_" ]] && TOMBKEY+="$_head\n"

    TOMBKEY+="-----BEGIN PGP MESSAGE-----\n"
    TOMBKEY+="$key\n"
    TOMBKEY+="-----END PGP MESSAGE-----\n"

    return 0
}

# Retrieve the tomb key from the file specified from the command line,
# or from stdin if -k - was selected.  Run validity checks on the
# file.  On success, return 0 and print out the full path of the key.
# Set global variables TOMBKEY and TOMBKEYFILE.
_load_key() {
    local keyfile="$1"    # Unique argument is an optional keyfile

    [[ -z $keyfile ]] && keyfile=$(option_value -k)
    [[ -z $keyfile ]] && {
        _failure "This operation requires a key file to be specified using the -k option." }

    if [[ $keyfile == "-" ]]; then
        _verbose "load_key reading from stdin."
        _message "Waiting for the key to be piped from stdin... "
        TOMBKEYFILE=stdin
        TOMBKEY=$(cat)
    elif [[ $keyfile == "cleartext" ]]; then
        _verbose "load_key reading SECRET from stdin"
        _message "Waiting for the key to be piped from stdin... "
        TOMBKEYFILE=cleartext
        TOMBKEY=cleartext
        TOMBSECRET=$(cat)
    else
        _verbose "load_key argument: ::1 key file::" $keyfile
        [[ -r $keyfile ]] || _failure "Key not found, specify one using -k."
        TOMBKEYFILE=$keyfile
        TOMBKEY="${mapfile[$TOMBKEYFILE]}"
    fi

    _verbose "load_key: ::1 key::" $TOMBKEYFILE

    [[ "$TOMBKEY" = "" ]] && {
        # something went wrong, there is no key to load
        # this occurs especially when piping from stdin and aborted
        _failure "Key not found, specify one using -k."
    }

    is_valid_key $TOMBKEY || {
        _warning "The key seems invalid or its format is not known by this version of Tomb."
        _tomb_key_recover $TOMBKEY
    }

    # Declared TOMBKEYFILE (path)
    # Declared TOMBKEY (contents)

    return 0
}

# takes two args just like get_lukskey
# prints out the decrypted content
# contains tweaks for different gpg versions
gpg_decrypt() {
    # fix for gpg 1.4.11 where the --status-* options don't work ;^/
    local gpgver=$(gpg --version --no-permission-warning | awk '/^gpg/ {print $3}')
    local gpgpass="$1\n$TOMBKEY"
    local gpgstatus

    [[ $gpgver == "1.4.11" ]] && {
        _verbose "GnuPG is version 1.4.11 - adopting status fix."

        TOMBSECRET=`print - "$gpgpass" | \
            gpg --batch --passphrase-fd 0 --no-tty --no-options`
        ret=$?
        unset gpgpass

    } || { # using status-file in gpg != 1.4.11

        TOMBSECRET=`print - "$gpgpass" | \
            gpg --batch --passphrase-fd 0 --no-tty --no-options \
            --status-fd 2 --no-mdc-warning --no-permission-warning \
            --no-secmem-warning` |& grep GNUPG: \
            | read -r -d'\n' gpgstatus

        unset gpgpass

        ret=1

        [[ "${gpgstatus}" =~ "DECRYPTION_OKAY" ]] && { ret=0 }


    }
    return $ret

}


# Gets a key file and a password, prints out the decoded contents to
# be used directly by Luks as a cryptographic key
get_lukskey() {
    # $1 is the password
    _verbose "get_lukskey"

    _password="$1"


    firstline="${TOMBKEY[(f)1]}"

    # key is KDF encoded
    if [[ $firstline =~ '^_KDF_' ]]; then
        kdf_hash="${firstline[(ws:_:)2]}"
        _verbose "KDF: ::1 kdf::" "$kdf_hash"
        case "$kdf_hash" in
            "pbkdf2sha1")
                kdf_salt="${firstline[(ws:_:)3]}"
                kdf_ic="${firstline[(ws:_:)4]}"
                kdf_len="${firstline[(ws:_:)5]}"
                _verbose "KDF salt: $kdf_salt"
                _verbose "KDF ic: $kdf_ic"
                _verbose "KDF len: $kdf_len"
                _password=$(tomb-kdb-pbkdf2 $kdf_salt $kdf_ic $kdf_len 2>/dev/null <<<$_password)
                ;;
            *)
                _failure "No suitable program for KDF ::1 program::." $pbkdf_hash
                unset _password
                return 1
                ;;
        esac

        # key needs to be exhumed from an image
    elif [[ -r $TOMBKEYFILE && $(file $TOMBKEYFILE) =~ "JP.G" ]]; then

        exhume_key $TOMBKEYFILE "$_password"

    fi

    gpg_decrypt "$_password" # Save decrypted contents into $TOMBSECRET

    ret="$?"

    _verbose "get_lukskey returns ::1::" $ret
    return $ret
}

# This function asks the user for the password to use the key it tests
# it against the return code of gpg on success returns 0 and saves
# the password in the global variable $TOMBPASSWORD
ask_key_password() {
    [[ -z "$TOMBKEYFILE" ]] && {
        _failure "Internal error: ask_key_password() called before _load_key()." }

    [[ "$TOMBKEYFILE" = "cleartext" ]] && {
        _verbose "no password needed, using secret bytes from stdin"
        return 0 }

    _message "A password is required to use key ::1 key::" $TOMBKEYFILE
    passok=0
    tombpass=""
    if [[ "$1" = "" ]]; then

        for c in 1 2 3; do
            if [[ $c == 1 ]]; then
                tombpass=$(ask_password "Insert password to: $TOMBKEYFILE")
            else
                tombpass=$(ask_password "Insert password to: $TOMBKEYFILE (attempt $c)")
            fi
            [[ $? = 0 ]] || {
                _warning "User aborted password dialog."
                return 1
            }

            get_lukskey "$tombpass"

            [[ $? = 0 ]] && {
                passok=1; _message "Password OK."
                break;
            }
        done

    else
        # if a second argument is present then the password is already known
        tombpass="$1"
        _verbose "ask_key_password with tombpass: ::1 tomb pass::" $tombpass

        get_lukskey "$tombpass"

        [[ $? = 0 ]] && {
            passok=1; _message "Password OK."
        }

    fi
    [[ $passok == 1 ]] || return 1

    TOMBPASSWORD=$tombpass
    return 0
}

# call cryptsetup with arguments using the currently known secret
# echo flags eliminate newline and disable escape (BSD_ECHO)
_cryptsetup() {
    print -R -n - "$TOMBSECRET" | _sudo cryptsetup --key-file - ${=@}
    return $?
}

# change tomb key password
change_passwd() {
    local tmpnewkey lukskey c tombpass tombpasstmp

    _check_swap  # Ensure swap is secure, if any
    _load_key    # Try loading key from option -k and set TOMBKEYFILE

    _message "Commanded to change password for tomb key ::1 key::" $TOMBKEYFILE

    _tmp_create
    tmpnewkey=$TOMBTMP

    if option_is_set --tomb-old-pwd; then
        local tomboldpwd="`option_value --tomb-old-pwd`"
        _verbose "tomb-old-pwd = ::1 old pass::" $tomboldpwd
        ask_key_password "$tomboldpwd"
    else
        ask_key_password
    fi
    [[ $? == 0 ]] || _failure "No valid password supplied."

    _success "Changing password for ::1 key file::" $TOMBKEYFILE

    # Here $TOMBSECRET contains the key material in clear

    { option_is_set --tomb-pwd } && {
        local tombpwd="`option_value --tomb-pwd`"
        _verbose "tomb-pwd = ::1 new pass::" $tombpwd
        gen_key "$tombpwd" >> "$tmpnewkey"
    } || {
        gen_key >> "$tmpnewkey"
    }

    { is_valid_key "${mapfile[$tmpnewkey]}" } || {
        _failure "Error: the newly generated keyfile does not seem valid." }

    # Copy the new key as the original keyfile name
    cp -f "${tmpnewkey}" $TOMBKEYFILE
    _success "Your passphrase was successfully updated."

    return 0
}


# takes care to encrypt a key
# honored options: --kdf  --tomb-pwd -o
gen_key() {
    # $1 the password to use, if not set then ask user
    # -o is the --cipher-algo to use (string taken by GnuPG)
    local algopt="`option_value -o`"
    local algo="${algopt:-AES256}"
    # here user is prompted for key password
    tombpass=""
    tombpasstmp=""

    if [ "$1" = "" ]; then
        while true; do
            # 3 tries to write two times a matching password
            tombpass=`ask_password "Type the new password to secure your key"`
            if [[ $? != 0 ]]; then
                _failure "User aborted."
            fi
            if [ -z $tombpass ]; then
                _failure "You set empty password, which is not possible."
            fi
            tombpasstmp=$tombpass
            tombpass=`ask_password "Type the new password to secure your key (again)"`
            if [[ $? != 0 ]]; then
                _failure "User aborted."
            fi
            if [ "$tombpasstmp" = "$tombpass" ]; then
                break;
            fi
            unset tombpasstmp
            unset tombpass
        done
    else
        tombpass="$1"
        _verbose "gen_key takes tombpass from CLI argument: ::1 tomb pass::" $tombpass
    fi

    header=""
    [[ $KDF == 1 ]] && {
        { option_is_set --kdf } && {
            # KDF is a new key strenghtening technique against brute forcing
            # see: https://github.com/dyne/Tomb/issues/82
            itertime="`option_value --kdf`"
            # removing support of floating points because they can't be type checked well
            if [[ "$itertime" != <-> ]]; then
                unset tombpass
                unset tombpasstmp
                _failure "Wrong argument for --kdf: must be an integer number (iteration seconds)."
            fi
            # --kdf takes one parameter: iter time (on present machine) in seconds
            local -i microseconds
            microseconds=$(( itertime * 1000000 ))
            _success "Using KDF, iteration time: ::1 microseconds::" $microseconds
            _message "generating salt"
            pbkdf2_salt=`tomb-kdb-pbkdf2-gensalt`
            _message "calculating iterations"
            pbkdf2_iter=`tomb-kdb-pbkdf2-getiter $microseconds`
            _message "encoding the password"
            # We use a length of 64bytes = 512bits (more than needed!?)
            tombpass=`tomb-kdb-pbkdf2 $pbkdf2_salt $pbkdf2_iter 64 <<<"${tombpass}"`

            header="_KDF_pbkdf2sha1_${pbkdf2_salt}_${pbkdf2_iter}_64\n"
        }
    }


    print $header

    # TODO: check result of gpg operation
    cat <<EOF | gpg --openpgp --force-mdc --cipher-algo ${algo} \
        --batch --no-options --no-tty --passphrase-fd 0 --status-fd 2 \
        -o - -c -a
${tombpass}
$TOMBSECRET
EOF
    # print -n "${tombpass}" \
    #     | gpg --openpgp --force-mdc --cipher-algo ${algo} \
    #     --batch --no-options --no-tty --passphrase-fd 0 --status-fd 2 \
    #     -o - -c -a ${lukskey}

    TOMBPASSWORD="$tombpass"    # Set global variable
    unset tombpass
    unset tombpasstmp
}

# prints an array of ciphers available in gnupg (to encrypt keys)
list_gnupg_ciphers() {
    # prints an error if GnuPG is not found
    which gpg 2>/dev/null || _failure "gpg (GnuPG) is not found, Tomb cannot function without it."

    ciphers=(`gpg --version | awk '
BEGIN { ciphers=0 }
/^Cipher:/ { gsub(/,/,""); sub(/^Cipher:/,""); print; ciphers=1; next }
/^Hash:/ { ciphers=0 }
{ if(ciphers==0) { next } else { gsub(/,/,""); print; } }
'`)
    print " ${ciphers}"
    return 1
}

# Steganographic function to bury a key inside an image.
# Requires steghide(1) to be installed
bury_key() {

    _load_key    # Try loading key from option -k and set TOMBKEY

    imagefile=$PARAM

    [[ "`file $imagefile`" =~ "JPEG" ]] || {
        _warning "Encode failed: ::1 image file:: is not a jpeg image." $imagefile
        return 1
    }

    _success "Encoding key ::1 tomb key:: inside image ::2 image file::" $TOMBKEY $imagefile
    _message "Please confirm the key password for the encoding"
    # We ask the password and test if it is the same encoding the
    # base key, to insure that the same password is used for the
    # encryption and the steganography. This is a standard enforced
    # by Tomb, but its not strictly necessary (and having different
    # password would enhance security). Nevertheless here we prefer
    # usability.

    { option_is_set --tomb-pwd } && {
        local tombpwd="`option_value --tomb-pwd`"
        _verbose "tomb-pwd = ::1 tomb pass::" $tombpwd
        ask_key_password "$tombpwd"
    } || {
        ask_key_password
    }
    [[ $? != 0 ]] && {
        _warning "Wrong password supplied."
        _failure "You shall not bury a key whose password is unknown to you." }

    # We omit armor strings since having them as constants can give
    # ground to effective attacks on steganography
    print - "$TOMBKEY" | awk '
/^-----/ {next}
/^Version/ {next}
{print $0}' \
    | steghide embed --embedfile - --coverfile ${imagefile} \
    -p $TOMBPASSWORD -z 9 -e serpent cbc
    if [ $? != 0 ]; then
        _warning "Encoding error: steghide reports problems."
        res=1
    else
        _success "Tomb key encoded succesfully into image ::1 image file::" $imagefile
        res=0
    fi

    return $res
}

# mandatory 1st arg: the image file where key is supposed to be
# optional 2nd arg: the password to use (same as key, internal use)
# optional 3rd arg: the key where to save the result (- for stdout)
exhume_key() {
    [[ "$1" = "" ]] && {
        _failure "Exhume failed, no image specified" }

    local imagefile="$1"  # The image file where to look for the key
    local tombpass="$2"   # (Optional) the password to use (internal use)
    local destkey="$3"    # (Optional) the key file where to save the
    # result (- for stdout)
    local r=1             # Return code (default: fail)

    # Ensure the image file is a readable JPEG
    [[ ! -r $imagefile ]] && {
        _failure "Exhume failed, image file not found: ::1 image file::" "${imagefile:-none}" }
    [[ ! $(file "$imagefile") =~ "JP.G" ]] && {
        _failure "Exhume failed: ::1 image file:: is not a jpeg image." $imagefile }

    # When a password is passed as argument then always print out
    # the exhumed key on stdout without further checks (internal use)
    [[ -n "$tombpass" ]] && {
        TOMBKEY=$(steghide extract -sf $imagefile -p $tombpass -xf -)
        [[ $? != 0 ]] && {
            _failure "Wrong password or no steganographic key found" }

        recover_key $TOMBKEY

        return 0
    }

    # Ensure we have a valid destination for the key
    [[ -z $destkey ]] && { option_is_set -k } && destkey=$(option_value -k)
    [[ -z $destkey ]] && {
        destkey="-" # No key was specified: fallback to stdout
        _message "printing exhumed key on stdout" }

    # Bail out if destination exists, unless -f (force) was passed
    [[ $destkey != "-" && -s $destkey ]] && {
        _warning "File exists: ::1 tomb key::" $destkey
        { option_is_set -f } && {
            _warning "Use of --force selected: overwriting."
            rm -f $destkey
        } || {
            _warning "Make explicit use of --force to overwrite."
            _failure "Refusing to overwrite file. Operation aborted." }
    }

    _message "Trying to exhume a key out of image ::1 image file::" $imagefile
    { option_is_set --tomb-pwd } && {
        tombpass=$(option_value --tomb-pwd)
        _verbose "tomb-pwd = ::1 tomb pass::" $tombpass
    } || {
        [[ -n $TOMBPASSWORD ]] && tombpass=$TOMBPASSWORD
    } || {
        tombpass=$(ask_password "Insert password to exhume key from $imagefile")
        [[ $? != 0 ]] && {
            _warning "User aborted password dialog."
            return 1
        }
    }

    # Extract the key from the image
    steghide extract -sf $imagefile -p ${tombpass} -xf $destkey
    r=$?

    # Report to the user
    [[ "$destkey" = "-" ]] && destkey="stdout"
    [[ $r == 0 ]] && {
        _success "Key succesfully exhumed to ::1 key::." $destkey
    } || {
        _warning "Nothing found in ::1 image file::" $imagefile
    }

    return $r
}

# Produces a printable image of the key contents so that it can be
# backuped on paper and hidden in books etc.
engrave_key() {

    _load_key    # Try loading key from option -k and set TOMBKEYFILE

    local keyname=$(basename $TOMBKEYFILE)
    local pngname="$keyname.qr.png"

    _success "Rendering a printable QRCode for key: ::1 tomb key file::" $TOMBKEYFILE
    # we omit armor strings to save space
    awk '/^-----/ {next}; /^Version/ {next}; {print $0}' $TOMBKEYFILE \
        | qrencode --size 4 --level H --casesensitive -o $pngname
    [[ $? != 0 ]] && {
        _failure "QREncode reported an error." }

    _success "Operation successful:"
    # TODO: only if verbose and/or not silent
    ls -lh $pngname
    file $pngname
}

# }}} - Key handling

# {{{ Create

# Since version 1.5.3, tomb creation is a three-step process that replaces create_tomb():
#
# * dig a .tomb (the large file) using /dev/urandom (takes some minutes at least)
#
# * forge a .key (the small file) using /dev/random (good entropy needed)
#
# * lock the .tomb file with the key, binding the key to the tomb (requires dm_crypt format)

# Step one - Dig a tomb
#
# Synopsis: dig_tomb /path/to/tomb -s sizemegabytes
#
# It will create an empty file to be formatted as a loopback
# filesystem.  Initially the file is filled with random data taken
# from /dev/urandom to improve overall tomb's security and prevent
# some attacks aiming at detecting how much data is in the tomb, or
# which blocks in the filesystem contain that data.

dig_tomb() {
    local    tombpath="$1"    # Path to tomb
    # Require the specification of the size of the tomb (-s) in MB
    local -i tombsize=$(option_value -s)

    _message "Commanded to dig tomb ::1 tomb path::" $tombpath

    [[ -n "$tombpath"   ]] || _failure "Missing path to tomb"
    [[ -n "$tombsize"   ]] || _failure "Size argument missing, use -s"
    [[ $tombsize == <-> ]] || _failure "Size must be an integer (megabytes)"
    [[ $tombsize -ge 10 ]] || _failure "Tombs can't be smaller than 10 megabytes"

    _plot $tombpath          # Set TOMB{PATH,DIR,FILE,NAME}

    [[ -e $TOMBPATH ]] && {
        _warning "A tomb exists already. I'm not digging here:"
        ls -lh $TOMBPATH
        return 1
    }

    _success "Creating a new tomb in ::1 tomb path::" $TOMBPATH

    _message "Generating ::1 tomb file:: of ::2 size::MiB" $TOMBFILE $tombsize

    # Ensure that file permissions are safe even if interrupted
    touch $TOMBPATH
    [[ $? = 0 ]] || {
        _warning "Error creating the tomb ::1 tomb path::" $TOMBPATH
        _failure "Operation aborted."
    }
    chmod 0600 $TOMBPATH

    _verbose "Data dump using ::1:: from /dev/urandom" ${DD[1]}
    ${=DD} if=/dev/urandom bs=1048576 count=$tombsize of=$TOMBPATH

    [[ $? == 0 && -e $TOMBPATH ]] && {
        ls -lh $TOMBPATH
    } || {
        _warning "Error creating the tomb ::1 tomb path::" $TOMBPATH
        _failure "Operation aborted."
    }

    _success "Done digging ::1 tomb name::" $TOMBNAME
    _message "Your tomb is not yet ready, you need to forge a key and lock it:"
    _message "tomb forge ::1 tomb path::.key" $TOMBPATH
    _message "tomb lock ::1 tomb path:: -k ::1 tomb path::.key" $TOMBPATH

    return 0
}

# Step two -- Create a detached key to lock a tomb with
#
# Synopsis: forge_key [destkey|-k destkey] [-o cipher]
#
# Arguments:
# -k                path to destination keyfile
# -o                Use an alternate algorithm
#
forge_key() {
    # can be specified both as simple argument or using -k
    local destkey="$1"
    { option_is_set -k } && { destkey=$(option_value -k) }

    local algo="AES256"  # Default encryption algorithm

    [[ -z "$destkey" ]] && {
        _failure "A filename needs to be specified using -k to forge a new key." }

    _message "Commanded to forge key ::1 key::" $destkey

    _check_swap # Ensure the available memory is safe to use

    # Ensure GnuPG won't exit with an error before first run
    [[ -r $HOME/.gnupg/pubring.gpg ]] || {
        mkdir -m 0700 $HOME/.gnupg
        touch $HOME/.gnupg/pubring.gpg }

    # Do not overwrite any files accidentally
    [[ -r "$destkey" ]] && {
        ls -lh $destkey
        _failure "Forging this key would overwrite an existing file. Operation aborted." }

    touch $destkey
    [[ $? == 0 ]] || {
        _warning "Cannot generate encryption key."
        _failure "Operation aborted." }
    chmod 0600 $destkey

    # Update algorithm if it was passed on the command line with -o
    { option_is_set -o } && algopt="$(option_value -o)"
    [[ -n "$algopt" ]] && algo=$algopt

    _message "Commanded to forge key ::1 key:: with cipher algorithm ::2 algorithm::" \
        $destkey $algo

    TOMBKEYFILE="$destkey"    # Set global variable

    _message "This operation takes time, keep using this computer on other tasks,"
    _message "once done you will be asked to choose a password for your tomb."
    _message "To make it faster you can move the mouse around."
    _message "If you are on a server, you can use an Entropy Generation Daemon."

    # Use /dev/random as the entropy source, unless --use-urandom is specified
    local random_source=/dev/random
    { option_is_set --use-urandom } && random_source=/dev/urandom

    _verbose "Data dump using ::1:: from ::2 source::" ${DD[1]} $random_source
    TOMBSECRET=$(${=DD} bs=1 count=256 if=$random_source)
    [[ $? == 0 ]] || {
        _warning "Cannot generate encryption key."
        _failure "Operation aborted." }

    # Here the global variable TOMBSECRET contains the naked secret

    _success "Choose the  password of your key: ::1 tomb key::" $TOMBKEYFILE
    _message "(You can also change it later using 'tomb passwd'.)"
    # _user_file $TOMBKEYFILE

    tombname="$TOMBKEYFILE" # XXX ???
    # the gen_key() function takes care of the new key's encryption
    { option_is_set --tomb-pwd } && {
        local tombpwd="`option_value --tomb-pwd`"
        _verbose "tomb-pwd = ::1 new pass::" $tombpwd
        gen_key "$tombpwd" >> $TOMBKEYFILE
    } || {
        gen_key >> $TOMBKEYFILE
    }

    # load the key contents (set global variable)
    TOMBKEY="${mapfile[$TOMBKEYFILE]}"

    # this does a check on the file header
    is_valid_key $TOMBKEY || {
        _warning "The key does not seem to be valid."
        _warning "Dumping contents to screen:"
        print "${mapfile[$TOMBKEY]}"
        _warning "--"
        _sudo umount ${keytmp}
        rm -r $keytmp
        _failure "Operation aborted."
    }

    _message "Done forging ::1 key file::" $TOMBKEYFILE
    _success "Your key is ready:"
    ls -lh $TOMBKEYFILE
}

# Step three -- Lock tomb
#
# Synopsis: tomb_lock file.tomb file.tomb.key [-o cipher]
#
# Lock the given tomb with the given key file, in fact formatting the
# loopback volume as a LUKS device.
# Default cipher 'aes-xts-plain64:sha256'can be overridden with -o
lock_tomb_with_key() {
    # old default was aes-cbc-essiv:sha256
    # Override with -o
    # for more alternatives refer to cryptsetup(8)
    local cipher="aes-xts-plain64:sha256"

    local tombpath="$1"      # First argument is the path to the tomb

    [[ -n $tombpath ]] || {
        _warning "No tomb specified for locking."
        _warning "Usage: tomb lock file.tomb file.tomb.key"
        return 1
    }

    _plot $tombpath

    _message "Commanded to lock tomb ::1 tomb file::" $TOMBFILE

    [[ -f $TOMBPATH ]] || {
        _failure "There is no tomb here. You have to dig it first." }

    _verbose "Tomb found: ::1 tomb path::" $TOMBPATH

    lo_mount $TOMBPATH
    nstloop=`lo_new`

    _verbose "Loop mounted on ::1 mount point::" $nstloop

    _message "Checking if the tomb is empty (we never step on somebody else's bones)."
    _sudo cryptsetup isLuks ${nstloop}
    if [ $? = 0 ]; then
        # is it a LUKS encrypted nest? then bail out and avoid reformatting it
        _warning "The tomb was already locked with another key."
        _failure "Operation aborted. I cannot lock an already locked tomb. Go dig a new one."
    else
        _message "Fine, this tomb seems empty."
    fi

    _load_key    # Try loading key from option -k and set TOMBKEYFILE

    # the encryption cipher for a tomb can be set when locking using -c
    { option_is_set -o } && algopt="$(option_value -o)"
    [[ -n "$algopt" ]] && cipher=$algopt
    _message "Locking using cipher: ::1 cipher::" $cipher

    # get the pass from the user and check it
    if option_is_set --tomb-pwd; then
        tomb_pwd="`option_value --tomb-pwd`"
        _verbose "tomb-pwd = ::1 tomb pass::" $tomb_pwd
        ask_key_password "$tomb_pwd"
    else
        ask_key_password
    fi
    [[ $? == 0 ]] || _failure "No valid password supplied."

    _success "Locking ::1 tomb file:: with ::2 tomb key file::" $TOMBFILE $TOMBKEYFILE

    _message "Formatting Luks mapped device."
    _cryptsetup --batch-mode \
        --cipher ${cipher} --key-size 256 --key-slot 0 \
        luksFormat ${nstloop}
    [[ $? == 0 ]] || {
        _warning "cryptsetup luksFormat returned an error."
        _failure "Operation aborted." }

    _cryptsetup --cipher ${cipher} luksOpen ${nstloop} tomb.tmp
    [[ $? == 0 ]] || {
        _warning "cryptsetup luksOpen returned an error."
        _failure "Operation aborted." }

    _message "Formatting your Tomb with Ext3/Ext4 filesystem."
    _sudo mkfs.ext4 -q -F -j -L $TOMBNAME /dev/mapper/tomb.tmp

    [[ $? == 0 ]] || {
        _warning "Tomb format returned an error."
        _warning "Your tomb ::1 tomb file:: may be corrupted." $TOMBFILE }

    # Sync
    _sudo cryptsetup luksClose tomb.tmp

    _message "Done locking ::1 tomb name:: using Luks dm-crypt ::2 cipher::" $TOMBNAME $cipher
    _success "Your tomb is ready in ::1 tomb path:: and secured with key ::2 tomb key::" \
        $TOMBPATH $TOMBKEYFILE

}

# This function changes the key that locks a tomb
change_tomb_key() {
    local tombkey="$1"      # Path to the tomb's key file
    local tombpath="$2"     # Path to the tomb

    _message "Commanded to reset key for tomb ::1 tomb path::" $tombpath

    [[ -z "$tombpath" ]] && {
        _warning "Command 'setkey' needs two arguments: the old key file and the tomb."
        _warning "I.e:  tomb -k new.tomb.key old.tomb.key secret.tomb"
        _failure "Execution aborted."
    }

    _check_swap

    # this also calls _plot()
    is_valid_tomb $tombpath

    lo_mount $TOMBPATH
    nstloop=`lo_new`
    _sudo cryptsetup isLuks ${nstloop}
    # is it a LUKS encrypted nest? we check one more time
    [[ $? == 0 ]] || {
        _failure "Not a valid LUKS encrypted volume: ::1 volume::" $TOMBPATH }

    _load_key $tombkey    # Try loading given key and set TOMBKEY and
    # TOMBKEYFILE
    local oldkey=$TOMBKEY
    local oldkeyfile=$TOMBKEYFILE

    # we have everything, prepare to mount
    _success "Changing lock on tomb ::1 tomb name::" $TOMBNAME
    _message "Old key: ::1 old key::" $oldkeyfile

    # render the mapper
    mapdate=`date +%s`
    # save date of mount in minutes since 1970
    mapper="tomb.$TOMBNAME.$mapdate.$(basename $nstloop)"

    # load the old key
    if option_is_set --tomb-old-pwd; then
        tomb_old_pwd="`option_value --tomb-old-pwd`"
        _verbose "tomb-old-pwd = ::1 old pass::" $tomb_old_pwd
        ask_key_password "$tomb_old_pwd"
    else
        ask_key_password
    fi
    [[ $? == 0 ]] || {
        _failure "No valid password supplied for the old key." }
    old_secret=$TOMBSECRET

    # luksOpen the tomb (not really mounting, just on the loopback)
    print -R -n - "$old_secret" | _sudo cryptsetup --key-file - \
        luksOpen ${nstloop} ${mapper}
    [[ $? == 0 ]] || _failure "Unexpected error in luksOpen."

    _load_key # Try loading new key from option -k and set TOMBKEYFILE

    _message "New key: ::1 key file::" $TOMBKEYFILE

    if option_is_set --tomb-pwd; then
        tomb_new_pwd="`option_value --tomb-pwd`"
        _verbose "tomb-pwd = ::1 tomb pass::" $tomb_new_pwd
        ask_key_password "$tomb_new_pwd"
    else
        ask_key_password
    fi
    [[ $? == 0 ]] || {
        _failure "No valid password supplied for the new key." }

    _tmp_create
    tmpnewkey=$TOMBTMP
    print -R -n - "$TOMBSECRET" >> $tmpnewkey

    print -R -n - "$old_secret" | _sudo cryptsetup --key-file - \
        luksChangeKey "$nstloop" "$tmpnewkey"

    [[ $? == 0 ]] || _failure "Unexpected error in luksChangeKey."

    _sudo cryptsetup luksClose "${mapper}" || _failure "Unexpected error in luksClose."

    _success "Succesfully changed key for tomb: ::1 tomb file::" $TOMBFILE
    _message "The new key is: ::1 new key::" $TOMBKEYFILE

    return 0
}

# }}} - Creation

# {{{ Open

# $1 = tombfile $2(optional) = mountpoint
mount_tomb() {
    local tombpath="$1"    # First argument is the path to the tomb
    [[ -n "$tombpath" ]] || _failure "No tomb name specified for opening."

    _message "Commanded to open tomb ::1 tomb name::" $tombpath

    _check_swap

    # this also calls _plot()
    is_valid_tomb $tombpath

    _load_key # Try loading new key from option -k and set TOMBKEYFILE

    tombmount="$2"
    [[ "$tombmount" = "" ]] && {
        tombmount=/media/$TOMBNAME
        [[ -d /media ]] || { # no /media found, adopting /run/media/$USER (udisk2 compat)
            tombmount=/run/media/$_USER/$TOMBNAME
        }
        _message "Mountpoint not specified, using default: ::1 mount point::" $tombmount
    }

    _success "Opening ::1 tomb file:: on ::2 mount point::" $TOMBNAME $tombmount

    lo_mount $TOMBPATH
    nstloop=`lo_new`

    _sudo cryptsetup isLuks ${nstloop} || {
        # is it a LUKS encrypted nest? see cryptsetup(1)
        _failure "::1 tomb file:: is not a valid Luks encrypted storage file." $TOMBFILE }

    _message "This tomb is a valid LUKS encrypted device."

    luksdump="`_sudo cryptsetup luksDump ${nstloop}`"
    tombdump=(`print $luksdump | awk '
        /^Cipher name/ {print $3}
        /^Cipher mode/ {print $3}
        /^Hash spec/   {print $3}'`)
    _message "Cipher is \"::1 cipher::\" mode \"::2 mode::\" hash \"::3 hash::\"" $tombdump[1] $tombdump[2] $tombdump[3]

    slotwarn=`print $luksdump | awk '
        BEGIN { zero=0 }
        /^Key slot 0/ { zero=1 }
        /^Key slot.*ENABLED/ { if(zero==1) print "WARN" }'`
    [[ "$slotwarn" == "WARN" ]] && {
        _warning "Multiple key slots are enabled on this tomb. Beware: there can be a backdoor." }

    # save date of mount in minutes since 1970
    mapdate=`date +%s`

    mapper="tomb.$TOMBNAME.$mapdate.$(basename $nstloop)"

    _verbose "dev mapper device: ::1 mapper::" $mapper
    _verbose "Tomb key: ::1 key file::" $TOMBKEYFILE

    # take the name only, strip extensions
    _verbose "Tomb name: ::1 tomb name:: (to be engraved)" $TOMBNAME

    { option_is_set --tomb-pwd } && {
        tomb_pwd="`option_value --tomb-pwd`"
        _verbose "tomb-pwd = ::1 tomb pass::" $tomb_pwd
        ask_key_password "$tomb_pwd"
    } || {
        ask_key_password
    }
    [[ $? == 0 ]] || _failure "No valid password supplied."

    _cryptsetup luksOpen ${nstloop} ${mapper}
    [[ $? = 0 ]] || {
        _failure "Failure mounting the encrypted file." }

    # preserve the loopdev after exit
    lo_preserve "$nstloop"

    # array: [ cipher, keysize, loopdevice ]
    tombstat=(`_sudo cryptsetup status ${mapper} | awk '
    /cipher:/  {print $2}
    /keysize:/ {print $2}
    /device:/  {print $2}'`)
    _success "Success unlocking tomb ::1 tomb name::" $TOMBNAME
    _verbose "Key size is ::1 size:: for cipher ::2 cipher::" $tombstat[2] $tombstat[1]

    _message "Checking filesystem via ::1::" $tombstat[3]
    _sudo fsck -p -C0 /dev/mapper/${mapper}
    _verbose "Tomb engraved as ::1 tomb name::" $TOMBNAME
    _sudo tune2fs -L $TOMBNAME /dev/mapper/${mapper} > /dev/null

    # we need root from here on
    _sudo mkdir -p $tombmount

    # Default mount options are overridden with the -o switch
    { option_is_set -o } && {
        local oldmountopts=$MOUNTOPTS
        MOUNTOPTS="$(option_value -o)" }

    # TODO: safety check MOUNTOPTS
    # safe_mount_options && \
    _sudo mount -o $MOUNTOPTS /dev/mapper/${mapper} ${tombmount}
    # Clean up if the mount failed
    [[ $? == 0 ]] || {
        _warning "Error mounting ::1 mapper:: on ::2 tombmount::" $mapper $tombmount
        [[ $oldmountopts != $MOUNTOPTS ]] && \
          _warning "Are mount options '::1 mount options::' valid?" $MOUNTOPTS
        # TODO: move cleanup to _endgame()
        [[ -d $tombmount ]] && _sudo rmdir $tombmount
        [[ -e /dev/mapper/$mapper ]] && _sudo cryptsetup luksClose $mapper
        # The loop is taken care of in _endgame()
        _failure "Cannot mount ::1 tomb name::" $TOMBNAME
    }

    _sudo chown $UID:$GID ${tombmount}
    _sudo chmod 0711 ${tombmount}

    _success "Success opening ::1 tomb file:: on ::2 mount point::" $TOMBFILE $tombmount

    local tombtty tombhost tombuid tombuser

    # print out when was opened the last time, by whom and where
    [[ -r ${tombmount}/.last ]] && {
        tombtty=$(_cat ${tombmount}/.tty)
        tombhost=$(_cat ${tombmount}/.host)
        tomblast=$(_cat ${tombmount}/.last)
        tombuid=$(_cat ${tombmount}/.uid | tr -d ' ')
        for e in ${(f@)mapfile[/etc/passwd]}; do
            [[ "$e" =~ ":$tombuid:" ]] && {
                tombuser="${e[(ws@:@)1]}" }
        done
        _message "Last visit by ::1 user::(::2 tomb build::) from ::3 tty:: on ::4 host::" $tombuser $tombuid $tombtty $tombhost
        _message "on date ::1 date::" "`date --date=@${tomblast} +%c`"
    }
    # write down the UID and TTY that opened the tomb
    rm -f ${tombmount}/.uid
    print $_UID > ${tombmount}/.uid
    rm -f ${tombmount}/.tty
    print $_TTY > ${tombmount}/.tty
    # also the hostname
    rm -f ${tombmount}/.host
    hostname > ${tombmount}/.host
    # and the "last time opened" information
    # in minutes since 1970, this is printed at next open
    rm -f ${tombmount}/.last
    date +%s > ${tombmount}/.last
    # human readable: date --date=@"`cat .last`" +%c


    # process bind-hooks (mount -o bind of directories)
    # and post-hooks (execute on open)
    { option_is_set -n } || {
        exec_safe_bind_hooks ${tombmount}
        exec_safe_post_hooks ${tombmount} open }

    return 0
}

## HOOKS EXECUTION
#
# Execution of code inside a tomb may present a security risk, e.g.,
# if the tomb is shared or compromised, an attacker could embed
# malicious code.  When in doubt, open the tomb with the -n switch in
# order to skip this feature and verify the files mount-hooks and
# bind-hooks inside the tomb yourself before letting them run.

# Mount files and directories from the tomb to the current user's HOME.
#
# Synopsis: exec_safe_bind_hooks /path/to/mounted/tomb
#
# This can be a security risk if you share tombs with untrusted people.
# In that case, use the -n switch to turn off this feature.
exec_safe_bind_hooks() {
    local mnt="$1"   # First argument is the mount point of the tomb

    # Default mount options are overridden with the -o switch
    [[ -n ${(k)OPTS[-o]} ]] && MOUNTOPTS=${OPTS[-o]}

    # No HOME set? Note: this should never happen again.
    [[ -z $HOME ]] && {
        _warning "How pitiful!  A tomb, and no HOME."
        return 1 }

    [[ -z $mnt || ! -d $mnt ]] && {
        _warning "Cannot exec bind hooks without a mounted tomb."
        return 1 }

    [[ -r "$mnt/bind-hooks" ]] || {
        _verbose "bind-hooks not found in ::1 mount point::" $mnt
        return 1 }

    typeset -Al maps        # Maps of files and directories to mount
    typeset -al mounted     # Track already mounted files and directories

    # better parsing for bind hooks checks for two separated words on
    # each line, using zsh word separator array subscript
    _bindhooks="${mapfile[${mnt}/bind-hooks]}"
    for h in ${(f)_bindhooks}; do
        s="${h[(w)1]}"
        d="${h[(w)2]}"
        [[ "$s" = "" ]] && { _warning "bind-hooks file is broken"; return 1 }
        [[ "$d" = "" ]] && { _warning "bind-hooks file is broken"; return 1 }
        maps+=($s $d)
        _verbose "bind-hook found: $s -> $d"
    done
    unset _bindhooks

    for dir in ${(k)maps}; do
        [[ "${dir[1]}" == "/" || "${dir[1,2]}" == ".." ]] && {
            _warning "bind-hooks map format: local/to/tomb local/to/\$HOME"
            continue }

        [[ "${${maps[$dir]}[1]}" == "/" || "${${maps[$dir]}[1,2]}" == ".." ]] && {
            _warning "bind-hooks map format: local/to/tomb local/to/\$HOME.  Rolling back"
            for dir in ${mounted}; do _sudo umount $dir; done
            return 1 }

        if [[ ! -r "$HOME/${maps[$dir]}" ]]; then
            _warning "bind-hook target not existent, skipping ::1 home::/::2 subdir::" $HOME ${maps[$dir]}
        elif [[ ! -r "$mnt/$dir" ]]; then
            _warning "bind-hook source not found in tomb, skipping ::1 mount point::/::2 subdir::" $mnt $dir
        else
            _sudo mount -o bind,$MOUNTOPTS $mnt/$dir $HOME/${maps[$dir]} \
                && mounted+=("$HOME/${maps[$dir]}")
        fi
    done
}

# Execute automated actions configured in the tomb.
#
# Synopsis: exec_safe_post_hooks /path/to/mounted/tomb [open|close]
#
# If an executable file named 'post-hooks' is found inside the tomb,
# run it as a user.  This might need a dialog for security on what is
# being run, however we expect you know well what is inside your tomb.
# If you're mounting an untrusted tomb, be safe and use the -n switch
# to verify what it would run if you let it.  This feature opens the
# possibility to make encrypted executables.
exec_safe_post_hooks() {
    local mnt=$1     # First argument is where the tomb is mounted
    local act=$2     # Either 'open' or 'close'

    # Only run if post-hooks has the executable bit set
    [[ -x $mnt/post-hooks ]] || return

    # If the file starts with a shebang, run it.
    cat $mnt/post-hooks | head -n1 | grep '^#!\s*/' &> /dev/null
    [[ $? == 0 ]] && {
        _success "Post hooks found, executing as user ::1 user name::." $USERNAME
        $mnt/post-hooks $act $mnt
    }
}

# }}} - Tomb open

# {{{ List

# list all tombs mounted in a readable format
# $1 is optional, to specify a tomb
list_tombs() {

    local tombname tombmount tombfs tombfsopts tombloop
    local ts tombtot tombused tombavail tombpercent tombp tombsince
    local tombtty tombhost tombuid tombuser
    # list all open tombs
    mounted_tombs=(`list_tomb_mounts $1`)
    [[ ${#mounted_tombs} == 0 ]] && {
        _failure "I can't see any ::1 status:: tomb, may they all rest in peace." ${1:-open} }

    for t in ${mounted_tombs}; do
        mapper=`basename ${t[(ws:;:)1]}`
        tombname=${t[(ws:;:)5]}
        tombmount=${t[(ws:;:)2]}
        tombfs=${t[(ws:;:)3]}
        tombfsopts=${t[(ws:;:)4]}
        tombloop=${mapper[(ws:.:)4]}

        # calculate tomb size
        ts=`df -hP /dev/mapper/$mapper |
awk "/mapper/"' { print $2 ";" $3 ";" $4 ";" $5 }'`
        tombtot=${ts[(ws:;:)1]}
        tombused=${ts[(ws:;:)2]}
        tombavail=${ts[(ws:;:)3]}
        tombpercent=${ts[(ws:;:)4]}
        tombp=${tombpercent%%%}
        tombsince=`date --date=@${mapper[(ws:.:)3]} +%c`

        # find out who opens it from where
        [[ -r ${tombmount}/.tty ]] && {
            tombtty=$(_cat ${tombmount}/.tty)
            tombhost=$(_cat ${tombmount}/.host)
            tombuid=$(_cat ${tombmount}/.uid | tr -d ' ')
            for ee in ${(f@)mapfile[/etc/passwd]}; do
                [[ "$ee" =~ ":${tombuid}:" ]] && {
                    tombuser="${ee[(ws@:@)1]}" }
            done
        }

        { option_is_set --get-mountpoint } && { print $tombmount; continue }

        _message "::1 tombname:: open on ::2 tombmount:: using ::3 tombfsopts::" \
            $tombname $tombmount $tombfsopts

        _verbose "::1 tombname:: /dev/::2 tombloop:: device mounted (detach with losetup -d)" $tombname $tombloop

        _message "::1 tombname:: open since ::2 tombsince::" $tombname $tombsince

        [[ -z "$tombtty" ]] || {
            _message "::1 tombname:: open by ::2 tombuser:: from ::3 tombtty:: on ::4 tombhost::" \
                $tombname $tombuser $tombtty $tombhost
        }

        _message "::1 tombname:: size ::2 tombtot:: of which ::3 tombused:: (::5 tombpercent::%) is used: ::4 tombavail:: free " \
            $tombname $tombtot $tombused $tombavail $tombpercent

        [[ ${tombp} -ge 90 ]] && {
            _warning "::1 tombname:: warning: your tomb is almost full!" $tombname
        }

        # Now check hooks
        mounted_hooks=(`list_tomb_binds $tombname`)
        for h in ${mounted_hooks}; do
            _message "::1 tombname:: hooks ::2 hookname:: on ::3 hookdest::" \
                $tombname "`basename ${h[(ws:;:)1]}`" ${h[(ws:;:)2]}
        done
    done
}


# Print out an array of mounted tombs (internal use)
# Format is semi-colon separated list of attributes
# if 1st arg is supplied, then list only that tomb
#
# String positions in the semicolon separated array:
#
# 1. full mapper path
#
# 2. mountpoint
#
# 3. filesystem type
#
# 4. mount options
#
# 5. tomb name
list_tomb_mounts() {
    [[ -z "$1" ]] && {
        # list all open tombs
        mount -l \
            | awk '
BEGIN { main="" }
/^\/dev\/mapper\/tomb/ {
  if(main==$1) next;
  print $1 ";" $3 ";" $5 ";" $6 ";" $7
  main=$1
}
'
    } || {
        # list a specific tomb
        mount -l \
            | awk -vtomb="[$1]" '
BEGIN { main="" }
/^\/dev\/mapper\/tomb/ {
  if($7!=tomb) next;
  if(main==$1) next;
  print $1 ";" $3 ";" $5 ";" $6 ";" $7
  main=$1
}
'
    }
}

# list_tomb_binds
# print out an array of mounted bind hooks (internal use)
# format is semi-colon separated list of attributes
# needs an argument: name of tomb whose hooks belong
list_tomb_binds() {
    [[ -z "$1" ]] && {
        _failure "Internal error: list_tomb_binds called without argument." }

    # list bind hooks on util-linux 2.20 (Debian 7)
    mount -l \
        | awk -vtomb="$1" '
BEGIN { main="" }
/^\/dev\/mapper\/tomb/ {
  if($7!=tomb) next;
  if(main=="") { main=$1; next; }
  if(main==$1)
    print $1 ";" $3 ";" $5 ";" $6 ";" $7
}
'

    # list bind hooks on util-linux 2.17 (Debian 6)
    tombmount=`mount -l \
      | awk -vtomb="$1" '
/^\/dev\/mapper\/tomb/ { if($7!=tomb) next; print $3; exit; }'`

    mount -l | grep "^$tombmount" \
        | awk -vtomb="$1" '
        /bind/ { print $1 ";" $3 ";" $5 ";" $6 ";" $7 }'
}

# }}} - Tomb list

# {{{ Index and search

# index files in all tombs for search
# $1 is optional, to specify a tomb
index_tombs() {
    { command -v updatedb 1>/dev/null 2>/dev/null } || {
        _failure "Cannot index tombs on this system: updatedb (mlocate) not installed." }

    updatedbver=`updatedb --version | grep '^updatedb'`
    [[ "$updatedbver" =~ "GNU findutils" ]] && {
        _warning "Cannot use GNU findutils for index/search commands." }
    [[ "$updatedbver" =~ "mlocate" ]] || {
        _failure "Index command needs 'mlocate' to be installed." }

    _verbose "$updatedbver"

    mounted_tombs=(`list_tomb_mounts $1`)
    [[ ${#mounted_tombs} == 0 ]] && {
        # Considering one tomb
        [[ -n "$1" ]] && {
            _failure "There seems to be no open tomb engraved as [::1::]" $1 }
        # Or more
        _failure "I can't see any open tomb, may they all rest in peace." }

    _success "Creating and updating search indexes."

    # start the LibreOffice document converter if installed
    { command -v unoconv 1>/dev/null 2>/dev/null } && {
        unoconv -l 2>/dev/null &
        _verbose "unoconv listener launched."
        sleep 1 }

    for t in ${mounted_tombs}; do
        mapper=`basename ${t[(ws:;:)1]}`
        tombname=${t[(ws:;:)5]}
        tombmount=${t[(ws:;:)2]}
        [[ -r ${tombmount}/.noindex ]] && {
            _message "Skipping ::1 tomb name:: (.noindex found)." $tombname
            continue }
        _message "Indexing ::1 tomb name:: filenames..." $tombname
        updatedb -l 0 -o ${tombmount}/.updatedb -U ${tombmount}

        # here we use swish to index file contents
        [[ $SWISH == 1 ]] && {
            _message "Indexing ::1 tomb name:: contents..." $tombname
            rm -f ${tombmount}/.swishrc
            _message "Generating a new swish-e configuration file: ::1 swish conf::" ${tombmount}/.swishrc
            cat <<EOF > ${tombmount}/.swishrc
# index directives
DefaultContents TXT*
IndexDir $tombmount
IndexFile $tombmount/.swish
# exclude images
FileRules filename regex /\.jp.?g/i
FileRules filename regex /\.png/i
FileRules filename regex /\.gif/i
FileRules filename regex /\.tiff/i
FileRules filename regex /\.svg/i
FileRules filename regex /\.xcf/i
FileRules filename regex /\.eps/i
FileRules filename regex /\.ttf/i
# exclude audio
FileRules filename regex /\.mp3/i
FileRules filename regex /\.ogg/i
FileRules filename regex /\.wav/i
FileRules filename regex /\.mod/i
FileRules filename regex /\.xm/i
# exclude video
FileRules filename regex /\.mp4/i
FileRules filename regex /\.avi/i
FileRules filename regex /\.ogv/i
FileRules filename regex /\.ogm/i
FileRules filename regex /\.mkv/i
FileRules filename regex /\.mov/i
FileRules filename regex /\.flv/i
FileRules filename regex /\.webm/i
# exclude system
FileRules filename is ok
FileRules filename is lock
FileRules filename is control
FileRules filename is status
FileRules filename is proc
FileRules filename is sys
FileRules filename is supervise
FileRules filename regex /\.asc$/i
FileRules filename regex /\.gpg$/i
# pdf and postscript
FileFilter .pdf pdftotext "'%p' -"
FileFilter .ps  ps2txt "'%p' -"
# compressed files
FileFilterMatch lesspipe "%p" /\.tgz$/i
FileFilterMatch lesspipe "%p" /\.zip$/i
FileFilterMatch lesspipe "%p" /\.gz$/i
FileFilterMatch lesspipe "%p" /\.bz2$/i
FileFilterMatch lesspipe "%p" /\.Z$/
# spreadsheets
FileFilterMatch unoconv "-d spreadsheet -f csv --stdout %P" /\.xls.*/i
FileFilterMatch unoconv "-d spreadsheet -f csv --stdout %P" /\.xlt.*/i
FileFilter .ods unoconv "-d spreadsheet -f csv --stdout %P"
FileFilter .ots unoconv "-d spreadsheet -f csv --stdout %P"
FileFilter .dbf unoconv "-d spreadsheet -f csv --stdout %P"
FileFilter .dif unoconv "-d spreadsheet -f csv --stdout %P"
FileFilter .uos unoconv "-d spreadsheet -f csv --stdout %P"
FileFilter .sxc unoconv "-d spreadsheet -f csv --stdout %P"
# word documents
FileFilterMatch unoconv "-d document -f txt --stdout %P" /\.doc.*/i
FileFilterMatch unoconv "-d document -f txt --stdout %P" /\.odt.*/i
FileFilterMatch unoconv "-d document -f txt --stdout %P" /\.rtf.*/i
FileFilterMatch unoconv "-d document -f txt --stdout %P" /\.tex$/i
# native html support
IndexContents HTML* .htm .html .shtml
IndexContents XML*  .xml
EOF

            swish-e -c ${tombmount}/.swishrc -S fs -v3
        }
        _message "Search index updated."
    done
}

search_tombs() {
    { command -v locate 1>/dev/null 2>/dev/null } || {
        _failure "Cannot index tombs on this system: updatedb (mlocate) not installed." }

    updatedbver=`updatedb --version | grep '^updatedb'`
    [[ "$updatedbver" =~ "GNU findutils" ]] && {
        _warning "Cannot use GNU findutils for index/search commands." }
    [[ "$updatedbver" =~ "mlocate" ]] || {
        _failure "Index command needs 'mlocate' to be installed." }

    _verbose "$updatedbver"

    # list all open tombs
    mounted_tombs=(`list_tomb_mounts`)
    [[ ${#mounted_tombs} == 0 ]] && {
        _failure "I can't see any open tomb, may they all rest in peace." }

    _success "Searching for: ::1::" ${(f)@}
    for t in ${mounted_tombs}; do
        _verbose "Checking for index: ::1::" ${t}
        mapper=`basename ${t[(ws:;:)1]}`
        tombname=${t[(ws:;:)5]}
        tombmount=${t[(ws:;:)2]}
        [[ -r ${tombmount}/.updatedb ]] && {
            # Use mlocate to search hits on filenames
            _message "Searching filenames in tomb ::1 tomb name::" $tombname
            locate -d ${tombmount}/.updatedb -e -i "${(f)@}"
            _message "Matches found: ::1 matches::" \
                $(locate -d ${tombmount}/.updatedb -e -i -c ${(f)@})

            # Use swish-e to search over contents
            [[ $SWISH == 1 && -r $tombmount/.swish ]] && {
                _message "Searching contents in tomb ::1 tomb name::" $tombname
                swish-e -w ${=@} -f $tombmount/.swish -H0 }
        } || {
            _warning "Skipping tomb ::1 tomb name::: not indexed." $tombname
            _warning "Run 'tomb index' to create indexes." }
    done
    _message "Search completed."
}

# }}} - Index and search

# {{{ Resize

# resize tomb file size
resize_tomb() {
    local tombpath="$1"    # First argument is the path to the tomb

    _message "Commanded to resize tomb ::1 tomb name:: to ::2 size:: megabytes." $1 $OPTS[-s]

    [[ -z "$tombpath" ]] && _failure "No tomb name specified for resizing."
    [[ ! -r $tombpath ]] && _failure "Cannot find ::1::" $tombpath

    newtombsize="`option_value -s`"
    [[ -z "$newtombsize" ]] && {
        _failure "Aborting operations: new size was not specified, use -s" }

    # this also calls _plot()
    is_valid_tomb $tombpath

    _load_key # Try loading new key from option -k and set TOMBKEYFILE

    local oldtombsize=$(( `stat -c %s "$TOMBPATH" 2>/dev/null` / 1048576 ))
    local mounted_tomb=`mount -l |
        awk -vtomb="[$TOMBNAME]" '/^\/dev\/mapper\/tomb/ { if($7==tomb) print $1 }'`

    # Tomb must not be open
    [[ -z "$mounted_tomb" ]] || {
        _failure "Please close the tomb ::1 tomb name:: before trying to resize it." $TOMBNAME }
    # New tomb size must be specified
    [[ -n "$newtombsize" ]] || {
        _failure "You must specify the new size of ::1 tomb name::" $TOMBNAME }
    # New tomb size must be an integer
    [[ $newtombsize == <-> ]] || _failure "Size is not an integer."
    # Tombs can only grow in size
    [[ "$newtombsize" -gt "$oldtombsize" ]] || {
        _failure "The new size must be greater then old tomb size." }

    delta="$(( $newtombsize - $oldtombsize ))"

    _message "Generating ::1 tomb file:: of ::2 size::MiB" $TOMBFILE $newtombsize

    _verbose "Data dump using ::1:: from /dev/urandom" ${DD[1]}
    ${=DD} if=/dev/urandom bs=1048576 count=${delta} >> $TOMBPATH

    [[ $? == 0 ]] || {
        _failure "Error creating the extra resize ::1 size::, operation aborted." $tmp_resize }

    { option_is_set --tomb-pwd } && {
        tomb_pwd="`option_value --tomb-pwd`"
        _verbose "tomb-pwd = ::1 tomb pass::" $tomb_pwd
        ask_key_password "$tomb_pwd"
    } || {
        ask_key_password
    }
    [[ $? == 0 ]] || _failure "No valid password supplied."

    lo_mount "$TOMBPATH"
    nstloop=`lo_new`

    mapdate=`date +%s`
    mapper="tomb.$TOMBNAME.$mapdate.$(basename $nstloop)"

    _cryptsetup luksOpen ${nstloop} ${mapper} || {
        _failure "Failure mounting the encrypted file." }

    _sudo cryptsetup resize "${mapper}" || {
        _failure "cryptsetup failed to resize ::1 mapper::" $mapper }

    _sudo e2fsck -p -f /dev/mapper/${mapper} || {
        _failure "e2fsck failed to check ::1 mapper::" $mapper }

    _sudo resize2fs /dev/mapper/${mapper} || {
        _failure "resize2fs failed to resize ::1 mapper::" $mapper }

    # close and free the loop device
    _sudo cryptsetup luksClose "${mapper}"

    return 0
}

# }}}

# {{{ Close

umount_tomb() {
    local tombs how_many_tombs
    local pathmap mapper tombname tombmount loopdev
    local ans pidk pname

    if [ "$1" = "all" ]; then
        mounted_tombs=(`list_tomb_mounts`)
    else
        mounted_tombs=(`list_tomb_mounts $1`)
    fi

    [[ ${#mounted_tombs} == 0 ]] && {
        _failure "There is no open tomb to be closed." }

    [[ ${#mounted_tombs} -gt 1 && -z "$1" ]] && {
        _warning "Too many tombs mounted, please specify one (see tomb list)"
        _warning "or issue the command 'tomb close all' to close them all."
        _failure "Operation aborted." }

    for t in ${mounted_tombs}; do
        mapper=`basename ${t[(ws:;:)1]}`
        tombname=${t[(ws:;:)5]}
        tombmount=${t[(ws:;:)2]}
        tombfs=${t[(ws:;:)3]}
        tombfsopts=${t[(ws:;:)4]}
        tombloop=${mapper[(ws:.:)4]}

        _verbose "Name: ::1 tomb name::" $tombname
        _verbose "Mount: ::1 mount point::" $tombmount
        _verbose "Mapper: ::1 mapper::" $mapper

        [[ -e "$mapper" ]] && {
            _warning "Tomb not found: ::1 tomb file::" $1
            _warning "Please specify an existing tomb."
            return 0 }

        [[ -n $SLAM ]] && {
            _success "Slamming tomb ::1 tomb name:: mounted on ::2 mount point::" \
                $tombname $tombmount
            _message "Kill all processes busy inside the tomb."
            { slam_tomb "$tombmount" } || {
                _failure "Cannot slam the tomb ::1 tomb name::" $tombname }
        } || {
            _message "Closing tomb ::1 tomb name:: mounted on ::2 mount point::" \
                $tombname $tombmount }

        # check if there are binded dirs and close them
        bind_tombs=(`list_tomb_binds $tombname`)
        for b in ${bind_tombs}; do
            bind_mapper="${b[(ws:;:)1]}"
            bind_mount="${b[(ws:;:)2]}"
            _message "Closing tomb bind hook: ::1 hook::" $bind_mount
            _sudo umount $bind_mount || {
                [[ -n $SLAM ]] && {
                    _success "Slamming tomb: killing all processes using this hook."
                    slam_tomb "$bind_mount" || _failure "Cannot slam the bind hook ::1 hook::" $bind_mount
                    umount $bind_mount || _failure "Cannot slam the bind hook ::1 hook::" $bind_mount
                } || {
                    _failure "Tomb bind hook ::1 hook:: is busy, cannot close tomb." $bind_mount
                }
            }
        done

        # Execute post-hooks for eventual cleanup
        { option_is_set -n } || {
            exec_safe_post_hooks ${tombmount%%/} close }

        _verbose "Performing umount of ::1 mount point::" $tombmount
        _sudo umount ${tombmount}
        [[ $? = 0 ]] || { _failure "Tomb is busy, cannot umount!" }

        # If we used a default mountpoint and is now empty, delete it
        [[ "$tombmount" -regex-match "[/run]?/media[/$_USER]?/$tombname" ]] && {
            _sudo rmdir $tombmount }

        _sudo cryptsetup luksClose $mapper
        [[ $? == 0 ]] || {
            _failure "Error occurred in cryptsetup luksClose ::1 mapper::" $mapper }

        # Normally the loopback device is detached when unused
        [[ -e "/dev/$tombloop" ]] && _sudo losetup -d "/dev/$tombloop"
        [[ $? = 0 ]] || {
            _verbose "/dev/$tombloop was already closed." }

        _success "Tomb ::1 tomb name:: closed: your bones will rest in peace." $tombname

    done # loop across mounted tombs

    return 0
}

# Kill all processes using the tomb
slam_tomb() {
    # $1 = tomb mount point
    if [[ -z `fuser -m "$1" 2>/dev/null` ]]; then
        return 0
    fi
    #Note: shells are NOT killed by INT or TERM, but they are killed by HUP
    for s in TERM HUP KILL; do
        _verbose "Sending ::1:: to processes inside the tomb:" $s
        if option_is_set -D; then
            ps -fp `fuser -m /media/a.tomb 2>/dev/null`|
            while read line; do
                _verbose $line
            done
        fi
        fuser -s -m "$1" -k -M -$s
        if [[ -z `fuser -m "$1" 2>/dev/null` ]]; then
            return 0
        fi
        if ! option_is_set -f; then
            sleep 3
        fi
    done
    return 1
}

# }}} - Tomb close

# {{{ Main routine

main() {

    _ensure_dependencies  # Check dependencies are present or bail out

    local -A subcommands_opts
    ### Options configuration
    #
    # Hi, dear developer!  Are you trying to add a new subcommand, or
    # to add some options?  Well, keep in mind that option names are
    # global: they cannot bear a different meaning or behaviour across
    # subcommands.  The only exception is "-o" which means: "options
    # passed to the local subcommand", and thus can bear a different
    # meaning for different subcommands.
    #
    # For example, "-s" means "size" and accepts one argument. If you
    # are tempted to add an alternate option "-s" (e.g., to mean
    # "silent", and that doesn't accept any argument) DON'T DO IT!
    #
    # There are two reasons for that:
    #    I. Usability; users expect that "-s" is "size"
    #   II. Option parsing WILL EXPLODE if you do this kind of bad
    #       things (it will complain: "option defined more than once")
    #
    # If you want to use the same option in multiple commands then you
    # can only use the non-abbreviated long-option version like:
    # -force and NOT -f
    #
    main_opts=(q -quiet=q D -debug=D h -help=h v -version=v f -force=f -tmp: U: G: T: -no-color -unsafe)
    subcommands_opts[__default]=""
    # -o in open and mount is used to pass alternate mount options
    subcommands_opts[open]="n -nohook=n k: -kdf: o: -ignore-swap -tomb-pwd: "
    subcommands_opts[mount]=${subcommands_opts[open]}

    subcommands_opts[create]="" # deprecated, will issue warning

    # -o in forge and lock is used to pass an alternate cipher.
    subcommands_opts[forge]="-ignore-swap k: -kdf: o: -tomb-pwd: -use-urandom "
    subcommands_opts[dig]="-ignore-swap s: -size=s "
    subcommands_opts[lock]="-ignore-swap k: -kdf: o: -tomb-pwd: "
    subcommands_opts[setkey]="k: -ignore-swap -kdf: -tomb-old-pwd: -tomb-pwd: "
    subcommands_opts[engrave]="k: "

    subcommands_opts[passwd]="k: -ignore-swap -kdf: -tomb-old-pwd: -tomb-pwd: "
    subcommands_opts[close]=""
    subcommands_opts[help]=""
    subcommands_opts[slam]=""
    subcommands_opts[list]="-get-mountpoint "

    subcommands_opts[index]=""
    subcommands_opts[search]=""

    subcommands_opts[help]=""
    subcommands_opts[bury]="k: -tomb-pwd: "
    subcommands_opts[exhume]="k: -tomb-pwd: "
    # subcommands_opts[decompose]=""
    # subcommands_opts[recompose]=""
    # subcommands_opts[install]=""
    subcommands_opts[askpass]=""
    subcommands_opts[source]=""
    subcommands_opts[resize]="-ignore-swap s: -size=s k: -tomb-pwd: "
    subcommands_opts[check]="-ignore-swap "
    #    subcommands_opts[translate]=""

    ### Detect subcommand
    local -aU every_opts #every_opts behave like a set; that is, an array with unique elements
    for optspec in $subcommands_opts$main_opts; do
        for opt in ${=optspec}; do
            every_opts+=${opt}
        done
    done
    local -a oldstar
    oldstar=("${(@)argv}")
    #### detect early: useful for --option-parsing
    zparseopts -M -D -Adiscardme ${every_opts}
    if [[ -n ${(k)discardme[--option-parsing]} ]]; then
        print $1
        if [[ -n "$1" ]]; then
            return 1
        fi
        return 0
    fi
    unset discardme
    if ! zparseopts -M -E -D -Adiscardme ${every_opts}; then
        _failure "Error parsing."
        return 127
    fi
    unset discardme
    subcommand=$1
    if [[ -z $subcommand ]]; then
        subcommand="__default"
    fi

    if [[ -z ${(k)subcommands_opts[$subcommand]} ]]; then
        _warning "There's no such command \"::1 subcommand::\"." $subcommand
        exitv=127 _failure "Please try -h for help."
    fi
    argv=("${(@)oldstar}")
    unset oldstar

    ### Parsing global + command-specific options
    # zsh magic: ${=string} will split to multiple arguments when spaces occur
    set -A cmd_opts ${main_opts} ${=subcommands_opts[$subcommand]}
    # if there is no option, we don't need parsing
    if [[ -n $cmd_opts ]]; then
        zparseopts -M -E -D -AOPTS ${cmd_opts}
        if [[ $? != 0 ]]; then
            _warning "Some error occurred during option processing."
            exitv=127 _failure "See \"tomb help\" for more info."
        fi
    fi
    #build PARAM (array of arguments) and check if there are unrecognized options
    ok=0
    PARAM=()
    for arg in $*; do
        if [[ $arg == '--' || $arg == '-' ]]; then
            ok=1
            continue #it shouldnt be appended to PARAM
        elif [[ $arg[1] == '-'  ]]; then
            if [[ $ok == 0 ]]; then
                exitv=127 _failure "Unrecognized option ::1 arg:: for subcommand ::2 subcommand::" $arg $subcommand
            fi
        fi
        PARAM+=$arg
    done
    # First parameter actually is the subcommand: delete it and shift
    [[ $subcommand != '__default' ]] && { PARAM[1]=(); shift }

    ### End parsing command-specific options

    # Use colors unless told not to
    { ! option_is_set --no-color } && { autoload -Uz colors && colors }
    # Some options are only available during insecure mode
    { ! option_is_set --unsafe } && {
        for opt in --tomb-pwd --use-urandom --tomb-old-pwd; do
            { option_is_set $opt } && {
                exitv=127 _failure "You specified option ::1 option::, which is DANGEROUS and should only be used for testing\nIf you really want so, add --unsafe" $opt }
        done
    }
    # read -t or --tmp flags to set a custom temporary directory
    option_is_set --tmp && TMPPREFIX=$(option_value --tmp)


    # When we run as root, we remember the original uid:gid to set
    # permissions for the calling user and drop privileges
    _whoami # Reset _UID, _GID, _TTY

    [[ "$PARAM" == "" ]] && {
        _verbose "Tomb command: ::1 subcommand::" $subcommand
    } || {
        _verbose "Tomb command: ::1 subcommand:: ::2 param::" $subcommand $PARAM
    }

    [[ -z $_UID ]] || {
        _verbose "Caller: uid[::1 uid::], gid[::2 gid::], tty[::3 tty::]." \
            $_UID $_GID $_TTY
    }

    _verbose "Temporary directory: $TMPPREFIX"

    # Process subcommand
    case "$subcommand" in

        # USAGE
        help)
            usage
            ;;

        # DEPRECATION notice (leave here as 'create' is still present in old docs)
        create)
            _warning "The create command is deprecated, please use dig, forge and lock instead."
            _warning "For more informations see Tomb's manual page (man tomb)."
            _failure "Operation aborted."
            ;;

        # CREATE Step 1: dig -s NN file.tomb
        dig)
            dig_tomb ${=PARAM}
            ;;

        # CREATE Step 2: forge file.tomb.key
        forge)
            forge_key ${=PARAM}
            ;;

        # CREATE Step 2: lock -k file.tomb.key file.tomb
        lock)
            lock_tomb_with_key ${=PARAM}
            ;;

        # Open the tomb
        mount|open)
            mount_tomb ${=PARAM}
            ;;

        # Close the tomb
        # `slam` is used to force closing.
        umount|close|slam)
            [[ "$subcommand" ==  "slam" ]] && SLAM=1
            umount_tomb $PARAM[1]
            ;;

        # Grow tomb's size
        resize)
            [[ $RESIZER == 0 ]] && {
                _failure "Resize2fs not installed: cannot resize tombs." }
            resize_tomb $PARAM[1]
            ;;

        ## Contents manipulation

        # Index tomb contents
        index)
            index_tombs $PARAM[1]
            ;;

        # List tombs
        list)
            list_tombs $PARAM[1]
            ;;

        # Search tomb contents
        search)
            search_tombs ${=PARAM}
            ;;

        ## Locking operations

        # Export key to QR Code
        engrave)
            [[ $QRENCODE == 0 ]] && {
                _failure "QREncode not installed: cannot engrave keys on paper." }
            engrave_key ${=PARAM}
            ;;

        # Change password on existing key
        passwd)
            change_passwd $PARAM[1]
            ;;

        # Change tomb key
        setkey)
            change_tomb_key ${=PARAM}
            ;;

        # STEGANOGRAPHY: hide key inside an image
        bury)
            [[ $STEGHIDE == 0 ]] && {
                _failure "Steghide not installed: cannot bury keys into images." }
            bury_key $PARAM[1]
            ;;

        # STEGANOGRAPHY: read key hidden in an image
        exhume)
            [[ $STEGHIDE == 0 ]] && {
                _failure "Steghide not installed: cannot exhume keys from images." }
            exhume_key $PARAM[1]
            ;;

        ## Internal commands useful to developers

        # Make tomb functions available to the calling shell or script
        'source')   return 0 ;;

        # Ask user for a password interactively
        askpass)    ask_password $PARAM[1] $PARAM[2] ;;

        # Default operation: presentation, or version information with -v
        __default)
            _print "Tomb ::1 version:: - a strong and gentle undertaker for your secrets" $VERSION
            _print "\000"
            _print " Copyright (C) 2007-2015 Dyne.org Foundation, License GNU GPL v3+"
            _print " This is free software: you are free to change and redistribute it"
            _print " For the latest sourcecode go to <http://dyne.org/software/tomb>"
            _print "\000"
            option_is_set -v && {
                local langwas=$LANG
                LANG=en
                _print " This source code is distributed in the hope that it will be useful,"
                _print " but WITHOUT ANY WARRANTY; without even the implied warranty of"
                _print " MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."
                LANG=$langwas
                _print " When in need please refer to <http://dyne.org/support>."
                _print "\000"
                _print "System utils:"
                _print "\000"
                cat <<EOF
  `sudo -V | head -n1`
  `cryptsetup --version`
  `pinentry --version`
  `gpg --version | head -n1` - key forging algorithms (GnuPG symmetric ciphers):
  `list_gnupg_ciphers`
EOF
                _print "\000"
                _print "Optional utils:"
                _print "\000"
                _list_optional_tools version
                return 0
            }
            usage
            ;;

        # Reject unknown command and suggest help
        *)
            _warning "Command \"::1 subcommand::\" not recognized." $subcommand
            _message "Try -h for help."
            return 1
            ;;
    esac
    return $?
}

# }}}

# {{{ Run

main "$@" || exit $?   # Prevent `source tomb source` from exiting

# }}}

# -*- tab-width: 4; indent-tabs-mode:nil; -*-
# vim: set shiftwidth=4 expandtab:
