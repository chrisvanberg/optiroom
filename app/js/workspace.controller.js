var workspaceID;
angular.module('tokenAuthApp.workspace', [])
    .controller('workspaceController', workspaceController);

workspaceController.$inject = ['workspaceService','$scope','$stateParams','$location'];

//Faut add les locaux de manière rapide genre la description et tout après
//Faudra genre pouvoir mettre les heures aussi (genres selects) et les jours
//Into griser les jours ou on veut que ça soit pas dispo ducoup faut un calendrier
//8h - 18h preset
function workspaceController(workspaceService, scope, params, $location){
    const vm = this;
    vm.workspaceData = {};
    vm.bookingData = {};
    vm.workspaceToAdd = {};
    workspaceID = $location.search()['workspaceID'];
    if(typeof (workspaceID) !== undefined && workspaceID > 0){
        editWorkspace();
    }
    vm.onAddWorkspace = function() {
        workspaceService.getCoordsByAddress(composeGoogleAPIUrl(vm.workspaceData.postcode, vm.workspaceData.city, vm.workspaceData.street, vm.workspaceData.number, vm.workspaceData.country)).then(function(data){
            vm.workspaceData.latitude = data.data.results[0].geometry.location.lat;
            vm.workspaceData.longitude = data.data.results[0].geometry.location.lng;
            if(!vm.workspaceData.hasProjector){
                vm.workspaceData.hasProjector = false;
            }
            if(!vm.workspaceData.hasWifi){
                vm.workspaceData.hasWifi = false;
            }
            vm.workspaceToAdd.address = {
                "buildingName" : vm.workspaceData.buildingName,
                "street" : vm.workspaceData.street,
                "number" : vm.workspaceData.number,
                "postcode" : vm.workspaceData.postcode,
                "city" : vm.workspaceData.city,
                "country" : vm.workspaceData.country,
                "longitude" : vm.workspaceData.longitude,
                "latitude" : vm.workspaceData.latitude
            };
            vm.workspaceToAdd.workspace = {
                "workspaceName" : vm.workspaceData.workspaceName,
                "description" : vm.workspaceData.description,
                "seats" : vm.workspaceData.seats,
                "hasWifi" : vm.workspaceData.hasWifi,
                "hasProjector" : vm.workspaceData.hasProjector,
                "minPrice" : vm.workspaceData.minPrice,
            };
            console.log(vm.workspaceToAdd);
            workspaceService.addWorkspace(vm.workspaceToAdd);
            $("#labase").css("display","none");
            $("#retourEnvoi").css("display","block");
        });
    };
    vm.onEditWorkspace = function() {
        var input = $('input');
        input.trigger('input');
        input.trigger('change');
        console.log(vm.workspaceData);
        vm.workspaceData.country = "BEL";
        workspaceService.getCoordsByAddress(composeGoogleAPIUrl(vm.workspaceData.postcode, vm.workspaceData.city, vm.workspaceData.street, vm.workspaceData.number, vm.workspaceData.country)).then(function(data){
            vm.workspaceData.latitude = data.data.results[0].geometry.location.lat;
            vm.workspaceData.longitude = data.data.results[0].geometry.location.lng;
            if(!vm.workspaceData.hasProjector){
                vm.workspaceData.hasProjector = false;
            }
            if(!vm.workspaceData.hasWifi){
                vm.workspaceData.hasWifi = false;
            }
            vm.workspaceToAdd.address = {
                "buildingName" : vm.workspaceData.buildingName,
                "street" : vm.workspaceData.street,
                "number" : vm.workspaceData.number,
                "postcode" : vm.workspaceData.postcode,
                "city" : vm.workspaceData.city,
                "country" : vm.workspaceData.country,
                "longitude" : vm.workspaceData.longitude,
                "latitude" : vm.workspaceData.latitude
            };
            vm.workspaceToAdd.workspace = {
                "workspace_id" : workspaceID,
                "workspaceName" : vm.workspaceData.workspaceName,
                "description" : vm.workspaceData.description,
                "seats" : vm.workspaceData.seats,
                "hasWifi" : vm.workspaceData.hasWifi,
                "hasProjector" : vm.workspaceData.hasProjector,
                "minPrice" : vm.workspaceData.minPrice,
            };
            console.log(vm.workspaceToAdd);
            workspaceService.editWorkspace(vm.workspaceToAdd);

            $("#labase").css("display","none");
            $("#retourEnvoi").css("display","block");
        });
    };

}
function editWorkspace(){
    angular.element(document.body).injector().get("workspaceService").getWorkspaceByID(workspaceID).then(function(ws) {
       console.log(ws.data);
       $("#building_name").val(ws.data.building_name).trigger('input');
       $("#workspace_name").val(ws.data.workspace_name).trigger('input');
       $("#seats").val(ws.data.nbSeats).trigger('input');
       $("#description").val(ws.data.description).trigger('input');
       $("#street").val(ws.data.street).trigger('input');
       $("#number").val(ws.data.building_number).trigger('input');
       $("#city").val(ws.data.city).trigger('input');
       $("#postcode").val(ws.data.postcode).trigger('input');
       $("#country").val(ws.data.country);
       $("#price").val(ws.data.minPrice).trigger('input');
       $('#wifi').prop('checked', ws.data.hasWifi == 1 ? true :false);
       $('#projector').prop('checked', ws.data.hasProjector == 1 ? true :false);
    });

    }
