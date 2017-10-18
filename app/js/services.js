angular.module('tokenAuthApp.services', []).service('authService', authService);

authService.$inject = ['$http','$window'];

function authService($http,$window) {
    this.parseJwt = function(token) {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace('-', '+').replace('_', '/');
        return JSON.parse($window.atob(base64));
    }
    const baseURL = 'http://localhost:5000/auth/';
    this.login = function(user) {
        return $http({
            method: 'POST',
            url: baseURL + 'login',
            data: user,
            headers: {'Content-Type': 'application/json'}
        });
    };
}