module.exports = {
    isDigit: function(s) {
        var patrn = /^[0-9]{1,20}$/;
        if (!patrn.exec(s)) {
            return false
        }
        return true
    },
    isPwd: function(s) {
        var patrn = /^(\w){6,20}$/;
        if (!patrn.exec(s)) {
            return false
        }
        return true
    },
    isSamePwd: function(pwd1, pw2) {
        return pwd1 === pw2;
    },
    isMobile: function(s) {
        //var patrn=/^[+]{0,1}(\d){1,3}[ ]?([-]?(\d){1,12})+$/;
        var patrn = /^[+]{0,1}(\d){1,3}[ ]?([-]?((\d)|[ ]){1,12})+$/;

        var patrn = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
        if (!patrn.exec(s)) {
            return false
        }
        return true
    },

    validateForm: function($form) {
        var self = this;
        var isSuccess = true;
        var $input = $form.find('input');
        if ($input.length) {
            $input.each(function(index, item) {
                var $item = $(item);
                if (!isSuccess) {
                    return
                }
                if (!self.validateInput($item)) {
                    isSuccess = false;
                }

            })
        }
        return isSuccess;
    },
    checkInput: function(input) {
        return this.validateInput($(input))
    },
    checkForm: function(form) {
        return this.validateForm($(form))
    },
    validateInput: function($input) {
        var that = this;
        var value = $input.val();
        var ruleType = $input.data('rule-type');
        var inputType = $input.attr('type');
        var maxLenth = $input.data('max-length');
        var minLenth = $input.data('min-length');
        var nullMsg = $input.data('null-msg');
        var errorMsg = $input.data('error-msg');
        var required = $input.data('required');
        var length = value.length;

        if (ruleType == 'number') {
            length = +value;
            if (isNaN(length)) {
                return that.showValidateResult($input, '请输入正确的数字');
            }
        }

        if (inputType == 'file') {
            //file 校验规则;
        }
        if (inputType == 'radio' || inputType == 'checkbox') {
            //file 校验规则;
            var $checked = $input.closest('.input-wrapper').find("input:checked");
            if (!$checked.length) {
                return that.showValidateResult($input, nullMsg);
            } else {
                return that.hideValidateResult($input, nullMsg);
            }
        }

        if (!length && required) {
            return that.showValidateResult($input, nullMsg);
        }
        //存在
        if (maxLenth && (length > maxLenth) && errorMsg) {
            return that.showValidateResult($input, errorMsg);
        }

        if (minLenth >= 0 && length < minLenth) {
            return that.showValidateResult($input, errorMsg);
        }
        return that.hideValidateResult($input);
    },

    showValidateResult: function($this, msg, inputWrapperClass) {
        if (!msg) {
            msg = '此项不能为空';
        }
        if (!inputWrapperClass) {
            inputWrapperClass = '.input-wrapper';
        }
        var $inputWrapper = $this.closest(inputWrapperClass);
        var $Validform_checktip = $inputWrapper.find('.Validform_checktip');
        if (!$Validform_checktip.length) {
            $Validform_checktip = $('<span class="Validform_checktip "></span>')
        }
        $inputWrapper.append($Validform_checktip);
        $this.addClass('Validform_error');
        $Validform_checktip.show().addClass('Validform_wrong').html(msg);
        return false;

    },
    hideValidateResult: function($this, inputWrapperClass) {
        console.log('hideValidateResult');
        $this.removeClass('Validform_error');
        if (!inputWrapperClass) {
            inputWrapperClass = '.input-wrapper';
        }
        var $inputWrapper = $this.closest(inputWrapperClass);
        var $Validform_checktip = $inputWrapper.find('.Validform_checktip');
        if ($Validform_checktip.length) {
            $Validform_checktip.hide();
        }
        return true;
    }
};