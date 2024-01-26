# TRANSLATIONS
## 1. How to translate
Tomb uses the [Weblate](https://hosted.weblate.org/projects/tomb/tomb/) platform to manage the translation efforts of it's user community.

In Weblate, an user can click "Start new translation", choose a language and click "Request new translation". Additionally, just to reinforce your request, we recommend opening an [issue](https://github.com/dyne/Tomb/issues/new) requesting the development team to open a new translation for your language.

## 2. About files in this folder
All translation files in this folder (those with a ".po" extension) are based on the `tomb.pot` file.

POT files are just templates and they don't contain any translations. To do a translation, create a new PO file based on the template.

The `tomb.pot` template must be created using the perl script `generate_translatable_strings.pl` **for each new version of Tomb**:

```sh
$ perl generate_translatable_strings.pl > tomb.pot
```

After that, just open the `tomb.pot` file in the [poedit](https://poedit.net/) program, and click on "Start new translation" (bottom left button), select your language, save and start translating.

## 3. Updating translation
In your favorite shell, make a backup of old file adding it's version, then update with `msgmerge`:

```sh
$ msgmerge --update <language>.po tomb.pot
```

Open the new updated PO translation file and start reviewing the translation. Poedit will highlight what has changed and what needs revision.