angular.module('tokenAuthApp.workspace', [])
    .controller('workspaceController', workspaceController);

workspaceController.$inject = ['workspaceService'];

function workspaceController(workspaceService){
    const vm = this;
    vm.workspaceData = {};
    vm.onAddWorkspace = function() {
        workspaceService.addWorkspace(vm.workspaceData);
        console.log(vm.workspaceData);
        $("#labase").css("display","none");
        $("#retourEnvoi").css("display","block");
    };
}