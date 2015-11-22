// 根据传入参数拼装url，并跳转到该url
exports.goTo = function(params, without) {
    var oldParams = without ? {} : this.getUrlParameter();
    var newParams = _.extend({}, oldParams, params);

    location.href = '/search?' + $.param(newParams);
}

exports.assert = function(value, msg) {
    if (!value) {
        exports.warn(msg);
    }
}

exports.assertEquals = function(value, anotherValue, msg) {
    if (value !== anotherValue) {
        exports.warn(msg);   
    }
}

exports.warn = function(msg) {
    window.alert(msg);
}

exports.compileTpl = function(tpl, data) {
    return tpl.replace(/\{(\w+)\}/g, function(all, param) {
        return data[param] || '';
    })
}

var $doc = $(document);
var $win = $(window);

exports.loadMore = function(callback) {

    var controller = {
        timeoutId: '',
        clearTimeout: function() {
            this.timeoutId = '';
        }   
    };
    // 处理加载更多
    $win.scroll(function() {
        var LOADING_GAP = 200;
        if ($doc.height() < $doc.scrollTop() + $win.height() + LOADING_GAP) {
            if (controller.timeoutId) {
                return;
            }
            controller.timeoutId = setTimeout(function() {
                callback.call(controller);
            }, 300);
        }
    })
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

exports.isLogin = function() {
    return $('#reg').length === 0;
}