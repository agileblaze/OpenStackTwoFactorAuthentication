(function() {
  'use strict';
  angular.module('MagicSearch', ['ui.bootstrap'])
  /**
   * @ngdoc directive
   * @name MagicSearch:magicOverrides
   * @description
   * A directive to modify / extend Magic Search functionality for use in
   * Horizon.
   * 1. The base Magic Search widget makes Foundation (a responsive front-end
   * framework) specific calls in showMenu and hideMenu.  In Horizon we use
   * Bootstrap, therefore we need to override those methods.
   *
   * 2.  Added 'facetsChanged' listener so we can notify base Magic Search
   * widget that new facets are available so they will be picked up.  (Use
   * if your table has dynamic facets)
   *
   * 3.  Due to the current inconsistencies in the APIs, where some support
   * filtering and others do not, we wanted a way to distinguish client-side
   * filtering (searching the visible subset) vs server-side filtering
   * (another server filter query).
   *
   * To support this distinguishment we overrode methods removeFacet &
   * initfacets to emit 'checkFacets' event so implementers can add property
   * 'isServer' to facets (what triggers the facet icon and color difference).
   *
   * Each table that incorporates Magic Search is responsible for adding
   * property 'isServer' to their facets as they have the intimate knowledge
   * of the API supplying the table data.  The setting of this property needs
   * to be done in the Magic Search supporting JavaScript for each table.
   *
   * Example:
   * // Set property 'isServer' on facets that you want to render as server
   * // facet (server icon, lighter grey color).  Note: If the property
   * // 'isServer' is not set, then facet renders with client icon and darker
   * // grey color.
   * scope.$on('checkFacets', function(event, currentSearch) {
   *   angular.forEach(currentSearch, function(facet) {
   *     if (apiVersion < 3) {
   *       facet.isServer = true;
   *     }
   *   });
   * });
   *
   * 4.  Overrode initfacets to fix refresh / bookmark issue where facets
   * menu wasn't removing facets that were already on url.
   *
   * @restrict A
   * @scope
   *
   * @example
   * ```
   * <div class="magic-search" magic-overrides>
   * ```
   */
  .directive('magicOverrides', function() {
    return {
      restrict: 'A',
      controller: ['$scope', '$timeout',
        function($scope, $timeout) {
          // showMenu and hideMenu depend on foundation's dropdown. They need
          // to be modified to work with another dropdown implementation.
          // For bootstrap, they are not needed at all.
          $scope.showMenu = function() {
            $timeout(function() {
              $scope.isMenuOpen = true;
            });
          };
          $scope.hideMenu = function() {
            $timeout(function() {
              $scope.isMenuOpen = false;
            });
          };
          $scope.isMenuOpen = false;

          // Add ability to update facet
          // Broadcast event when fact options are returned via ajax.
          // Should magic_search.js absorb this?
          $scope.$on('facetsChanged', function() {
            $timeout(function() {
              $scope.currentSearch = [];
              $scope.initSearch();
            });
          });

          // Override magic_search.js initFacets to fix browswer refresh issue
          // and to emit('checkFacets') to flag facets as isServer
          $scope.initFacets = function() {
            // set facets selected and remove them from facetsObj
            var initialFacets = window.location.search;
            if (initialFacets.indexOf('?') === 0) {
              initialFacets = initialFacets.slice(1);
            }
            initialFacets = initialFacets.split('&');
            if (initialFacets.length > 1 || initialFacets[0].length > 0) {
              $timeout(function() {
                $scope.strings.prompt = '';
              });
            }
            angular.forEach(initialFacets, function(facet) {
              var facetParts = facet.split('=');
              angular.forEach($scope.facetsObj, function(value) {
                if (value.name == facetParts[0]) {
                  if (value.options === undefined) {
                    $scope.currentSearch.push({
                      'name': facet,
                      'label': [value.label, facetParts[1]]
                    });

                    // for refresh case, need to remove facets that were bookmarked/
                    // current when broswer refresh was clicked
                    $scope.deleteFacetEntirely(facetParts);

                  } else {
                    angular.forEach(value.options, function(option) {
                      if (option.key == facetParts[1]) {
                        $scope.currentSearch.push({
                          'name': facet,
                          'label': [value.label, option.label]
                        });
                        if (value.singleton === true) {
                          $scope.deleteFacetEntirely(facetParts);
                        } else {
                          $scope.deleteFacetSelection(facetParts);
                        }
                      }
                    });
                  }
                }
              });
            });
            if ($scope.textSearch !== undefined) {
              $scope.currentSearch.push({
                'name': 'text=' + $scope.textSearch,
                'label': [$scope.strings.text, $scope.textSearch]
              });
            }
            $scope.filteredObj = $scope.facetsObj;

            // broadcast to check facets for serverside
            $scope.$emit('checkFacets', $scope.currentSearch);
          };

          // Override magic_search.js removeFacet to emit('checkFacets')
          // to flag facets as isServer after removing facet and
          // either update filter or search
          $scope.removeFacet = function($index) {
            var removed = $scope.currentSearch[$index].name;
            $scope.currentSearch.splice($index, 1);
            if ($scope.facetSelected === undefined) {
              $scope.emitQuery(removed);
            } else {
              $scope.resetState();
              $('.search-input').val('');
            }
            if ($scope.currentSearch.length === 0) {
              $scope.strings.prompt = $scope.promptString;
            }
            // re-init to restore facets cleanly
            $scope.facetsObj = $scope.copyFacets($scope.facetsSave);
            $scope.currentSearch = [];
            $scope.initFacets();

            // broadcast to check facets for serverside
            $scope.$emit('checkFacets', $scope.currentSearch);
          };

        }
      ]
    }; // end of return
  }); // end of directive
})();
