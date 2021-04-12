var arr2 = [];

function initialize() {
    var temp_edit_submission_array = arr2;
    var lat = temp_edit_submission_array[0].substring(1, temp_edit_submission_array[0].indexOf(","));
    var lng = temp_edit_submission_array[0].substring(temp_edit_submission_array[0].indexOf(",") + 2, temp_edit_submission_array[0].length - 1);

    var co_ord = new google.maps.LatLng(lat, lng);
    var map = new google.maps.Map(document.getElementById('map'), {
        center: co_ord,
        zoom: 15,
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




    // TODO: @Pearl @khushdip Import the data to this variable and replace the array
    // It should be imported in the following format [lat, lng, address, chosen issue, additional info]
    // var infowindow = new google.maps.InfoWindow();

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: map,
    });
    var contentString = "<h4>" + temp_edit_submission_array[1] + "</h4>" + temp_edit_submission_array[2];
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
            infowindow.setContent("<h4>" + temp_edit_submission_array[1] + "</h4>" + temp_edit_submission_array[2]);
            infowindow.open(map, marker);
        }
    })(marker));
}


function store_sub(vari) {
    arr2.push(vari);
}

google.maps.event.addDomListener(window, 'load', initialize);