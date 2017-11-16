angular.module('tokenAuthApp.signup', [])
    .controller('signupController', signupController);

signupController.$inject = ['signupService'];

function signupController(signupService){
    const vm = this;
    vm.signupdata = {};

    vm.onSignupFormSend = function() {
        signupService.sendSignupForm(vm.signupdata).then(function(returnMessage) {
            console.log(returnMessage);
        },function(err){
            console.log("Erreur");
        });
    };
}