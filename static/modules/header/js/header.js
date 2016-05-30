require('../css/header');
var _ = require('../../../lib/lodash/lodash.min');
var utils = require('../../../common/utils');

// export something which is related to header
module.exports = function() {}

$(function() {

    // placeholder polyfill
    $('input, textarea').placeholder();
    
    var $win = $(window);
    var $doc = $(document);
    var $area = $('#area');
    var $areaDroplist = $area.find('#area-droplist');
    var $search = $('#search');
    // 查询开始下标
    var from = 0;
    // 查询的记录数
    var size = 20;

    // 初始化地区筛选列表
    if ($areaDroplist.citySelect) {
        $areaDroplist.citySelect({
            prov: '北京',
            nodata: 'none'
        });
    }

    // 获取地区数据
    $areaDroplist.on('click', 'button', function() {
        var prov = $('.prov').val() || '';
        var city = $('.city').val() || '';

        utils.goTo({
            loc: prov + '|' + city
        })
    });

    $area.on('click', function() {
        $areaDroplist.show();
    });

    // 处理搜索
    $doc.click(function(ev) {
        if (!$(ev.target).closest('#area').length) {
            $areaDroplist.hide();
        }
    }).on('keyup', function(ev) {
        var q = $search.find('input').val();
        if (ev.keyCode === 13) {
            if (q) {
                utils.goTo({
                    q: q
                }, true)
            }
        } else if (ev.keyCode === 27) {
            $areaDroplist.hide();   
        }
    })
});