/**
 *
 * Gestion des changements de page
 *
 */


var lastLoaded;
var path = new Array(2);
$(document).ready(function() {
    //Animations du menu
    $(".mainElement").bind("click", function () {
        var cat = "."+(this.classList[1]);
        if(cat != lastLoaded){
            $(".subElement").slideUp(400);
            $(".mainElement").css("font-weight","normal");
            $(".mainElement").css("color","white");
            $(".subElement").css("color","white");
        }
        $(cat).css("font-weight","800");
        $(this).css("color","#FFDB38");
        $(".subElement"+cat).slideDown(200, function () {
            $(".subElement"+cat).css("display", "table");
        });
        path[0] = this.text;
        path[1] = "";
        setPath();
    });
    $(".subElement").bind("click",function(){
        $(".subElement").css("color","white");
        path[1] = " / " + this.text;
        $(this).css("color","#FFDB38");
        setPath();
    });

});

//
function setPath(){
    $("#top-bar span").text("");
    for(i in path){
        $("#top-bar span").append(path[i]);
    }
}

//Routes pour l'affichage des pages
var app = angular.module("optiroom", ["ngRoute"]);
app.config(function($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl : "overview.html",
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
app.controller('ctrl', function($scope) {
});