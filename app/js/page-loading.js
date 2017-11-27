$( document ).ready(function() {
    $("#datetimepicker").datepicker({
        dateFormat: 'dd-mm-yy',
    });
    $("#datetimepicker").datepicker('setDate', new Date());
    showMap(false);

    $(window).scroll(function() {
        var height = $(window).scrollTop();
        if(height > 316){
            $('#google-map').css('top', $(this).scrollTop()-310);
        }
    });
});

function userAuthentificated(vm){
    $(".visible-offline").hide();
    $(".visible-online").show();
    $("#user-avatar").html("<img src='img/default-avatar.png'>"); //Faudra get l'avatar dans la bdd si possible
}

function showMap(bool) {
    if(bool){
        $("#google-map").show();
        google.maps.event.trigger(map, 'resize');
    }else{
        $("#google-map").hide();
    }
}