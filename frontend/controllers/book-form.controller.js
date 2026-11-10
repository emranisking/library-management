(function () {
  'use strict';

  angular.module('libraryApp').controller('BookFormController', ['$routeParams', '$location', 'BookService', 'ToastService', function ($routeParams, $location, BookService, ToastService) {
    var vm = this;

    vm.isEdit = !!$routeParams.id;
    vm.maxYear = new Date().getFullYear();
    vm.minYear = 1900;
    vm.book = { title: '', author: '', category: '', published_year: null };
    vm.categories = [];
    vm.loading = vm.isEdit;
    vm.saving = false;
    vm.error = null;
    vm.submitted = false;
    vm.borrowedInfo = null;

    BookService.getCategories().then(function (c) { vm.categories = c; }).catch(angular.noop);

    if (vm.isEdit) {
      BookService.getById($routeParams.id).then(function (b) {
        vm.book = {
          title: b.title,
          author: b.author,
          category: b.category || '',
          published_year: b.published_year
        };
        if (b.is_borrowed) { vm.borrowedInfo = b.borrower_name; }
      }).catch(function (err) {
        vm.error = err.message;
      }).finally(function () { vm.loading = false; });
    }

    vm.save = function (form) {
      vm.submitted = true;
      vm.error = null;
      if (form.$invalid || vm.saving) { return; }

      vm.saving = true;
      var payload = {
        title: vm.book.title,
        author: vm.book.author,
        category: vm.book.category || null,
        published_year: vm.book.published_year
      };
      var request = vm.isEdit
        ? BookService.update($routeParams.id, payload)
        : BookService.create(payload);

      request.then(function (saved) {
        ToastService.success('"' + saved.title + '" ' + (vm.isEdit ? 'updated' : 'added'));
        $location.path('/books');
      }).catch(function (err) {
        vm.error = err.message;
        vm.saving = false;
      });
    };

    vm.cancel = function () { $location.path('/books'); };
  }]);
})();
