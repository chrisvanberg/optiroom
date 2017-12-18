var workspaceID;
angular.module('tokenAuthApp.workspace', [])
    .controller('workspaceController', workspaceController);

workspaceController.$inject = ['workspaceService','$scope','$stateParams','$location'];

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
            $("#formulaireAjout").css("display","none");
            notify("Le workspace a bien été ajouté", "green");
        }),function(err){
            notify("Il y a eu une erreur","red");
        };;
    };
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
        notify("La réservation a bien été éffectuée","green");
    }),function(err){
        notify("Il y a eu une erreur","red");
    };
}
function getBookings(){
    angular.element(document.body).injector().get("workspaceService").getBookings().then(function(ws) {
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
            $("#my-bookings-list>.booking"+i).append("<br>Contact: "+ ws.data[i].firstname + " "+ ws.data[i].lastname);
            $("#my-bookings-list>.booking"+i).append("<br>Email: "+ ws.data[i].email);
            $("#my-bookings-list>.booking"+i).append("<br>Telephone: "+ ws.data[i].phone);

        });
    });
}
