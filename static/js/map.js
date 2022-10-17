const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: attribution });
const map = L.map('map', { layers: [osm], minZoom: 6 })
map.
    locate()
    .on("locationfound", (e) => map.setView(e.latlng, 7))
    .on("locationerror", () => map.setView([37.5664700, 126.9779630], 7));


const markers = JSON.parse(document.getElementById('device-data').textContent);

let feature = L.geoJSON(markers).bindPopup(function (layer) {
    return layer.feature.properties.name;
}).addTo(map);
map.fitBounds(feature.getBounds(), { padding: [100, 100] });