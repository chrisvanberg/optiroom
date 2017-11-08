angular.module('tokenAuthApp.services', []).service('authService', authService);

authService.$inject = ['$http','$window'];

function authService($http,$window) {
    this.parseJwt = function(token) {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace('-', '+').replace('_', '/');
        return JSON.parse($window.atob(base64));
    }
    const baseURL = 'https://54.36.181.116:5000/';

    this.login = function(user) {
        return $http({
            method: 'POST',
            url: baseURL + 'auth/login',
            data: user,
            headers: {'Content-Type': 'application/json'}
        });
    };

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
}