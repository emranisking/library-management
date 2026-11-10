(function () {
  'use strict';

  /**
   * The only place that talks HTTP. Controllers never call $http directly.
   * Every method rejects with a human-readable string.
   */
  angular.module('libraryApp').factory('BookService', ['$http', '$q', 'API_BASE', function ($http, $q, API_BASE) {
    var url = API_BASE + '/books';

    function data(res) { return res.data; }

    function fail(err) {
      var message;
      if (err && err.data && err.data.error) {
        message = err.data.error;
      } else if (err && (err.status === -1 || err.status === 0)) {
        message = 'Cannot reach the server. Please check your connection.';
      } else {
        message = 'Something went wrong. Please try again.';
      }
      return $q.reject({ message: message, status: err && err.status });
    }

    return {
      getAll: function (filters) {
        var params = {};
        if (filters && filters.search) { params.search = filters.search; }
        if (filters && filters.category) { params.category = filters.category; }
        return $http.get(url, { params: params }).then(data).catch(fail);
      },
      getCategories: function () {
        return $http.get(url + '/categories').then(data).catch(fail);
      },
      getById: function (id) {
        return $http.get(url + '/' + id).then(data).catch(fail);
      },
      create: function (book) {
        return $http.post(url, book).then(data).catch(fail);
      },
      update: function (id, book) {
        return $http.put(url + '/' + id, book).then(data).catch(fail);
      },
      remove: function (id) {
        return $http.delete(url + '/' + id).then(function () { return true; }).catch(fail);
      },
      borrow: function (id, borrowerName) {
        return $http.post(url + '/' + id + '/borrow', { borrower_name: borrowerName }).then(data).catch(fail);
      },
      giveBack: function (id) {
        return $http.post(url + '/' + id + '/return').then(data).catch(fail);
      }
    };
  }]);
})();
