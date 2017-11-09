angular.module('tokenAuthApp.auth', [])
    .controller('authLoginController', authLoginController)
    .controller('authStatusController', authStatusController);

authLoginController.$inject = ['authService'];
authStatusController.$inject = ['authService'];

function authLoginController(authService){
    /*jshint validthis: true */
    const vm = this;
    vm.user = {};
    vm.onLogin = function() {
        authService.login(vm.user).then(function(user) {
            localStorage.setItem('token',user.data.access_token);
            window.location.href = '#!/';
        },function(err){
            if(err.status == "401"){
                $("#login-form :input").blur();
                $("#login-form").effect("shake");
                $("#login-form :input:text").css("background-color","#ff988a");
                $("#login-form :input:password").css("background-color","#ff988a");
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
        vm.username = (authService.parseJwt(localStorage.getItem('token')).identity);
        userAuthentificated(vm);
    }
}