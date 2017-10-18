steak = {
    "id": "auth",
    "response": {
        "status": "success",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODQ2NzY4MjEsImlhdCI6MTQ4MzQ2NzIyMSwic3ViIjoyfQ.hMcrXz-63iD4jX-ves3cZMznSS3UhZD4NCPry2zLkHo"
    }
};
angular.module('tokenAuthApp.services', []).service('authService', authService);

authService.$inject = ['$http'];

function authService($http) {

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