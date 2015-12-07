require('../../../common/pkgs/button/button');
require('../css/activity');
var common = require('../../../lib/common/common.js');
var applyList = require('./apply-list');

$(function() {

    var main = {
        init: function() {
            $('.look-detail').on('touchend', function(e) {
                var $target = $(e.currentTarget);
                $target.closest('.tr').toggleClass('open')
            })
        }

    };
    main.init();
    applyList.init();
});