# GPS Map for Hikers

Beautiful map using [Leaflet](https://leafletjs.com/) and [GPSLogger](https://github.com/mendhak/gpslogger).

## Production

Copy all files from the `host` folder to the [PythonAnywhere](https://www.pythonanywhere.com) hosting account.

Details:
- Python version: `3.10`
- Force HTTPS: enabled
- Web app type: Bottle

## Development

### Installation

```console
$ python3.11 -m venv venv
$ . venv/bin/activate
$ python -m pip install -U pip
$ python -m pip install -r requirements-dev.txt
```

### Quality

```console
$ ./checks.sh
```

### Tests

```console
$ python -m pytest
```

### Local Server

```console
$ python server.py
```
