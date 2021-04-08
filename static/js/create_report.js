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
  var marker = new google.maps.Marker({
    map: map,
    position: co_ord,
    draggable: true,
    anchorPoint: new google.maps.Point(0, -29)
  });
  var input = document.getElementById('searchInput');
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  var autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.bindTo('bounds', map);
  var infowindow = new google.maps.InfoWindow();
  autocomplete.addListener('place_changed', function () {
    infowindow.close();
    marker.setVisible(false);
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      window.alert("Click on the Address");
      return;
    }
    let latlng = new google.maps.LatLng(place.geometry.location.lat(), place.geometry.location.lng())
    // TODO: @Pearl Store Lat Lng from here
    localStorage.setItem("loc", latlng)

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(12.75);
    }

    marker.setPosition(place.geometry.location);
    marker.setVisible(true);

    bindDataToForm(place.formatted_address);
    infowindow.setContent(place.formatted_address);
    infowindow.open(map, marker);

  });

}
function bindDataToForm(address) {
  document.getElementById('address').value = address;

}

var Data = [];
function storeRecipe() {
  var stuff = {};
  let address = document.getElementById("address");
  if (address.value == "") {
    //address.setCustomValidity('Please add a location.');
    //address.reportValidity();
    document.getElementById('address_error').innerHTML = "Please specify location of the issue.";
    return false;
  } 
  else {
    document.getElementById('address_error').innerHTML = "";
  }
  stuff["address"] = address.value;
  let issues = document.getElementById("issues");
  if (issues.validity.valueMissing) {
    issues.setCustomValidity('Please select an issue from the list.');
    issues.reportValidity();
    return false;
  }
  stuff["issues"] = issues.value;
  let additional = document.getElementById("additional").value;
  stuff["additional"] = additional;
  co_ord = localStorage.getItem('loc');
  stuff["loc"] = co_ord;
  localStorage.setItem("data", stuff);
  sendJSON(stuff);
  window.alert("Your request has been submitted.")
  window.location.reload();
}

function sendJSON(report_info){
  
  // Creating a XHR object
  let xhr = new XMLHttpRequest();
  let url = "http://localhost:5000/create_report";

  // open a connection
  xhr.open("POST", url, true);

  // Set the request header i.e. which type of content you are sending
  xhr.setRequestHeader("Content-Type", "application/json");

  // Create a state change callback
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {

          // Print received data from server
          result.innerHTML = this.responseText;

      }
  };

  // Converting JSON data to string
  let temporary_coord = "" + report_info['loc'].toString();
  report_info['loc'] = temporary_coord;
  let data = JSON.stringify(report_info);
  console.log(data);
  // Sending data with the request
  xhr.send(data);
}

google.maps.event.addDomListener(window, 'load', initialize);