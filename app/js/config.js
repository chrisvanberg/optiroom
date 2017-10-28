angular.module('tokenAuthApp.config', ['ui.router']).config(appConfig).run(routeStart);

function appConfig($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('homepage', {
            url: '/',
            templateUrl: 'informations.html',
            controller: 'authStatusController',
            controllerAs: 'authStatusCtrl',
            restrictions: {
                ensureAuthenticated: false,
                loginRedirect: false
            }
        })
        .state('login', {
            url: '/login',
            templateUrl: 'login.html',
            controller: 'authLoginController',
            controllerAs: 'authLoginCtrl',
            restrictions: {
                ensureAuthenticated: false,
                loginRedirect: false
            }

        })
        .state('map', {
            url: '/map',
            templateUrl: 'google-map.html',
            controller: 'authLoginController',
            controllerAs: 'authLoginCtrl',
            restrictions: {
                ensureAuthenticated: false,
                loginRedirect: false
            }

        })
        ;
        $urlRouterProvider.otherwise('/');
};


function routeStart($transitions) {
    $transitions.onStart({}, function (trans) {
       // showMenu();
        if (trans.to().restrictions.ensureAuthenticated) {
            if (!localStorage.getItem('token')) {
                console.log("Acces restriction")
                window.location.href = '#!/';
            }
        }
        if (trans.to().restrictions.loginRedirect) {
            if (localStorage.getItem('token')) {
                window.location.href = '#!/';
            }
        }
        setPath(trans);
    });
}

function setPath(trans){

    console.log(trans.to().url);
    var path = trans.to().url;
    var page = path.replace("/","");
    console.log(page);
    $("a.menu-item:not(a[title='"+page+"'])").css("font-weight","normal");
    $("a.menu-item:not(a[title='"+page+"'])").css("color","white");
    $("a[title='"+page+"']").css("font-weight","700");
    $("a[title='"+page+"']").css("color","#FFDB38");
    switch(path){
        case "/UI" :
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
function routeStart($rootScope, $location, $route) {
    $rootScope.$on('$routeChangeStart', (event, next, current) => {
        if (next.restrictions.ensureAuthenticated) {
        if (!localStorage.getItem('token')) {
            $location.path('/login');
        }
    }
    if (next.restrictions.loginRedirect) {
        if (localStorage.getItem('token')) {
            $location.path('/status');
        }
    }
});
}*/