
let app = angular.module('myApp', []);
app.controller('mainController', function($scope, require) { //$resource

    // let router = require('/:loc/:lag/location', {loc : '@loc', lag : '@lag'});
    $scope.listOfShit = ['hi', 'bye', 'yossi'];
    $scope.nameOfShit = 'yossi';
    // router.$get({loc : '128', lag : '189'}, function(res) {
    //
    // });


});