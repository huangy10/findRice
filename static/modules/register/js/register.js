require('../../../common/pkgs/button/button');
require('../css/register');

var zhaomi = require('../../../lib/common/common');
var utils = require('../../../common/utils');
var rValidImg = /\.(jpg|jpeg|png)$/;

var toast = require('../../../common/pkgs/toast/toast');

$(function() {

    // placeholder polyfill
    $('input, textarea').placeholder();
    
    // 处理在ff下的bug
    if ($.browser.mozilla) {
        $(document).on('click', 'label', function(e) {
            if (e.currentTarget === this && e.target.nodeName !== 'INPUT') {
                $(this.control).click();
            }
        });
    }

    // 注册第一步
    $('#register-form').submit(function() {

        var username = $('#username').val();
        var pwd = $('#pwd').val();
        var confirmedPwd = $('#pwd-confirm').val();

        $(this).ajaxSubmit({
            beforeSubmit: function(formData, jqForm, options) {
                if (!username) {
                    utils.warn('请填写邮箱/用户名!');
                    return false;
                }

                if (!/^[\w-]+$/.test(username)) {
                    utils.warn('请使用字母、数字或下划线!');
                    return false;   
                }

                if (!pwd) {
                    utils.warn('请填写密码!');
                    return false;
                }

                if (pwd !== confirmedPwd) {
                    utils.warn('两次密码输入不相同!');
                    return false;
                }
            },
            dataType: 'json',
            success: function(res) {
                var success = res && res.success;
                var data = res && res.data;
                
                if (success) {
                    if (data.url) {
                        location.href = data.url;  
                    } 
                } else {
                    for (var key in data) {
                        $('#' + key).parent().removeClass('focus').addClass('err');
                        utils.warn(data[key]);
                        break;
                    }
                }
            }
        });

        return false;
    });

    $('input').focus(function() {
        $(this).parent().removeClass('err').addClass('focus');
    }).blur(function() {
        $(this).parent().removeClass('focus');
    })
    
    // 第二步注册
    $('#mobile-wrapper').on('click', '#sendcode', function() {

        var $wrapper = $('#mobile-wrapper');
        if ($wrapper.hasClass('disabled')) {
            return;
        }

        var mobile = $('#mobile').val();

        if (!mobile) {
            utils.warn('请先填写电话号码！');
            return false;
        }

        zhaomi.postData('/sendcode', {
            mobile: mobile
        }, function() {
            countdown($wrapper);
        })

        function countdown(wrapper) {
            var $sendCode = wrapper.find('#sendcode');
            var iId;
            var numCD = 60;

            wrapper.addClass('disabled');
            $sendCode.text('重新发送(' + --numCD + ')');

            iId = setInterval(function() {
                if (numCD <= 0) {
                    clearInterval(iId);
                    wrapper.removeClass('disabled');
                    $sendCode.text('重新发送');
                } else {
                    $sendCode.text('重新发送(' + --numCD + ')');
                }
            }, 1000);
        }
    })

    $('#portrait').on('change', function() {
        var portrait = $(this).val();
        var files, $uploadImgBox, objectUrl;

        if (portrait && !rValidImg.test(portrait)) {
            utils.warn('请上传png/jpg图片！');
            return false;
        }

        if (window.URL && window.URL.createObjectURL) {
            $uploadImgBox = $(this).closest('#portrait-c');
            
            objectUrl = window.URL.createObjectURL($(this)[0].files[0]);
            $uploadImgBox.find('img').attr('src', objectUrl);
        } else {
            $(this).siblings('span').css('visibility', 'visible');    
        }
    })

    // 注册第二步
    $('#register').submit(function() {
        var code = $('#verifycode').val();
        var name = $('#name').val();
        var gender = $('#gender').val();
        var bday = $('#bday').val();

        $(this).ajaxSubmit({
            beforeSubmit: function(formData, jqForm, options) {
                if (!code) {
                    utils.warn('请填写验证码!');
                    return false;
                }

                if (!name) {
                    utils.warn('请填写用户名/公司名!');
                    return false;
                }

                if (!gender) {
                    utils.warn('请选择性别!');
                    return false;
                }

                if (!bday) {
                    utils.warn('请选择生日!');
                    return false;
                }
            },
            dataType: 'json',
            success: function(res) {
                var success = res && res.success;
                var data = res && res.data;
                
                if (success) {
                    if (data.url) {
                        // location.href = data.url;  
                        toast.show({
                            txt: '注册成功，正在跳转…',
                            nextAction: data.url,
                            timeout: 2000
                        });
                    } 
                } else {
                    for (var key in data) {
                        $('#' + key).parent().removeClass('focus').addClass('err');
                        utils.warn(data[key]);
                        break;
                    }
                }
            }
        });

        return false;
    })
    
    // 重置密码
    $('#resetForm').submit(function() {
        
        var mobile = $('#mobile').val();
        var code = $('#verifycode').val();
        var pwd = $('#pwd').val();
        var pwdConfirmed = $('#pwd-confirm').val();

        $(this).ajaxSubmit({
            beforeSubmit: function(formData, jqForm, options) {
                if (!mobile) {
                    utils.warn('请填写手机号!');
                    return false;
                }

                if (!code) {
                    utils.warn('请填写验证码!');
                    return false;
                }

                if (!pwd) {
                    utils.warn('请填写密码!');
                    return false;
                }

                if (!pwdConfirmed) {
                    utils.warn('请填写确认密码!');
                    return false;
                }

                if (pwd !== pwdConfirmed) {
                    utils.warn('请确保两次填写的密码一致!');
                    return false;
                }
            },
            dataType: 'json',
            success: function(res) {
                var success = res && res.success;
                var data = res && res.data;
                
                if (success) {
                    if (data.url) {
                        location.href = data.url;  
                    } 
                } else {
                    for (var key in data) {
                        $('#' + key).parent().removeClass('focus').addClass('err');
                        utils.warn(data[key]);
                        break;
                    }
                }
            }
            
        }); 
        return false;
    })

    if ($('.form_datetime').datetimepicker) {
        $('.form_datetime').datetimepicker({
            language: 'zh-CN',
            weekStart: 1,
            autoclose: 1,
            startView: 4,
            forceParse: 0,
            minView: 2,
            maxView: 4,
            format: 'yyyy-mm-dd',
            pickerPosition: 'bottom-left',
            initialDate: new Date('1990-01-01')
        });
    }

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