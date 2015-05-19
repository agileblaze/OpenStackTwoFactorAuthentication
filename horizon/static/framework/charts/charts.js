(function() {
  'use strict';

  /**
   * @ngdoc overview
   * @name hz.widget.charts
   * @description
   *
   * # hz.widget.charts
   *
   * The `hz.widget.charts` module provides directives for simple charts
   * used in Horizon, such as the pie and donut chart. Charts are
   * implemented using D3.
   *
   * Requires {@link http://d3js.org `D3`} to be installed.
   *
   * | Constants                                                                 |
   * |---------------------------------------------------------------------------|
   * | {@link hz.widget.charts.constant:donutChartSettings `donutChartSettings`} |
   * | {@link hz.widget.charts.constant:quotaChartDefaults `quotaChartDefaults`} |
   *
   * | Directives                                                                |
   * |---------------------------------------------------------------------------|
   * | {@link hz.widget.charts.directive:pieChart `pieChart`}                    |
   *
   */
  angular.module('hz.widget.charts', [])

    /**
     * @ngdoc parameters
     * @name hz.widget.charts.constant:donutChartSettings
     * @param {number} innerRadius Pie chart inner radius in pixels, default: 24
     * @param {number} outerRadius Pie chart outer radius in pixels, default: 30
     * @param {object} label with properties font-size and fill (optional)
     * @param {string} titleClass CSS class to override title,
     *  default: pie-chart-title-medium
     *  alternative: pie-chart-title-large
     * @param {boolean} showTitle Show title, default: true
     * @param {boolean} showLabel Show label, default: true
     * @param {boolean} showLegend Show legend default: true
     * @param {string} tooltipIcon Tooltip key icon, default: 'fa-square'
     *
     */
    .constant('donutChartSettings', {
      innerRadius: 24,
      outerRadius: 30,
      titleClass: 'pie-chart-title-medium',
      showTitle: true,
      showLabel: true,
      showLegend: true,
      tooltipIcon: 'fa-square'
    })

    /**
     * @ngdoc parameters
     * @name hz.widget.charts.constant:pieChartSettings
     * @param {number} innerRadius Pie chart inner radius in pixels, default: 0
     * @param {number} outerRadius Pie chart outer radius in pixels, default: 30
     * @param {object} label with properties font-size and fill (optional)
     * @param {string} titleClass CSS class to override title,
     *  default: pie-chart-title-medium
     *  alternative: pie-chart-title-large
     * @param {boolean} showTitle Show title, default: true
     * @param {boolean} showLabel Show label, default: true
     * @param {boolean} showLegend Show legend default: true
     * @param {string} tooltipIcon Tooltip key icon, default: 'fa-square'
     *
     */
    .constant('pieChartSettings', {
      innerRadius: 0,
      outerRadius: 30,
      titleClass: 'pie-chart-title-medium',
      showTitle: true,
      showLabel: true,
      showLegend: true,
      tooltipIcon: 'fa-square'
    })

    /**
     * @ngdoc parameters
     * @name hz.widget.charts.constant:quotaChartDefaults
     * @param {string} usageLabel label text for Usage, default: 'Current Usage'
     * @param {string} usageColorClass css class for Usage , default: 'usage'
     * @param {string} addedLabel label text for Added, default: 'Added'
     * @param {string} addedColorClass CSS class for Added , default: 'added'
     * @param {string} remainingLabel label text for Remaining, default: 'Remaining'
     * @param {string} remainingColorClass CSS class for Remaining , default: 'remaining'
     *
     */
    .constant('quotaChartDefaults', {
      usageLabel: gettext('Current Usage'),
      usageColorClass: 'usage',
      addedLabel: gettext('Added'),
      addedColorClass: 'added',
      remainingLabel: gettext('Remaining'),
      remainingColorClass: 'remaining'
    })

    /**
     * @ngdoc filter
     * @name hz.widget.charts.filter:showKeyFilter
     * @function Filter based on 'hideKey' value of each slice
     * @returns {function} A filtered list of keys to show in legend
     *
     */
    .filter('showKeyFilter', function() {
      return function(items) {
        return items.filter(function (item) {
          return !item.hideKey;
        });
      };
    });

})();