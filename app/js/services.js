angular.module('tokenAuthApp.services', []).service('authService', authService).service('signupService',signupService);

authService.$inject = ['$http','$window'];
signupService.$inject = ['$http','$window'];

function authService($http,$window) {

    const baseURL = 'https://dev.optiroom.net/api/';

    //Connexion
    this.login = function(user) {
        return $http({
            method: 'POST',
            url: baseURL + 'auth/login',
            data: user,
            headers: {'Content-Type': 'application/json'}
        });
    };
    //Check si l'user est authentifié
    this.ensureAuthenticated = function(token) {
        return $http({
            method: 'GET',
            url: baseURL + 'user',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + token
            }
        });
    };

    //Parser de token
    this.parseJwt = function(token) {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace('-', '+').replace('_', '/');
        return JSON.parse($window.atob(base64));
    }

}
function signupService($http, $window) {

    this.sendSignupForm = function (signupdata) {
        console.log("formulaire envoyé");
        console.log(signupdata);
        return true;
    }

}