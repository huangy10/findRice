require('./sharebox.less');
var share = require('../share/share');
var utils = require('../../utils');

module.exports = {
    /**
     * 展示分享框
     *
     * @param data
     *  - selector
     *  - shareLink
     *  - width
     */
    show: function(data) {

        if (!data || !data.shareLink) {
            return;
        }

        // 检测是否已登陆
        if (!utils.isLogin()) {
            location.href = '/login?next=' + encodeURI(location.href);
            return;
        }

        var id = data.id || 'share-dialog';
        var idSelector = '#' + id;
        var $dialog = $(idSelector);
        var shareLink = data.shareLink;
        var width = data.width || 500;
        var compiledTpl;

        if (shareLink.indexOf('/') === 0) {
            shareLink = 'http://zhao-mi.net' + shareLink;
        }

        compiledTpl = utils.compileTpl(SHAREBOX_TPL, {
            id: id,
            shareLink: shareLink
        })

        if (!$dialog.length) {
            $dialog = $(compiledTpl);
            $('body').append($dialog);
            $dialog.on('click', '.socials span', function() {
                var webid = $(this).data('webid');
                share({
                    webid: webid,
                    url: shareLink
                })
            })
        }

        $dialog.find('.share-link').text(shareLink);
        $dialog.find('.share-qrcode').empty().qrcode({
            render: 'table',
            text: shareLink,
            width: 200,
            height: 200
        });

        $dialog.dialog({
            resizable: false,
            width: width,
            modal: true,
            title: '通过以下专属渠道分享，可为您自动计算米币'
        });

        
    }
}

var SHAREBOX_TPL = '<div id="{id}" class="z-dialog share-dialog">' +
            '<p class="dialog-txt">复制连接分享</p>' +
            '<span class="share-link">{shareLink}</span>' +
            '<p class="dialog-txt">手机扫一扫，分享给更多人</p>' +
            '<span class="share-qrcode"></span>' +
            '<p class="dialog-txt mb0">点击分享到更多平台</p>' +
            '<p class="dialog-txt-hint">微信好友、朋友圈请使用手机微信扫描后分享</p>' +
            '<div class="socials">' +
                '<span id="wechat" title="请用微信扫描上方二维码后分享"></span>' +
                '<span id="wechat-group" title="请用微信扫描上方二维码后分享"></span>' +
                '<span id="qq" data-webid="cqq"></span>' +
                '<span id="sina" data-webid="tsina" class="last"></span>' +
            '</div>' +
        '</div>';