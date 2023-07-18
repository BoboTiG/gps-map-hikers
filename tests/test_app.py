from unittest.mock import patch

import pytest
from boddle import boddle
from bottle import HTTPResponse

from host.app import asset, emergency, emergency_done, emergency_ongoing, home, new_trace, robots


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


def test_emergency():
    assert not emergency_ongoing()

    with pytest.raises(HTTPResponse):
        emergency()
    assert emergency_ongoing()

    with pytest.raises(HTTPResponse):
        emergency_done()
    assert not emergency_ongoing()


def test_new_trace_already_present(tmp_path):
    (tmp_path / "1689705170.json").write_text("")
    with patch("host.app.CURRENT_TRIP", tmp_path), boddle(query={"epoch": 1689705170}):
        new_trace()


def test_new_trace(tmp_path):
    with patch("host.app.CURRENT_TRIP", tmp_path), boddle(
        query={
            "epoch": 1689705170,
            "alt": 68.4,
            "dist": 459.0,
            "lat": 44.77042298298329,
            "lon": 0.7979252468794584,
            "speed": 0.0,
        }
    ):
        new_trace()
    assert (tmp_path / "1689705170.json").is_file()


#
