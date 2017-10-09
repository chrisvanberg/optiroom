/*var lastLoaded;
function loadPage(page){

    $("#content").load(page+'.html');
    var selector = "." + page;
    if(page != lastLoaded){
        $(".subElement"+ selector).css("display","none");
        $(".subElement").slideUp(200);
    }
    $(".subElement"+ selector).slideDown(200,function(){
        $(".subElement"+ selector).css("display","table");
    });
    lastLoaded = page;

}
function loadSubPage(page){
    $("#content").load(page+'.html');

}*/
var lastLoaded;

$(document).ready(function() {
    $(".mainElement").bind("click", function () {
        var cat = "."+(this.classList[1]);
        if(cat != lastLoaded){
            $(".subElement").slideUp(400);
            $(".mainElement").css("font-weight","normal");
        }

        $(cat).css("font-weight","800");
        $(".subElement"+cat).slideDown(200, function () {
            $(".subElement"+cat).css("display", "table");

        });

    });
});
var app = angular.module("optiroom", ["ngRoute"]);
app.config(function($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl : "overview.html"
        })
        .when("/rooms", {
            templateUrl : "rooms.php"
        })
        .when("/book", {
            templateUrl : "book.html"
        })
        .when("/my-bookings",{
            templateUrl : "my-bookings.html"
        })
        .when("/management",{
            templateUrl : "management.html"
        });
});