var journey = [],
    first = positions[0],
    last = positions[positions.length - 1],
    previous_distance = 0.0,
    total_distance = 0.0,

    // Icônes
    green = new L.Icon({
        iconUrl: 'assets/css/images/marker-icon-2x-green.png',
        shadowUrl: 'assets/css/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    }),
    yellow = new L.Icon({
        iconUrl: 'assets/css/images/marker-icon-2x-yellow.png',
        shadowUrl: 'assets/css/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    }),
    blue = new L.Icon({
        iconUrl: 'assets/css/images/marker-icon-2x.png',
        shadowUrl: 'assets/css/images/marker-shadow.png',
        iconSize: [18, 30],
        iconAnchor: [12, 30],
        popupAnchor: [-2, -24],
        shadowSize: [30, 30]
    }),

    // Cartes
    attrib = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    title_layer_options = {maxZoom: 22, updateWhenZooming: false, updateWhenIdle: true},
    osm = L.tileLayer(
       'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: attrib,
        ...title_layer_options,
    }),
    osm_hot = L.tileLayer(
        'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: attrib,
        ...title_layer_options,
    }),
    watercolor = L.tileLayer(
        'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {
        attribution: attrib + ', map tiles by <a href="http://stamen.com">Stamen Design</a>',
        ...title_layer_options,
    }),
    cartoon = L.tileLayer(
        'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: attrib + ', map tiles bt <a href="http://cartodb.com/attributions">CartoDB</a>',
        ...title_layer_options,
    }),
    maps = {
        'OpenStreetMap': osm,
        'OpenStreetMap II': osm_hot,
        'Carto': cartoon,
        'Watercolor': watercolor,
    },
    map = L.map('map', {layers: [osm], preferCanvas: true}).setView(last.pos, 13),
    is_int = function(n) {
        return n % 1 === 0;
    },
    number_format = function(number) {
        let value = number.toFixed(is_int(number) ? 0 : 2 ); 
        return value.replace(/(\d)(?=(\d{3})+\.)/g, '$1 ').replace(".", ",");
    };

L.control.layers(maps).addTo(map);

positions.forEach(function(position) {
    let opt = {icon: blue},
        text = '<p style="text-align:center">';

    if (position == first) {
        // Premier marqueur
        opt = {icon: yellow};
        text += '<b>Top départ !</b> 🚥';
    } else if (position == last) {
        // Dernier marqueur
        opt = {icon: green};
        text += '<b>Nous en sommes là !</b>';
    } else if (!position.pos.speed && !position.pos.alt && !position.pos.dist) {
        // Auncune information, on zappe
        return true;
    } else if (!position.pos.dist) {
        // On repart, sûrement après une longue pause (genre le lendemain)
        opt = {icon: yellow};
        text += '<b>Et c’est reparti !</b> 🚦';
    }

    journey.push(position.pos);

    if (position.pos.speed) {
        text += '<br>🚀 ' + number_format(position.pos.speed) + ' km/h';
    }
    if (position.pos.alt) {
        text += '<br>⛰ ' + number_format(parseInt(position.pos.alt)) + ' m';
    }
    if (position.pos.dist) {
        previous_distance = position.pos.dist;
        text += '<br>🚩 ' + number_format((total_distance + position.pos.dist) / 1000) + ' km';
    } else if (!position.pos.dist || position == last) {
        total_distance += previous_distance;
        if (total_distance) {
            text += '<br>🚩 ' + number_format(total_distance / 1000) + ' km';
        }
    }
    text += '<br><br><small>' + position.date + '</small></p>';

    let marker = L.marker(position.pos, opt).addTo(map);
    marker.bindPopup(text);
    if (position == last) {
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
