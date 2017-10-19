angular.module('tokenAuthApp.config', ['ui.router']).config(appConfig).run(routeStart);

function appConfig($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('login', {
            url: '/',
            templateUrl: 'homepage.html',
            controller: 'authLoginController',
            controllerAs: 'authLoginCtrl',
            restrictions: {
                ensureAuthenticated: false,
                loginRedirect: false
            }
        })
        .state('UI', {
            url: '/UI',
            templateUrl: 'user-interface.php',
            controller: 'authStatusController',
            controllerAs: 'authStatusCtrl',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
            }

        })
        .state('UI.overview',{
            url: '/',
            templateUrl: 'overview.html',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
            }
            }
        )
        .state('UI.rooms',{
            url: '/rooms',
            templateUrl: 'rooms.php',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
            }
            }
        )
        .state('UI.management',{
                url: '/management',
                templateUrl: 'management.html',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
            }
            }
        )
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
                window.location.href = '#!/UI';
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