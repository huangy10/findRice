

//区域选择
$(function () {
    var json = {
        innerWidth: 0,
        outerWidth: 0,
        innerHeight: 0,
        outerHeight: 0,
        width: 0,
        height: 0,
        ratio: 0
    }
    json.innerWidth = window.innerWidth;
    json.outerWidth = window.outerWidth
    json.innerHeight = window.innerHeight;
    json.outerHeight = window.outerHeight;
    json.width = screen.width;
    json.height = screen.height;
    json.ratio = window.devicePixelRatio;
    var text = JSON.stringify(json);

    //选择事件
    $("#SelectDialog").on("click", ".select-dia-check", function () {
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
    })

    //选择省份
    $("[data-select-area = 'true']").on("click", function () {
        $(this).text("");
        GetAreaSelect($(this));
    });

    //选择
    $("#SelectDialog").on("focus", ".birthmin,.birthadd", function () {
        return false;
    });
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
    $("#SelectDialog").addClass("hi");
    setTimeout(function () {
        $("#SelectDialog").hide().find(".select-dia").empty();
    }, 500)
}
//加载弹出选择框
function LoadDialog(templateid, data) {
    var html = template(templateid, data);
    $("#SelectDialog .select-dia").html(html);
    $("#SelectDialog").removeClass("hi").show();
    return $("#SelectDialog");
}


//地区弹出框
function GetAreaSelect($current) {
    var targetArray = $current.attr("data-select-target").split(",");
    var $first = $(targetArray[0]);
    var firstData = $first.attr("data-select-data");
    var json = { title: $current.data("select-title"), list: 0, target: targetArray[0] }
    var values = new Array();
    for (var i = 1; i < PCAP.length; i++) {
        values[i - 1] = { Key: i, Value: PCAP[i] };
    }
    json.list = values;
    var $dialog = LoadDialog("dialogarea", json);
    //省级
    $dialog.find(".select-area-check").on("click", function () {

        var val = $(this).attr("data-value");
        var ptarget = $($(this).attr("data-target"));
        ptarget.val(val);
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
        $mydialog.find(".select-area-check").on("click", function () {

            var val = $(this).attr("data-value");
            var ctarget = $($(this).attr("data-target"));
            ctarget.val(val);
            ctarget.blur();
            //var val = $.map($current.nextAll(":input").toArray(), function (n) { return $(n).val() });
            var val = $.map($current.parent().find("input").toArray(), function (n) { return $(n).val() });
            if(val[0] == "北京" || val[0] == "上海" || val[0] == "天津" || val[0] == "重庆"){
                $current.text(val[1]);
            } else {
                val = val.join("-");
                $current.text(val);
            }

            HideDialog();
        });
    })
}
