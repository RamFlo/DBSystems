
let app = angular.module('myApp', ["angucomplete-alt",'datatables']);
// app.directive("tablePostRepeatDirective",function(){
//     return function(scope, element, attrs) {
//         if (scope.$last){
//             // iteration is complete, do whatever post-processing
//             // is necessary
//             // element.parent().css('border', '1px solid black');
//             scope.initRestDataTable();
//         }
//     };
// });
app.controller('mainController', ['$scope','$rootScope','$timeout', function($scope,$rootScope,$timeout) { //$resource /*, $sce, require  '$sce','require'*/

    $scope.currentLocation = 0;

    $scope.searchType = 0;
    $scope.autoCompleteRes = {};
    $scope.ingredPriceLevel = 0;
    $scope.ingredDelivery = 0;

    // Determine the view for each query
    $scope.decision = function (dec) {
        $scope.searchType = dec;
    };


    $rootScope.parseInput = function(str) {
        let emptyStr="";
        return emptyStr;
    };

    $scope.searchIngRes = {};

    $scope.autocompleteIngHandler= function (userInputString, timeoutPromise) {
        return $timeout(async function () {
            console.log("searching for: " + userInputString);
            let urlString = 'ingredient_prefix/' + userInputString;
            await fetch(urlString)
                .then(data => {
                    return data.json()
                })
                .then(res => {
                    $scope.searchIngRes = res;
                })
                .catch(error => console.log(error));
            return {"data": $scope.searchIngRes};
        }, 1000);};

    // $scope.searchAPI = function(userInputString, timeoutPromise) {
    //     console.log("searching for: "+userInputString);
    //     let urlString = 'ingredient_prefix/'+userInputString;
    //     fetch(urlString)
    //         .then(data=>{return data.json()})
    //         .then(res=>{
    //             return res;
    //         })
    //         .catch(error=>console.log(error));
    //
    //     if ($scope.searchType == 0) {
    //         $scope.currIngredient = this.searchStr;
    //     }
    //     else if ($scope.searchType == 1) {
    //         $scope.currResturant = this.searchStr;
    //     }
    //     else if ($scope.searchType == 2) {
    //         $scope.currUniqueIngred = this.searchStr;
    //     }
    //
    //
    //     return $http.post('/yourownapi/', {q: userInputString}, {timeout: timeoutPromise});
    // };

    // Auto complete according to the search type and the input text
    $scope.changeSearchType = function(/*text*/) {

        // let searchStrIng = document.getElementById("ingredient_value").value;
        // console.log("searching for: "+searchStrIng);
        // // let urlString = 'ingredient_prefix/'+this.searchStr;
        // let urlString = 'ingredient_prefix/'+searchStrIng;
        // fetch(urlString)
        //     .then(data=>{return data.json()})
        //     .then(res=>{
        //         $scope.autoCompleteRes = res;
        //     })
        //     .catch(error=>console.log(error));

        if ($scope.searchType == 0) {
            $scope.currIngredient = this.searchStr;
        }
        else if ($scope.searchType == 1) {
            $scope.currResturant = this.searchStr;
        }
        else if ($scope.searchType == 2) {
            $scope.currUniqueIngred = this.searchStr;
        }
    };

    $scope.submitIngredient = function() {
        let a = $scope.currIngredient;
        let b = $scope.ingredPriceLevel;
        let c = $scope.ingredDelivery;
        let d = $scope.currentLocation;
        //example for result
        //$scope.restFromIngred = [{restaurant_name : 'ret1', cuisine : "Italian" ,agg_review : 3.2, lat : 42, lng : 39, price_category : 3, featured_photo_url : "url"}, {restaurant_name : 'ret1', agg_review : 3.2, lat : 142, lng : 152, price_category : 3, featured_photo_url : "url"}, {restaurant_name : 'ret1', agg_review : 3.2, lat : 142, lng : 152, price_category : 3, featured_photo_url : "url"}];
        let submittedIng = document.getElementById("ingredient_value").value;
        let urlString = 'restaurants/'+submittedIng;
        fetch(urlString)
            .then(data=>{return data.json()})
            .then(res=>{
                $scope.restFromIngred = res;
                $scope.$apply();
                })
            .catch(error=>console.log(error));
    };

    // $scope.initRestDataTable = function() {
    //     $(document).ready(function() {
    //         $('restFromIngredTable').DataTable({
    //             // pageLength:10,
    //             // lengthMenu: [ 10, 25, 50, 75, 100 ],
    //             // dom: 'Bfrtip',
    //             // buttons: [ 'pageLength' ]
    //             //"lengthChange": false
    //             "scrollY":        "200px",
    //             "scrollCollapse": true,
    //             "paging":         false
    //         });
    //     } )
    // };


    let populateCuisineList = function () {
        const Url2 = 'get_cuisines';
        fetch(Url2).then(data=>{return data.json()}).then(res=>{$scope.discoverNewCuisine = res});
    };

    $scope.newCuisines = {};
    $scope.cuisineUniqueIng={};
    $scope.showNewCuisinesTable = 0;
    $scope.showCuisineUniqueTable = 0;
    $scope.newCuisinesLoading = 0;
    $scope.cuisineSubmitChoice = 0;
    $scope.showNewFranchiseTable = 0;
    $scope.newFranchiseLoading = 0;

    $scope.submitDiscoverNewCuisine = function () {
        let choice = document.getElementById("cuisineChoiceRadios")
        $scope.newCuisinesLoading = 1;
        let Url="";
        if ($scope.cuisineSubmitChoice == 0)
            Url = 'discover_new_cuisines/'+ document.getElementById("discoverNewCuisineBaseSelect").value;
        else
            Url = 'unique_ingredients/'+ document.getElementById("discoverNewCuisineBaseSelect").value;
        fetch(Url).then(data=>{return data.json()}).then(res=>{
            if ($scope.cuisineSubmitChoice == 0) {
                $scope.showCuisineUniqueTable = 0;
                $scope.showNewCuisinesTable = 1;
                $scope.newCuisines = res;
            }
            else {
                $scope.showCuisineUniqueTable = 1;
                $scope.showNewCuisinesTable = 0;
                $scope.cuisineUniqueIng = res;
            }
            $scope.newCuisinesLoading = 0;
            $scope.$apply();
        });

    };

    populateCuisineList();


    $scope.submitUniqueIngredients = function() {
        // uniqueIngredRouter.$get({}, function(res){});
        let a = $scope.currUniqueIngred;

        $scope.uniqueIngredintsResult = [{ingredient : "apple"}, {ingredient : "banana"}];
    };


    mapboxgl.accessToken = 'pk.eyJ1IjoicmFtZmxvIiwiYSI6ImNqcWZjNmFuajUzMHo0YW1zeTJ5ZDFrMTcifQ.-6GAbzLXvYr7ftYbYeKMUg';
    let map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v9',
        center: [-73.996155, 40.732013],
        zoom: 10
    });


    $scope.locateRestInMap = function (rest) {
        let geojson = {
            type: 'FeatureCollection',
            features: [{
                type: 'Feature',
                geometry: {
                    type: 'Point',
                    coordinates: [rest.lng, rest.lat]
                },
                properties: {
                    title: rest.cuisine,
                    description: rest.restaurant_name
                }
            }]
        };

        // add markers to map
        geojson.features.forEach(function(marker) {

            // create a HTML element for each feature
            let el = document.createElement('div');
            el.className = 'marker';

            // make a marker for each feature and add to the map
            new mapboxgl.Marker(el)
                .setLngLat(marker.geometry.coordinates)
                .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
                    .setHTML('<h3>' + marker.properties.title + '</h3><p>' + marker.properties.description + '</p>'))
                .addTo(map);
        });
        map.flyTo({center: [rest.lng, rest.lat] ,zoom : 14});
    };

    $scope.getLocation = function() {
        $scope.newFranchiseLoading = 1;
        let center = map.getCenter();
        let Url='new_franchise/'+ center[0] + '/' + center[1];
        fetch(Url).then(data=>{
            return data.json()})
            .then(res=>{
                $scope.showNewFranchiseTable = 1;
                $scope.newFranchiseArr = res;
            $scope.newCuisinesLoading = 0;
            $scope.$apply();
        });
    };

}]);