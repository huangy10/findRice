
require('./reg.less');

require('./pcasunzip');
var libUtil = require('../common/util');

var template = require('./template');

// 是否正在选择省份、城市
var isSelecting = false;

//区域选择
module.exports = {


    init: function(obj){

        // Fastclick.attach($('.selectdialog')[0]);

        //var tpl = '<div class="selectdialog" id="SelectDialog">' +
        //    '<div class="select-dia-mask">' +
        //    '</div>' +
        //    '<div class="select-dia-table">' +
        //    '<div class="select-dia-cell"></div>' +
        //    '</div>' +
        //    '</div>' +
        //    '</div>'
        // ;
        //$(tpl).appendTo('body');
        var json = {
            innerWidth: 0,
            outerWidth: 0,
            innerHeight: 0,
            outerHeight: 0,
            width: 0,
            height: 0,
            ratio: 0
        };
        json.innerWidth = window.innerWidth;
        json.outerWidth = window.outerWidth
        json.innerHeight = window.innerHeight;
        json.outerHeight = window.outerHeight;
        json.width = screen.width;
        json.height = screen.height;
        json.ratio = window.devicePixelRatio;
        var text = JSON.stringify(json);
        var $SelectDialog ;
        var $selectBtn ;
        if (obj && obj.targetBtn){
            $selectBtn = $(obj.targetBtn);
        } else {
          $selectBtn = $("[data-select-area = 'true']");
        }


        $SelectDialog = $('#SelectDialog');

        //选择事件
        $SelectDialog.on("click", ".select-dia-check", function () {
            var target = $($(this).attr("data-target"));
            var val = $(this).attr("data-value");
            target.val(val);
            target.blur();
            target.parent().find(".input").text($(this).text());
            HideDialog();
        });

        //加载
        $("[data-select='true']").on("click", function () {
            $(this).text("");
            GetSelectData($(this));
        });
        var callback;
        //选择省份
        $selectBtn.on("click", function () {
            if (!obj || !obj.callback) {
                 callback = function(value) {
                    var urlParams = libUtil.parseQuery();
                    urlParams['loc'] = value[0] + '|' + value[1];
                    var href = libUtil.getUrlFromParams({
                        loc: value[0] + '|' + value[1]
                    });
                    window.location.href = href;
                }
            } else {
                callback = obj.callback;
            }
            GetAreaSelect($(this), callback);
        });

        //选择
        $SelectDialog.on("focus", ".birthmin, .birthadd", function () {
            return false;
        });


//验证

//普通弹出框
        function GetSelectData(current) {
            var selectdata = $("<div/>").html(current.attr("data-select-data")).text();
            var jsonarray = JSON.parse(selectdata);
            var data = { title: "", target: "", list: [{}] }
            data.title = current.attr("data-select-title");
            data.target = current.attr('data-select-target');
            data.list = jsonarray;
            var $dialog = LoadDialog("dialogselect", data);
        }

//隐藏选择框
        function HideDialog() {
            $(document).off('click.city');
            $SelectDialog.addClass("hi");
            setTimeout(function () {
                $SelectDialog.hide().find(".select-dia").empty();
            }, 500)
        }
//加载弹出选择框
        function LoadDialog(templateid, data) {
            var html = template(templateid, data);
            $SelectDialog.find(".select-dia").html(html);
            $SelectDialog.removeClass("hi").show();
            return $SelectDialog;
        }


//地区弹出框
        function GetAreaSelect($current, callback) {

            var targetArray = $current.attr("data-select-target").split(",");
            var $first = $(targetArray[0]);
            var firstData = $first.attr("data-select-data");
            var json = { title: $current.data("select-title"), list: 0, target: targetArray[0] }
            var values = new Array();
            for (var i = 1; i < PCAP.length; i++) {
                values[i - 1] = { Key: i, Value: PCAP[i] };
            }
            var selectValue = [];
            json.list = values;
            var $dialog = LoadDialog("dialogarea", json);
            //省级
            $dialog.find(".select-area-check").off('click').on("click", function () {

                isSelecting = true;
                var val = $(this).attr("data-value");
                var ptarget = $($(this).attr("data-target"));
                ptarget.val(val);
                selectValue.push(val);
                ptarget.blur();
                var index = $(this).attr("data-index");
                var citys = PCAC[index];
                var jsoncity = { title: val, list: 0, target: targetArray[1] };
                var cityvalues = new Array();
                for (var i = 1; i < citys.length; i++) {
                    cityvalues[i - 1] = { Key: i, Value: citys[i] };
                }
                jsoncity.list = cityvalues;
                var $mydialog = LoadDialog("dialogarea", jsoncity);
                //城市
                $mydialog.find(".select-area-check").off('click').on("click", function () {

                    var val = $(this).attr("data-value");
                    selectValue.push(val);
                    callback(selectValue)
                    isSelecting = false;
                    HideDialog();
                });
            });

            // 需要延迟绑定点击事件，否则该document代理的click事件会直接处理弹出选择框的那个click事件
            setTimeout(function() {
                $(document).on('click.city', function(ev) {
                    // console.log($(ev.target).attr('class'))
                    // if (!isSelecting &&
                    //     !$(ev.target).closest('.select-dia').length) {
                    //     HideDialog();
                    // }
                    if ($(ev.target).hasClass('select-dia-cell')) {
                        HideDialog();
                    }
                })
            }, 0);
        }
    }
};
