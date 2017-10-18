angular.module('tokenAuthApp.config', ['ui.router']).config(appConfig).run(routeStart);

function appConfig($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('login', {
            url: '/',
            templateUrl: 'login.html',
            controller: 'authLoginController',
            controllerAs: 'authLoginCtrl',
            restrictions: {
                ensureAuthenticated: false,
                loginRedirect: true
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
                trans.router.stateService.transitionTo('login');
                return true;
            }
        }
        if (trans.to().restrictions.loginRedirect) {
            if (localStorage.getItem('token')) {
                trans.router.stateService.transitionTo('UI');
                return true;
            }
        }
    });
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