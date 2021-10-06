import pytest
from pystac_client.item_search import ItemSearch


STAC_API = "https://api/endpoint"


@pytest.fixture(autouse=True)
def mock_responses(
    requests_mock,
    landing_page_response,
    collections_response,
    collection_response,
    search_response,
):

    requests_mock.get(f"{STAC_API}", json=landing_page_response)
    requests_mock.get(f"{STAC_API}/collections", json=collections_response)
    requests_mock.get(
        f"{STAC_API}/collections/simple-collection", json=collection_response
    )
    requests_mock.post(f"{STAC_API}/search", json=search_response)


@pytest.fixture(scope="module")
def landing_page_response():
    return {
        "stac_version": "1.0.0",
        "stac_api_version": "0.9.0",
        "type": "Catalog",
        "id": "stac-server",
        "title": "STAC API",
        "description": "Test STAC API",
        "links": [
            {
                "rel": "child",
                "href": "https://api/endpoint/collections/simple-collection",
            },
            {
                "rel": "service-desc",
                "type": "application/vnd.oai.openapi+json;version=3.0",
                "href": "https://api/endpoint/api",
            },
            {
                "rel": "conformance",
                "type": "application/json",
                "href": "https://api/endpoint/conformance",
            },
            {
                "rel": "data",
                "type": "application/json",
                "href": "https://api/endpoint/collections",
            },
            {
                "rel": "self",
                "type": "application/json",
                "href": "https://api/endpoint/",
            },
            {
                "rel": "search",
                "type": "application/geo+json",
                "href": "https://api/endpoint/search",
            },
            {"rel": "docs", "href": "https://stac-utils.github.io/stac-server/"},
        ],
        "conformsTo": [
            "https://api.stacspec.org/v1.0.0-beta.2/core",
            "https://api.stacspec.org/v1.0.0-beta.2/item-search",
            "https://api.stacspec.org/v1.0.0-beta.2/item-search#fields",
            "https://api.stacspec.org/v1.0.0-beta.2/item-search#sort",
            "https://api.stacspec.org/v1.0.0-beta.2/item-search#query",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
        ],
    }


@pytest.fixture(scope="module")
def collections_response(collection_response):
    return {"collections": [collection_response]}


@pytest.fixture(scope="module")
def collection_response():
    return {
        "id": "simple-collection",
        "type": "Collection",
        "stac_extensions": [
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
        ],
        "stac_version": "1.0.0",
        "description": "A simple collection demonstrating core catalog fields with links to a couple of items",
        "title": "Simple Example Collection",
        "providers": [
            {
                "name": "Remote Data, Inc",
                "description": "Producers of awesome spatiotemporal assets",
                "roles": ["producer", "processor"],
                "url": "http://remotedata.io",
            }
        ],
        "extent": {
            "spatial": {
                "bbox": [
                    [
                        172.91173669923782,
                        1.3438851951615003,
                        172.95469614953714,
                        1.3690476620161975,
                    ]
                ]
            },
            "temporal": {
                "interval": [["2020-12-11T22:38:32.125Z", "2020-12-14T18:02:31.437Z"]]
            },
        },
        "license": "CC-BY-4.0",
        "summaries": {
            "platform": ["cool_sat1", "cool_sat2"],
            "constellation": ["ion"],
            "instruments": ["cool_sensor_v1", "cool_sensor_v2"],
            "gsd": {"minimum": 0.512, "maximum": 0.66},
            "eo:cloud_cover": {"minimum": 1.2, "maximum": 1.2},
            "proj:epsg": {"minimum": 32659, "maximum": 32659},
            "view:sun_elevation": {"minimum": 54.9, "maximum": 54.9},
            "view:off_nadir": {"minimum": 3.8, "maximum": 3.8},
            "view:sun_azimuth": {"minimum": 135.7, "maximum": 135.7},
        },
        "links": [
            {
                "rel": "root",
                "href": "./collection.json",
                "type": "application/json",
                "title": "Simple Example Collection",
            },
            {
                "rel": "item",
                "href": "./simple-item.json",
                "type": "application/geo+json",
                "title": "Simple Item",
            },
            {
                "rel": "item",
                "href": "./core-item.json",
                "type": "application/geo+json",
                "title": "Core Item",
            },
            {
                "rel": "item",
                "href": "./extended-item.json",
                "type": "application/geo+json",
                "title": "Extended Item",
            },
            {
                "rel": "self",
                "href": "https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0/examples/collection.json",
                "type": "application/json",
            },
        ],
    }


@pytest.fixture(scope="module")
def search_response():
    return {
        "type": "FeatureCollection",
        "stac_version": "1.0.0-beta.2",
        "stac_extensions": [],
        "context": {"page": 1, "limit": 10, "matched": 3337, "returned": 1},
        "numberMatched": 3337,
        "numberReturned": 1,
        "features": [
            {
                "stac_version": "1.0.0",
                "stac_extensions": [],
                "type": "Feature",
                "id": "20201211_223832_CS2",
                "bbox": [
                    172.91173669923782,
                    1.3438851951615003,
                    172.95469614953714,
                    1.3690476620161975,
                ],
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [172.91173669923782, 1.3438851951615003],
                            [172.95469614953714, 1.3438851951615003],
                            [172.95469614953714, 1.3690476620161975],
                            [172.91173669923782, 1.3690476620161975],
                            [172.91173669923782, 1.3438851951615003],
                        ]
                    ],
                },
                "properties": {"datetime": "2020-12-11T22:38:32.125000Z"},
                "collection": "simple-collection",
                "links": [],
                "assets": {
                    "visual": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "title": "3-Band Visual",
                        "roles": ["visual"],
                    },
                    "thumbnail": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
                        "title": "Thumbnail",
                        "type": "image/jpeg",
                        "roles": ["thumbnail"],
                    },
                },
            }
        ],
    }
