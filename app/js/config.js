
angular
    .module('tokenAuthApp.config', [])
    .config(appConfig);
function appConfig($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'js/components/main/main.view.html',
            controller: 'mainController'
        })
        .when('/login', {
            templateUrl: 'js/components/auth/auth.login.view.html',
            controller: 'authLoginController',
            controllerAs: 'authLoginCtrl'
        })
        .otherwise({
            redirectTo: '/'
        });
}