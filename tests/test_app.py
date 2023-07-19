from unittest.mock import patch

import pytest
from boddle import boddle
from bottle import HTTPResponse

from host.app import (
    PWD,
    USER,
    asset,
    emergency,
    emergency_done,
    emergency_ongoing,
    favicon,
    home,
    new_trace,
    picture_form,
    picture_get,
    picture_upload,
    robots,
)


def test_asset():
    response = asset("css/images/layers.png")
    assert response.status_code == 200
    assert response.content_type == "image/png"


def test_home():
    content = home()
    assert "<title>Trek</title>" in content
    assert "var traces = [" in content


def test_robots():
    response = robots()
    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=UTF-8"


def test_favicon():
    response = favicon()
    assert response.status_code == 200
    assert response.content_type == "image/png"


def test_emergency():
    assert not emergency_ongoing()

    with boddle(auth=(USER, PWD)), pytest.raises(HTTPResponse):
        emergency()
    assert emergency_ongoing()

    with boddle(auth=(USER, PWD)), pytest.raises(HTTPResponse):
        emergency_done()
    assert not emergency_ongoing()


def test_new_trace_already_present(tmp_path):
    (tmp_path / "1689705170.json").write_text("")
    with (
        patch("host.app.CURRENT_TRIP", tmp_path),
        boddle(auth=(USER, PWD), query={"epoch": 1689705170}),
    ):
        new_trace()


def test_new_trace(tmp_path):
    with (
        patch("host.app.CURRENT_TRIP", tmp_path),
        boddle(
            auth=(USER, PWD),
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
        new_trace()
    assert (tmp_path / "1689705170.json").is_file()


def test_picture_form():
    with boddle(auth=(USER, PWD)):
        content = picture_form()
        assert "<title>Trek | Photo</title>" in content
        assert '<form action="picture/upload"' in content


def test_upload_picure_no_trace():
    with (
        pytest.raises(HTTPResponse),
        boddle(auth=(USER, PWD), params={"trace": "123"}),
    ):
        picture_upload()


def test_upload_picure(tmp_path):
    pytest.skip("boddle does not support mocking requests.files")

    pictures = tmp_path / "pictures"
    pictures.mkdir()
    (tmp_path / "1689705170.json").write_text("")

    # from io import BytesIO

    # jpg = BytesIO(b"data")

    with (
        patch("host.app.CURRENT_TRIP", tmp_path),
        patch("host.app.PICTURES", pictures),
        pytest.raises(HTTPResponse),
        boddle(auth=(USER, PWD), query={"trace": "1689705170"}, files=...),
    ):
        picture_upload()

    assert (pictures / "1689705170.jpg").is_file()


def test_picture_get(tmp_path):
    pictures = tmp_path / "pictures"
    pictures.mkdir()
    (pictures / "1689705170.jpg").write_bytes(b"data")

    with patch("host.app.PICTURES", pictures):
        response = picture_get("1689705170.jpg")
        assert response.status_code == 200
        assert response.content_type == "image/jpeg"
