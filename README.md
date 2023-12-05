> NOTE: This branch is a complete rewrite of the client! See the [TODO](TODO.md).

# Groupings

A GTK4/Libadwaita [GroupMe](https://groupme.com/) client in Python.

## Dependencies

 - [rhgrant10/GroupyAPI](https://github.com/rhgrant10/Groupy) (REST API)
 - [cuuush/groupme-push](https://github.com/cuuush/groupme-push) (Push messaging service)
 - GTK4 Python Bindings (gobject-introspection) (GUI)
 - Libadwaita 1+ (GUI)

## Installation

Groupings is currently only supported as a flatpak.

### Flatpak

1. Install
    ```
    flatpak-builder --install --user --force-clean build-dir xyz.krafterdev.Groupings.yaml
    ```
2. Run
    ```
    flatpak run xyz.krafterdev.Groupings
    ```

## Licenses

Groupings Copyright (c) 2023 Krafter, is distributed subject to the Mozilla Public License version 2.0 or later.

`flatpak-pip-generator` is licensed subject to the MPL license.

<details>

###### Notes for Devs

Emojis: [How Tuba does it](https://github.com/GeopJr/Tuba/issues/622#issuecomment-1781663957) 

Documentation:
 - [GroupyAPI](http://groupy.readthedocs.org/en/latest/)
 - [groupme-push](https://pypi.org/project/groupme-push/)
 - [GroupMe Developers](https://dev.groupme.com/)
 - [keyring](https://pypi.org/project/keyring/)
 - [PyXDG](https://pyxdg.readthedocs.io/en/latest/)
 - [PyGOBject](https://lazka.github.io/pgi-docs/)
 - [Adw](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1.4/index.html)
 - [Gtk4](https://docs.gtk.org/gtk4/index.html)
 - [PyWebkitGTK](https://code.google.com/archive/p/pywebkitgtk/)
 - [keyring_minimal (src)](https://github.com/hrehfeld/python-keyring-minimal/blob/master/keyring_minimal/__init__.py)


Generating manifest modules: `python3 ./src/assets/tools/flatpak-pip-generator --yaml -r requirements.txt`

</details>
