# GPS Map for Hikers

Beautiful map using those awesome free and open-source softwares:

- [GPSLogger](https://github.com/mendhak/gpslogger)
- [Leaflet](https://leafletjs.com/)
  - [Leaflet.Terminator](https://github.com/joergdietrich/Leaflet.Terminator) (day/night regions)
  - [leaflet-ui](https://github.com/Raruto/leaflet-ui) (UI)

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

### Security

Several endpoints are protected by a user/password combination.
Credentials are to be set in the `host/basic_auth.txt` file using that format: `user:password`.

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
