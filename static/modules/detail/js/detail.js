require('../../../common/pkgs/button/button');
require('../css/detail');

var header = require('../../header/js/header');
var shareBox = require('../../../common/pkgs/sharebox/sharebox');
var utils = require('../../../common/utils');
var zhaomi = require('../../../lib/common/common');

var RADIO = 'radio';
var CHECKBOX = 'checkbox';
var QUESTION = 'question';
var UPLOAD = 'upload';

$(function() {

    var $detailContainer = $('#detail-container');
    var $detailQuestions = $detailContainer.find('#detail-questions');

    $detailQuestions.on('click', '.detail-answers li', function() {
        var $detailItem = $(this).closest('.detail-item');
        var type = $detailItem.data('type');

        if (type === RADIO) {
            $(this).parents('.detail-answers').find('span').removeClass('selected');
            $(this).find('span').addClass('selected');
        } else if (type === CHECKBOX) {
            $(this).find('span').toggleClass('selected');
        }
    })

    $detailContainer.on('click', '.share, .share-bonus', function(e) {
        var shareLink = $detailContainer.data('link');
        if (shareLink) {
            shareBox.show({
                selector: '#share-dialog',
                shareLink: shareLink
            })
        }
        
    }).on('click', '.like', function() {
        var $like = $(this);
        var actionId = $like.data('id');
        
        zhaomi.postData('/action/like', {
            id: actionId
        }, function(res) {
            var success = res && res.success;
            var data = res && res.data;

            if (success) {
                if (data.url) {
                    location.href = data.url;
                } else {
                    $like.toggleClass('selected');    
                }
            }
        })
    })

    var rValidImg = /\.(jpg|jpeg|png)$/;
    $('input[type="file"]').on('change', function() {
        if (rValidImg.test($(this).val())) {
            $(this).data('valid', true);
        } else {
            utils.warn('请上传png/jpg图片！');
        }
    })

    $('#apply-form').submit(function(ev) {
        var data = collectData();

        var $applyBtnW = $(this).find('#detail-apply');
        var $applyBtn = $applyBtnW.find('.apply');

        if ($applyBtnW.hasClass('ing')) {
            return false;
        }

        $(this).ajaxSubmit({
            beforeSubmit: function() {

                var $fileInputs = $('input[type="file"]');
                var isValid = true;

                if (!utils.isLogin()) {
                    location.href = '/login?next=' + encodeURI(location.href);
                    return false;
                }

                for (var i = 0, leni = $fileInputs.length; i < leni; i++) {
                    if (!$fileInputs.eq(i).data('valid')) {
                        isValid = false;
                        break;
                    }
                }

                if (!isValid) {
                    utils.warn('请上传png/jpg图片！');
                    return false;
                }

                if ($('.detail-item').length !== data.length) {
                    utils.warn('有题目未作答！');
                    return false;
                }

                $applyBtnW.addClass('ing');
                $applyBtn.text('报名中...');
            },
            dataType: 'json',
            data: {
                answer: JSON.stringify(data)
            },
            success: function(res) {
                var success = res && res.success;
                var data = res && res.data;
                
                if (success) {
                    if (data.url) {
                        location.href = data.url;  
                    } 
                } else {
                    for (var key in data) {
                        $('#' + key).removeClass('focus').addClass('err');
                        utils.warn(data[key]);

                        $applyBtnW.removeClass('ing');
                        $applyBtn.text('报名');
                        break;
                    }
                }
            }
        })

        return false;
    })

})

function collectData() {
    var data = [];

    $('.detail-item').each(function(idx, elem) {
        var q, type , opts = [];
        var $detailItem = $(elem);
        var singleRet;
        var arr = [];
        var question;

        type = $detailItem.data('type');
        
        if (type === RADIO || type === CHECKBOX) {
            $detailItem.find('.detail-answers li')
                .each(function(idx, elem) {
                    if ($(elem).children('span').hasClass('selected')) {
                        arr.push(idx);
                    }
                })

            if (arr.length) {
                data.push({
                    type: type,
                    result: type === RADIO? arr[0] : arr
                })
            }
            
        } else if (type === QUESTION) {
            question = $detailItem.find('textarea').val();

            if (question) {
                data.push({
                    type: type,
                    result: question
                })
            }
        } else if (type === UPLOAD) {
            if ($detailItem.find('input').val()) {
                data.push({
                    type: type,
                    name: $detailItem.find('input').attr('name'),
                    result: 'whatever'
                })
            }
        }
    })

    return data;
}