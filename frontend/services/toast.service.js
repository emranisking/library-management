(function () {
  'use strict';

  angular.module('libraryApp').factory('ToastService', ['$timeout', function ($timeout) {
    var toasts = [];
    var counter = 0;

    function remove(toast) {
      var i = toasts.indexOf(toast);
      if (i > -1) { toasts.splice(i, 1); }
    }

    function push(type, message) {
      var toast = { id: ++counter, type: type, message: message };
      toasts.push(toast);
      $timeout(function () { remove(toast); }, 4000);
      return toast;
    }

    return {
      toasts: toasts,
      dismiss: remove,
      success: function (m) { return push('success', m); },
      error: function (m) { return push('error', m); },
      info: function (m) { return push('info', m); }
    };
  }]);
})();
