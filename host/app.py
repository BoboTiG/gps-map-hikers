"""
GPS Map for Hikers.
Script maintained by Mickaël Schoentgen <contact@tiger-222.fr>.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from bottle import HTTPResponse, auth_basic, default_app, redirect, request, route, static_file, template

__version__ = "1.2.0"
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
TRACES = ROOT / "traces"
PICTURES = TRACES / "pictures"
SOS = ROOT / "sos"
VIEWS = ROOT / "views"
USER, PWD = (ROOT / "basic_auth.txt").read_text().strip().split(":", 1)
SLEEP_SEC = 2

PICTURES.mkdir(exist_ok=True, parents=True)


def get_timezone(folder: Path) -> ZoneInfo:
    file = folder / "tz.txt"
    return ZoneInfo(file.read_text().strip() if file.is_file() else "Europe/Paris")


def is_authenticated_user(user: str, password: str) -> bool:
    time.sleep(SLEEP_SEC)
    return user == USER and password == PWD


def get_all_traces(folder: Path | None = None) -> list[dict]:
    """Retrieve all recorded traces."""
    folder = folder or TRACES
    pictures = sorted((folder / "pictures").glob("*.*"))
    folder_prefix = str(folder)
    tz = get_timezone(folder)

    traces = []
    for file in sorted(folder.glob("*.json")):
        data = json.loads(file.read_text())
        data["ts"] = int(file.stem)
        data["date"] = datetime.fromtimestamp(int(file.stem), tz=tz).isoformat(sep=" ", timespec="seconds")
        data["pic"] = str(next((p for p in pictures if p.stem == file.stem), "")).removeprefix(folder_prefix)
        traces.append(data)
    return traces


def adapt_traces(traces: list[dict]) -> list[dict]:
    """
    Adapt traces details.
    Traces without relevant data are ignored.

    Trace data:
        - alt: altitude
        - date: converted to a string at expected timezone (see `get_timezone()`)
        - dist: distance since last trace
        - lat: latitude
        - lon: longitude
        - pic: optional picture
        - speed
        - tdist: total distance since the begining
        - tdist2: total distance since the pause, or the begining if none
        - ts: timestamp of the raw date
        - type: start | end | pause | step | sos-past | sos
    """
    if not traces:
        return traces

    traces = fix_distance(traces)

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
            "pic": trace["pic"],
            "ts": trace["ts"],
            "dist": 0.0,
            "speed": 0.0,
            "tdist": 0.0,
            "tdist2": 0.0,
        }

        if trace == first:
            # First trace
            fmt_trace["type"] = "start"
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
            elif not trace["dist"]:
                # Continuing the trip, maybe after the night, or a long pause
                fmt_trace["type"] = "pause"
                total_distance_since_last_pause = 0.0
            else:
                # Normal trace, we are moving
                fmt_trace["type"] = "step"

        fmt_traces.append(fmt_trace)

    fmt_traces = check_for_sos(fmt_traces)
    fmt_traces = fix_speed(fmt_traces)

    return fmt_traces


def check_for_sos(traces: list[dict]) -> list[dict]:
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


def fix_distance(traces: list[dict]) -> list[dict]:
    """
    Adapt traces distance.

    Trace data that may be updated:
        - type: dist
    """
    for idx in range(len(traces) - 1, 1, -1):
        if not traces[idx]["dist"]:
            continue
        diff = traces[idx]["dist"] - traces[idx - 1]["dist"]
        traces[idx]["dist"] = diff
    return traces


def fix_speed(traces: list[dict]) -> list[dict]:
    """
    Adapt traces speed.

    Trace data that may be updated:
        - type: speed
    """
    for previous, current in zip(traces, traces[1:]):
        if not current["dist"]:
            continue
        elapsed = current["ts"] - previous["ts"]
        meters_per_sec = current["dist"] / elapsed
        current["speed"] = meters_per_sec * 3.6

    return traces


def emergency_ongoing() -> bool:
    """Check the current emergency state."""
    return SOS.is_file()


@route("/assets/<file:path>", method="GET")
def asset(file: str) -> HTTPResponse:
    """Get a resource file used by the website."""
    return static_file(file, root=ASSETS)


@route("/favicon.png", method="GET")
def favicon() -> HTTPResponse:
    """Get the favicon file."""
    return static_file("favicon.png", root=ASSETS)


@route("/robots.txt", method="GET")
def robots() -> HTTPResponse:
    """Get the robots.txt file (for search engine crawlers)."""
    return static_file("robots.txt", root=ASSETS)


@route("/", method="GET")
def home() -> str:
    """Display the home page with the map."""
    return template(
        "home",
        traces=adapt_traces(get_all_traces()),
        emergency_ongoing=emergency_ongoing(),
        template_lookup=[VIEWS],
    )


@route("/picture", method="GET")
@auth_basic(is_authenticated_user)
def picture_form() -> str:
    """Upload picture form."""
    if not (traces := get_all_traces()):
        redirect("/")
    return template("picture", traces=traces, template_lookup=[VIEWS])


@route("/picture/upload", method="POST")
@auth_basic(is_authenticated_user)
def picture_upload() -> None:
    """Upload a picture."""
    trace = request.forms["trace"]
    if not (TRACES / f"{trace}.json").is_file():
        redirect("/picture")

    PICTURES.mkdir(exist_ok=True, parents=True)

    upload = request.files["picture"]
    picture = Path(upload.filename)
    ext = picture.suffix.lower().replace("jpeg", "jpg")
    file = PICTURES / f"{trace}{ext}"
    with file.open(mode="wb") as fh:
        upload.save(fh)

    redirect("/")


@route("/pictures/<picture:path>", method="GET")
def picture_get(picture: str) -> HTTPResponse:
    """Get a picture file."""
    return static_file(picture, root=PICTURES)


@route("/log", method="GET")
@auth_basic(is_authenticated_user)
def new_trace() -> None:
    """
    A new trace is sent for recording.
    All details are here: https://gpslogger.app/#usingthecustomurlfeature

    Current URL set in GPSLogger:
        /log?lat=%LAT&lon=%LON&alt=%ALT&epoch=%TIMESTAMP&dist=%DIST&speed=%SPD

    Example:
        /log?lat=49.08291963&lon=6.18369653&alt=256.0&epoch=1615654079&dist=143&speed=0.0
    """
    params = request.query

    file = TRACES / f"{params.epoch}.json"
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
@auth_basic(is_authenticated_user)
def emergency_done() -> None:
    """Stop the SOS signal."""
    SOS.unlink(missing_ok=True)
    redirect("/")


@route("/sos", method="GET")
@auth_basic(is_authenticated_user)
def emergency() -> None:
    """Start a SOS signal."""
    if not emergency_ongoing():
        SOS.write_text(time.strftime("%d/%m/%Y à %H:%M:%S", time.localtime(time.time())))
    redirect("/")


application = default_app()
