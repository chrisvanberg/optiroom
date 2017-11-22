var markers;
var place;
var map;
var workspaces;
function initAutocomplete(){

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
        getWorkspaces();
    }
}

function drawMarkers(workspacesSelection){
    /*var image = {
        url: 'img/marker.png',
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32),
        scaledSize: new google.maps.Size(32, 40)
    };*/
    angular.forEach(workspacesSelection, function(value, key) {
        new google.maps.Marker({
            position : workspacesSelection[key].position,
            map : map,
            title : workspacesSelection[key].title
        });
    });
}
function drawList(workspacesSelection){
    $("#workspace-list").html("");
    for(i in workspacesSelection){
        $("#workspace-list").append("<div class='workspace' data-workspace="+i+"></div>");
        $('*[data-workspace="'+i+'"]').append("<img src='img/default-room.jpg'>");
        $('*[data-workspace="'+i+'"]').append("<h2>"+workspacesSelection[i].building_name+"</h2>");
        $('*[data-workspace="'+i+'"]').append("<h3>"+workspacesSelection[i].workspace_name+"</h3>");
        $('*[data-workspace="'+i+'"]').append("<h4>Prix: x €/h</h4>");
        $('*[data-workspace="'+i+'"]').append("<div class='clearfix'></div>");
    }
}
var coords = [];
var workspacesRt;
function getWorkspaces(){
    workspacesRt = {};
    //Faut un range de xkm max
        angular.element(document.body).injector().get("workspaceService").getWorkspaces().then(function(ws) {
            workspaces = ws.data;
            angular.forEach(workspaces, function(value, key) {
                var googleAPIUrl = "https://maps.googleapis.com/maps/api/geocode/json?address=";
                googleAPIUrl += workspaces[key].postcode +"+";
                googleAPIUrl += workspaces[key].city +"+";
                googleAPIUrl += workspaces[key].street +"+";
                googleAPIUrl += workspaces[key].building_number +"+";
                googleAPIUrl += workspaces[key].country +"+";
                googleAPIUrl += "&key=AIzaSyArx_F8KA-tYiYKkoDkAkOX3PJHPvn-vCQ";
                angular.element(document.body).injector().get("workspaceService").getCoordsByAddress(googleAPIUrl).then(function(data){
                    coords[key] = data.data.results[0].geometry.location;
                    workspacesRt[key] = ({
                        position: new google.maps.LatLng(coords[key].lat, coords[key].lng),
                        title: workspaces[key].building_name,
                        price: key
                    });
                    drawMarkers(workspacesRt);
                    drawList(workspaces);
                });
            });
        });
}