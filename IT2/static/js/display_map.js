function initialize() {
    var co_ord = new google.maps.LatLng(43.66788041586209, -79.39434794852102);
    var map = new google.maps.Map(document.getElementById('map'), {
        center: co_ord,
        zoom: 12.75,
        styles: [
            { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
            {
                elementType: "labels.text.stroke",
                stylers: [{ color: "#242f3e" }],
            },
            {
                elementType: "labels.text.fill",
                stylers: [{ color: "#746855" }],
            },
            {
                featureType: "administrative.locality",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }],
            },
            {
                featureType: "poi",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }],
            },
            {
                featureType: "poi.park",
                elementType: "geometry",
                stylers: [{ color: "#263c3f" }],
            },
            {
                featureType: "poi.park",
                elementType: "labels.text.fill",
                stylers: [{ color: "#6b9a76" }],
            },
            {
                featureType: "road",
                elementType: "geometry",
                stylers: [{ color: "#38414e" }],
            },
            {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{ color: "#212a37" }],
            },
            {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{ color: "#9ca5b3" }],
            },
            {
                featureType: "road.highway",
                elementType: "geometry",
                stylers: [{ color: "#746855" }],
            },
            {
                featureType: "road.highway",
                elementType: "geometry.stroke",
                stylers: [{ color: "#1f2835" }],
            },
            {
                featureType: "road.highway",
                elementType: "labels.text.fill",
                stylers: [{ color: "#f3d19c" }],
            },
            {
                featureType: "transit",
                elementType: "geometry",
                stylers: [{ color: "#2f3948" }],
            },
            {
                featureType: "transit.station",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }],
            },
            {
                featureType: "water",
                elementType: "geometry",
                stylers: [{ color: "#17263c" }],
            },
            {
                featureType: "water",
                elementType: "labels.text.fill",
                stylers: [{ color: "#515c6d" }],
            },
            {
                featureType: "water",
                elementType: "labels.text.stroke",
                stylers: [{ color: "#17263c" }],
            },
        ],
    });
    
    const marker_label = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let i = 0;
    
    var Data = [{"loc":{ lat: 43.660485, lng: -79.384455 },"Address": "777 Bay St, Toronto, ON M5B 2H4, Canada", 
    "issue": "Option 1", "additional": "ssssss" }, {"loc":{ lat: 43.6573933, lng: -79.37426909999999 },
    "Address": "251 Jarvis St, Toronto, ON M5B 0C3, Canada", "issue": "Option 2", "additional": "sksksk" }];
    
    $.each(Data, function (key, value) {
        let label = marker_label[i++ % marker_label.length];
        addMarker(value.loc, map, label)
        $('tbody').append(`<tr><td>${label}</td>
        <td>${value.Address}</td>
        <td>${value.issue}</td>
        <td>${value.additional}</td>
        </tr>`);
    })
}

function addMarker(location,map,label) {
    // Add the marker at the clicked location, and add the next-available label
    // from the array of alphabetical characters.
    new google.maps.Marker({
      position: location,
      label: label,
      map: map,
    });

}

google.maps.event.addDomListener(window, 'load', initialize);

    