function buildWorkspaceList(){
    angular.element(document.body).injector().get("workspaceService").getWorkspacesByUser().then(function(ws) {
        for (i in ws.data) {
            $("#my-workspace-list").html("");
            for (i in ws.data) {
                $("#my-workspace-list").append("<div class='row col-md-6 workspace nopadding ng-scope' id='marker" + i + "' data-workspace=" + i + "></div>");
                $('*[data-workspace="' + i + '"]').append("<div class='price'>" + ws.data[i].price + " €</div>");
                $('*[data-workspace="' + i + '"]').append("<img src='img/default-room.jpg' class='col-md-12'>");

                $('*[data-workspace="' + i + '"]').append("<h2>" + ws.data[i].building_name + "</h2>");
                $('*[data-workspace="' + i + '"]').append("<h3>" + ws.data[i].workspace_name + "</h3>");

                $('*[data-workspace="' + i + '"]').append("<span title='Wifi' class='glyphicon glyphicon-signal'></span>");
                $('*[data-workspace="' + i + '"]').append(
                    ws.data[i].hasWifi == 1 ? "<span>Oui</span>" : "<span>Non</span>"
                );
                $('*[data-workspace="' + i + '"]').append(" - <span title='Projecteur' class='glyphicon glyphicon-facetime-video'></span>");
                $('*[data-workspace="' + i + '"]').append(
                    ws.data[i].hasProjector == 1 ? "<span>Oui</span>" : "<span>Non</span>"
                );
                $('*[data-workspace="' + i + '"]').append("<br><span title='Nombre de places' class='glyphicon glyphicon-user'></span>");
                $('*[data-workspace="' + i + '"]').append(ws.data[i].nbSeats);

                $('*[data-workspace="' + i + '"]').append("<h4>Description:</h4>");
                $('*[data-workspace="' + i + '"]').append("<p>" + ws.data[i].description + "</p>");
                $('*[data-workspace="' + i + '"]').append(("<button onclick='window.location.href =\"#!/edit-workspace?workspaceID="+ws.data[i].workspace_id+"\" ;' class='btn-success btn-sm form-control ng-scope'>Modifier</button>"));
            }
        }
    });
}
function bookWorkspace(id){
    var date = ($("#datetimepicker").val());
    var hour = $("*[data-workspaceBeginning=workspace"+id+"]").val();
    var bookingData = {
        "workspace_id" : id,
        "startDateTime" : date +" "+ hour +":00.000",
        "nbHours" : $("*[data-workspaceHour=workspace"+id+"]").val(),
    };
    angular.element(document.body).injector().get("workspaceService").bookWorkspace(bookingData).then(function(ws) {
        alert("La réservation a bien été éffectuée");
    });
}
function getBookings(){
    angular.element(document.body).injector().get("workspaceService").getBookings().then(function(ws) {
        console.log(ws.data);
        angular.forEach(ws.data, function(value, i) {
            $("#my-bookings-list").append("<div class=booking"+i+"></div>");
            $("#my-bookings-list>.booking"+i).append("<br>Début: " + ws.data[i].startDate);
            $("#my-bookings-list>.booking"+i).append("<br>Fin: " + ws.data[i].endDate);
            $("#my-bookings-list>.booking"+i).append("<br>Prix: " + ws.data[i].price+" €");
            angular.element(document.body).injector().get("workspaceService").getWorkspaceByID(ws.data[i].workspace_id).then(function (address) {
                $("#my-bookings-list>.booking"+i).append("<br>Adresse: " + address.data.street + " " + address.data.building_number + " " + address.data.postcode + " " + address.data.city);
                $("#my-bookings-list>.booking"+i).append("<hr style='border-bottom:1px solid #CCCCCC'>");
                $("#my-bookings-list>.booking"+i).prepend("Workspace: " + address.data.workspace_name);
            });
            $("#my-bookings-list>.booking"+i).append("<br>Contact: ");
            $("#my-bookings-list>.booking"+i).append("<br>Email: "+ ws.data[i].email);
            $("#my-bookings-list>.booking"+i).append("<br>Telephone: "+ ws.data[i].phone);

        });
    });
}