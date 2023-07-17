"""
GPS Map for Hikers.
Script maintained by Mickaël Schoentgen <contact@tiger-222.fr>.
"""

import json
import locale
import sys
import time
from pathlib import Path

from bottle import request, route, run, static_file, template

__version__ = "1.1.0"
__author__ = "Mickaël Schoentgen"
__copyright__ = """
Copyright (c) 2021-2023, Mickaël 'Tiger-222' Schoentgen

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby
granted, provided that the above copyright notice appear in all copies
and that both that copyright notice and this permission notice appear
in supporting documentation or portions thereof, including
modifications, that you make.
"""

CURRENT_TRIP = "2023-pyrenees"


def get_all_traces():
    """Retrieve all recorded traces."""
    folder = Path("traces") / CURRENT_TRIP
    traces = []
    for file in sorted(folder.glob("*.json")):
        data = json.loads(file.read_text())
        data["date"] = time.strftime(
            "%d/%m/%Y à %H:%M:%S", time.localtime(int(file.stem))
        )
        traces.append(data)
    return traces


@route("/assets/<file:path>", method="GET")
def asset(file):
    """Get a resource file used by the website."""
    return static_file(file, root="assets")


@route("/", method="GET")
def home():
    """Display the home page with the map."""
    return template("home", traces=get_all_traces())


@route("/log", method="GET")
def new_trace():
    """
    A new trace is sent for recording.
    All details are here: https://gpslogger.app/#usingthecustomurlfeature

    Current URL set in GPSLogger:
        /log?lat=%LAT&lon=%LON&alt=%ALT&epoch=%TIMESTAMP&dist=%DIST&speed=%SPD

    Example:
        /log?lat=49.08291963&lon=6.18369653&alt=256.0&epoch=1615654079&dist=143&speed=0.0
    """
    params = request.query

    file = Path("traces") / CURRENT_TRIP / f"{params.epoch}.json"
    if file.is_file():
        # The app may send the same trace several times
        return

    data = {
        "alt": float(params.alt),
        "dist": float(params.dist),
        "lat": float(params.lat),
        "lon": float(params.lon),
        "speed": float(params.speed),
    }
    file.write_text(json.dumps(data))


def main():
    """Main logic."""

    # Set the locale to the system one for number formatting
    locale.setlocale(locale.LC_ALL, "")

    run(host="0.0.0.0", port=9999, reloader=True)


if __name__ == "__main__":
    sys.exit(main())
