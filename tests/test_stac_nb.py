#!/usr/bin/env python

"""Tests for `stac_nb` package."""

from typing import Generator
from stac_nb import STAC_Query_UI


def test_stac_query_ui(collections_response):
    """Test UI initialization."""

    stac_api = "https://api/endpoint"

    ui = STAC_Query_UI(stac_api)

    assert len(ui.children) == 4
    assert ui.query_results is None
    assert ui.collections_w.options[0] == collections_response["collections"][0]["id"]


stac_api = "https://api/endpoint"


def test_display_ui(requests_mock, collection_response):
    """Test displaying the UI."""

    ui = STAC_Query_UI(stac_api)
    ui.display()

    assert True


def test_button_click(search_response):
    """Test UI button click."""

    ui = STAC_Query_UI(stac_api)
    assert ui.query_results is None

    ui.click_button(ui.query_btn_w)

    assert isinstance(ui.query_results, Generator)


def test_bbox(requests_mock, collection_response, search_response):
    """Test sending bbox in query."""

    ui = STAC_Query_UI(stac_api)
    assert ui.query_results is None
    ui.bbox_w.value = "-123,45,-124,46"

    ui.click_button(ui.query_btn_w)
    assert isinstance(ui.query_results, Generator)


def test_ids(requests_mock, collection_response, search_response):
    """Test sending ids in query."""

    ui = STAC_Query_UI(stac_api)
    assert ui.query_results is None
    ui.ids_w.value = "20201211_223832_CS2, another_id"

    ui.click_button(ui.query_btn_w)
    assert isinstance(ui.query_results, Generator)


def test_print_query(requests_mock, capfd, collection_response, search_response):
    """Test showing query."""

    ui = STAC_Query_UI(stac_api)
    assert ui.query_results is None
    ui.show_query_w.value = True

    ui.click_button(ui.query_btn_w)

    out, err = capfd.readouterr()
    assert "QUERY" in out
    assert not err

    assert isinstance(ui.query_results, Generator)
