angular.module('tokenAuthApp.workspace', [])
    .controller('workspaceController', workspaceController);

workspaceController.$inject = ['workspaceService'];
//Faut add les locaux de manière rapide genre la description et tout après
//Faudra genre pouvoir mettre les heures aussi (genres selects) et les jours
//Into griser les jours ou on veut que ça soit pas dispo ducoup faut un calendrier
//8h - 18h preset
function workspaceController(workspaceService){
    const vm = this;
    vm.workspaceData = {};
    vm.onAddWorkspace = function() {
        workspaceService.addWorkspace(vm.workspaceData);
        $("#labase").css("display","none");
        $("#retourEnvoi").css("display","block");
    };
    function getWorkspacesSteak(){
        return workspaceService.getWorkspaces();
    }
}
