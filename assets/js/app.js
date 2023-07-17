var marker, opt, text,
    journey = [],
    first = positions[0],
    last = positions[positions.length - 1],

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
    osm = L.tileLayer(
       'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: attrib,
        updateWhenZooming: false,
        updateWhenIdle: true,
    }),
    osm_hot = L.tileLayer(
        'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: attrib,
        updateWhenZooming: false,
        updateWhenIdle: true,
    }),
    watercolor = L.tileLayer(
        'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {
        attribution: attrib + ', map tiles by <a href="http://stamen.com">Stamen Design</a>',
        updateWhenZooming: false,
        updateWhenIdle: true,
    }),
    cartoon = L.tileLayer(
        'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: attrib + ', map tiles bt <a href="http://cartodb.com/attributions">CartoDB</a>',
        updateWhenZooming: false,
        updateWhenIdle: true,
    }),
    maps = {
        'OpenStreetMap': osm,
        'OpenStreetMap II': osm_hot,
        'Carto': cartoon,
        'Watercolor': watercolor,
    },

    map = L.map('map', {layers: [osm], preferCanvas: true}).setView(last.pos, 13),
    number_format = function(number) {
        return number.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1 ').replace(".", ",");
    };

L.control.layers(maps).addTo(map);

positions.forEach(function(position) {
    opt = {icon: blue};
    text = '<p style="text-align:center">';
    if (position == first) {
        opt = {icon: yellow};
        text += '<b>Point de départ</b> 🚦';
    } else if (position == last) {
        opt = {icon: green};
        text += '<b>Nous en sommes là !</b>';
    } else if (!position.pos.speed && !position.pos.alt && !position.pos.dist) {
        return true;
    }

    if (position.pos.speed) {
        text += '<br>🚀 ' + position.pos.speed + ' km/s';
    }
    if (position.pos.alt) {
        text += '<br>⛰ ' + position.pos.alt + ' m';
    }
    if (position.pos.dist) {
        text += '<br>🚩 ' + position.pos.dist + ' m';
    }
    text += '<br><br><small>' + position.date + '</small></p>';

    journey.push(position.pos);

    marker = L.marker(position.pos, opt).addTo(map);
    marker.bindPopup(text);
    if (position == last) {
        marker.openPopup();
    }
});

var route = L.Routing.control({
    waypoints: journey,
    addWaypoints: false,  // Ne pas créer de nouveaux points lors d'un clic sur le trajet
    createMarker: function() {},  // Ne pas remplacer nos icônes
    lineOptions: {
        styles: [{color: 'black', opacity: 0.15, weight: 9},
                 {color: 'white',opacity: 0.8, weight: 6},
                 {color: 'blue', opacity: 0.4, weight: 3}]
    },
}).addTo(map);

route.on('routesfound', function(e) {
    const distance = e.routes[0].summary.totalDistance;
    console.log('Distance totale parcourue :', number_format(distance / 1000), 'km.');
});
