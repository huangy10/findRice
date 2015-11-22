var utils = require('../../../common/utils');
var shareBox = require('../../../common/pkgs/sharebox/sharebox');

exports.init = function() {

    var $personalInfo = $('#personal-info-origin');
    var $modifiedInfo = $('#personal-info-modify');
    var $form = $('#personal-info-form');
    
    $personalInfo.on('click', '.edit', function() {
        $personalInfo.hide();
        $modifiedInfo.show();
    }).on('click', '.recommend', function() {
        var shareLink = $(this).data('link');

        if (shareLink) {
            shareBox.show({
                shareLink: shareLink
            })
        }
    });

    $form.submit(function() {

        var name = $('#info-name').val();
        var mobile = $('#info-mobile').val();
        var gender = $('#info-gender').val();
        var bday = $('#info-bday').val();

        $(this).ajaxSubmit({
            beforeSubmit: function(formData, jqForm, options) {
                
                // if (!name) {
                //     utils.warn('请填写姓名!');
                //     return false;
                // }

                // if (!mobile) {
                //     utils.warn('请填写手机号!');
                //     return false;
                // }

                // if (!gender || (gender !== '男' && gender !== '女')) {
                //     utils.warn('请正确填写性别!');
                //     return false;
                // }

                // if (!bday || !/\d{4}\-\d{2}-\d{2}/.test(bday)) {
                //     utils.warn('请选择生日，格式为1990-01-01!');
                //     return false;
                // }
            },
            dataType: 'json',
            success: function(res) {
                var success = res && res.success;
                var data = res && res.data;
                
                if (success) {
                    $personalInfo.show();
                    $modifiedInfo.hide(); 
                    for (var key in data) {
                        if (key === 'portrait' && data[key]) {
                            $personalInfo.find('.portrait img')
                                .attr('src', data[key]);
                        } else {
                            $personalInfo.find('#' + key).text(data[key]);    
                        }
                    }
                } else {
                    for (var key in data) {
                        utils.warn(data[key]);
                        break;
                    }
                }
            }
        });

        return false;
    });
}