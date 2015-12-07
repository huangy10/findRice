var common = require('../../../lib/common/common.js');
var utils = common;
var zhaomi = common;

exports.init = function() {
    var btnMapper = {
        'approve': '<button class="zui-btn zui-btn-action" data-optype="approve">通过</button>',
        'approve_cancel': '<button class="zui-btn zui-btn-important" data-optype="approve_cancel">取消通过</button>',
        'deny': '<button class="zui-btn zui-btn-important" data-optype="deny">拒绝</button>',
        'deny_cancel': '<button class="zui-btn zui-btn-action" data-optype="deny_cancel">取消拒绝</button>',
        'finish': '<button class="zui-btn zui-btn-action" data-optype="finish">确认完成</button>',
        'finished': '<button class="zui-btn zui-btn-action" data-optype="finished">已完成</button>',
        'denied': '<button class="zui-btn zui-btn-important">已谢绝</button>'
    }

    $('.mine-content').on('click', '.zui-btn', function() {
        var $applyItemCon = $(this).closest('.apply-item-content');
        var $applyItem = $applyItemCon.closest('.apply-item');
        var $container = $applyItem.closest('#mine-container');
        var opType = $(this).data('optype');
        var actionId = $container.data('action');
        var targetId = $applyItem.data('target');
        var isFinished = $applyItem.data('status') === 'finished';

        switch (opType) {
            case 'deny':
                post(opType, actionId, targetId, function() {
                    addBtns(['deny_cancel', 'denied']);
                });
                break;
            case 'deny_cancel':
                post(opType, actionId, targetId, function() {
                    addBtns(['approve', 'deny']);
                });
                break;
            case 'approve':
                post(opType, actionId, targetId, function() {
                    addBtns(['finish', 'approve_cancel']);
                });
                break;
            case 'approve_cancel':
                post(opType, actionId, targetId, function() {
                    addBtns(['approve', 'deny']);
                });
                break;
            case 'finish':
                if (isFinished) {
                    post(opType, actionId, targetId, function() {
                        addBtns(['finished']);
                    });    
                } else {
                    var toast = common.modal({
                        countDown: {
                            timeout: 2,
                            text: '活动尚未结束，请结束后操作'
                        },
                        isSimpleModal: true
                    });
                    toast.show();   
                }
                break;
        }

        function removeBtns(opType) {
            if (btnMapper[opType]) {
                $applyItemCon.find('.zui-btn').remove();
            }
        }

        function addBtns(typeArr) {
            for (var i = 0, leni = typeArr.length; i < leni; i++) {
                $applyItemCon.append($(btnMapper[typeArr[i]]));
            }
        }

        function post(opType, actionId, target, callback) {
            zhaomi.postData('/mine/manage', {
                action: actionId,
                target: target,
                optype: opType,
            }, function(res) {
                var success = res && res.success;
                var data = res.data;

                if (res.success) {
                    removeBtns(opType);
                    callback();
                } else {
                    for (var i in data) {
                        utils.warn(data[i]);
                        break;
                    }
                    
                }
            });
        }
    })

}