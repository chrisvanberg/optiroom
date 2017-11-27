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
        .state('my-account', {
            url: '/my-account',
            templateUrl: 'my-account.html',
            controller: 'authStatusController',
            controllerAs: 'authStatusCtrl',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
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
        .state('add-optiroom', {
            url: '/add-optiroom',
            templateUrl: 'add-optiroom.html',
            controller: 'workspaceController',
            controllerAs: 'workspaceCtrl',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
            }

        })
        .state('my-workspaces', {
            url: '/my-workspaces',
            templateUrl: 'my-workspaces.html',
            controller: 'workspaceController',
            controllerAs: 'workspaceCtrl',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
            }

        })
        ;
        $urlRouterProvider.otherwise('/');
};


function routeStart($transitions) {
    $transitions.onStart({}, function (trans) {
        if(trans.to().url != "/map"){
            showMap(false);
        }else{
            showMap(true);
        }
        console.log(trans.to().url);
        if (trans.to().restrictions.ensureAuthenticated) {
            if (!localStorage.getItem('token')) {
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