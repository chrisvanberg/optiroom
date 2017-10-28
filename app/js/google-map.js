var place;
function initAutocomplete(){
    var options = {
        types: ['(cities)'],
        componentRestrictions: {country: "be"}
    };
    var mapProp= {
        center:new google.maps.LatLng(50.665813, 4.612194),
        zoom:13
    };
    var map = new google.maps.Map(document.getElementById('google-map'),mapProp);
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
    }
}

