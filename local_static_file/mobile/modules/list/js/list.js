require('../../../common/pkgs/button/button');
require('../css/list');
require('../../../lib/unslider/unslider');
require('../../../lib/event-swipe/event-swipe');
var city = require('../../../lib/city/city');
var libUtil = require('../../../lib/common/util');
var common = require('../../../lib/common/common.js');
var utils = common;

$(function() {

    var $list = $('.activity-lists');

    var main = {
        init: function() {
            var $banner = $('.banner');
            city.init();
            //this.initCateList()
            this.initBanner($banner);
            this.initCateList();
            this.initEvents();
        },
        initLinkUrl: function($obj) {

            $obj.on('touchend', '.tab-content-item a', function(e) {
                e.preventDefault();
                
                var typeName = $(this).closest('ul').data('type-name');
                var newParams = {};
                newParams[typeName] = $(this).data('type');

                common.goTo(newParams);
            })
        },
        initCateList: function() {
            var $cateList = $('#cateList');
            var isInitLink = false;
            var that = this;
            if ($cateList.length) {
                $cateList.on('touchend', '.tab .tab-item', function(e) {
                    if (!isInitLink) {
                        that.initLinkUrl($cateList);
                        isInitLink = true;
                    }

                    var $target = $(e.currentTarget);
                    var index = $cateList.find('.tab .tab-item').index($target);
                    var $tabContentItems = $cateList.find('.tab-content-item');
                    var hasActive = $target.hasClass('active');

                    $cateList.addClass('open');
                    $cateList.find('.active').removeClass('active');

                    if (hasActive) {
                        hideCateList();
                    } else {
                        $target.addClass('active');
                        $tabContentItems.removeClass('active');
                        $tabContentItems.eq(index).addClass('active');
                    }

                    e.stopImmediatePropagation();

                }).on('touchend', '.tab-content', function() {
                    hideCateList();
                });
                $(document).on('touchend', function() {
                    hideCateList();
                });
                function hideCateList() {
                    setTimeout(function() {
                        $cateList.find('.active').removeClass('active');
                        $cateList.removeClass('open');
                    }, 50)
                }

            }

        },

        initBanner: function($banner) {
            var slide;
            var data;
            var numItems = $banner.find('img').length;
            // alert($(window).width())
            // $banner.height($(window).width() * 35 / 119);
            slide = $banner.unslider({
                speed: 600,
                delay: 4000, 
                dots: numItems > 1 ? true : false,
            });
            $banner.height($(window).width() * 35 / 119);
            data = slide.data('unslider')

            // $banner.swipeLeft(function() {
            //     data.next();
            // }).swipeRight(function() {
            //     data.prev();
            // })
        },

        initEvents: function() {
            $list.on('tap', '.activity-list-item', function() {
                var detailUrl = $(this).data('detail');

                if (detailUrl) {
                    location.href = detailUrl;
                }
            })

            var fullDataReturned = true;
            var start = 12, size = 12;

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