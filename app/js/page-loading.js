//Ce qui est initialisé au chargement
$( document ).ready(function() {
    $("#datetimepicker").datepicker({
        dateFormat: 'yy-mm-dd',
    });
    $("#datetimepicker").datepicker('setDate', new Date());
    showMap(false);

    $(window).scroll(function() {
        var height = $(window).scrollTop();
        if(height > $("#homepage-header").height()){
            $('#google-map').css('top', $(this).scrollTop()-$("#homepage-header").height());
        }
    });
});

function userAuthentificated(vm){
    $(".visible-offline").hide();
    $(".visible-online").show();
    $("#user-avatar").html("<img src='img/default-avatar.png'>");
    $("#username").html("Mon compte ("+vm.username+")");
}
//Sert à afficher ou non la map en fonction de la vue
function showMap(bool) {
    if(bool){
        $("#google-map").show();
        google.maps.event.trigger(map, 'resize');
    }else{
        $("#google-map").hide();
    }
}