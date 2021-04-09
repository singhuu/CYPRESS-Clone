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

    // TODO: @Pearl @khushdip Import the data to this variable and replace the array
    // It should be imported in the following format [lat, lng, address, chosen issue, additional info]
    var locations = [
        [43.660485, -79.384455, "777 Bay St, Toronto, ON M5B 2H 4, Canada", "Option 1", "ssssss"],
        [43.6573933, -79.37426909999999, "251 Jarvis St, Toronto, ON M5B 0C3, Canada", "Option 2", "sksksk"]
    ];
    var infowindow = new google.maps.InfoWindow();
    var container = document.getElementById('container');
    var table = document.createElement('table');
    var tbody = document.createElement('tbody');

    for (j = 0; j < locations.length; j++) {
        if (locations[j][2].length != '') {
            var marker = new google.maps.Marker({
                label: marker_label[j],
                position: new google.maps.LatLng(locations[j][0], locations[j][1]),
                map: map,
                title: locations[j][3],
            });
            var contentString = "<h1>" + locations[j][3] + "</h1>" + locations[j][4];
            var infowindow = new google.maps.InfoWindow({
                content: contentString,
                maxWidth: 160
            });

            // Event that closes the Info Window with a click on the map
            google.maps.event.addListener(map, 'click', (function(infowindow) {
                return function() {
                    infowindow.close();
                }
            })(infowindow));

            google.maps.event.addListener(marker, 'click', (function(marker, j) {
                return function() {
                    // close all the other infowindows that opened on load
                    google.maps.event.trigger(map, 'click')
                        // var contentString = 'Title on Click';
                    infowindow.setContent("<h3>" + locations[j][3] + "</h3>" + locations[j][4]);
                    infowindow.open(map, marker);
                }
            })(marker, j));
        }
        var val = locations[j];
        var row = document.createElement('tr');

        for (var k = 1; k < val.length; k++) {
            var cell = document.createElement('td');
            if (k == 1) {
                cell.textContent = marker_label[j];
            } else { cell.textContent = val[k]; }
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
    container.appendChild(table);

}


google.maps.event.addDomListener(window, 'load', initialize);