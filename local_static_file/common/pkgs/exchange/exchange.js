require('./exchange.less');
var utils = require('../../utils');
var zhaomi = require('../../../lib/common/common');

var rAlipay = /^\w+$/;
var boxInited = false;

module.exports = {
    show: function(data) {

        data = data || {};
        var width = data.width || 500;
        var BOX_ID = 'exchange-box';
        var $box;

        if (!$('#' + BOX_ID).length) {
            $('body').append(utils.compileTpl(EXCHANGE_TPL, {}))
        }

        $box = $('#' + BOX_ID);
        $box.dialog({
            resizable: false,
            width: width
        });

        if (!boxInited) {
            boxInited = true;
            $box.find('.exchange-btn button').click(function() {
                var num = $box.find('.exchange-num').val();
                var alipayAcc = $box.find('.exchange-alipay').val();

                if (!num) {
                    utils.warn('请填写需要兑换的米币值');
                    return false;
                }

                if (!rAlipay.test(alipayAcc)) {
                    utils.warn('余额宝账号格式不对');
                    return false;
                }
                zhaomi.postData('/mine/exchange', {
                    num: num,
                    alipay: alipayAcc
                }, function(res) {
                    var success = res && res.success;
                    var data = res && res.data;

                    $box.dialog('close');
                    if (success) {
                        utils.warn('兑换成功，还剩 ' + data.coin + ' 米币');
                        $('.numMibi').text(data.coin + '米币');
                    } else {
                        for (var key in data) {
                            utils.warn(data[key]);
                            return false;
                        }
                    }
                })
            })
        }
        
    }
}

var EXCHANGE_TPL = '<div id="exchange-box">' +
        '<p class="exchange-txt">米币余额大于200的用户可以兑换米币提现，找米平台将于每月1日，15日向您的支付宝打款</p>' +
        '<div class="exchange-input">' +
            '<div class="exchange-item">' +
                '<span class="exchange-img exchange-img-mi"></span>' +
                '<input type="text" class="exchange-num" placeholder="请填写您希望兑换的米币金额">' +
            '</div>' +
            '<div class="exchange-item">' +
                '<span class="exchange-img exchange-img-alipay"></span>' +
                '<input type="text" class="exchange-alipay" placeholder="请留下您的支付宝账号">' +
            '</div>' +
        '</div>' +
        '<div class="exchange-btn">' +
            '<button class="z-btn green">兑换</button>' +
        '</div>' +
    '</div>';