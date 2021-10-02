=====
Usage
=====

To use stac-nb in a project, start Jupyter Lab (`jupyter lab`), create a new notebook, then::

    from stac_nb import STAC_Query_UI

Display the UI for a STAC API::
    
    ui = STAC_Query_UI("https://earth-search.aws.element84.com/v0")
    ui.display()

After you have run the query, retrieve the results::
    
    ui.query_results
