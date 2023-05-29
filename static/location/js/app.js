//On recupère les données de la base de données pour les manipuler dans mapbox 
var donnees = document.getElementById('donnees');

//Donnees de localisation de l'utilisateur ou client Web
var lat = donnees.getAttribute('data-lat');
var lon = donnees.getAttribute('data-lon');
var position_btn = document.getElementById('position');
 
console.log(lon)
console.log(lat)
 

mapboxgl.accessToken = 'pk.eyJ1IjoiZXRhbGltIiwiYSI6ImNsaGZjcWdqeDBxem0zcW80dXJzbjRpaHEifQ.itgOJ87A8zoGZP_a7KQTbA';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    style: 'mapbox://styles/mapbox/streets-v12', // style URL
    center: [11.4976021,3.8676609], // starting position [lng, lat]
    zoom: 12 // starting zoom
});

position_btn.addEventListener('click', function(){
   // Créer un nouveau marqueur
    /*const marker = new mapboxgl.Marker({
        color: 'red',
        scale: 0.75,
    })
    .setLngLat([lon, lat]) // Position du marqueur [lng, lat]
    .setPopup(new mapboxgl.Popup().setHTML("<h4><b>Moi!</b></h4>"))
    .addTo(map); // Ajouter le marqueur à la carte

    //on centre la map sur le point de localisation de l'utilisateur
    map.flyTo({
        center: [lon, lat], 
        essential: true,
        curve: 1
    })*/
    map.addControl(
        new mapboxgl.GeolocateControl({
        positionOptions: {
        enableHighAccuracy: true
        },
        // When active the map will receive updates to the device's location as it changes.
        trackUserLocation: true,
        // Draw an arrow next to the location dot to indicate which direction the device is heading.
        showUserHeading: true
        })
    );

});

//Ici on va placer sur la carte les points de localisation de l'utilisateur recherché
for(i=0; i< positionsData.length; i++){
    console.log(positionsData[i].longitude, positionsData[i].latitude);
    moment = new Date(positionsData[i].timestamp) // on convertit le timestamp qui est de type string en type Date()
    console.log(moment.toDateString());
    const marker1 = new mapboxgl.Marker({
        color: '#d513d2',
        rotation: 30,
        scale:0.75
    })
    .setLngLat([positionsData[i].longitude, positionsData[i].latitude]) // Position du marqueur [lng, lat]
    .setPopup(new mapboxgl.Popup().setHTML('<b>' + moment.toDateString() + ' à ' + moment.toTimeString() + '</b>')) // afficher les informations sur la date et l'heure de la position.
    .addTo(map); // Ajouter le marqueur à la carte
}

coordonnees = []

for(i=0; i<positionsData.length; i++){
    coordonnees.push([positionsData[i].longitude, positionsData[i].latitude]);
}

directions = new MapboxDirections({
    accessToken: mapboxgl.accessToken,
    unit: 'metric',
});

console.log(coordonnees[0])

directions.setOrigin(coordonnees[0]);
directions.setDestination(coordonnees[coordonnees.length - 1]);

for(var i=0;i<coordonnees.length - 1;i++){
    directions.addWaypoint(i, coordonnees[i]);
}

map.addControl(
    directions,
    'top-right'
);

map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');