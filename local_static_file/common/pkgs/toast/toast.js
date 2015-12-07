require('../box/box.less');
require('./toast.less');
var utils = require('../../utils');

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

        if (!data) {
            return;
        }

        var id = data.id || 'toast-dialog';
        var idSelector = '#' + id;
        var $dialog = $(idSelector);
        
        var txt = data.txt || '操作成功';
        var width = data.width || 320;
        var toastTimeout = data.timeout || 3000;
        var nextAction = data.nextAction;
        var compiledTpl;

        compiledTpl = utils.compileTpl(TOAST_TPL, {
            id: id,
            txt: txt
        })

        if (!$dialog.length) {
            $dialog = $(compiledTpl);
            $('body').append($dialog);
        }

        $dialog.dialog({
            dialogClass: 'without toast',
            resizable: false,
            modal: true,
            width: width,
            title: ''
        });

        setTimeout(function() {
            $dialog.dialog('close');
            if (nextAction) {
                location.href = nextAction;  
            }
        }, toastTimeout);
    }
}

var TOAST_TPL = '<div id="{id}" class="tip-dialog">' +
      '<p class="txt">{txt}</p>' +
      '</div>';