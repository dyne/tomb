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

## 3. Notes on versioning

**As of June 27, 2023**, the current `tomb.pot` template was created on January 2, 2017 for `Tomb version 2.3`, which was released on the same date, as can be seen in [tag v2.3](https://github.com/dyne/Tomb/releases/tag/v2.3).

```sh
$ sed -n '9p' tomb.pot
"PO-Revision-Date: Mon Jan  2 22:40:32 2017\n"
```

***Thus, all files in this folder, as of June 27, 2023, are valid for tomb version 2.3 `only`.***

Old translations may work with recent versions of Tomb, but will be incomplete and wrong at many points.

### 3.1 Exception
Translation files for Brazilian Portuguese (pt_BR) was created in June 27, 2023. Precisely when it was noticed that the translations were out of date.

So the translator created two versions: one for Tomb 2.3 (`pt_BR.pot` based upon `tomb.pot`) and another for Tomb 2.10 (`pt_BR-2.10.pot` based upon `tomb-2.10.pot`).

For now it is the only updated translation for the current version of Tomb.

## 4. Updating translation
In your favorite shell, make a backup of old file adding it's version, then update with `msgmerge`:

```sh
$ cp lang.po lang-2.3.pot
$ msgmerge --update lang.po tomb-2.10.pot
```

Open the new updated PO translation file and start reviewing the translation.