
let app = angular.module('myApp', ["angucomplete-alt",'datatables']);

app.controller('mainController', ['$scope','$rootScope','$timeout','DTOptionsBuilder', function($scope,$rootScope,$timeout,DTOptionsBuilder) { //$resource /*, $sce, require  '$sce','require'*/

    $scope.currentLocation = 0;
    $scope.searchType = 0;
    $scope.autoCompleteRes = {};
    $scope.ingredPriceLevel = 0;
    $scope.ingredDelivery = 0;

    // Determine the view for each query
    $scope.decision = function (dec) {
        $scope.searchType = dec;
    };


    // handler for the auto-complete
    $rootScope.parseInput = function(str) {
        let emptyStr="";
        return emptyStr;
    };

    $scope.searchIngRes = {};

    // Handler for the auto-complete text search
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



    // Auto complete according to the search type and the input text
    $scope.changeSearchType = function(/*text*/) {


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


    let $radios = $('input[name=priceRangeIng]').change(function () {
        let value = $radios.filter(':checked').val();
        $scope.ingredPriceLevel = value;
    });

    $scope.tastePriceLevel = 0;

    $scope.minRevScoreTasteVal = 0;

    let $radiosTaste = $('input[name=priceRangeTaste]').change(function () {
        let value = $radiosTaste.filter(':checked').val();
        $scope.tastePriceLevel = value;
    });

    $scope.minRevScoreIngVal = 0;
    $scope.showCuisineByIngred = 0;

    // Get the filter params for 'find restaurants by ingredients', pass them to the server and display the results
    $scope.submitIngredient = function() {
        let location;
        let submittedIng = document.getElementById("ingredient_value").value;
        let ingredDelivery = document.getElementById("ingredDelivery").checked;
        let currentLocation = document.getElementById("currentLocation").checked;
        if (currentLocation) {
            location = map.getCenter();
        }
        let urlString = 'restaurants/'+submittedIng;
        if(ingredDelivery != 0 || $scope.ingredPriceLevel != 0 || currentLocation ||  $scope.minRevScoreIngVal != 0) {
            urlString += '/?';
        }
        if($scope.ingredPriceLevel != 0) {
            urlString += '&price_category=' + $scope.ingredPriceLevel;
        }
        if(ingredDelivery != 0) {
            urlString += '&online_delivery=' + '1';
        }
        if(currentLocation) {
            urlString += '&loclat=' + location.lat + '&loclng=' + location.lng;
        }
        if($scope.minRevScoreIngVal != 0){
            urlString += '&min_review=' + $scope.minRevScoreIngVal;
        }
        fetch(urlString)
            .then(data=>{return data.json()})
            .then(res=>{
                $scope.restFromIngred = res;
                $scope.showCuisineByIngred = 1;
                $scope.$apply();
                })
            .catch(error=>{
                console.log(error);
                $scope.showCuisineByIngred = 1;
                $scope.$apply();
            });
    };

    // Get all cuisine list
    let populateCuisineList = function () {
        const Url2 = 'get_cuisines';
        fetch(Url2).then(data=>{return data.json()}).then(res=>{$scope.discoverNewCuisine = res}).catch(error=>console.log(error));
    };

    $scope.newCuisines = {};
    $scope.cuisineUniqueIng={};
    $scope.showNewCuisinesTable = 0;
    $scope.showCuisineUniqueTable = 0;
    $scope.newCuisinesLoading = 0;
    $scope.cuisineSubmitChoice = 0;
    $scope.showNewFranchiseTable = 0;
    $scope.newFranchiseLoading = 0;

    // Discover new cuisine according to the user input
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
        }).catch(error=>{
            console.log(error);
            if ($scope.cuisineSubmitChoice == 0) {
                $scope.showCuisineUniqueTable = 0;
                $scope.showNewCuisinesTable = 1;
            }
            else {
                $scope.showCuisineUniqueTable = 1;
                $scope.showNewCuisinesTable = 0;
            }
            $scope.newCuisinesLoading = 0;
            $scope.$apply();
        });

    };

    $scope.newCusTableOptions = DTOptionsBuilder.newOptions().withOption('order',[]);

    $scope.disableAutoOrderTableOptions = DTOptionsBuilder.newOptions().withOption('order',[]);

    $scope.cuisineUniqueTableOptions = DTOptionsBuilder.newOptions().withOption('order',[1,'desc']);

    populateCuisineList();

    // Create the map
    mapboxgl.accessToken = 'pk.eyJ1IjoicmFtZmxvIiwiYSI6ImNqcWZjNmFuajUzMHo0YW1zeTJ5ZDFrMTcifQ.-6GAbzLXvYr7ftYbYeKMUg';
    let map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v9',
        center: [-73.97450195452336, 40.786381192719745],
        zoom: 10
    });

    // For locating the restaurant in the map
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
                    title: rest.restaurant_name,
                    description: rest.establishment_name
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

    // search for new franchise according to the map center
    $scope.getLocation = function() {
        $scope.newFranchiseLoading = 1;
        let center = map.getCenter();
        let Url='new_franchise/'+ center.lat + '/' + center.lng;
        fetch(Url).then(data=>{
            return data.json()})
            .then(res=>{
                $scope.showNewFranchiseTable = 1;
                $scope.newFranchiseArr = res;
            $scope.newCuisinesLoading = 0;
            $scope.$apply();
        }).catch(error=>{
            console.log(error);
            $scope.showNewFranchiseTable = 1;
            $scope.newCuisinesLoading = 0;
            $scope.$apply();
        });
        $scope.newFranchiseLoading = 0;
    };


    $scope.restsByTaste = {};
    $scope.restByTasteTableDivShow = 0;
    $scope.restByTasteLoading = 0;

    $scope.saltToggleValue = false;
    $scope.sweetToggleValue = false;
    $scope.sourToggleValue = false;
    $scope.bitterToggleValue = false;


    // Get the filter params for 'find restaurants by taste', pass them to the server and display the results
    $scope.submitSearchRestByTaste = function () {

        $scope.restByTasteTableDivShow = 0;
        $scope.restByTasteLoading = 1;
        let salt = $scope.saltToggleValue? 1:0;
        let sweet = $scope.sweetToggleValue? 1:0;
        let sour = $scope.sourToggleValue? 1:0;
        let bitter = $scope.bitterToggleValue? 1:0;
        let Url = 'restaurants/'+salt+'/'+sweet+'/'+sour+'/'+bitter;


        let locationTaste;
        let tasteDelivery = document.getElementById("tasteDelivery").checked;
        let currentLocationTaste = document.getElementById("currentLocationTaste").checked;
        if (currentLocationTaste) {
            locationTaste = map.getCenter();
        }
        if(tasteDelivery != 0 || $scope.tastePriceLevel != 0 || currentLocationTaste ||  $scope.minRevScoreTasteVal != 0) {
            Url += '/?';
        }
        if($scope.tastePriceLevel != 0) {
            Url += '&price_category=' + $scope.tastePriceLevel;
        }
        if(tasteDelivery != 0) {
            Url += '&online_delivery=' + '1';
        }
        if(currentLocationTaste) {
            Url += '&loclat=' + locationTaste.lat + '&loclng=' + locationTaste.lng;
        }
        if($scope.minRevScoreTasteVal != 0){
            Url += '&min_review=' + $scope.minRevScoreTasteVal;
        }


        fetch(Url).then(data=>{return data.json()}).then(res=> {
            $scope.restByTasteTableDivShow = 1;
            $scope.restsByTaste = res;
            $scope.restByTasteLoading = 0;
            $scope.$apply();
        }).catch(error=>{
            console.log(error);
            $scope.restByTasteTableDivShow = 1;
            $scope.restByTasteLoading = 0;
            $scope.$apply();
        });

    };


    $scope.commonIngredLoading = 0;
    $scope.showCommonIngredTable = 0;

    // search for common ingredients for the user input
    $scope.submitCommonIngred = function() {
        let ingredInput = document.getElementById("commonIngredient_value").value;
        if (ingredInput !="")
            $scope.commonIngredLoading = 1;
        let Url = 'get_common_ingredients_with/'+ingredInput;
        fetch(Url).then(data=>{return data.json()}).then(res=> {
            $scope.showCommonIngredTable = 1;
            $scope.commonIngredData = res;
            $scope.commonIngredLoading = 0;
            $scope.$apply();
        }).catch(error=>{
            console.log(error);
            $scope.showCommonIngredTable = 1;
            $scope.commonIngredLoading = 0;
            $scope.$apply();
        });
    }

}]);