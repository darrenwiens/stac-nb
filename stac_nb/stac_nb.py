from IPython.display import display
import ipywidgets as widgets
import json
import os
import requests


class STAC_Query_UI(widgets.VBox):
    def __init__(self, stac_api: str, **kwargs):
        super().__init__(**kwargs)
        self.stac_api = stac_api
        self.query_results = None

        collections_endpoint = os.path.join(stac_api, "collections")
        collection_response = get_request(collections_endpoint, headers).json()
        collection_ids = [i["id"] for i in collection_response["collections"]]

        collections_w = widgets.SelectMultiple(
            options=collection_ids,
            description="Collection(s):",
            disabled=False,
        )

        limit_w = widgets.BoundedIntText(
            value=10, min=0, max=1000, step=1, description="Limit:", disabled=False
        )

        ids_w = widgets.Textarea(
            placeholder="Comma delimited list of IDs",
            description="ID(s):",
            disabled=False,
        )

        bbox_w = widgets.Text(
            placeholder="Comma delimited list of bounds (order: W, S, E, N)",
            description="BBox:",
            disabled=False,
            layout={
                "width": "95%",
            },
        )

        start_date_w = widgets.DatePicker(description="Start Date", disabled=False)

        end_date_w = widgets.DatePicker(description="End Date", disabled=False)

        query_btn_w = widgets.Button(
            description="Run Query",
            disabled=False,
            button_style="",
            tooltip="Run Query",
            icon="check",
        )

        response_text = widgets.Output()

        def on_query_btn_clicked(b):
            start_datetime = start_date_w.value or "1900-01-01T00:00:00Z"
            end_datetime = end_date_w.value or "2900-01-01T00:00:00Z"

            payload_dict = dict(
                collections=collections_w.value,
                datetime=f"{start_datetime}/{end_datetime}",
                limit=limit_w.value,
            )

            try:
                bbox = [float(i) for i in bbox_w.value.split(",")]
            except ValueError:
                bbox = []

            if len(bbox) != 4:
                payload_dict["bbox"] = [-180, -90, 180, 90]
            else:
                payload_dict["bbox"] = bbox

            payload = json.dumps(payload_dict)

            search_endpoint = os.path.join(stac_api, "search")

            query_response = post_request(
                search_endpoint, headers=headers, data=payload
            )

            self.query_results = query_response.json()
            with response_text:
                matches = query_response.json()
                print(f"MATCHES: {len(matches['features'])}")

        query_btn_w.on_click(on_query_btn_clicked)

        common_widgets = widgets.VBox([collections_w, limit_w, ids_w])
        spatial_widgets = widgets.VBox([bbox_w])
        temporal_widgets = widgets.VBox([start_date_w, end_date_w])

        children = [common_widgets, spatial_widgets, temporal_widgets]
        tab = widgets.Tab()
        tab.children = children
        titles = ["Common", "Spatial", "Temporal"]
        for i in range(len(titles)):
            tab.set_title(i, str(titles[i]))

        self.children = [tab, query_btn_w, response_text]

    def display(self):
        display(self)


headers = {"Content-Type": "application/json"}


def get_request(url, headers={}):
    response = requests.get(url, headers=headers)
    return response


def post_request(url, headers={}, data={}):
    response = requests.post(url, headers=headers, data=data)
    return response
