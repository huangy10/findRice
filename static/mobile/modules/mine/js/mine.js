require('../../../common/pkgs/button/button');
require('../css/mine');
var common = require('../../../lib/common/common.js');

var zhaomi = common;
var utils = common;
var rAlipay = /^\w+$/;
var rValidImg = /\.(jpg|jpeg|png)$/;

$(function() {

    var $list = $('.activity-lists');
    var $form = $('#personal-info-form');

    var main = {
        init: function() {
            this.$pageMine = $('#pageMine');
            var $userCenterPage = this.$userCenterPage = this.$pageMine.find('#userCenterPage');
            if ($userCenterPage.length) {
                this.isUserCenterPage = true;
            }
            this.initEvent();
            this.initDatePicker();

        },
        initDatePicker: function() {
            var $target = $('.bday .edit-input');
            var opt={};
            opt.date = {preset : 'date'};
            opt.datetime = {preset : 'datetime'};
            opt.time = {preset : 'time'};
            opt.default = {
                theme: 'android-ics light', //皮肤样式
                display: 'modal', //显示方式
                dateFormat: 'yy-mm-dd',
                mode: 'scroller', //日期选择模式
                lang: 'zh',
                showNow: true,
                nowText: "今天"
            };
            if ($target.mobiscroll) {
                $target.mobiscroll($.extend(opt['date'], opt['default']));    
            }
        },
        initEvent: function() {
            var that = this;
            if (this.isUserCenterPage) {
                this.$userCenterPage.on('click', '.btn-edit', function(e) {
                    var $userMsg = $(this).closest('.content');
                    $userMsg.addClass('editing');
                });

                var $userMsg = $('#user-msg');
                var $form = $('#personal-info-form');
                var $exchangeBox = $('#exchange-box');
                var $otherMsg = $('.other-msg');
                var $bottom = $('.bottom');

                $userMsg.on('click', '.exchange', function() {
                    $otherMsg.hide();
                    $exchangeBox.show();
                    $bottom.hide();

                }).on('click', '.share', function() {
                    utils.warn('请在保证登录后，通过浏览器自带分享功能分享！');
                });

                $('.upload-img-box input').change(function(evt) {
                    var portrait = $(this).val();
                    var files, $uploadImgBox, objectUrl;

                    if (portrait && !rValidImg.test(portrait)) {
                        utils.warn('请上传png/jpg图片！');
                        return false;
                    }

                    if (window.URL && window.URL.createObjectURL) {
                        $uploadImgBox = $(this).closest('.upload-img-box');
                        
                        objectUrl = window.URL.createObjectURL($(this)[0].files[0]);
                        $uploadImgBox.find('img').attr('src', objectUrl);
                        $('.nav .user img').attr('src', objectUrl);
                    }
                });

                $form.submit(function() {

                    var name = $('.name input').val();
                    var gender = $('.gender select').val();
                    var bday = $('.bday input').val();

                    $(this).ajaxSubmit({
                        beforeSubmit: function(formData, jqForm, options) {
                            
                            if (!name) {
                                utils.warn('请填写姓名!');
                                return false;
                            }

                            if (!bday || !/\d{4}\-\d{2}-\d{2}/.test(bday)) {
                                utils.warn('请选择生日，格式为1990-01-01!');
                                return false;
                            }
                        },
                        dataType: 'json',
                        success: function(res) {
                            var success = res && res.success;
                            var data = res && res.data;
                            
                            if (success) {
                                $userMsg.removeClass('editing');
                                for (var key in data) {
                                    if (key === 'portrait' && data[key]) {
                                        $userMsg.find('.user-pic img')
                                            .attr('src', data[key]);
                                    } else {
                                        $userMsg.find('#' + key + ' span').text(data[key]);    
                                    }
                                }
                            } else {
                                for (var key in data) {
                                    utils.warn(data[key]);
                                    break;
                                }
                            }
                        }
                    });

                    return false;
                });

                $exchangeBox.on('click', '.exchange-btn button', function() {
                    var num = $exchangeBox.find('.exchange-num').val();
                    var alipayAcc = $exchangeBox.find('.exchange-alipay').val();

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

                        $otherMsg.show();
                        $exchangeBox.hide();
                        $bottom.show();

                        if (success) {
                            $userMsg.find('.mibi').text(data.coin + '米币');
                            utils.warn('兑换成功，米币还剩' + data.coin);
                        } else {
                            for (var key in data) {
                                utils.warn(data[key]);
                                return false;
                            }
                        }
                    })
                })
            }

            // 活动信息中的各种操作
            $list.on('click', '.activity-list-item .list-item', function() {
                var $actionCard = $(this).closest('.activity-list-item');
                var shareLink = $actionCard.data('link');
                var detailLink = $actionCard.data('detail');

                if (shareLink || detailLink) {
                    location.href = shareLink || detailLink;    
                }
            }).on('click', '.activity-list-item .edit', function() {
                var action = $(this).data('action');
                if (action) {
                    location.href = action;    
                }
            }).on('click', '.activity-list-item .delete', function() {
                var action = $(this).data('action');
                if (confirm('确定要删除该活动吗？')) {
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
            }).on('click', '.activity-list-item .duplicate', function() {
                var action = $(this).data('action');
                if (confirm('确定要复制该活动吗？')) {
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
            }).on('click', '.activity-list-item .publish', function() {
                var $actionCard = $(this).closest('.activity-list-item');
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
                
            }).on('click', '.activity-list-item .apply-forbidden', function() {
                var $actionCard = $(this).closest('.activity-list-item');
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
            }).on('click', '.activity-list-item .apply-resume', function() {
                var $actionCard = $(this).closest('.activity-list-item');
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
            }).on('click', '.activity-list-item .unapply', function() {
                var $actionCard = $(this).closest('.activity-list-item');
                var actionId = $actionCard.data('id');

                if (actionId) {
                    zhaomi.postData('/action/' + actionId + '/unapply', {
                        
                    }, function(res) {
                        var success = res && res.success;

                        if (success) {
                            var toast = common.modal({
                                countDown: {
                                    timeout: 2,
                                    text: "取消申请成功，即将刷新页面…",
                                    callback: function() {
                                        location.href = '/mine/apply';
                                    }
                                },
                                isSimpleModal: true
                            });
                            toast.show();
                        }
                    });    
                }
            });

            var fullDataReturned = true;
            var start = 12, size = 12;

            // 加载更多
            $('.more-btn').click(function() {

                var $moreBtn = $(this);

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
                            $moreBtn.parent().addClass('no-more');
                        }
                        
                        $('.activity-lists').append(data.html);
                        
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log(errorThrown)
                    }
                });
            })
        }
    };

    main.init();

    

});