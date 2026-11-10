(function () {
  'use strict';

  angular
    .module('libraryApp', ['ngRoute', 'ngAnimate'])
    .constant('API_BASE', '/api')
    .config(['$locationProvider', function ($locationProvider) {
      $locationProvider.hashPrefix('!');
    }]);
})();
