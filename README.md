> NOTE: This branch is a complete rewrite of the client!

# Groupings

A GTK4/Libadwaita GroupMe client in Python.

## Dependencies

 - [TheKrafter/GroupPy](https://github.com/TheKrafter/GroupPy) (Custom OAuth Flow)
 - [rhgrant10/GroupyAPI](https://github.com/rhgrant10/Groupy) (REST API)
 - [cuuush/groupme-push](https://github.com/cuuush/groupme-push) (Push messaging service)
 - GTK4 Python Bindings (gobject-introspection) (GUI)
 - Libadwaita 1+ (GUI)

## Installation

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


<details>

####### Notes for Devs

Emojis: [How Tuba does it](https://github.com/GeopJr/Tuba/issues/622#issuecomment-1781663957) 

Documentation:
 - [GroupyAPI](http://groupy.readthedocs.org/en/latest/)
 - [groupme-push](https://pypi.org/project/groupme-push/)
 - [keyring](https://pypi.org/project/keyring/)

OAuth Flow: take from [TheKrafter/GroupPy](https://github.com/TheKrafter/GroupPy/blob/main/grouppy/__init__.py#L37)

</details>