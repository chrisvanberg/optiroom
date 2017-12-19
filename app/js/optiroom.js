//Ce qui est initialisé au chargement
$( document ).ready(function() {
    $("#datetimepicker").datepicker({
        dateFormat: 'yy-mm-dd',
        minDate : 0
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
//Ce qui change dans le header si l'user est connecté
function userAuthenticated(vm){
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
//Affiche les notifications d'erreur
function notify(notif,color){
    $("#notification").html(notif);
    $("#notification").show();
    if(color == "green"){
        $("#notification").css("background-color","#5DBD37");
    }else if(color == "red"){
        $("#notification").css("background-color","#f06862");
    }
    $(window).scrollTop(0);
}