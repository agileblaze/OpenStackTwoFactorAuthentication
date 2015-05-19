/**
 * Copyright 2015 IBM Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function(){
  'use strict';

  describe('hzOtpLoginCtrl', function(){

    var $controller;

    beforeEach(module('hz'));
    beforeEach(inject(function(_$controller_){
      $controller = _$controller_;
    }));

    describe('$scope.auth_type', function(){
      it('should initialize to credentials', function(){
        var scope = {};
        $controller('hzOtpLoginCtrl', { $scope: scope });
        expect(scope.auth_type).toEqual('credentials');
      });
    });

  });

  describe('hzLoginFinder', function(){

    var $compile, $rootScope, $timeout;

   
    beforeEach(module('hz'));
    beforeEach(inject(function(_$compile_, _$rootScope_, _$timeout_){
      $compile = _$compile_;
      $rootScope = _$rootScope_;
      $timeout = _$timeout_;
    }));     
    });

  });
})();