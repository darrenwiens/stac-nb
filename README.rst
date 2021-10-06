stac-nb
=================
STAC in Jupyter Notebooks
-------------------------

.. image:: https://readthedocs.org/projects/stac-nb/badge/?version=latest&style=flat
    :target: https://stac-nb.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://badge.fury.io/py/stac-nb.svg
    :target: https://badge.fury.io/py/stac-nb
    :alt: PyPI Status
.. image:: https://coveralls.io/repos/github/darrenwiens/stac-nb/badge.svg?branch=main
    :target: https://coveralls.io/github/darrenwiens/stac-nb?branch=main
.. image:: https://github.com/darrenwiens/stac-nb/actions/workflows/python-package.yml/badge.svg
    :alt: Build Status

Install
-------------------------
::

    pip install stac-nb

Usage
-------------------------

To use stac-nb in a project, start Jupyter Lab (``jupyter lab``), create a new notebook, then::

    from stac_nb import STAC_Query_UI

Display the UI for a STAC API::

    ui = STAC_Query_UI("https://earth-search.aws.element84.com/v0")
    ui.display()

After you have run the query, retrieve the results from ``ui.query_results``::

    ui.query_results
