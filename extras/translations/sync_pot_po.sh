#! /usr/bin/sh
# (create a new pot template from the current tomb script via script)
# use the pot file as reference to update all the po files

perl generate_translatable_strings.pl > tomb.pot

for po in ./*.po; do
  msgmerge --update ${po} tomb.pot
done
