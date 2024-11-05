# Postopus

[Postopus](https://gitlab.com/octopus-code/postopus/) (the POST-processing of OctoPUS data) is an environment that
can help with the analysis of data that was computed using the [Octopus](https://octopus-code.org) TDDFT package.

- Documentation of Postopus: https://octopus-code.gitlab.io/postopus/index.html
- Quick start guide of Postopus on the MPCDF Binder: [![Binder](https://notebooks.mpcdf.mpg.de/binder/badge_logo.svg)](https://notebooks.mpcdf.mpg.de/binder/v2/git/https%3A%2F%2Fgitlab.mpcdf.mpg.de%2Fpostopus%2Fpostopus.git/main?labpath=docs%2Fnotebooks%2FQuick_Start.ipynb)
- Run parts of the documentation interactivly: [![Binder](https://notebooks.mpcdf.mpg.de/binder/badge_logo.svg)](https://notebooks.mpcdf.mpg.de/binder/v2/git/https%3A%2F%2Fgitlab.mpcdf.mpg.de%2Fpostopus%2Fpostopus.git/main?labpath=docs%2Fnotebooks%2FREADME.ipynb)
- Run the [Octopus tutorials](https://octopus-code.org/documentation/13/tutorial/) re-written using Postopus: [![Binder](https://notebooks.mpcdf.mpg.de/binder/badge_logo.svg)](https://notebooks.mpcdf.mpg.de/binder/v2/git/https%3A%2F%2Fgitlab.mpcdf.mpg.de%2Fpostopus%2Fpostopus.git/main?labpath=dev%2FTutorials%2FReadme.ipynb)


## Version support

| Source                | Octopus versions supported                 | Python versions supported|
|-----------------------|--------------------------------------------|--------------------------|
| main branch           | Octopus@13, 14, 15                         | 3.9, 3.10, 3.11, 3.12    |
| PyPI – postopus 0.3.0 | Octopus@13, 14, 15                         | 3.9, 3.10, 3.11, 3.12    |
| PyPI – postopus 0.2.0 | Octopus@12                                 | 3.8, 3.9, 3.10           |
| PyPI – postopus 0.1.0 | Octopus@12                                 | 3.8, 3.9, 3.10           |

## Installation
Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):
```
pip install postopus[recommended]
```
Using `pip install postopus[recommended]` instead of `pip install postopus`
will install some optional dependencies (like matplotlib and jupyter) which are highly recommended for all users.
See [DEVELOPERNOTES.md](DEVELOPERNOTES.md#developer-setup) for an editable installation.


## How to cite
[Zenodo entry](https://zenodo.org/record/8287137)

## Binder and MPCDF Gitlab repository clone
The MPCDF Binder service we use only accepts repositories on the
[MPCDF Gitlab](https://gitlab.mpcdf.mpg.de). The authoritative Postopus source is at
https://gitlab.com/octopus/postopus. We thus have a clone of the Postopus repository at
[the MPCDF Gitlab](https://gitlab.mpcdf.mpg.de/postopus/postopus). The main branch
of [the repo at gitlab.com](https://gitlab.com/octopus-code/postopus/) is
pushed to the MPCDF repository regularly. See
[DEVELOPERNOTES.md](DEVELOPERNOTES.md#mpcdf-repository-syncronization) for details.
