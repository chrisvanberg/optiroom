angular.module('tokenAuthApp.components.main', []).controller('mainController', mainController);

mainController.$inject = ['$scope'];

function mainController($scope) {
        $scope.test = 'sanity check';
}