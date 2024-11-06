===============
pymt_permamodel
===============


.. image:: https://img.shields.io/badge/CSDMS-Basic%20Model%20Interface-green.svg
        :target: https://bmi.readthedocs.io/
        :alt: Basic Model Interface

.. image:: https://img.shields.io/badge/recipe-pymt_permamodel-green.svg
        :target: https://anaconda.org/conda-forge/pymt_permamodel

.. image:: https://readthedocs.org/projects/pymt-permamodel/badge/?version=latest
        :target: https://pymt-permamodel.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://github.com/pymt-lab/pymt_permamodel/actions/workflows/test.yml/badge.svg
        :target: https://github.com/pymt-lab/pymt_permamodel/actions/workflows/test.yml

.. image:: https://github.com/pymt-lab/pymt_permamodel/actions/workflows/flake8.yml/badge.svg
        :target: https://github.com/pymt-lab/pymt_permamodel/actions/workflows/flake8.yml

.. image:: https://github.com/pymt-lab/pymt_permamodel/actions/workflows/black.yml/badge.svg
        :target: https://github.com/pymt-lab/pymt_permamodel/actions/workflows/black.yml


PyMT plugins for Permamodel components


* Free software: MIT License
* Documentation: https://pymt-permamodel.readthedocs.io.




=========== =====================================
Component   PyMT
=========== =====================================
FrostNumber `from pymt.models import FrostNumber`
Ku          `from pymt.models import Ku`
KuEnhanced  `from pymt.models import KuEnhanced`
=========== =====================================

---------------
Installing pymt
---------------

Installing `pymt` from the `conda-forge` channel can be achieved by adding
`conda-forge` to your channels with:

.. code::

  conda config --add channels conda-forge

*Note*: Before installing `pymt`, you may want to create a separate environment
into which to install it. This can be done with,

.. code::

  conda create -n pymt python=3
  conda activate pymt

Once the `conda-forge` channel has been enabled, `pymt` can be installed with:

.. code::

  conda install pymt

It is possible to list all of the versions of `pymt` available on your platform with:

.. code::

  conda search pymt --channel conda-forge

--------------------------
Installing pymt_permamodel
--------------------------

Once `pymt` is installed, the dependencies of `pymt_permamodel` can
be installed with:

.. code::

  conda install permamodel

To install `pymt_permamodel`,

.. code::

  conda install pymt_permamodel
