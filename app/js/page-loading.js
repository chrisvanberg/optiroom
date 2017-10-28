function userAuthentificated(vm){
    $(".visible-offline").hide();
    $(".visible-online").show();
    $("#username").append(vm.username);
}