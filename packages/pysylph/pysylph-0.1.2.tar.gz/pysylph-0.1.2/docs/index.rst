|Logo| PySylph |Stars|
======================

.. |Logo| image:: /_images/logo.png
   :scale: 40%
   :class: dark-light

.. |Stars| image:: https://img.shields.io/github/stars/althonos/pysylph.svg?style=social&maxAge=3600&label=Star
   :target: https://github.com/althonos/pysylph/stargazers
   :class: dark-light

*PyO3 bindings and Python interface to* `sylph <https://github.com/bluenote-1577/sylph>`_, *an ultrafast method for containment ANI querying and taxonomic profiling.*

|Actions| |Coverage| |PyPI| |Bioconda| |AUR| |Wheel| |Versions| |Implementations| |License| |Source| |Mirror| |Issues| |Docs| |Changelog| |Downloads|

.. |Actions| image:: https://img.shields.io/github/actions/workflow/status/althonos/pysylph/test.yml?branch=main&logo=github&style=flat-square&maxAge=300
   :target: https://github.com/althonos/pysylph/actions

.. |Coverage| image:: https://img.shields.io/codecov/c/gh/althonos/pysylph?logo=codecov&style=flat-square&maxAge=600
   :target: https://codecov.io/gh/althonos/pysylph/

.. |PyPI| image:: https://img.shields.io/pypi/v/pysylph.svg?style=flat-square&maxAge=3600
   :target: https://pypi.python.org/pypi/pysylph

.. |Bioconda| image:: https://img.shields.io/conda/vn/bioconda/pysylph?ogo=anaconda&style=flat-square&maxAge=3600
   :target: https://anaconda.org/bioconda/pysylph

.. |AUR| image:: https://img.shields.io/aur/version/python-pysylph?logo=archlinux&style=flat-square&maxAge=3600
   :target: https://aur.archlinux.org/packages/python-pysylph

.. |Wheel| image:: https://img.shields.io/pypi/wheel/pysylph?style=flat-square&maxAge=3600
   :target: https://pypi.org/project/pysylph/#files

.. |Versions| image:: https://img.shields.io/pypi/pyversions/pysylph.svg?logo=python&style=flat-square&maxAge=3600
   :target: https://pypi.org/project/pysylph/#files

.. |Implementations| image:: https://img.shields.io/pypi/implementation/pysylph.svg?logo=python&style=flat-square&maxAge=3600&label=impl
   :target: https://pypi.org/project/pysylph/#files

.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square&maxAge=3600
   :target: https://choosealicense.com/licenses/mit/

.. |Source| image:: https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=2678400&style=flat-square
   :target: https://github.com/althonos/pysylph/

.. |Mirror| image:: https://img.shields.io/badge/mirror-EMBL-009f4d?style=flat-square&maxAge=2678400
   :target: https://git.embl.de/larralde/pysylph/

.. |Issues| image:: https://img.shields.io/github/issues/althonos/pysylph.svg?style=flat-square&maxAge=600
   :target: https://github.com/althonos/pysylph/issues

.. |Docs| image:: https://img.shields.io/readthedocs/pysylph?style=flat-square&maxAge=3600
   :target: http://pysylph.readthedocs.io/en/stable/?badge=stable

.. |Changelog| image:: https://img.shields.io/badge/keep%20a-changelog-8A0707.svg?maxAge=2678400&style=flat-square
   :target: https://github.com/althonos/pysylph/blob/master/CHANGELOG.md

.. |Downloads| image:: https://img.shields.io/pypi/dm/pysylph?style=flat-square&color=303f9f&maxAge=86400&label=downloads
   :target: https://pepy.tech/project/pysylph


Overview
--------

``sylph`` is a method developed by `Jim Shaw <https://jim-shaw-bluenote.github.io/>`_
and `Yun William Yu <https://github.com/yunwilliamyu>`_ for fast and robust
ANI querying or metagenomic profiling for metagenomic shotgun samples. It uses 
a statistical model based on Poisson coverage to compute coverage-adjusted ANI
instead of naive ANI. 

``pysylph`` is a Python module, implemented using the `PyO3 <https://pyo3.rs/>`_
framework, that provides bindings to ``sylph``. It directly links to the
``sylph`` code, which has the following advantages over CLI wrappers:

.. grid:: 1 2 3 3
   :gutter: 1

   .. grid-item-card:: :fas:`battery-full` Batteries-included

      Just add ``pysylph`` as a ``pip`` or ``conda`` dependency, no need
      for the HMMER binaries or any external dependency.

   .. grid-item-card:: :fas:`screwdriver-wrench` Flexible

      Create input `~pysylph.GenomeSketch` and `~pysylph.SampleSketch` 
      objects with the :doc:`API <api/index>`, or load them from a file.

   .. grid-item-card:: :fas:`gears` Practical

      Retrieve nested results as lists of `~pysylph.AniResult` objects,
      write them to a file, or use them for further Python analysis.


Setup
-----

Run ``pip install pysylph`` in a shell to download the latest release and all
its dependencies from PyPi, or have a look at the
:doc:`Installation page <guide/install>` to find other ways to install ``pysylph``.


Citation
--------

Pysylph is scientific software, and builds on top of ``sylph``. Please cite 
`sylph <https://github.com/bluenote-1577/sylph>`_ if you are using it in
an academic work, for instance as:

   ``pysylph``, a Python library binding to ``sylph`` (Shaw & Yu, 2024).



Library
-------

.. toctree::
   :maxdepth: 2

   User Guide <guide/index>
   API Reference <api/index>


Related Projects
----------------

The following Python libraries may be of interest for bioinformaticians.

.. include:: related.rst


License
-------

This library is provided under the `MIT License <https://choosealicense.com/licenses/mit/>`_.
It contains some code included verbatim from the the `sylph` source code, which 
was written by `Jim Shaw <https://jim-shaw-bluenote.github.io/>`_ and is distributed 
under the terms of the `MIT License <https://choosealicense.com/licenses/mit/>`_
as well. Source distributions of `pysylph` vendors additional sources under their 
own terms using the ``cargo vendor`` command. See the 
:doc:`Copyright Notice <guide/copyright>` section for more information.

*This project is in no way not affiliated, sponsored, or otherwise endorsed by
the original* `sylph <https://github.com/bluenote-1577/sylph>`_ *authors. It was developed by*
`Martin Larralde <https://github.com/althonos/pyhmmer>`_ *during his PhD project
at the* `Leiden University Medical Center <https://www.lumc.nl/en/>`_
*in the* `Zeller team <https://github.com/zellerlab>`_.
