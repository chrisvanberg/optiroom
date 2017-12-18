/**
 *
 * Ce fichier gère tous ce qui a trait au router angular
 *
 */
angular.module('tokenAuthApp.config', ['ui.router']).config(appConfig).run(routeStart);

//Router pour les différentes vues pouvant être affichées
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
        .state('add-workspace', {
            url: '/add-workspace',
            templateUrl: 'add-workspace.html',
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
            },
            onEnter: function(){
                buildWorkspaceList();
            }

        })
        .state('edit-workspace', {
            url: '/edit-workspace',
            templateUrl: 'edit-workspace.html',
            controller: 'workspaceController',
            controllerAs: 'workspaceCtrl',
            restrictions: {
                ensureAuthenticated: true,
                loginRedirect: false
            }
        })
        .state('my-bookings', {
            url: '/my-bookings',
            templateUrl: 'my-bookings.html',
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

//Fonction qui se lancent quand la route change
function routeStart($transitions) {
    $("#notification").hide();
    $transitions.onStart({}, function (trans) {
        if(trans.to().url != "/map"){
            showMap(false);
        }else{
            showMap(true);
        }
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