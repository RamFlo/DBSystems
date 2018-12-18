
let app = angular.module('myApp', []);
app.controller('mainController', ['$scope', function($scope, require, $sce) { //$resource

    // let router = require('/:loc/:lag/location', {loc : '@loc', lag : '@lag'});

    // router.$get({loc : '128', lag : '189'}, function(res) {
    //
    // });
    //$sce.trustAsUrl("https://www.google.com/maps/embed/v1/place?key=AIzaSyDVi-8TbF6uKXPHynmXSztCauLR7WjKI74&q=American+museum+of+Natural+History+New+York+City");

    //$scope.mapsQuery = $sce.trustAsUrl("https://www.google.com/maps/embed/v1/place?key=AIzaSyDVi-8TbF6uKXPHynmXSztCauLR7WjKI74&q=American+museum+of+Natural+History+New+York+City");
    //$scope.mapsQuery += "American+museum+of+Natural+History+New+York+City" // the answer from the server
    document.getElementById("googleLocation").src = "https://www.google.com/maps/embed/v1/place?key=AIzaSyDVi-8TbF6uKXPHynmXSztCauLR7WjKI74&q=central+park+New+York+City";
    
}]);