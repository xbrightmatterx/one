app.controller('HomeController', ['$scope', 'UsersFactory', '$state', function ($scope, UsersFactory, $state) {
  $scope.logIn = function( username, password ) {
    var user = {'username': username, 'password': password};
    UsersFactory.login(user)
    .then(function(res) {
      if(res.data === '') {
        console.log('User already exists.');
      } else {
        console.log('Successful login.', res.data);
        sessionStorage.setItem('at', res.data.auth_token);
        $state.go('feed');
      }
    })
    .catch(function(err) {
      throw(err);
    });
  };

  $scope.signUp = function( username, password ) {
    var user = {'username': username, 'password': password};
    UsersFactory.signup(user)
    .then(function(res) {
      if(res.data === 'User already exists.') {
        console.log('User already exists.');
      } else {
        console.log('User added.', res.data);
        sessionStorage.setItem('at', res.data.auth_token);
        $state.go('feed');
      }
    })
    .catch(function(err) {
      throw(err);
    });
  };

}]);
