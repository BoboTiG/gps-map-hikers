<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <title>Trek</title>
    <link href="favicon.png" rel="icon" type="image/x-icon">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <link rel="stylesheet" href="assets/css/leaflet.css" />
    <link rel="stylesheet" href="assets/css/app.css" />
</head>

<body>
%if emergency_ongoing:
<div class="sos">
    <b class="blink">🆘</b> Entrez en contact avec nous au plus vite&nbsp;!
    <br>
    Date d’émission du signal : {{ traces[-1]["date"] }}
    <br>
     <a href="https://www.openstreetmap.org/?mlat={{ traces[-1]["lat"] }}&mlon={{ traces[-1]["lon"] }}#map=16/{{ traces[-1]["lat"] }}/{{ traces[-1]["lon"] }}" target="_blank">Coordonnées</a> : lat/lon {{ traces[-1]["lat"] }} {{ traces[-1]["lon"] }}
</div>
%end
<div id="legend">
    🚀 Vitesse de marche
    <br>
    ⛰ Altitude (à peu près)
    <br>
    ⛳ Distance parcourue depuis le <abbr title="Un marqueur bleu représente un relevé GPS.">dernier <img src="assets/css/images/marker-blue.png"></abbr>
    <br>
    🚩 Distance parcourue depuis le <abbr title="Un marqueur jaune représente une pause longue, du genre une nuit au frais.">dernier <img src="assets/css/images/marker-yellow.png"></abbr>
    <br>
    🏁 Distance totale parcourue
</div>
<div id="map"></div>

<script>
    var traces = [
    %for trace in traces:
        { date: "{{ trace["date"] }}", dist: {{ trace["dist"] }}, lat: {{ trace["lat"] }}, lon: {{ trace["lon"] }}, alt: {{ trace["alt"] }}, speed: {{ trace["speed"] }}, tdist: {{ trace["tdist"] }}, tdist2: {{ trace["tdist2"] }}, type: "{{ trace["type"] }}" },
    %end
    ];
</script>
%if traces:
<script src="assets/js/leaflet.js"></script>
<script src="assets/js/leaflet-routing-machine.min.js"></script>
<script src="assets/js/app.js"></script>
%end
</body>

</html>
