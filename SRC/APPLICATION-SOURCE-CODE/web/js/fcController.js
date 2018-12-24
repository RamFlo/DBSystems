
let app = angular.module('myApp', []);
app.controller('mainController', ['$scope', function($scope) { //$resource /*, $sce, require  '$sce','require'*/

    // let router = require('/:loc/:lag/location', {loc : '@loc', lag : '@lag'});

    // router.$get({loc : '128', lag : '189'}, function(res) {
    //
    // });
    //$sce.trustAsUrl("https://www.google.com/maps/embed/v1/place?key=AIzaSyDVi-8TbF6uKXPHynmXSztCauLR7WjKI74&q=American+museum+of+Natural+History+New+York+City");

    //$scope.mapsQuery = $sce.trustAsUrl("https://www.google.com/maps/embed/v1/place?key=AIzaSyDVi-8TbF6uKXPHynmXSztCauLR7WjKI74&q=American+museum+of+Natural+History+New+York+City");
    //$scope.mapsQuery += "American+museum+of+Natural+History+New+York+City" // the answer from the server



    //document.getElementById("googleLocation").src = "https://www.google.com/maps/embed/v1/place?key=AIzaSyDVi-8TbF6uKXPHynmXSztCauLR7WjKI74&q=central+park+New+York+City";
    $scope.favor = "hello";
    $scope.favorFunc = function(){
        $scope.favor = document.getElementById("favorC").value; // Just for debugging
        let result = document.getElementById("favorC").value;
        // Pass result to the server
    };
    $scope.reply = {1 : "Italian", 2 : "french", 3 : "bulgarian", 4 : "American"};

    // Ingredients function
    $scope.ingredFunc = function() {
        let i;
        $scope.ingred = [];
        for(i = 1; i <= 4; i++) {
            $scope.ingred.push(document.getElementById("ingred"+i).value);
            // Pass to server ingred array
        };
    };
}]);