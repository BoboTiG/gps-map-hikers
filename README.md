# GPS Map for Hikers

Beautiful map using [Leaflet](https://leafletjs.com/) and [GPSLogger](https://github.com/mendhak/gpslogger).

## Adventure

For each hiking adventure, GPS traces & medias will be stored into the "traces" folders.
You don't have to deal with those folders.

If you need to set a timezone different from *Europe/Paris*, then create the `traces/tz.txt` file with the content of the expected timezone.

For instance, an adventure taking place in the North of the New Zealand, the appropriate timezone would be [*Pacific/Auckland*](https://github.com/python/tzdata/blob/master/src/tzdata/zoneinfo/Pacific/Auckland). For that example, you would put `Pacific/Auckland` into the `traces/tz.txt` file.

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
