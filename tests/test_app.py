from unittest.mock import patch

import pytest
from boddle import boddle
from bottle import HTTPResponse

from host import app

app.SLEEP_SEC = 0


def test_asset():
    response = app.asset("css/images/layers.png")
    assert response.status_code == 200
    assert response.content_type == "image/png"


def test_home_no_traces(tmp_path):
    with patch("host.app.TRACES", tmp_path):
        content = app.home()
    assert "La carte sera affichée" in content


def test_home(tmp_path):
    (tmp_path / "1689705170.json").write_text('{"alt": 0.0, "lat": 0.0, "lon": 0.0}')
    with patch("host.app.TRACES", tmp_path):
        content = app.home()
    assert "<title>Trek</title>" in content
    assert "var traces = [" in content


def test_robots():
    response = app.robots()
    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=UTF-8"


def test_favicon():
    response = app.favicon()
    assert response.status_code == 200
    assert response.content_type == "image/png"


def test_emergency():
    assert not app.emergency_ongoing()

    with boddle(auth=(app.USER, app.PWD)), pytest.raises(HTTPResponse):
        app.emergency()
    assert app.emergency_ongoing()

    with boddle(auth=(app.USER, app.PWD)), pytest.raises(HTTPResponse):
        app.emergency_done()
    assert not app.emergency_ongoing()


def test_new_trace_already_present(tmp_path):
    (tmp_path / "1689705170.json").write_text("")
    with (
        patch("host.app.TRACES", tmp_path),
        boddle(auth=(app.USER, app.PWD), query={"epoch": 1689705170}),
    ):
        app.new_trace()


def test_new_trace(tmp_path):
    with (
        patch("host.app.TRACES", tmp_path),
        boddle(
            auth=(app.USER, app.PWD),
            query={
                "epoch": 1689705170,
                "alt": 68.4,
                "dist": 459.0,
                "lat": 44.77042298298329,
                "lon": 0.7979252468794584,
                "speed": 0.0,
            },
        ),
    ):
        app.new_trace()
    assert (tmp_path / "1689705170.json").is_file()


def test_picture_form_no_traces(tmp_path):
    with (
        patch("host.app.TRACES", tmp_path),
        pytest.raises(HTTPResponse),
        boddle(auth=(app.USER, app.PWD)),
    ):
        app.picture_form()


def test_picture_form(tmp_path):
    (tmp_path / "1689705170.json").write_text('{"pic": "", "ts": 1689705170}')

    with (
        patch("host.app.TRACES", tmp_path),
        boddle(auth=(app.USER, app.PWD)),
    ):
        content = app.picture_form()
        assert "<title>Trek | Photo</title>" in content
        assert '<form action="picture/upload"' in content


def test_upload_picure_no_trace():
    with (
        pytest.raises(HTTPResponse),
        boddle(auth=(app.USER, app.PWD), params={"trace": "123"}),
    ):
        app.picture_upload()


def test_upload_picure(tmp_path):
    pytest.skip("boddle does not support mocking requests.files")

    pictures = tmp_path / "pictures"
    pictures.mkdir()
    (tmp_path / "1689705170.json").write_text("")

    # from io import BytesIO

    # jpg = BytesIO(b"data")

    with (
        patch("host.app.TRACES", tmp_path),
        patch("host.app.PICTURES", pictures),
        pytest.raises(HTTPResponse),
        boddle(auth=(app.USER, app.PWD), query={"trace": "1689705170"}, files=...),
    ):
        app.picture_upload()

    assert (pictures / "1689705170.jpg").is_file()


def test_picture_get(tmp_path):
    pictures = tmp_path / "pictures"
    pictures.mkdir()
    (pictures / "1689705170.jpg").write_bytes(b"data")

    with patch("host.app.PICTURES", pictures):
        response = app.picture_get("1689705170.jpg")
        assert response.status_code == 200
        assert response.content_type == "image/jpeg"
