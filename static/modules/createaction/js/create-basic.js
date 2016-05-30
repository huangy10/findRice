require('../../../common/pkgs/button/button');
require('../../../common/pkgs/progress/progress');
require('../css/create');

var header = require('../../header/js/header');
var utils = require('../../../common/utils');

var FORMAT = 'YYYY-MM-DD HH:mm';
var rValidImg = /\.(jpg|jpeg|png)$/;

$(function() {
    
    var startDate;

    $('#addr').citySelect({
        prov: '北京',
        nodata: 'none'
    });

    $('#form_datetime_start').datetimepicker({
        language: 'zh-CN',
        weekStart: 1,
        autoclose: 1,
        startView: 2,
        forceParse: 0,
        minView: 0,
        maxView: 4,
        pickerPosition: 'bottom-left',
        format: 'yyyy-mm-dd hh:ii',
        startDate: new Date()
    }).on('changeDate', function(ev) {
        var $startDate = $('#startdate');
        var day = $('#id_day').val() || 0;
        var hour = $('#id_hour').val() || 0;
        var minute = $('#id_minute').val() || 0;
        var $endDate = $('#enddate'), endDate = $endDate.val();
        var diffObj;

        startDate = $startDate.val();

        // 删除日期
        if (!startDate) {
            return;
        }

        if (endDate && endDate <= startDate) {
            utils.warn('开始时间不能晚于结束时间');
            $startDate.val('');
            return;
        }

        if (!isDurationEmpty(day, hour, minute)) {
            endDate = getOppositeDate(startDate, day, hour, minute);
            $endDate.val(endDate);
        } else {
            if (endDate) {
                diffObj = getDiff(startDate, endDate);
                $('#id_day').val(diffObj.day);
                $('#id_hour').val(diffObj.hour);
                $('#id_minute').val(diffObj.minute);
            }
        }

        $('#form_datetime_end').datetimepicker('setStartDate', startDate);
    });

    $('#form_datetime_end').datetimepicker({
        language: 'zh-CN',
        weekStart: 1,
        autoclose: 1,
        startView: 2,
        forceParse: 0,
        minView: 0,
        maxView: 4,
        pickerPosition: 'bottom-left',
        format: 'yyyy-mm-dd hh:ii',
        startDate: startDate || new Date()
    }).on('changeDate', changeEndDateHandler);

    function changeEndDateHandler(ev) {
        var $startDate = $('#startdate');
        var startDate = $startDate.val();
        var day = $('#id_day').val() || 0;
        var hour = $('#id_hour').val() || 0;
        var minute = $('#id_minute').val() || 0;
        var $endDate = $('#enddate');
        var endDate = $endDate.val();
        var diffObj;

        // 删除日期
        if (!endDate) {
            return;
        }

        if (startDate && endDate <= startDate) {
            utils.warn('开始时间不能晚于结束时间');
            $endDate.val('');
            return;
        }

        if (!isDurationEmpty(day, hour, minute)) {
            startDate = getOppositeDate(endDate, -day, -hour, -minute);
            $startDate.val(startDate);
        } else {
            if (startDate) {
                diffObj = getDiff(startDate, endDate);
                $('#id_day').val(diffObj.day);
                $('#id_hour').val(diffObj.hour);
                $('#id_minute').val(diffObj.minute);    
            }
        }
    }

    function isDurationEmpty(day, hour, minute) {
        day = +day;
        hour = +hour;
        minute = +minute;
        return !day && !hour && !minute;
    }

    function getDiff(startDate, endDate) {
        
        var s = moment(startDate).format(FORMAT);
        var e = moment(endDate).format(FORMAT);
        var millis = moment(endDate).diff(moment(startDate));
        var seconds = millis / 1000;
        var day, hour, minute;

        day = Math.floor(seconds / (24 * 3600));
        hour = Math.floor((seconds - day * 24 * 3600) / 3600);
        minute = Math.floor((seconds - day * 24 * 3600 - hour * 3600) / 60);

        return {
            day: day,
            hour: hour,
            minute: minute
        }
    }

    $('#secondary .time').change(function() {
        var id = $(this).attr('id');
        var day = $('#id_day').val() || 0;
        var hour = $('#id_hour').val() || 0;
        var minute = $('#id_minute').val() || 0;
        var rDigits = /^\d*$/;
        var $startDate = $('#startdate');
        var startDate = $startDate.val();
        var $endDate = $('#enddate');
        var endDate = $endDate.val();
        var isValid = true;

        switch (id) {
            case 'id_day':
                if (!rDigits.test(day) || +day < 0) {
                    isValid = false;
                    utils.warn('您输入的持续天数不合法！');
                }
                break;
            case 'id_hour':
                if (!rDigits.test(hour) || +hour < 0 || +hour > 23) {
                    isValid = false;
                    utils.warn('您输入的持续小时不合法！');
                }
                break;
            case 'id_minute':
                if (!rDigits.test(minute) || +minute < 0 || +minute > 59) {
                    isValid = false;
                    utils.warn('您输入的持续分钟不合法！');
                }
                break;
        }      

        // if (isValid) {
        //     if (startDate) {
        //         endDate = getOppositeDate(startDate, day, hour, minute);
        //         $endDate.val(endDate);
        //     } else if (endDate) {
        //         startDate = getOppositeDate(endDate, -day, -hour, -minute);
        //         $startDate.val(startDate);
        //     }
        // }
    });

    function getOppositeDate(date, day, hour, minute) {
        return moment.max(moment(date, FORMAT)
            .add(day, 'day')
            .add(hour, 'hour')
            .add(minute, 'minute'), moment()).format(FORMAT);
    }

    $('#poster').change(function() {
        var poster = $(this).val();
        if (poster) {
            if (!rValidImg.test(poster)) {
                utils.warn('请上传png/jpg图片！');
                return false;
            }
            $('#poster-hint').text(poster);
        }
        
    });

    $('.money').on('click', '.cb', function() {

        if ($(this).hasClass('checked')) {
            $('#id_present').parent('.presendWrapper').remove();
            $(this).removeClass('checked');
        } else {
            $('#secondary').append('<div class="presendWrapper">' +
                '<input id="id_present" name="present" class="content"' + 
                ' placeholder="请输入礼品详情"></div>')
            $(this).addClass('checked');
            // placeholder polyfill
            $('input, textarea').placeholder();
        }
        
    })

    var $actionTypeContainer = $('#action-type-c');
    var $actionTypeDroplist = $actionTypeContainer.find('#action-type-droplist');
    var $actionType = $actionTypeContainer.find('#action-type');

    $('#action-type-c').on('mouseenter', function() {
        $actionTypeDroplist.show();
    }).on('mouseleave', function() {
        $actionTypeDroplist.hide();
    }).on('click', 'ul li', function() {
        var actionTypeTxt = $(this).data('txt');
        var actionType = $(this).data('val');
        $actionTypeContainer.find('p').text(actionTypeTxt);
        $actionType.val(actionType);
        $actionTypeDroplist.hide();
    });

    $('#create-action-first').submit(function() {
        var name = $('#name').val();
        var host = $('#host').val();
        var prov = $('#prov').val();
        var city = $('#city').val();
        var addr = $('#detail-addr').val();
        var durationDay = $('#id_day').val();
        var durationHour = $('#id_hour').val();
        var durationMin = $('#id_minute').val();
        var maxAttendee = $('#id_max_attend').val();
        var bonus = $('#id_reward').val();
        var presentChecked = $('.money .cb').hasClass('checked');
        var present = $('#id_present').val();
        var desc = $('#desc').val();
        var actionType = $('#action-type').val();
        var poster = $('#poster').val();

        var $nextBtnW = $(this).find('#btns');
        var $nextBtn = $nextBtnW.find('button');

        if ($nextBtnW.hasClass('ing')) {
            return false;
        }

        $(this).ajaxSubmit({
            beforeSubmit: function(formData, jqForm, options) {
                if (!name) {
                    utils.warn('请填写活动名称!');
                    return false;
                }

                if (!host) {
                    utils.warn('请填写主办方!');
                    return false;
                }

                if (!prov) {
                    utils.warn('请选择省份!');
                    return false;
                }

                if (!city) {
                    utils.warn('请选择城市!');
                    return false;
                }

                if (!addr) {
                    utils.warn('请填写具体的地址!');
                    return false;
                }

                if (durationDay === '') {
                    utils.warn('请填写持续天数!');
                    return false;
                }

                if (+durationDay < 0) {
                    utils.warn('天数应该大于等于0天!');
                    return false;
                }

                if (durationHour === '') {
                    utils.warn('请填写持续小时数!');
                    return false;
                }

                if (+durationHour < 0 || +durationHour > 23) {
                    utils.warn('小时数不合法!');
                    return false;
                }

                if (durationMin === '') {
                    utils.warn('请填写持续分钟数!');
                    return false;
                }

                if (+durationMin < 0 || +durationMin > 59) {
                    utils.warn('分钟数不合法!');
                    return false;
                }

                if (maxAttendee === '') {
                    utils.warn('请填写持续分钟数!');
                    return false;
                }

                if (maxAttendee <= 0) {
                    utils.warn('参与人数应该大于0!');
                    return false;
                }

                if (bonus < 0) {
                    utils.warn('奖励金额值不合法!');
                    return false;
                }

                if (presentChecked && !present) {
                    utils.warn('请输入礼品详情!');
                    return false;
                }

                if (!desc) {
                    utils.warn('请填写活动简介!');
                    return false;
                }

                if (actionType === '') {
                    utils.warn('请选择活动类型!');
                    return false;
                }

                if (poster && !/\.(jpg|jpeg|png)$/.test(poster)) {
                    utils.warn('活动海报海报仅支持png/jpg格式的文件!');
                    return false;
                }

                $nextBtnW.addClass('ing');
                $nextBtn.text('上传中...');
            },
            dataType: 'json',
            data: {
                province: prov,
                city: city
            },
            success: function(res) {
                var success = res && res.success;
                var data = res && res.data;
                
                if (success) {
                    if (data.url) {
                        location.href = data.url;  
                    } 
                } else {
                    for (var key in data) {
                        $('#' + key).removeClass('focus').addClass('err');
                        utils.warn(data[key]);

                        $nextBtnW.removeClass('ing');
                        $nextBtn.text('下一步');
                        break;
                    }
                }
            },
            error: function() {
                console.error('擦了，创建活动提交失败~')
                $nextBtnW.removeClass('ing');
                $nextBtn.text('下一步');
            }
        });

        return false;
    })

    $('input').focus(function() {
        $(this).removeClass('err').addClass('focus');
    }).blur(function() {
        $(this).removeClass('focus');
    })
});