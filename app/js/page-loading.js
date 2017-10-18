/**
 * Gestion des changements de page
 */

//Animation du menu et affichage de la page courante dans le header
function setPath(){
    var path = $('[ng-controller="ctrl"]').scope().currentPage;
    var page = path.replace("/","#!");
    $("a.menu-item:not(a[href='"+page+"'])").css("font-weight","normal");
    $("a.menu-item:not(a[href='"+page+"'])").css("color","white");
    $("a[href='"+page+"']").css("font-weight","700");
    $("a[href='"+page+"']").css("color","#FFDB38");
    switch(path){
        case "/" :
            path = "Acceuil"
            break;
        case "/rooms":
            path = "Locaux"
            break;
        case "/book":
            path = "Réserver"
            break;
        case "/my-bookings":
            path = "Mes réservations"
            break;
        case "/management":
            path = "Gestion"
            break;
    }
    $("header span").text(path);

}
/*
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
app.controller('ctrl', function($scope,$location) {
    $scope.$on('$routeChangeSuccess', function () {
        $scope.currentPage = $location.path();
        setPath();
        showMenu();
    });
});

*/
//Gestion du menu sur mobile et tablette
var mobileMenu;

function showMenu(){
    if(mobileMenu){
        rotateMenuImg();
        $("#menu").removeClass("visible-xs");
        $("#menu").removeClass("visible-sm");
        $("#menu").addClass("hidden-sm");
        $("#menu").addClass("hidden-xs");
        $("#content").removeClass("hidden-sm");
        $("#content").removeClass("hidden-xs");
        $("#content").addClass("visible-sm");
        $("#content").addClass("visible-xs");
        mobileMenu = false;
    }else{
        rotateMenuImg();
        $("#menu").removeClass("hidden-xs");
        $("#menu").removeClass("hidden-sm");
        $("#menu").addClass("visible-sm");
        $("#menu").addClass("visible-xs");
        $("#content").removeClass("visible-sm");
        $("#content").removeClass("visible-xs");
        $("#content").addClass("hidden-sm");
        $("#content").addClass("hidden-xs");
        mobileMenu = true;
    }

}

function rotateMenuImg(){
    $("#mobile-menu img").rotate({
        duration:500,
        angle: 0,
        animateTo:180
    });
}