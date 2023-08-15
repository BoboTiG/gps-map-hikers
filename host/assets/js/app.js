var journey = [],
    last = traces[traces.length - 1],

    // Icônes
    new_icon = function(color, size) {
        return new L.Icon({
            iconUrl: 'assets/css/images/marker-' + color + '.png',
            shadowUrl: '',
            iconSize: size == 'small' ? [18, 30] : [25, 41],
            iconAnchor: size == 'small' ? [12, 30] : [12, 41],
            popupAnchor: size == 'small' ? [-2, -24] : [1, -34],
            shadowSize: size == 'small' ? [30, 30] : [41, 41]
        });
    },
    marker_color = {
        "end": new_icon('green', 'normal'),
        "step": new_icon('blue', 'small'),
        "pause": new_icon('yellow', 'small'),
        "start": new_icon('yellow', 'normal'),
        "sos": new_icon('red', 'normal'),
        "sos-past": new_icon('red', 'small'),
    },

    // Carte
    map = L.map(
        'map',
        {
            attributionControl: false,
            center: [last.lat, last.lon],
            editInOSMControl: false,
            fullscreenControl: false,
            gestureHandling: false,
            locateControl: false,
            mapTypeId: 'satellite',
            mapTypeIds: ['streets', 'satellite', 'topo'],
            minimapControl: false,
            pegmanControl: false,
            preferCanvas: true,
            rotate: false,
            searchControl: false,
            zoom: 13,
        }
    ),
    is_int = function(n) {
        return n % 1 === 0;
    },
    number_format = function(number) {
        let value = number.toFixed(is_int(number) ? 0 : 2 ); 
        return value.replace(/(\d)(?=(\d{3})+\.)/g, '$1 ').replace(".", ",");
    },
    markers = [],
    show_traces = function (with_media_only) {
        // Remove current markers, if any
        markers.forEach(function(marker) {
            map.removeLayer(marker);
        });

        traces.forEach(function(trace) {
            const position = {lat: trace.lat, lon: trace.lon};

            journey.push(position);

            if (with_media_only && !trace.pic) {
                return;
            }

            let text = '<p style="text-align:center">';
        
            if (trace.type == 'sos') {
                text += '<b class="blink red">SOS</b><br>';
                text += 'Lat/Lon : ' + position.lat.toFixed(4) + ' / ' + position.lon.toFixed(4) + '<br>';
            } else if (trace.type == 'sos-past') {
                text += '<b>🦺 Hors de danger !</b><br>';
            } else if (trace.type == 'start') {
                text += '<b>Top départ !</b> 🚥<br>';
            } else if (trace.type == 'end') {
                text += '<b>Nous en sommes là !</b><br>';
            } else if (trace.type == 'pause') {
                text += '<b>Et c’est reparti !</b> 🚦<br>';
            }
        
            if (trace.speed) {
                text += '<br>🚀 ' + number_format(trace.speed) + ' km/h';
            }
            if (trace.alt) {
                text += '<br>⛰ ' + number_format(parseInt(trace.alt)) + ' m';
            }
            if (trace.dist) {
                text += '<br>⛳ ' + number_format(trace.dist / 1000) + ' km';
            }
            if (trace.tdist2) {
                text += '<br>🚩 ' + number_format(trace.tdist2 / 1000) + ' km';
            }
            if (trace.tdist) {
                text += '<br>🏁 ' + number_format(trace.tdist / 1000) + ' km';
            }
            if (trace.pic) {
                text += '<br><br>📷 <a href="' + trace.pic + '" target="_blank">Photo</a>';
            }
            text += '<br><br><small>' + trace.date + '</small></p>';
        
            let marker = L.marker(position, {icon: marker_color[trace.type]}).addTo(map);
            markers.push(marker);
            marker.bindPopup(text);
        })
    };

// Option - Afficher seulement les marqueurs ayant un média
L.Control.OptionMarkerWithMediaOnly = L.Control.extend({
    onAdd: function(map) {
        let div = L.DomUtil.create('div'),
            a = L.DomUtil.create('a');
        const txt_all = '📷',
            txt_media_only = '📸';

        a.title = "Afficher seulement les marqueurs contenant un media";
        a.style.fontSize = '2em';
        a.style.cursor = 'pointer';
        a.text = txt_all;
        L.DomEvent.on(a, 'click', function() {
            if (a.text == txt_all) {
                a.text = txt_media_only;
                show_traces(true);
            } else {
                a.text = txt_all;
                show_traces(false);
            }
        });
        div.appendChild(a);
        return div;
    }
});
L.control.option_marker_with_media_only = function(opts) {
    return new L.Control.OptionMarkerWithMediaOnly(opts);
}
L.control.option_marker_with_media_only({ position: 'topright' }).addTo(map);

// Affichage jour/nuit suivant l'heure courante
terminator = L.terminator().addTo(map);
map.addEventListener('zoomstart movestart popupopen', function(e) {
    terminator.setTime();
});

// Afficher les marqueurs
show_traces(false);

// L.Routing.control({
//     waypoints: journey,
//     addWaypoints: false,  // Ne pas créer de nouveaux points lors d'un clic sur le trajet
//     createMarker: function() {},  // Ne pas remplacer nos icônes
//     lineOptions: {
//         styles: [{color: 'black', opacity: 0.15, weight: 9},
//                  {color: 'white',opacity: 0.8, weight: 6},
//                  {color: 'blue', opacity: 0.4, weight: 3}]
//     },
//     router: new L.Routing.OSRMv1({
//         serviceUrl: 'https://router.project-osrm.org/route/v1',
//         profile: 'trip',
//         timeout: 30 * 1000,
//         routingOptions: {
//             alternatives: false,
//             steps: false,
//             a: 'b',
//         },
//         useHints: false,
//         suppressDemoServerWarning: true,
//         language: 'en',
//     }),
// }).addTo(map);
