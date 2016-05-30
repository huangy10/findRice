require('../../../common/pkgs/button/button');
var ValidateForm = require('../../../lib/common/validateform');
require('../css/login');
var common = require('../../../lib/common/common.js');


var utils = common;

$(function() {
    var $pageRegister = $('#pageRegister');
    var $pageLogin = $('#pageLogin');
    var $pageReset = $('#pageReset');

    $pageRegister.show();
    var main = {
        init: function() {
            this.initEvent();
            this.initDatePicker();
        },
        initDatePicker: function() {
            var $appDate = $("#appDate");
            if ($appDate.length) {
                var currYear = (new Date()).getFullYear();
                var opt = {};
                opt.date = {preset: 'date'};
                opt.datetime = {preset: 'datetime'};
                opt.time = {preset: 'time'};
                opt.default = {
                    theme: 'android-ics light', //皮肤样式
                    display: 'modal', //显示方式
                    mode: 'scroller', //日期选择模式
                    dateFormat: 'yyyy-mm-dd',
                    lang: 'zh',
                    showNow: true,
                    nowText: "今天",
                    startYear: currYear - 10, //开始年份
                    endYear: currYear + 10 //结束年份
                };

                $appDate.mobiscroll($.extend(opt['date'], opt['default']));
            }

        },
        initEvent: function() {
            if ($pageRegister.length) {
                this.initInputEvent($pageRegister);
                this.initInputEventForm($pageRegister);

            } else if ($pageLogin.length) {
                this.initInputEvent($pageLogin);

            } else if ($pageReset.length) {
                this.initInputEvent($pageReset);

                this.initInputEventForm($pageReset);
            }
        },
        initInputEventForm: function($page) {
            this.$verifyResultMsg = $('.verify-result-msg');

            var that = this;
            var vaildUtil = ValidateForm;

            $page.on('blur', '.reset-password #pwd1', function(e) {
                var $this = $(e.currentTarget);
                var value = $this.val();
                //if (value.length > 18 || value.length < 6 ){
                if (vaildUtil.isPwd(value)) {
                    that.hideVerifyResultMsg($this);
                } else {
                    that.showVerifyResultMsg($this, '密码长度在6~18之间');
                }
            });

            $page.on('blur', '.reset-password #pwd2', function(e) {
                var $this = $(e.currentTarget);
                var value = $this.val();
                var pwd1Value = $("#pwd1").val();
                if (vaildUtil.isSamePwd(pwd1Value, value)) {
                    that.hideVerifyResultMsg($this);
                } else {
                    that.showVerifyResultMsg($this, '两次密码不一致');
                }
            });

            $page.on('blur', 'input.phone', function(e) {
                var $this = $(e.currentTarget);
                var value = $this.val();

                if (vaildUtil.isMobile(value)) {
                    that.hideVerifyResultMsg($this);
                } else {
                    that.showVerifyResultMsg($this, '请输入正确的手机号');
                }
            });

            $page.on('blur', 'input#verifyCode', function(e) {
                var $this = $(e.currentTarget);
                var value = $this.val();
                if (value.length >= 3 && value.length <= 6) {
                    that.hideVerifyResultMsg($this);
                } else {
                    that.showVerifyResultMsg($this, '请输入正确的验证码');
                }
            });
        },

        showVerifyResultMsg: function($this, text) {
            var $inputWrapper = $this.closest('.input-wrapper');
            var $verifyResultMsg = this.$verifyResultMsg;
            $verifyResultMsg.show();
            $verifyResultMsg.find('.error-text').html(text);
            $inputWrapper.removeClass('success').addClass('error');
        },
        hideVerifyResultMsg: function($this) {
            var $inputWrapper = $this.closest('.input-wrapper');
            var $verifyResultMsg = this.$verifyResultMsg;
            $verifyResultMsg.hide();
            $inputWrapper.addClass('success').removeClass('error');

        },
        initInputEvent: function(obj) {

            obj.on('focus', '.input-wrapper input', function(e) {
                var $target = $(e.currentTarget);

                var $inputWrapper = $target.closest('.input-wrapper');
                $inputWrapper.addClass('focus');
            }).on('blur', '.input-wrapper input', function(e) {
                var $target = $(e.currentTarget);
                var $inputWrapper = $target.closest('.input-wrapper');
                $inputWrapper.removeClass('focus');
            });

        }
    };
    main.init();

    $('#login-form').submit(function() {
        
        var username = $('#username').val();
        var pwd = $('#pwd').val();

        $(this).ajaxSubmit({
            beforeSubmit: function(formData, jqForm, options) {
                if (!username) {
                    utils.warn('请填写邮箱/用户名!');
                    return false;
                }

                if (!pwd) {
                    utils.warn('请填写密码!');
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
                        $('#' + key).parents('.input-wrapper').addClass('error');
                        utils.warn(data[key]);
                        break;
                    }
                }
            }
        });

        return false;
    });
});