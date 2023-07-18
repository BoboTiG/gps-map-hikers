"""
GPS Map for Hikers.
Script maintained by Mickaël Schoentgen <contact@tiger-222.fr>.
"""

import json
import time
from pathlib import Path

from bottle import default_app, redirect, request, route, static_file, template

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

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
CURRENT_TRIP = ROOT / "traces" / "2023-pyrenees"
SOS = ROOT / "sos"
VIEWS = ROOT / "views"


def get_all_traces(folder=CURRENT_TRIP):
    """Retrieve all recorded traces."""
    traces = []
    for file in sorted(folder.glob("*.json")):
        data = json.loads(file.read_text())
        data["date"] = time.strftime("%d/%m/%Y à %H:%M:%S", time.localtime(int(file.stem)))
        traces.append(data)
    return adapt_traces(traces)


def adapt_traces(traces):
    """
    Adapt traces details.
    Traces without relevant data are ignored.

    Trace data:
        - alt: altitude
        - date
        - dist: distance since last trace
        - lat: latitude
        - lon: longitude
        - speed
        - tdist: total distance since the begining
        - tdist2: total distance since the pause, or the begining if none
        - type: start | end | pause | in-between | sos-past | sos
    """
    if not traces:
        return traces

    fmt_traces = []
    total_distance = 0.0
    total_distance_since_last_pause = 0.0
    first, last = traces[0], traces[-1]

    for trace in traces:
        fmt_trace = {
            "alt": trace["alt"],
            "date": trace["date"],
            "lat": trace["lat"],
            "lon": trace["lon"],
            "dist": 0.0,
            "speed": 0.0,
            "tdist": 0.0,
            "tdist2": 0.0,
        }

        if trace == first:
            # First trace
            fmt_trace["type"] = "start"
        elif trace["dist"] + trace["speed"] + trace["alt"] == 0.0:
            # No information, lets skip it then
            continue
        else:
            total_distance += trace["dist"]
            total_distance_since_last_pause += trace["dist"]
            fmt_trace["dist"] = trace["dist"]
            fmt_trace["tdist"] = total_distance
            fmt_trace["tdist2"] = total_distance_since_last_pause
            fmt_trace["speed"] = trace["speed"]

            if trace["sos"]:
                # Emergency!
                fmt_trace["type"] = "sos"
            elif trace == last:
                # Last trace
                fmt_trace["type"] = "end"
                total_distance_since_last_pause = 0.0
            elif not trace["dist"]:
                # Continuing the trip, maybe after the night, or a long pause
                fmt_trace["type"] = "pause"
                total_distance_since_last_pause = 0.0
            else:
                # Normal trace, we are moving
                fmt_trace["type"] = "in-between"

        fmt_traces.append(fmt_trace)

    return check_for_sos(fmt_traces)


def check_for_sos(traces):
    """
    Adapt traces for emergencies.

    Trace data that may be updated:
        - type: sos-past
    """
    start = -1
    for idx, trace in enumerate(traces):
        if trace["type"] == "sos":
            if start == -1:
                start = idx
            continue
        if start > -1:
            for i in range(start, idx):
                traces[i]["type"] = "sos-past"
            start = -1

    return traces


def emergency_ongoing():
    """Check the current emergency state."""
    return SOS.is_file()


@route("/assets/<file:path>", method="GET")
def asset(file):
    """Get a resource file used by the website."""
    return static_file(file, root=ASSETS)


@route("/robots.txt", method="GET")
def robots():
    """Get the robots.txt file (for search engine crawlers)."""
    return static_file("robots.txt", root=ROOT)


@route("/", method="GET")
def home():
    """Display the home page with the map."""
    return template(
        "home",
        traces=get_all_traces(),
        emergency_ongoing=emergency_ongoing(),
        template_lookup=[VIEWS],
    )


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

    file = CURRENT_TRIP / f"{params.epoch}.json"
    if file.is_file():
        # The app may send the same trace several times
        return

    data = {
        "alt": float(params.alt),
        "dist": float(params.dist),
        "lat": float(params.lat),
        "lon": float(params.lon),
        "speed": float(params.speed),
        "sos": SOS.is_file(),
    }
    file.write_text(json.dumps(data))


@route("/ok", method="GET")
def emergency_done():
    """Stop the SOS signal."""
    SOS.unlink(missing_ok=True)
    redirect("/")


@route("/sos", method="GET")
def emergency():
    """Start a SOS signal."""
    if not emergency_ongoing():
        SOS.write_text(time.strftime("%d/%m/%Y à %H:%M:%S", time.localtime(time.time())))
    redirect("/")


application = default_app()
