require('../../../common/pkgs/button/button');
require('../css/register');

$(function() {
    // 处理在ff下的bug
    if ($.browser.mozilla) {
        $(document).on('click', 'label', function(e) {
            if (e.currentTarget === this && e.target.nodeName !== 'INPUT') {
                $(this.control).click();
            }
        });
    }

    $('.form_datetime').datetimepicker({
        language: 'zh-CN',
        weekStart: 1,
        autoclose: 1,
        startView: 4,
        forceParse: 0,
        showMeridian: 1,
        minView: 2,
        maxView: 4,
        format: 'yyyy-mm-dd',
        initialDate: new Date('1990-01-01')
    });

    var $genderContainer = $('#gender-c');
    var $genderDroplist = $genderContainer.find('#gender-droplist');
    var $gender = $genderContainer.find('#gender');

    $('#gender-c').on('mouseenter', function() {
        $genderDroplist.show();
    }).on('mouseleave', function() {
        $genderDroplist.hide();
    }).on('click', 'ul li', function() {
        var genderTxt = $(this).data('txt');
        var gender = $(this).data('val');
        $genderContainer.find('p').text(genderTxt);
        $gender.val(gender);
        $genderDroplist.hide();
    });
});