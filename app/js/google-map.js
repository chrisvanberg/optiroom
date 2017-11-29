var markers;
var place;
var map;
var workspaces;
var bounds;
var image;
var coords = [];
var workspacesRt;
var weekdays=new Array(7);
weekdays[0]="mon";
weekdays[1]="tue";
weekdays[2]="wed";
weekdays[3]="thu";
weekdays[4]="fri";
weekdays[5]="sat";
weekdays[6]="sun";
function initAutocomplete(){
    var options = {
        types: ['(regions)'],
        componentRestrictions: {country: "be"}
    };
    var mapProp= {
        center:new google.maps.LatLng(50.665813, 4.612194),
        zoom: 8
    };
    image = {
        url: 'img/marker.png',
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32),
        scaledSize: new google.maps.Size(60, 32)
    };
    google.maps.event.trigger(map, 'resize');
    map = new google.maps.Map(document.getElementById('google-map'),mapProp);
    var input = document.getElementById('pac-input');
    var autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.bindTo('bounds', map);

    autocomplete.addListener('place_changed', function() {
        place = autocomplete.getPlace();
    });

    document.getElementById("search-button").addEventListener("click",function(){
        window.location.href = '#!/map';
        showMap(true);
        $("#workspace-list").html("<img class='col-md-4 col-md-offset-4' style='width:20%;' src='img/loading.gif'>");
        setTimeout(
            function()
            {
                if(typeof place !== 'undefined'){
                    search();
                }
            }, 1500);

    });
}
function search(){
    workspaces = [];
    var lat;
    var lng;
    if(typeof place !== 'undefined'){
        lat = (place.geometry.location.lat());
        lng = (place.geometry.location.lng());
    }else{
        lat = 50.665813;
        lng = 4.612194;
    }
    map.setCenter(new google.maps.LatLng(lat,lng));
    map.setZoom(11);
    google.maps.event.trigger(map, 'resize');
    var range = Math.round(((Math.abs(map.getBounds().getSouthWest().lat() - map.getBounds().getNorthEast().lat()))*110.574));

    var date = $("#datetimepicker").datepicker('getDate');
    var dayOfWeek = weekdays[date.getUTCDay()];
    var seats = $("#nbSeats").val();
    $('html, body').animate({
        scrollTop: $("#google-map").offset().top-100
    }, 1000);
    setTimeout(
        function()
        {
            getWorkspaces(lat,lng,range,dayOfWeek, seats);
        }, 1500);

}

function drawMarkers(workspacesSelection){
    var existingBuildings = [];

    angular.forEach(workspacesSelection, function(value, key) {
        if(($.inArray(workspacesSelection[key].title, existingBuildings) == -1)){
            existingBuildings.push(workspacesSelection[key].title);
            var marker = new google.maps.Marker({
                position : workspacesSelection[key].position,
                map : map,
                title : workspacesSelection[key].title,
                url: "marker"+key,
                label: {
                    text : workspacesSelection[key].price +" €",
                    color: "#FFFFFF"
                },
                icon : image
            });
            markers.push(marker);
            google.maps.event.addListener(marker, 'click', function() {
                $('html, body').animate({
                    scrollTop: $("#marker"+key).offset().top-150
                }, 500);
            });
        }
    });
}
function drawList(workspacesSelection){
    $("#workspace-list").html("");
    for(i in workspacesSelection){
        $("#workspace-list").append("<div class='row col-md-6 workspace nopadding' id='marker"+i+"' data-workspace="+i+"></div>");
        $('*[data-workspace="'+i+'"]').append("<img src='img/default-room.jpg' class='col-md-12'>");

        $('*[data-workspace="'+i+'"]').append("<h2>"+workspacesSelection[i].building_name+"</h2>");
        $('*[data-workspace="'+i+'"]').append("<h3>"+workspacesSelection[i].workspace_name+"</h3>");
       // $('*[data-workspace="'+i+'"]>.secondCol').append("<h4>Prix: x €/h</h4>");

        $('*[data-workspace="'+i+'"]').append("<span title='Wifi' class='glyphicon glyphicon-signal'></span>");
        $('*[data-workspace="'+i+'"]').append(
            workspacesSelection[i].hasWifi == 1 ? "<span>Oui</span>" : "<span>Non</span>"
        );
        $('*[data-workspace="'+i+'"]').append(" - <span title='Projecteur' class='glyphicon glyphicon-facetime-video'></span>");
        $('*[data-workspace="'+i+'"]').append(
            workspacesSelection[i].hasProjector == 1 ? "<span>Oui</span>" : "<span>Non</span>"
        );
        $('*[data-workspace="'+i+'"]').append("<br><span title='Nombre de places' class='glyphicon glyphicon-user'></span>");
        $('*[data-workspace="'+i+'"]').append(workspacesSelection[i].nbSeats);

        $('*[data-workspace="'+i+'"]').append("<div class='col-md-12 more'></div>");
        $('*[data-workspace="'+i+'"]>.more').append("<h4>Description:</h4>");
        $('*[data-workspace="'+i+'"]>.more').append("<p>"+workspacesSelection[i].description+"</p>");
        $('*[data-workspace="'+i+'"]>.more').append("<button class='btn-success btn-sm form-control'>Réserver</button>");

    }
    $(".workspace").click(function(){
        $(".more").not($(this).find(".more")).slideUp("slow");
        $(this).find(".more").slideDown("slow");
    });
    google.maps.event.trigger(map, 'resize');

}
function getWorkspaces(lat,lng,range,dayOfWeek, seats){
    workspacesRt = {};
    for (i in markers) {
        markers[i].setMap(null);
    }
    markers = [];
        angular.element(document.body).injector().get("workspaceService").getWorkspaces(lat,lng,range,dayOfWeek, seats).then(function(ws) {
            workspaces = ws.data;
            if(workspaces.length == 0){
                drawList(workspaces);
                $("#workspace-list").html("<h3>Aucun résultat ne correspond à vos critères de recherche</h3>");
            }else{
                angular.forEach(workspaces, function(value, i) {
                    var googleAPIUrl = "https://maps.googleapis.com/maps/api/geocode/json?address=";
                    googleAPIUrl += workspaces[i].postcode +"+";
                    googleAPIUrl += workspaces[i].city +"+";
                    googleAPIUrl += workspaces[i].street +"+";
                    googleAPIUrl += workspaces[i].building_number +"+";
                    googleAPIUrl += workspaces[i].country +"+";
                    googleAPIUrl += "&key=AIzaSyArx_F8KA-tYiYKkoDkAkOX3PJHPvn-vCQ";
                    angular.element(document.body).injector().get("workspaceService").getCoordsByAddress(googleAPIUrl).then(function(data){
                        coords[i] = data.data.results[0].geometry.location;
                        workspacesRt[i] = ({
                            position: new google.maps.LatLng(coords[i].lat, coords[i].lng),
                            title: workspaces[i].building_name,
                            price: workspaces[i].minPrice,
                        });
                        drawMarkers(workspacesRt);
                        drawList(workspaces);
                    });
                });
            }

        });
}