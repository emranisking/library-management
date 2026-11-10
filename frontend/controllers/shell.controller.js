(function () {
  'use strict';

  angular.module('libraryApp').controller('ShellController', ['ToastService', function (ToastService) {
    var vm = this;
    vm.toasts = ToastService.toasts;
    vm.dismiss = ToastService.dismiss;
  }]);
})();
