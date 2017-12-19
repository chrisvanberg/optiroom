/**
 *
 * Ce fichier gère tous ce qui a trait à l'authentification
 *
 */
angular.module('tokenAuthApp.auth', [])
    .controller('authLoginController', authLoginController)
    .controller('authStatusController', authStatusController);

authLoginController.$inject = ['authService'];
authStatusController.$inject = ['authService'];
//Envoie le formulaire de login au service aproprié
function authLoginController(authService){
    const vm = this;
    vm.user = {};
    vm.onLogin = function() {
        authService.login(vm.user).then(function(user) {
            localStorage.setItem('token',user.data.access_token);
            token = user.data.access_token;
            window.location.href = '#!/';
        },function(err){
            if(err.status == "401"){
                notify("Login ou mot de passe éroné","red");
                $("#login-form :input").blur();
                $("#login-form").effect("shake");
                $("#login-form :input:text").css("background-color","#ff988a");
                $("#login-form :input:password").css("background-color","#ff988a");
            }
        });
    }
    ;

}
//Vérifie si l'utilisateur est authentifié
function authStatusController(authService) {
    const vm = this;
    vm.isLoggedIn = false;
    const token = localStorage.getItem('token');
    if (token) {
        vm.username = (authService.parseJwt(localStorage.getItem('token')).identity);
        userAuthenticated(vm);
    }
}