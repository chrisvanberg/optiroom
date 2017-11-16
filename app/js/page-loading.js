$( document ).ready(function() {
    $("#datetimepicker").datepicker({ dateFormat: 'dd-mm-yy' });
});

function userAuthentificated(vm){
    $(".visible-offline").hide();
    $(".visible-online").show();
    $("#user-name").html(vm.username);
    $("#user-avatar").html("<img src='img/default-avatar.png'>"); //Faudra get l'avatar dans la bdd si possible
}

function hideSearchBar(bool){
    if(bool){
        $("#search-form").slideUp();
    }else{
        $("#search-form").slideDown();
    }
}

function hideMap(bool) {
    if(bool){
        $("#google-map").hide();
    }else{
        $("#google-map").show();
    }
}