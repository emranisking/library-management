(function () {
  'use strict';

  angular.module('libraryApp').config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/books', {
        templateUrl: 'views/book-list.html',
        controller: 'BookListController',
        controllerAs: 'vm'
      })
      .when('/books/new', {
        templateUrl: 'views/book-form.html',
        controller: 'BookFormController',
        controllerAs: 'vm'
      })
      .when('/books/:id/edit', {
        templateUrl: 'views/book-form.html',
        controller: 'BookFormController',
        controllerAs: 'vm'
      })
      .otherwise({ redirectTo: '/books' });
  }]);
})();
