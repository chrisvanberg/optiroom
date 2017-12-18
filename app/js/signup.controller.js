angular.module('tokenAuthApp.signup', [])
    .controller('signupController', signupController);

signupController.$inject = ['signupService'];

function signupController(signupService){
    const vm = this;
    vm.signupdata = {};

    vm.onSignupFormSend = function() {
        signupService.sendSignupForm(vm.signupdata).then(function(returnMessage) {
            console.log(returnMessage);
            window.location.href = "#!/";
            notify("Votre compte a bien été crée !", "green");
        },function(err){
            if(err.status == 409){
                notify("Cette adresse mail est déjà prise","red");
            }else{
                notify("Il y a une erreur dans vos données","red");
            }
            console.log(err);
        });
    };
}