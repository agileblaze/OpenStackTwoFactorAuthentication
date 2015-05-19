angular.module('hz')
   .controller('hzOtpLoginCtrl', function($scope) {
      $scope.checked1 = true;
      if(document.getElementById(id_otp).value!="")
      {
      	$scope.checked1 = true;
      }
    })