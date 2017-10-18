angular.module('tokenAuthApp.components.auth', [])
    .controller('authLoginController', authLoginController)
    .controller('authStatusController', authStatusController);

authLoginController.$inject = ['authService'];
authStatusController.$inject = ['authService'];

function authLoginController(authService){
    /*jshint validthis: true */
    const vm = this;
    vm.user = {};
    vm.user.username = "contact@chrisv.be";
    vm.user.password = "s@v@geCommando3TI";

    vm.onLogin = function() {
        console.log(authService.login(vm.user));
        authService.login(vm.user).then(function(user) {

            localStorage.setItem('token',user.data.access_token);



        },function(err){
            if(err.status == "401"){
                document.getElementById('test').innerHTML = ("Echec");
            }
        });

    }
    ;

}

function authStatusController(authService) {
    const vm = this;
    vm.isLoggedIn = false;
    const token = localStorage.getItem('token');
    if (token) {
        /*authService.ensureAuthenticated(token)
            .then(function(user) {
            if (user.data.status === 'success');
        vm.isLoggedIn = true;
    })
    ,function(err) {
            console.log(err);
    };*/
        vm.isLoggedIn = false;
    }
    vm.username = (authService.parseJwt(localStorage.getItem('token')).identity);
}