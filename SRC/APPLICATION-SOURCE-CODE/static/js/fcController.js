
let app = angular.module('myApp', ["angucomplete-alt"]);
app.controller('mainController', ['$scope', function($scope) { //$resource /*, $sce, require  '$sce','require'*/

    // let router = require('/:loc/:lag/location', {loc : '@loc', lag : '@lag'});
    //let autoCompleteRouter = require ('/:text/:type/autoComplete', {text : '@text', type : '@type'});
    //let ingredientRouter = require ('/:ingredient/:priceLevel/:delivery/autoComplete', {text : '@text', type : '@type'});


    // router.$get({loc : '128', lag : '189'}, function(res) {
    //
    // });

    $scope.currentLocation = 0;

    $scope.searchType = 0;
    $scope.autoCompleteRes = {};
    $scope.ingredPriceLevel = 0;
    $scope.ingredDelivery = 0;

    // Determine the view for each query
    $scope.decision = function (dec) {
        $scope.searchType = dec;
    };



    // Auto complete according to the search type and the input text
    $scope.autoComplete = function(/*text*/) {
      //   autoCompleteRouter.$get({text : text, this.searchStr : $scope.searchType}, function(res) {
      //
      // })\


        $scope.autoCompleteRes = [
            {entry_name : 'gbc'},
            {entry_name : 'jhg'},
            {entry_name : 'acc'},
            {entry_name : 'ahc'},
            {entry_name : 'gbc'},
            {entry_name : 'lui'},
            {entry_name : '123'},
            {entry_name : 'jhgr'},
            ];

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
        // ingredientRouter.$get({ingredient :$scope.currIngredient}, function(res) {
        //
        // });

        // send to ingredient router
        let a = $scope.currIngredient;
        let b = $scope.ingredPriceLevel;
        let c = $scope.ingredDelivery;
        let d = $scope.currentLocation;


        //example for result
        $scope.restFromIngred = [{restaurant_name : 'ret1', cuisine : "Italian" ,agg_review : 3.2, lat : 42, lng : 39, price_category : 3, featured_photo_url : "url"}, {restaurant_name : 'ret1', agg_review : 3.2, lat : 142, lng : 152, price_category : 3, featured_photo_url : "url"}, {restaurant_name : 'ret1', agg_review : 3.2, lat : 142, lng : 152, price_category : 3, featured_photo_url : "url"}];
    };


    $scope.submitDiscoverNewCuisine = function () {
      // discoverRouter.$get({}, function(res){});
        let a = $scope.currResturant;
        const Url2 = 'get_cuisines';
        fetch(Url2).then(data=>{return data.json()}).then(res=>{$scope.discoverNewCuisine = res});
        //$scope.discoverNewCuisine = [{cuisine_name : 'Italian'}, {cuisine_name : 'Italian'}, {cuisine_name : 'Italian'}];

    };


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



}]);