var markers;
var place;
var map;
function initAutocomplete(){
    markers = {
        "JB" :  {
            position: new google.maps.LatLng(50.668813, 4.608194),
            title:"JB's super fun house",
            price: 45
        },
        "Max": {
            position: new google.maps.LatLng(50.665813, 4.612194),
            title:"L'auberge du ragnard",
            price : 12
        },
        "Chris" : {
            position: new google.maps.LatLng(50.669813, 4.613194),
            title:"Chez Chris !",
            price: 33
        }
    };

    var options = {
        types: ['(cities)'],
        componentRestrictions: {country: "be"}
    };
    var mapProp= {
        center:new google.maps.LatLng(50.665813, 4.612194),
        zoom:13
    };
    map = new google.maps.Map(document.getElementById('google-map'),mapProp);
    var input = document.getElementById('pac-input');
    var autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.bindTo('bounds', map);

    autocomplete.addListener('place_changed', function() {
        place = autocomplete.getPlace();
    });

    document.getElementById("search-button").addEventListener("click",function(){
        if(place != null){
            searchButton();
        }
    });

    function searchButton(){
        $("#google-map").css("display","block");
        var lat = (place.geometry.location.lat());
        var lng = (place.geometry.location.lng);
        map.setCenter(new google.maps.LatLng(lat,lng()));
        google.maps.event.trigger(map, 'resize');
        $("#search-form").slideUp();
        $("#new-search-btn").show();
        window.location.href = '#!/map';
        drawMarkers();
    }
    drawMarkers();//Debug

}

function drawMarkers(){
    var image = {
        url: 'img/marker.png',
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32),
        scaledSize: new google.maps.Size(35, 28)
    };
    for(i in markers){
        new google.maps.Marker({
            position : markers[i].position,
            map : map,
            title : markers[i].title,
            label : markers[i].price + " €",
            icon : image
        });
    }
}