var marker, opt, text,
    journey = [],
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
        attribution: attrib
    }),
    osm_hot = L.tileLayer(
        'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: attrib
    }),
    watercolor = L.tileLayer(
        'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {
        attribution: attrib + ', map tiles by <a href="http://stamen.com">Stamen Design</a>'
    }),
    cartoon = L.tileLayer(
        'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: attrib + ', map tiles bt <a href="http://cartodb.com/attributions">CartoDB</a>'
    }),
    maps = {
        'OpenStreetMap': osm,
        'OpenStreetMap II': osm_hot,
        'Carto': cartoon,
        'Watercolor': watercolor,
    },

    map = L.map('map', {layers: [osm]}).setView(last.pos, 13),
    number_format = function(number) {
        return number.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1 ').replace(".", ",");
    };

L.control.layers(maps).addTo(map);

positions.forEach(function(position) {
    journey.push(position.pos);

    opt = {icon: yellow};
    text = '';
    if (position == last) {
        opt = {icon: green}
        text = '<p style="text-align:center">Nous en sommes là !<br>';
    } else if (position.text) {
        opt = {icon: blue}
        text = '<p style="text-align:center">' + position.text + '<br>';
    }
    marker = L.marker(position.pos, opt).addTo(map);
    marker.bindPopup(text + '<small>' + position.date + '</small></p>')
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
