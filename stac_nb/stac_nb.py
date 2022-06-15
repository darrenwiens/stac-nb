from IPython.display import display as iDisplay
import ipywidgets as widgets
from pystac_client import Client
import json

# This class is a proxy to visualize STAC responses nicely in Jupyter
# To show the actual list or dict in Jupyter, use repr() or print()


class VisualList(list):

    def __init__(self, data: list):
        list.__init__(self, data)

    def _repr_html_(self):
        # Construct HTML, but load Vue Components source files only if the
        # openEO HTML tag is not yet defined
        return """
        <script>
        if (!window.customElements || !window.customElements.get('openeo-items')) {{
            var el = document.createElement('script');
            el.src = "https://cdn.jsdelivr.net/npm/@openeo/vue-components@2/assets/openeo.min.js";
            document.head.appendChild(el);
        }}
        </script>
        <openeo-items>
            <script type="application/json">{props}</script>
        </openeo-items>
        """.format(
            props=json.dumps({'items': [i.to_dict() for i in self], 'show-map': True})
        )


class STAC_Query_UI(widgets.VBox):
    def __init__(self, stac_api: str, headers: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.client = Client.open(stac_api, headers=headers)
        self.query_results = None

        collection_ids = [c.id for c in self.client.get_all_collections()]

        self.collections_w = widgets.SelectMultiple(
            options=collection_ids,
            description="Collection(s):",
            disabled=False,
            layout={
                "width": "95%",
            },
        )

        self.limit_w = widgets.BoundedIntText(
            value=10,
            min=0,
            max=1000,
            step=1,
            description="Limit:",
            disabled=False,
            layout={
                "width": "95%",
            },
        )

        self.ids_w = widgets.Textarea(
            placeholder="Comma delimited list of IDs",
            description="ID(s):",
            disabled=False,
            layout={
                "width": "95%",
            },
        )

        self.bbox_w = widgets.Text(
            placeholder="Comma delimited list of bounds (order: W, S, E, N)",
            description="BBox:",
            disabled=False,
            layout={
                "width": "95%",
            },
        )

        self.start_date_w = widgets.DatePicker(description="Start Date", disabled=False)

        self.end_date_w = widgets.DatePicker(description="End Date", disabled=False)

        self.show_query_w = widgets.Checkbox(
            value=False,
            description="Print query",
            disabled=False,
            indent=False,
        )

        self.query_btn_w = widgets.Button(
            description="Run Query",
            disabled=False,
            button_style="",
            tooltip="Run Query",
            icon="check",
        )

        self.response_text = widgets.Output()

        self.query_btn_w.on_click(self.click_button)

        common_widgets = widgets.VBox([self.collections_w, self.limit_w, self.ids_w])
        spatial_widgets = widgets.VBox([self.bbox_w])
        temporal_widgets = widgets.VBox([self.start_date_w, self.end_date_w])

        children = [common_widgets, spatial_widgets, temporal_widgets]
        tab = widgets.Tab()
        tab.children = children
        titles = ["Common", "Spatial", "Temporal"]
        for i in range(len(titles)):
            tab.set_title(i, str(titles[i]))

        self.children = [tab, self.show_query_w, self.query_btn_w, self.response_text]

    def display(self):
        iDisplay(self)

    def click_button(self, b):
        start_datetime = self.start_date_w.value or "1900-01-01T00:00:00Z"
        end_datetime = self.end_date_w.value or "2900-01-01T00:00:00Z"

        payload_dict = dict(
            collections=self.collections_w.value,
            datetime=f"{start_datetime}/{end_datetime}",
            max_items=self.limit_w.value,
        )

        try:
            bbox = [float(i) for i in self.bbox_w.value.split(",")]
        except ValueError:
            bbox = []

        if len(bbox) != 4:
            payload_dict["bbox"] = [-180, -90, 180, 90]
        else:
            payload_dict["bbox"] = bbox

        ids = self.ids_w.value
        if ids is not None and len(ids) > 0:
            payload_dict["ids"] = [x.strip(" ") for x in ids.split(",")]

        query_response = self.client.search(**payload_dict)

        self.query_results = VisualList(query_response.get_items())

        with self.response_text:
            if self.show_query_w.value:
                print(f"QUERY: {vars(query_response)}")
            print(f"MATCHES: {len(self.query_results)}")
