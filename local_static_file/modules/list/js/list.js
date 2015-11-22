require('../../../common/pkgs/button/button');
require('../css/list');

var header = require('../../header/js/header');
var shareBox = require('../../../common/pkgs/sharebox/sharebox');
var zhaomi = require('../../../lib/common/common');
var utils = require('../../../common/utils');

$(function() {

    var $win = $(window);
    var $doc = $(document);
    var $hotWrapper = $('#hot-wrapper');
    var $categoryWrapper = $('#category-wrapper');
    var $container = $('#content');
    var $actionCard = $('.action-card');
    var $banner = $('#banner');
    var numItems = $banner.find('img').length;

    $banner.unslider({
        speed: 600,
        delay: 4000, 
        dots: numItems > 1 ? true : false,
        starting: function(banner, item) {
            
            var nextIdx = ($banner.find('ul li').index(item) + 2) % numItems;
            var $img = $banner.find('img').eq(nextIdx);
            if (!$img.attr('src')) {
                $img.attr('src', $img.data('src'));
            }
        }
    });

    setTimeout(function() {
        var $secondImg = $banner.find('img').eq(1);
        if (!$secondImg.attr('src')) {
            $secondImg.attr('src', $secondImg.data('src'));
        }
    }, 2000);

    $container.on('click', '.action-card', function(evt) {

        if ($(evt.target).hasClass('like') || $(evt.target).hasClass('share')) {
            return false;
        }
        var $actionCard = $(this);
        var shareLink = $actionCard.data('link');
        var detailLink = $actionCard.data('detail');

        if (shareLink || detailLink) {
            window.open(shareLink || detailLink, '_blank');
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
    }).on('click', '.action-card .share', function() {
        var $actionCard = $(this).closest('.action-card');
        var shareLink = $actionCard.data('link');

        shareBox.show({
            id: 'share-dialog',
            shareLink: shareLink
        })
    })

    // 处理过滤找米热门
    $hotWrapper.on('click', 'ul li', function() {
        utils.goTo({
            hot: $(this).data('type')
        });
    })

    // 处理过滤类别
    $categoryWrapper.on('click', 'ul li', function() {
        utils.goTo({
            type: $(this).data('type')
        });
    })

    var fullDataReturned = true;
    var start = 12, size = 12;

    utils.loadMore(function() {

        var controller = this;
        if (!fullDataReturned) {
            return;
        }

        $.ajax({
            url: utils.getJSONPUrl(start, size),
            dataType: 'jsonp',
            success: function(data) {
                // 清除timeout才能进行下一次请求
                controller.clearTimeout();
                data = data || {};
                if (data.size === size) {
                    fullDataReturned = true;
                    start = start + size;
                } else {
                    fullDataReturned = false;
                }
                if (!$('#more-list').length) {
                    $('#content').append('<div id="more-list" class="list"><ul></ul></div>')
                }
                $('#more-list ul').append(data.html);
                
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown)
            }
        });

    })
    
});