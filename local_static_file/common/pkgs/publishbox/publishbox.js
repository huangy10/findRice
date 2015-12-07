require('./publishbox.less');
var utils = require('../../utils');
var shareBox = require('../sharebox/sharebox');

module.exports = {
    /**
     * 展示保存/发布成功框
     *
     * @param data
     *  - selector
     *  - shareLink
     *  - saveTxt
     *  - width
     */
    show: function(data) {

        if (!data || !data.shareLink ||
                !data.nextAction) {
            return;
        }

        var id = data.id || 'publish-dialog';
        var idSelector = '#' + id;
        var $dialog = $(idSelector);
        var shareLink = data.shareLink;
        var saveTxt = data.saveTxt || '保存成功';
        var isVerified = data.isVerified;
        var verifiedUserAction = data.verifiedUserAction;
        var nextAction = data.nextAction;
        var width = data.width || 500;
        var compiledTpl;

        if (shareLink.indexOf('/') === 0) {
            shareLink = 'http://zhao-mi.net' + shareLink;
        }

        compiledTpl = utils.compileTpl(isVerified ? PUBLISHBOX_TPL : PUBLISHBOX_N_TPL, {
            id: id,
            shareLink: shareLink,
            saveTxt: saveTxt,
            nextAction: nextAction,
            verifiedUserAction: verifiedUserAction
        })

        if (!$dialog.length) {
            $dialog = $(compiledTpl);
            $('body').append($dialog);

            $dialog.on('click', '.share', function() {
                shareBox.show({
                    selector: idSelector,
                    shareLink: shareLink
                })
            })
        }

        $dialog.dialog({
            dialogClass: 'without',
            resizable: false,
            modal: true,
            width: width,
            title: ''
        });

    }
}

var PUBLISHBOX_TPL = '<div id="{id}" class="tip-dialog">' +
            '<div class="save-icon-w">' +
                '<span class="save-icon"></span>' +
            '</div>' +
            '<p class="save-txt">{saveTxt}</p>' +
            '<div class="goto">' +
                '<a href="{nextAction}" target="_self" class="confirm">确认</a>' +
            '</div>' +
        '</div>';

var PUBLISHBOX_N_TPL = '<div id="{id}" class="tip-dialog">' +
            '<div class="save-icon-w">' +
                '<span class="save-icon"></span>' +
            '</div>' +
            '<p class="save-txt">{saveTxt}</p>' +
            '<p class="save-tips">只有认证用户可将活动发布至找米平台首页，您可以直接分享邀请朋友加入</p>' +
            '<div class="btns">' +
                '<a class="z-btn share" data-link={shareLink}>分享</a>' +
                '<a class="z-btn" href="{verifiedUserAction}" target="_blank">申请认证用户</a>' +
            '</div>' +
            '<div class="goto">' +
                '<a href="{nextAction}" target="_self" class="confirm">确认</a>' +
            '</div>' +
        '</div>';