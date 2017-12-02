angular.module('tokenAuthApp.components.auth', []).controller('authLoginController', authLoginController);

authLoginController.$inject = ['authService'];

function authLoginController(authService){
    /*jshint validthis: true */
    const vm = this;
    vm.user = {};
    vm.user.username = "";
    vm.user.password = "";

    vm.onLogin = function() {
        console.log(authService.login(vm.user));
        authService.login(vm.user).then(function(user) {

            localStorage.setItem('token',user.data.access_token);
            user = (authService.parseJwt(localStorage.getItem('token')).identity);
            document.getElementById('test').innerHTML = ("Et salut " + user+" !");

        },function(err){
            if(err.status == "401"){
                document.getElementById('test').innerHTML = ("Echec");
            }
        });

    }
    ;
}