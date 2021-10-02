# stac-nb

STAC in Jupyter Notebooks

# Install

`pip install -e .`

# Usage

Start Jupyter Lab (`jupyter lab`), create new notebook, then:

```
from stac_nb import STAC_Query_UI

# display the UI for a STAC API
ui = STAC_Query_UI("https://earth-search.aws.element84.com/v0")
ui.display()

# retrieve query results
ui.query_results
```
