
angular
    .module('tokenAuthApp.config', [])
    .config(appConfig);
function appConfig($routeProvider) {
    $routeProvider

        .when('/', {
            templateUrl: 'login.html',
            controller: 'authLoginController',
            controllerAs: 'authLoginCtrl'
        })
        .otherwise({
            redirectTo: '/'
        });
}