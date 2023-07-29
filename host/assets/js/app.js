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
        "in-between": new_icon('blue', 'small'),
        "pause": new_icon('yellow', 'small'),
        "start": new_icon('yellow', 'normal'),
        "sos": new_icon('red', 'normal'),
        "sos-past": new_icon('red', 'small'),
    },

    // Cartes
    attrib = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    title_layer_options = {maxZoom: 19, updateWhenZooming: false, updateWhenIdle: true},
    maps = {
        'OpenStreetMap': L.tileLayer(
            'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: attrib,
                ...title_layer_options,
            }
        ),
        'OpenStreetMap II': L.tileLayer(
            'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
                attribution: attrib,
                ...title_layer_options,
            }
        ),
        'CartoDB': L.tileLayer(
            'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
                attribution: attrib + ', map tiles bt <a href="http://cartodb.com/attributions">CartoDB</a>',
                ...title_layer_options,
            }
        ),
        'Watercolor': L.tileLayer(
            'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {
                attribution: attrib + ', map tiles by <a href="http://stamen.com">Stamen Design</a>',
                ...title_layer_options,
            }
        ),
    },
    map = L.map('map', {layers: maps['OpenStreetMap'], preferCanvas: true}).setView({lat: last.lat, lon: last.lon}, 13),
    is_int = function(n) {
        return n % 1 === 0;
    },
    number_format = function(number) {
        let value = number.toFixed(is_int(number) ? 0 : 2 ); 
        return value.replace(/(\d)(?=(\d{3})+\.)/g, '$1 ').replace(".", ",");
    };

L.control.layers(maps).addTo(map);
L.control.scale({imperial: false, position: 'topright'}).addTo(map,);

traces.forEach(function(trace) {
    const position = {lat: trace.lat, lon: trace.lon};
    let text = '<p style="text-align:center">';

    journey.push(position);

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
    marker.bindPopup(text);
    if (trace == last) {
        marker.openPopup();
    }
});

L.Routing.control({
    waypoints: journey,
    addWaypoints: false,  // Ne pas créer de nouveaux points lors d'un clic sur le trajet
    createMarker: function() {},  // Ne pas remplacer nos icônes
    lineOptions: {
        styles: [{color: 'black', opacity: 0.15, weight: 9},
                 {color: 'white',opacity: 0.8, weight: 6},
                 {color: 'blue', opacity: 0.4, weight: 3}]
    },
}).addTo(map);

// Affichage jour/nuit suivant l'heure courante
terminator = L.terminator().addTo(map);
map.addEventListener('zoomstart movestart popupopen', function(e) {
    terminator.setTime();
});

