require('../../../common/pkgs/button/button');
require('../../../common/pkgs/box/box');
require('../../../common/pkgs/progress/progress');
require('../css/create');

require('../../header/js/header');

var utils = require('../../../common/utils');
var publishBox = require('../../../common/pkgs/publishbox/publishbox');

$(function() {

    var $form = $('#create-action-final');
    
    $('#publish').click(function() {

        if (!utils.isLogin()) {
            location.href = '/login?next=' + encodeURI(location.href);
            return;
        }

        var $publishWrapper = $(this).parents('#action-publish');
        var $container = $(this).parents('#action-container');
        var isVerified = $container.data('verified') === 'yes';
        var verifiedAction = $container.data('verifiedaction');
        var shareLink = $container.data('link');

        if (!$publishWrapper.hasClass('ing')) {
            $publishWrapper.addClass('ing');
            $form.ajaxForm({
                dataType: 'json',
                success: function(res) {
                    var success = res && res.success;
                    var data = res && res.data;
                    
                    if (success) {
                        if (data.url) {
                            publishBox.show({
                                id: 'publish-box',
                                shareLink: shareLink,
                                nextAction: data.url,
                                verifiedUserAction: verifiedAction,
                                saveTxt: '发布成功',
                                isVerified: isVerified
                            })
                        } 
                    } else {
                        for (var key in data) {
                            $('#' + key).removeClass('focus').addClass('err');
                            utils.warn(data[key]);
                            break;
                        }
                    }
                }
            })

            $form.submit();
        }
    });

    $('#save').click(function() {

        if (!utils.isLogin()) {
            location.href = '/login?next=' + encodeURI(location.href);
            return;
        }

        var actionUrl = $(this).data('action');
        var $publishWrapper = $(this).parents('#action-publish');
        var $container = $(this).parents('#action-container');
        var isVerified = $container.data('verified') === 'yes';
        var verifiedAction = $container.data('verifiedaction');
        var shareLink = $container.data('link');

        if (!$publishWrapper.hasClass('ing')) {

            $publishWrapper.addClass('ing');
            $form.ajaxForm({
                url: actionUrl,
                dataType: 'json',
                success: function(res) {
                    var success = res && res.success;
                    var data = res && res.data;
                    
                    if (success) {
                        if (data.url) {
                            publishBox.show({
                                id: 'save-box',
                                shareLink: shareLink,
                                nextAction: data.url,
                                verifiedUserAction: verifiedAction,
                                saveTxt: '保存成功',
                                isVerified: isVerified
                            })
                        }
                    } else {
                        for (var key in data) {
                            $('#' + key).removeClass('focus').addClass('err');
                            utils.warn(data[key]);
                            break;
                        }
                    }
                }
            })

            $form.submit();
        }
        

        
    });
    
});