require('../../../common/pkgs/button/button');
require('../../../common/pkgs/progress/progress');
require('../css/create');

var header = require('../../header/js/header');

$(function() {
    $('#city').citySelect({
        prov: '北京',
        nodata: "none"
    });

    $('#form_datetime_start').datetimepicker({
        language: 'zh-CN',
        weekStart: 1,
        autoclose: 1,
        startView: 1,
        forceParse: 0,
        showMeridian: 1,
        minView: 0,
        maxView: 4,
        format: 'yyyy-mm-dd hh:ii',
        initialDate: new Date()
    }).on('changeDate', function(ev) {
        var startDate = $('#startdate').val();

        $('#form_datetime_end').datetimepicker({
            language: 'zh-CN',
            weekStart: 1,
            autoclose: 1,
            startView: 1,
            forceParse: 0,
            showMeridian: 1,
            minView: 0,
            maxView: 4,
            format: 'yyyy-mm-dd hh:ii',
            startDate: startDate,
            initialDate: startDate
        })
    });

    var $actionTypeContainer = $('#action-type-c');
    var $actionTypeDroplist = $actionTypeContainer.find('#action-type-droplist');
    var $actionType = $actionTypeContainer.find('#action-type');

    $('#action-type-c').on('mouseenter', function() {
        $actionTypeDroplist.show();
    }).on('mouseleave', function() {
        $actionTypeDroplist.hide();
    }).on('click', 'ul li', function() {
        var actionTypeTxt = $(this).data('txt');
        var actionType = $(this).data('val');
        $actionTypeContainer.find('p').text(actionTypeTxt);
        $actionType.val(actionType);
        $actionTypeDroplist.hide();
    });
});