function userAuthentificated(vm){
    $(".visible-offline").hide();
    $(".visible-online").show();
    $("#user-name").append(vm.username);
    $("#user-avatar").append("<img src='img/default-avatar.png'>"); //Faudra get l'avatar dans la bdd si possible
}
$( document ).ready(function() {
    $("#user-name").bind( "click", function( event ) {
        $(".account-controls").show();
    });
});