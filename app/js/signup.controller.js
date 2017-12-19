/**
 *
 * Ce fichier gère tous ce qui a trait aux inscriptions
 *
 */
angular.module('tokenAuthApp.signup', [])
    .controller('signupController', signupController);

signupController.$inject = ['signupService'];
//Controlleur de l'inscription
function signupController(signupService){
    const vm = this;
    vm.signupdata = {};
    //Fonction appellée à l'envoi du formulaire d'inscription
    vm.onSignupFormSend = function() {
        signupService.sendSignupForm(vm.signupdata).then(function(returnMessage) {
            window.location.href = "#!/";
            notify("Votre compte a bien été crée !", "green");
        },function(err){
            if(err.status == 409){
                notify("Cette adresse mail est déjà prise","red");
            }else{
                notify("Il y a une erreur dans vos données","red");
            }
        });
    };
}