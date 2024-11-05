========
Postopus
========

This is the documentation of `Postopus <https://gitlab.com/octopus-code/postopus/>`_ (the POST-processing of OctoPUS data), which is an environment that
can help with the analysis of data that was computed using the `Octopus <https://octopus-code.org>`_ TDDFT package.

Installation
============
For installing the basic dependencies of postopus: ``pip install postopus``. Although for interacting with the tutorial notebooks a ``pip install postopus[recommended]`` is needed. This will install packages for analysis and plotting like ``matplotlib``, ``holoviews`` and ``jupyter`` among others.
If you want to contribute, develop, or build the documentation locally, please follow the instructions in the `DEVELOPERNOTES <https://gitlab.com/octopus-code/postopus/-/blob/main/DEVELOPERNOTES.md>`__.


Quick Start
============
The `quick start <notebooks/Quick_Start.ipynb>`__ summarises the most important functionalities Postopus provides.

.. toctree::
   :hidden:

   Quick Start <./notebooks/Quick_Start.ipynb>


Contents
========

.. toctree::
   :maxdepth: 1

   user_guide
   application_examples
   api/modules
   changelog


License
=======

Postopus is released under GPLv3. For details refer to the `LICENSE file <https://gitlab.com/octopus-code/postopus/-/blob/main/LICENSE>`__.
