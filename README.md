# GPS Map for Hikers

Beautiful map using [Leaflet](https://leafletjs.com/) and [GPSLogger](https://github.com/mendhak/gpslogger).

## Installation

```console
$ python3.11 -m venv venv
$ . venv/bin/activate
$ python -m pip install -U pip
$ python -m pip install -r requirements-dev.txt
```

## Development

```console
$ python -m isort server.py
$ python -m black server.py
$ python -m flake8 server.py
```

## Running the Server

With a hammer:

```bash
while true; do python server.py || true; done
```
