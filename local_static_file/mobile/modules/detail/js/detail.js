require('../../../common/pkgs/button/button');
require('../css/detail');
require('../../../lib/jquery-form/jquery.form');
var common = require('../../../lib/common/common.js');
var zhaomi = common;
var ValidateForm = require('../../../lib/common/validateform.js');
$(function() {
    var main = {
        init: function() {
            this.initEvents();
        },
        initEvents: function() {
            var $formCondition = this.$formCondition = $('#formCondition');
            var $banner = $('.banner');
            $formCondition.on('blur', 'input, textarea', function(e) {
                var $this = $(e.currentTarget);
                ValidateForm.checkInput($this);
            });

            $formCondition.on('change', 'input[type=radio], input[type=checkbox]', function(e) {
                var $this = $(e.currentTarget);
                ValidateForm.checkInput($this);
            });
            $formCondition.submit(function() {
                var data = collectData();
                var $applyBtn = $formCondition.find('.btn-submit');
                var $applyBtnW = $applyBtn.parent();
                
                if ($applyBtnW.hasClass('ing')) {
                    return false;
                }

                $(this).ajaxSubmit({
                    beforeSubmit: function() {

                        var $fileInputs = $('input[type="file"]');
                        var isValid = true;


                        // if (!common.isLogin()) {
                        //     location.href = '/login?next=' + encodeURI(location.href);
                        // }

                        for (var i = 0, leni = $fileInputs.length; i < leni; i++) {
                            if (!$fileInputs.eq(i).data('valid')) {
                                isValid = false;
                                break;
                            }
                        }

                        if (!isValid) {
                            common.warn('请上传png/jpg图片！');
                            return false;
                        }

                        if ($('.content .item').length !== data.length) {
                           common.warn('有题目未作答！')
                           return false;
                        }

                        $applyBtnW.addClass('ing');
                        $applyBtn.text('报名中...');
                        // return ValidateForm.checkForm($formCondition);
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
                                // $('#' + key).removeClass('focus').addClass('err');
                                common.warn(data[key]);

                                $applyBtnW.removeClass('ing');
                                $applyBtn.text('报名');
                                break;
                            }
                        }
                    }
                });

                return false;
            });
            $banner.on('click', '.like', function() {
                var $like = $(this).find('i');
                var $actionCard = $(this).closest('.banner');
                var actionId = $actionCard.data('id');
                zhaomi.postData('/action/like', {
                    id: actionId
                }, function(res) {
                    var success = res && res.success;
                    var data = res && res.data;

                    if (success) {

                        if (data && data.url) {
                            location.href = data.url;
                        } else {
                            if ($like.hasClass('icon-like')) {
                                $like.removeClass('icon-like').addClass('icon-unlike');
                            } else {
                                $like.removeClass('icon-unlike').addClass('icon-like');
                            }
                        }
                    }
                })
            })

            var rValidImg = /\.(jpg|jpeg|png)$/;
            $('input[type="file"]').on('change', function() {
                if (rValidImg.test($(this).val())) {
                    $(this).data('valid', true);
                } else {
                    common.warn('请上传png/jpg图片！');
                }
            })
        }
    };
    main.init();
});
// window.collectData = collectData;
function collectData() {
    var data = [];
    var RADIO = 'radio';
    var CHECKBOX = 'checkbox';
    var QUESTION = 'question';
    var UPLOAD = 'upload';

    $('.content .item').each(function(idx, elem) {
        var q, type , opts = [];
        var $detailItem = $(elem);
        var singleRet;
        var arr = [];
        var question;

        type = $detailItem.data('type');
        
        if (type === RADIO || type === CHECKBOX) {
            $detailItem.find('.result-item')
                .each(function(idx, elem) {
                    if ($(elem).find('input:checked').length) {
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
