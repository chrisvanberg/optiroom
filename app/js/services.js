var token;
angular.module('tokenAuthApp.services', []).service('authService', authService).service('signupService',signupService).service('workspaceService',workspaceService);

authService.$inject = ['$http','$window'];
signupService.$inject = ['$http'];
workspaceService.$inject = ['$http'];

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
                Authorization: 'Bearer ' + localStorage.getItem('token')
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
function signupService($http) {

    const baseURL = 'https://dev.optiroom.net/api/';

    this.sendSignupForm = function (signupdata) {
        return $http({
            method: 'POST',
            url: baseURL + 'signup',
            data: signupdata,
            headers: {'Content-Type': 'application/json'}
        });
    }

}
function workspaceService($http){

    const baseURL = 'https://dev.optiroom.net/api/';

    this.addWorkspace = function(workspacedata){
        return $http({
            method: 'POST',
            url: baseURL + 'workspace/add',
            data: workspacedata,
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
        });
    }
    this.getWorkspaces = function(lat,lng,range,dayOfWeek, seats){
        return $http({
            method: 'GET',
            url: baseURL + 'search/'+lat+'/'+lng+'/'+range+'/'+dayOfWeek+'/'+seats,
            headers: {'Content-Type': 'application/json'}
        });
    }
    this.getWorkspacesByUser = function(){
        return $http({
            method: 'GET',
            url: baseURL + 'user/workspaces',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
        });
    }
    this.getWorkspaceByID = function(id){
        return $http({
            method: 'GET',
            url: baseURL + 'workspace/'+id,
            headers: {'Content-Type': 'application/json'}
        });
    }
    this.getCoordsByAddress = function(googleAPIUrl){
        return $http({
            method: 'GET',
            url: googleAPIUrl,
            headers: {'Content-Type': 'application/json'}
        });
    }


}
