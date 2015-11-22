require('../../../common/pkgs/button/button');
require('../css/mine');

var header = require('../../header/js/header');
var zhaomi = require('../../../lib/common/common');
var shareBox = require('../../../common/pkgs/sharebox/sharebox');
var exchangeBox = require('../../../common/pkgs/exchange/exchange');
var toast = require('../../../common/pkgs/toast/toast');
var utils = require('../../../common/utils');
var applyList = require('./apply-list');
var personalMod = require('./personal-info');
var rValidImg = /\.(jpg|jpeg|png)$/;

$(function() {
    applyList.init();
    personalMod.init();

    var $list = $('#list');
    // 展示报名列表中的申请人详细信息
    $('#apply-list').on('click', '.detail', function() {
        var $content = $(this).closest('.apply-item').find('.detail-content');

        if ($(this).hasClass('on')) {
            $content.hide();
            $(this).removeClass('on');
        } else {
            $content.show();
            $(this).addClass('on');
        }   
    })

    // 活动信息中的各种操作
    $list.on('click', '.action-card', function(evt) {

        var $target = $(evt.target);
        // 点击opertion区域不算
        if ($target.hasClass('view') || 
            $target.hasClass('edit') ||
            $target.hasClass('duplicate') ||
            $target.hasClass('delete') ||
            $target.hasClass('b-share') ||
            $target.hasClass('like') || 
            $target.hasClass('c-share') ||
            $target.hasClass('share') ||
            $target.hasClass('apply-forbidden') ||
            $target.hasClass('publish') ||
            $target.hasClass('unapply') ||
            $target.hasClass('apply-resume')) {
            return false;
        }

        var $actionCard = $(this).closest('.action-card');
        var shareLink = $actionCard.data('link');
        var detailLink = $actionCard.data('detail');

        if (shareLink || detailLink) {
            window.open(shareLink || detailLink, '_blank');
        }
        
    }).on('click', '.action-card .view', function() {
        var action = $(this).data('action');
        if (action) {
            window.location.href = action;    
        }
    }).on('click', '.action-card .edit', function() {
        var action = $(this).data('action');
        if (action) {
            window.location.href = action;    
        }
    }).on('click', '.action-card .duplicate', function() {
        var action = $(this).data('action');

        if (confirm('确认要复制该活动吗？')) {
            if (action) {
                zhaomi.postData(action, {}, function(res) {
                    var success = res && res.success;
                    var data = res && res.data;
                    
                    if (success) {
                        if (data.url) {
                            location.href = data.url;  
                        } 
                    }
                });
            }    
        }
        
    }).on('click', '.action-card .delete', function() {
        var action = $(this).data('action');

        if (confirm('确认要删除该活动吗？')) {
            if (action) {
                zhaomi.postData(action, {}, function(res) {
                    var success = res && res.success;
                    var data = res && res.data;
                    
                    if (success) {
                        if (data.url) {
                            location.href = data.url;  
                        } 
                    }
                });
            }
        }
        
    }).on('click', '.action-card .c-share, .action-card .b-share, .action-card .share', function() {
        var $actionCard = $(this).closest('.action-card');
        var shareLink = $actionCard.data('link');

        if (shareLink) {
            shareBox.show({
                shareLink: shareLink
            })
        }
    }).on('click', '.action-card .like', function() {
        var $like = $(this);
        var $actionCard = $(this).closest('.action-card');
        var actionId = $actionCard.data('id');
        
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
    }).on('click', '.action-card .publish', function() {
        var $actionCard = $(this).closest('.action-card');
        var actionId = $actionCard.data('id');

        if (actionId) {
            zhaomi.postData('/action/' + actionId + '/publish', {
                from: 'start'
            }, function(res) {
                var success = res && res.success;

                if (success) {
                    location.href = '/mine/start';
                }
            });    
        }
        
    }).on('click', '.action-card .apply-forbidden', function() {
        var $actionCard = $(this).closest('.action-card');
        var actionId = $actionCard.data('id');

        if (actionId) {
            zhaomi.postData('/action/' + actionId + '/stop', {
                
            }, function(res) {
                var success = res && res.success;

                if (success) {
                    location.href = '/mine/start';
                }
            });    
        }
    }).on('click', '.action-card .apply-resume', function() {
        var $actionCard = $(this).closest('.action-card');
        var actionId = $actionCard.data('id');

        if (actionId) {
            zhaomi.postData('/action/' + actionId + '/start', {
                
            }, function(res) {
                var success = res && res.success;

                if (success) {
                    location.href = '/mine/start';
                }
            });    
        }
    }).on('click', '.action-card .unapply', function() {
        var $actionCard = $(this).closest('.action-card');
        var actionId = $actionCard.data('id');

        if (actionId) {
            zhaomi.postData('/action/' + actionId + '/unapply', {
                
            }, function(res) {
                var success = res && res.success;

                if (success) {
                    toast.show({
                        txt: '取消申请成功，即将刷新页面…',
                        nextAction: '/mine/apply',
                        timeout: 2000
                    });
                    // location.href = '/mine/apply';
                }
            });
        }
    });

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
            $('#personal-info img').attr('src', objectUrl);
        } else {
            $(this).siblings('span').css('visibility', 'visible');    
        }
    })

    // 推荐注册
    $('#personal-info-origin').on('click', '.exchange', function() {
        exchangeBox.show()
    });

    var fullDataReturned = true;
    var start = 12, size = 12;

    utils.loadMore(function() {

        if (!fullDataReturned) {
            return;
        }

        $.ajax({
            url: utils.getJSONPUrl(start, size),
            dataType: 'jsonp',
            success: function(data) {
                data = data || {};
                if (data.size === size) {
                    fullDataReturned = true;
                    start = start + size;
                } else {
                    fullDataReturned = false;
                }
                
                $('#list ul').append(data.html);
                
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown)
            }
        });

    })

});