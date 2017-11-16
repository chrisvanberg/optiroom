angular.module('tokenAuthApp.workspace', [])
    .controller('workspaceController', workspaceController);

workspaceController.$inject = ['workspaceService'];

function workspaceController(workspaceService){
    const vm = this;
    vm.workspaceData = {};
    vm.onAddWorkspace = function() {
        $("#labase").css("display","none");
        $("#retourEnvoi").css("display","block");
    };
}