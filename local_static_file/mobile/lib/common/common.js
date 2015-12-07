$(function(){
    (function() {
        var $topTab = $('.tab-wrapper.top-tab');
        if ($topTab.length) {
            var $tab = $topTab.find('.tab');
            var topPosition = calcOuterWidth($tab);
            $tab.width(topPosition.sumWidth);
            $topTab.scrollLeft(topPosition.scrollLeftValue);
        }

        function calcOuterWidth($topTab) {
            var $tabItem = $topTab.find('.tab-item');
            var sumWidth = 0;
            var scrollLeftValue = 0;
            var indexActive = $tabItem.index($tabItem.filter('.active'));
            $tabItem.each(function(index, item) {
                var $item = $(item);
                var itemWidth = $item.width()  + (parseInt($item.css('margin-left')) +1) * 2 ;
                if (index < indexActive) {
                    scrollLeftValue += (itemWidth-20);
                }
                sumWidth += itemWidth;
            });
            return {
                sumWidth: sumWidth,
                scrollLeftValue: scrollLeftValue
            };
        }
    })();

    $('input').on('input', function() {
        $(this).closest('.input-wrapper').removeClass('error');
    })
});

var noop = function() {}
exports.postData = function(url, data, successCallback, errorCallback) {

    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    return $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: $.extend(data, {csrfmiddlewaretoken: csrfToken}), 
        success: successCallback || noop,
        error: errorCallback || noop
    })
}
exports.warn = function(msg) {
    window.alert(msg);
}

// 根据传入参数拼装url，并跳转到该url
exports.goTo = function(params, without) {
    var oldParams = without ? {} : this.getUrlParameter();
    var newParams = $.extend({}, oldParams, params);

    location.href = '/search?' + $.param(newParams);
}

exports.getUrlParameter = function() {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    var pairs;
    var ret = {};
    for (var i = 0; i < sURLVariables.length; i++) {
        var pairs = sURLVariables[i].split('=');
        if (pairs[0]) {
            ret[pairs[0]] = decodeURIComponent(pairs[1]);
        }
    }
    return ret;
}

exports.getJSONPUrl = function(start, size) {
            
    var params = this.getUrlParameter();
    var newParams = {
        start: start,
        size: size
    };
    var queryStr = $.param($.extend({}, params, newParams))
    
    var rPrefix = /(https?:\/\/[^?]+)/;
    var matches, prefix;

    if (matches = rPrefix.exec(location.href)) {
        prefix = matches[1];
    }

    return prefix + '?' + queryStr;
}

exports.modal = function(options) {
    options = options || {};
    var selector = options.selector || '.zui-modal';
    var template = options.template;
    var modalTitle = options.title;
    var isSimpleModal = options.isSimpleModal || false;
    var modalContentText = options.contentText || '只有认证用户可将活动发布至找米平台首页，您可以直接分享邀请朋友加入';
    var optionsTipText = options.tipText;
    var isShowCloseBtn = options.showCloseBtn || false;
    var modalActions = options.actions;
    var countDown = options.countDown;
    var sureCallback = options.sureCallback || function(){};
    var cancelCallback = options.cancelCallback || function(){};
    var sureBtnText = options.sureBtnText || "确定";
    var verifiedAction = options.verifiedAction;
    var hasCountDown = false;

    if (typeof countDown == 'object') {
        var countDownCallback = countDown.callback;
        var countDownTime = countDown.timeout || 5;
        var countdownText = countDown.text || '秒中后跳转';
        hasCountDown = true;
    }


    var $modal = $(selector);
    var closeBtnTpl = '';
    var headerTpl = '';

    if (isShowCloseBtn) {
        closeBtnTpl = '<div class="zui-modal-close-btn"></div>';
    }

    if (modalTitle) {
        headerTpl = '<div class="zui-modal-header"></div>';
    }
    var maskTemplate = '<div class="zui-modal-mask"></div>';


    var tipText = '';
    if (!isSimpleModal) {
        tipText += '<div class="zui-align-center icon-tip">' +
            '<div class="tip-icon">' +
                '<span class="zui-icon icon-success icon-big"></span>' +
            '</div>';
        if (optionsTipText) {
            tipText += '<div class="tip-text">' + optionsTipText + '</div>';    
        }
        tipText += '</div>';
    }
    

    var contextText = '<div class="zui-align-center">' +
                        '<div class="text">' + modalContentText + '</div>'+
                      '</div>';

    var actionsContent =  '<div class="zui-modal-actions">' +
        '<div class="zui-align-center">' +
        '<a href="'+ verifiedAction +'" class="zui-btn" target="_blank">申请成为认证用户</a>' +
        '<div class="zui-modal-sure-btn tip-text">' + sureBtnText + '</div></div></div>' +
        '</div>';

    if (isSimpleModal) {
        contextText = '';
        actionsContent = '<div class="zui-modal-actions">' +
            '<div class="zui-align-center">' +
            '<div class="zui-modal-sure-btn zui-btn">' + sureBtnText + '</div></div></div>' +
            '</div>';
    }
    var modalContent =  tipText + contextText;

    if (!template) {
        if (isSimpleModal) {
            template = '<div class="zui-modal zui-simple-modal">' +
                headerTpl + closeBtnTpl +
                '<div class="zui-modal-content"> ' + modalContent + ' </div>' + actionsContent;
        } else {
            template = '<div class="zui-modal">' +
                headerTpl + closeBtnTpl +
                '<div class="zui-modal-content"> ' + modalContent + ' </div>' + actionsContent;
        } 
    }

    var $maskDialog = $('.zui-modal-mask');
    if (!$maskDialog.length) {
        template = template + maskTemplate;
    }
    var $html = $('html');
    if (!$modal.length) {
        $modal = $(template);
        $('body').append($modal);
        $modal.find('.zui-modal-header').html(modalTitle);
        $modal.find('.zui-modal-content').html(modalContent);
        $modal.find('.zui-modal-actions').html(modalActions);
    }

    if (isShowCloseBtn) {
        $modal.on('click', '.zui-modal-close-btn', function(){
            $modal.hide();
        });
    }

    $maskDialog.on('touchmove', function(e){
        e.preventDefault();
    });
    $modal.find('.zui-modal-sure-btn').on('click', function() {
        hideModal();
        sureCallback();
    });
    $modal.find('.zui-modal-cancel-btn').on('click', function() {
        hideModal();
        cancelCallback();
    });

    if (hasCountDown) {
        var timeIndex = 0;
        $modal.find('.zui-modal-actions').html('<div class="zui-align-center">' + countdownText + '</div>');

        var countDownTimer = setInterval(function(){
            timeIndex++;
            //var countDownText = countDownTime - timeIndex  + ''  + countdownText;
            // $modal.find('.zui-modal-actions').html('<div class="zui-align-center">' + countdownText + '</div>');
            if (timeIndex >= countDown.timeout) {
                clearInterval(countDownTimer);
                destroyModal();
                countDownCallback && countDownCallback();
            }
        }, 1000);
    }

    var showModal = function() {
        $html.addClass('overflow-scroll');
        $modal.show();
    };
    var hideModal = function() {
        $html.removeClass('overflow-scroll');
        $modal.hide();
    };
    var destroyModal = function() {
        $html.removeClass('overflow-scroll');
        $modal.hide();
        $modal.remove();
    };
    return {
        show: function(){
            showModal();
        },
        hide: function(){
            hideModal();
        },
        destroy: function(){
            destroyModal();
        }
    }
}

