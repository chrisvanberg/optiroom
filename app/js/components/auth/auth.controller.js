angular.module('tokenAuthApp.components.auth', []).controller('authLoginController', authLoginController);

authLoginController.$inject = ['authService'];

function authLoginController(authService){
    /*jshint validthis: true */
    const vm = this;
    vm.user = {};
    vm.onLogin = function() {
        console.log(authService.login(vm.user));
        authService.login(vm.user).then(function(user) {

            console.log(user);

        },function(err){
            console.log(err);
        });

    }
    ;
}