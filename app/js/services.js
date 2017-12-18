/**
 *
 * Ce fichier contient tous les services requis par la webapp,
 * ceux-ci servent à faire le lien avec l'API.
 *
 */

var token;
const baseURL = 'https://dev.optiroom.net/api/';
angular.module('tokenAuthApp.services', [])
    .service('authService', authService)
    .service('signupService',signupService)
    .service('workspaceService',workspaceService);

authService.$inject = ['$http','$window'];
signupService.$inject = ['$http'];
workspaceService.$inject = ['$http'];

//Service d'authentification
function authService($http,$window) {
    //Connexion
    this.login = function(user) {
        return $http({
            method: 'POST',
            url: baseURL + 'auth/login',
            data: user,
            headers: {'Content-Type': 'application/json'}
        });
    };
    //Parser de token, sert à récupèrer les informations de l'utilisateur connecté
    this.parseJwt = function(token) {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace('-', '+').replace('_', '/');
        return JSON.parse($window.atob(base64));
    }

}
//Service pour l'inscription
function signupService($http) {
    //Envoie les données de l'inscription vers l'API
    this.sendSignupForm = function (signupdata) {
        return $http({
            method: 'POST',
            url: baseURL + 'signup',
            data: signupdata,
            headers: {'Content-Type': 'application/json'}
        });
    }

}
//Service de gestion des workspaces
function workspaceService($http){
    //Ajouter un workspace
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
    //Permet de récupèrer une liste de workspaces
    this.getWorkspaces = function(lat,lng,range,dayOfWeek, seats){
        return $http({
            method: 'GET',
            url: baseURL + 'search/'+lat+'/'+lng+'/'+range+'/'+dayOfWeek+'/'+seats,
            headers: {'Content-Type': 'application/json'}
        });
    }
    //Permet de récuperer la liste des workspaces d'un utilisateur spécifique
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
    //Permet de récuperer les infos d'un workspace sur base de son ID
    this.getWorkspaceByID = function(id){
        return $http({
            method: 'GET',
            url: baseURL + 'workspace/'+id,
            headers: {'Content-Type': 'application/json'}
        });
    }
    //Utilise l'API de Google pour geocoder une adresse physique
    this.getCoordsByAddress = function(googleAPIUrl){
        return $http({
            method: 'GET',
            url: googleAPIUrl,
            headers: {'Content-Type': 'application/json'}
        });
    }
    //Permet de réserver un workspace
    this.bookWorkspace = function(data) {
        return $http({
            method: 'POST',
            url: baseURL +'workspace/book',
            data: data,
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
        });
    }
    //Permet de récupèrer la liste des réservations d'un utilisateur
    this.getBookings = function(){
        return $http({
            method: 'GET',
            url: baseURL + 'user/bookings',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
        });
    }
}
