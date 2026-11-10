(function () {
  'use strict';

  var CATEGORY_ICONS = {
    'technology': 'bi-cpu',
    'fiction': 'bi-magic',
    'self-help': 'bi-lightbulb',
    'history': 'bi-hourglass-split',
    'science': 'bi-rocket-takeoff',
    'psychology': 'bi-puzzle'
  };

  angular.module('libraryApp').controller('BookListController', ['BookService', 'ToastService', function (BookService, ToastService) {
    var vm = this;

    vm.books = [];
    vm.categories = [];
    vm.filters = { search: '', category: '' };
    vm.stats = { total: 0, available: 0, borrowed: 0 };
    vm.loading = true;
    vm.error = null;

    // dialog state
    vm.borrowDialog = null;   // { book, name, error, busy }
    vm.deleteDialog = null;   // { book, busy }
    vm.busyId = null;

    vm.hasFilters = function () {
      return !!(vm.filters.search || vm.filters.category);
    };

    vm.coverClass = function (book) { return 'cover-' + (book.id % 6); };
    vm.coverIcon = function (book) {
      var key = (book.category || '').toLowerCase();
      return CATEGORY_ICONS[key] || 'bi-book';
    };

    function loadStats() {
      return BookService.getAll({}).then(function (all) {
        vm.stats.total = all.length;
        vm.stats.borrowed = all.filter(function (b) { return b.is_borrowed; }).length;
        vm.stats.available = vm.stats.total - vm.stats.borrowed;
      }).catch(angular.noop);
    }

    function loadCategories() {
      return BookService.getCategories().then(function (c) { vm.categories = c; }).catch(angular.noop);
    }

    vm.load = function () {
      vm.loading = true;
      vm.error = null;
      return BookService.getAll(vm.filters)
        .then(function (books) { vm.books = books; })
        .catch(function (err) { vm.error = err.message; })
        .finally(function () { vm.loading = false; });
    };

    function refreshAll() {
      return vm.load().then(function () {
        loadStats();
        loadCategories();
      });
    }

    vm.clearFilters = function () {
      vm.filters.search = '';
      vm.filters.category = '';
      vm.load();
    };

    // ---- borrow -----------------------------------------------------
    vm.openBorrow = function (book) {
      vm.borrowDialog = { book: book, name: '', error: null, busy: false };
    };
    vm.closeBorrow = function () { vm.borrowDialog = null; };

    vm.confirmBorrow = function () {
      var d = vm.borrowDialog;
      if (!d || d.busy) { return; }
      if (!d.name || !d.name.trim()) {
        d.error = 'Borrower name is required';
        return;
      }
      d.busy = true;
      d.error = null;
      BookService.borrow(d.book.id, d.name.trim()).then(function (updated) {
        ToastService.success('"' + updated.title + '" borrowed by ' + updated.borrower_name);
        vm.borrowDialog = null;
        refreshAll();
      }).catch(function (err) {
        d.busy = false;
        d.error = err.message;
        if (err.status === 409) { refreshAll(); }
      });
    };

    // ---- return -----------------------------------------------------
    vm.giveBack = function (book) {
      vm.busyId = book.id;
      BookService.giveBack(book.id).then(function (updated) {
        ToastService.success('"' + updated.title + '" returned');
        return refreshAll();
      }).catch(function (err) {
        ToastService.error(err.message);
      }).finally(function () { vm.busyId = null; });
    };

    // ---- delete -----------------------------------------------------
    vm.openDelete = function (book) { vm.deleteDialog = { book: book, busy: false }; };
    vm.closeDelete = function () { vm.deleteDialog = null; };

    vm.confirmDelete = function () {
      var d = vm.deleteDialog;
      if (!d || d.busy) { return; }
      d.busy = true;
      BookService.remove(d.book.id).then(function () {
        ToastService.success('"' + d.book.title + '" deleted');
        vm.deleteDialog = null;
        return refreshAll();
      }).catch(function (err) {
        ToastService.error(err.message);
        vm.deleteDialog = null;
        refreshAll();
      });
    };

    // ---- init -------------------------------------------------------
    vm.load();
    loadStats();
    loadCategories();
  }]);
})();
