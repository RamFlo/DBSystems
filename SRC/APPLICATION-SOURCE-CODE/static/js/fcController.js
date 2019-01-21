
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

    // $scope.priceLevelChangeIngred = function(newPriceLevel){
    //     $scope.ingredPriceLevel = newPriceLevel;
    // };

    // $('#priceLevelSelector input').on("click",function(){
    //     alert(this.value())
    // });

    // $scope.priceLevelChangeBtn = 0;
    //
    // $scope.$watch('priceLevelChangeBtn', function(value) {
    //     console.log(value);
    // });

    let $radios = $('input[name=priceRangeIng]').change(function () {
        let value = $radios.filter(':checked').val();
        $scope.ingredPriceLevel = value;
    });

    $scope.submitIngredient = function() {
        let a = $scope.currIngredient;
        let location;



        let submittedIng = document.getElementById("ingredient_value").value;
        let ingredDelivery = document.getElementById("ingredDelivery").checked;
        let currentLocation = document.getElementById("currentLocation").checked;
        if (currentLocation) {
            location = map.getCenter();
        }
        let urlString = 'restaurants/'+submittedIng;
        if(ingredDelivery != 0 || $scope.ingredPriceLevel != 0 || currentLocation.hasOwnProperty("lat")) {
            urlString += '/?';
        }
        if($scope.ingredPriceLevel != 0) {
            urlString += '&price_category=' + $scope.ingredPriceLevel;
        }
        if(ingredDelivery != 0) {
            urlString += '&online_delivery=' + ingredDelivery;
        }
        if(currentLocation.hasOwnProperty("lat")) {
            urlString += '&loclat=' + location.lat + '&loclng=' + location.lng;
        }
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
                //$scope.newCusOptions = DTOptionsBuilder.newOptions().withOption('order',[]);
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

    //$scope.dtOptions = DTOptionsBuilder.newOptions().withOption('order',[]);
    $scope.newCusTableOptions = DTOptionsBuilder.newOptions().withOption('order',[]);

    $scope.disableAutoOrderTableOptions = DTOptionsBuilder.newOptions().withOption('order',[]);

    populateCuisineList();

    // $scope.submitUniqueIngredients = function() {
    //     // uniqueIngredRouter.$get({}, function(res){});
    //     let a = $scope.currUniqueIngred;
    //
    //     $scope.uniqueIngredintsResult = [{ingredient : "apple"}, {ingredient : "banana"}];
    // };


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
        let Url='new_franchise/'+ center.lat + '/' + center.lng;
        fetch(Url).then(data=>{
            return data.json()})
            .then(res=>{
                $scope.showNewFranchiseTable = 1;
                $scope.newFranchiseArr = res;
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
    $scope.submitSearchRestByTaste = function () {
        $scope.restByTasteTableDivShow = 0;
        $scope.restByTasteLoading = 1;
        let salt = $scope.saltToggleValue? 1:0;
        let sweet = $scope.sweetToggleValue? 1:0;
        let sour = $scope.sourToggleValue? 1:0;
        let bitter = $scope.bitterToggleValue? 1:0;
        let Url = 'restaurants/'+salt+'/'+sweet+'/'+sour+'/'+bitter;
        fetch(Url).then(data=>{return data.json()}).then(res=> {
            $scope.restByTasteTableDivShow = 1;
            $scope.restsByTaste = res;
            $scope.restByTasteLoading = 0;
            $scope.$apply();
        });

    };


    $scope.commonIngredLoading = 0;
    $scope.showCommonIngredTable = 0;
    $scope.submitCommonIngred = function() {
        $scope.commonIngredLoading = 1;
        let ingredInput = document.getElementById("commonIngredient_value").value;
        let Url = 'get_common_ingredients_with/'+ingredInput;
        fetch(Url).then(data=>{return data.json()}).then(res=> {
            $scope.showCommonIngredTable = 1;
            $scope.commonIngredData = res;
            $scope.commonIngredLoading = 0;
            $scope.$apply();
        });
    }

}]);