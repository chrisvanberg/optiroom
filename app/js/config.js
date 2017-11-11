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
                loginRedirect: true
            }

        })
        .state('signup', {
            url: '/signup',
            templateUrl: 'signup.html',
            controller: 'signupController',
            controllerAs: 'signupCtrl',
            restrictions: {
                ensureAuthenticated: false,
                loginRedirect: true
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
    });
}