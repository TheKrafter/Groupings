> NOTE: This branch is a complete rewrite of the client! See the [TODO](TODO.md).

# Groupings

A GTK4/Libadwaita GroupMe client in Python.

## Dependencies

 - [TheKrafter/GroupPy](https://github.com/TheKrafter/GroupPy) (Custom OAuth Flow)
 - [rhgrant10/GroupyAPI](https://github.com/rhgrant10/Groupy) (REST API)
 - [cuuush/groupme-push](https://github.com/cuuush/groupme-push) (Push messaging service)
 - GTK4 Python Bindings (gobject-introspection) (GUI)
 - Libadwaita 1+ (GUI)

## Installation

### Flatpak

1. Install
    ```
    flatpak-builder --install --user --force-clean build-dir xyz.krafterdev.Groupings.yaml
    ```
2. Run
    ```
    flatpak run xyz.krafterdev.Groupings
    ```

### Flit (Not Recommended)
1. Install [flit](https://flit.pypa.io/en/stable/):
    ```
    pip install flit
    ```
2. Build & Install:
    ```
    flit install --user
    ```
3. Run:
    ```
    python3 -m groupings
    ```

Refer to your system's package manager for how to install GTK 4 and Libadwaita.

## Licenses

Groupings Copyright (c) 2023 Krafter, is distributed subject to the Mozilla Public License version 2.0 or later.

`flatpak-pip-generator` is licensed subject to the MPL license.

<details>

###### Notes for Devs

Emojis: [How Tuba does it](https://github.com/GeopJr/Tuba/issues/622#issuecomment-1781663957) 

Documentation:
 - [GroupyAPI](http://groupy.readthedocs.org/en/latest/)
 - [groupme-push](https://pypi.org/project/groupme-push/)
 - [keyring](https://pypi.org/project/keyring/)
 - [PyXDG](https://pyxdg.readthedocs.io/en/latest/)
 - [PyGOBject](https://lazka.github.io/pgi-docs/)
 - [Adw](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1.4/index.html)
 - [Gtk4](https://docs.gtk.org/gtk4/index.html)

OAuth Flow: take from [TheKrafter/GroupPy](https://github.com/TheKrafter/GroupPy/blob/main/grouppy/__init__.py#L37)

Generating manifest modules: `./src/tools/flatpak-pip-generator --yaml --requirements-file='./requirements.txt'`

</details>
