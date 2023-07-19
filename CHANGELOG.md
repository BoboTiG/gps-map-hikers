## 1.1.0

`2023-07-20`

- Improve map rendering with lot of markers (closes #1).
- Capability to fire/stop a SOS signal (closes #3).
- Display more details in the marker's bubble (closes #2) (closes #4).
- Possibility to attach a picture to a marker (closes #5).
- Display a proper message when there is no trace.
- Improve the marker bubble design.
- Add a nice legend.
- Allow to zoom even more to see all details.
- The map will show different colors depending on the day/night (an old idea from the kewy-trip in 2016!)
- Set a generic website title (*Trek*).
- Use a cool font family for the website ([Victor Mono](https://rubjo.github.io/victor-mono/)).
- Website endpoints with write access are now protected.
- Prevent search engine crawlers to browse the website.
- [dev] Moved the traces logic from JS to Python.
- [dev] Adjust the code to fit into PythonAnywhere hosting.
- [dev] Keep a copy of the marker icon source.
- [dev] Introduce developement dependencies to lint, and test, the code.
- [dev] Ignore trace details (keep only a final ZIP'ed file containing all traces).
- [dev] Add JS dependency `leaflet-terminator` `1.1.0` to display differents colors given the current hour.
- [dev] Upgrade JS dependency `leaflet` from `1.7.1` to `1.9.4`.
- [dev] Upgrade JS dependency `leaflet-routing-machine` from `3.2.0` to `3.2.12`.
- [dev] Upgrade Python dependency `bottle` from `0.12.19` to `0.12.25`.
- [dev] Add Python dependency `paste` `3.5.3` to serve the local HTTP server.

## 1.0.0

`2021-03-13`

- Initial version.
