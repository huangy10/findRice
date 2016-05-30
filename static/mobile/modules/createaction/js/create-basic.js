require('../../../common/pkgs/button/button');
//require('../../../common/pkgs/progress/progress');
require('../../../lib/jquery-form/jquery.form');
require('../../../lib/jquery-form/validform');
require('../../../lib/jquery-form/validform.less');
require('../css/create');

var FastClick = require('../../../lib/fastclick/fastclick');
var common = require('../../../lib/common/common.js');
var ValidateForm = require('../../../lib/common/validateform.js');

var city = require('../../../lib/city/city');
var utils = common;

var FORMAT = 'YYYY-MM-DD HH:mm';

$(function() {
    //common.initNav();
    var $pageCreateAction = $('#pageCreateAction');

    var $createActionStep = $pageCreateAction.find('#createActionStep.step-01');

    var main = {
        init: function() {
            var that = this;
            this.initEvent();
            var $city = $('#prov_city');
            city.init({
                targetBtn: $city,
                callback: function(value) {
                    $city.val(value.join(" "));
                    ValidateForm.checkInput($city)
                }
            })
        },
        initEvent: function() {
            this.initCheckForm();
            this.initFormEvent();
            this.initDatePickers();
            this.initFastClick();
            this.initGift();
        },
        initGift: function() {
            //礼品展示
            $pageCreateAction.find('.active-gift').on('change', 'input', function(e){

                var isChecked = $(this)[0].checked;
                var $target =  $(this);
                var $li = $target.closest('li');
                //if (isChecked) {
                //    $target.closest('li').toggleClass('active')
                //} else {
                //    $target.closest('li').toggleClass('active')
                //}
                if ($li.hasClass('active')) {
                    $li.find('.input-gift input').attr('value', '');
                    $li.removeClass('active');
                } else {
                    $li.addClass('active');
                }
            });
        },
        initFastClick: function() {
            var $selectWrapper = $('.select-wrapper')

            if ($selectWrapper.length) {
                FastClick.attach($selectWrapper[0]);
            }

        },
        initDatePickers: function() {
            var $appDate = $(".select-date-time");
            var $startDate = $('#start-date');
            var $endDate = $('#end-date');

            initStartDatePicker();
            initEndDatePicker();

            $('.start-date-lbl').click(function() {
                $('#start-date').mobiscroll('show');
            })

            $('.end-date-lbl').click(function() {
                $('#end-date').mobiscroll('show');
            })

            function initStartDatePicker() {
                
                var currYear = (new Date()).getFullYear();
                var opt = {};
                opt.date = {
                    preset: 'date'
                };
                opt.datetime = {
                    preset: 'datetime'
                };
                opt.time = {
                    preset: 'time'
                };
                opt.default = {
                    theme: 'android-ics light', //皮肤样式
                    display: 'modal', //显示方式
                    mode: 'scroller', //日期选择模式
                    dateFormat: 'yy-mm-dd',
                    timeFormat: 'HH:ii',
                    lang: 'zh',
                    showNow: true,
                    nowText: "今天",
                    minDate: new Date(),
                    endYear: currYear + 10,
                    onSelect: function(selectedStartDate) {
                            
                        var startDate = $startDate.val();
                        var day = $('#id_day').val() || 0;
                        var hour = $('#id_hour').val() || 0;
                        var minute = $('#id_minute').val() || 0;
                        var $endDate = $('#end-date');
                        var endDate = $endDate.val();
                        var diffObj;

                        $startDate.siblings('span').removeClass('ph').text(selectedStartDate);

                        if (!isDurationEmpty(day, hour, minute)) {
                            endDate = getOppositeDate(startDate, day, hour, minute);
                            $endDate.val(endDate);
                            $endDate.siblings('span').removeClass('ph').text(endDate);
                        } else {
                            if (endDate) {
                                diffObj = getDiff(startDate, endDate);
                                $('#id_day').val(diffObj.day);
                                $('#id_hour').val(diffObj.hour);
                                $('#id_minute').val(diffObj.minute);    
                            }
                        }
                        initEndDatePicker(new Date(moment(selectedStartDate, FORMAT).valueOf()));
                    }
                };
                var optDateTime = $.extend(opt['datetime'], opt['default']);
                $startDate.mobiscroll().datetime(optDateTime);
            }

            function initEndDatePicker(minimumDate) {
                
                var currYear = (new Date()).getFullYear();
                var opt = {};
                opt.date = {
                    preset: 'date'
                };
                opt.datetime = {
                    preset: 'datetime'
                };
                opt.time = {
                    preset: 'time'
                };
                opt.default = {
                    theme: 'android-ics light', //皮肤样式
                    display: 'modal', //显示方式
                    mode: 'scroller', //日期选择模式
                    dateFormat: 'yy-mm-dd',
                    timeFormat: 'HH:ii',
                    lang: 'zh',
                    showNow: true,
                    nowText: "今天",
                    minDate: minimumDate || new Date(),
                    endYear: currYear + 10,
                    // startYear: currYear - 10, //开始年份
                    // endYear: currYear + 10,//结束年份,
                    onSelect: function(val) {
                            
                        var startDate = $startDate.val();
                        var day = $('#id_day').val() || 0;
                        var hour = $('#id_hour').val() || 0;
                        var minute = $('#id_minute').val() || 0;
                        var endDate = $endDate.val();
                        var diffObj;

                        $endDate.siblings('span').removeClass('ph').text(val);

                        if (!isDurationEmpty(day, hour, minute)) {
                            startDate = getOppositeDate(endDate, -day, -hour, -minute);
                            $startDate.val(startDate);
                            $startDate.siblings('span').removeClass('ph').text(startDate);
                        } else {
                            if (startDate) {
                                diffObj = getDiff(startDate, endDate);
                                $('#id_day').val(diffObj.day);
                                $('#id_hour').val(diffObj.hour);
                                $('#id_minute').val(diffObj.minute);    
                            }
                        }
                    }
                };
                var optDateTime = $.extend(opt['datetime'], opt['default']);
                $endDate.mobiscroll().datetime(optDateTime);
            }

        },

        initFormEvent: function() {

        },
        initCheckForm: function() {
            var $selectWrapper = $('.select-wrapper');
            $selectWrapper.on('click', '.select-activity-type', function() {
                $selectWrapper.find('.select-list-content').toggle();
            });

            $selectWrapper.on('click', '.select-list-content span', function(e) {
                var $this = $(e.currentTarget);
                var text = $this.html();
                var value = $this.data('val');
                $selectWrapper.find('.select-activity-type').html(text);
                $('#action-type').val(value);
                $selectWrapper.find('.select-list-content').toggle();
            });
        }
    };

    main.init();

    $('.distance-input .zui-input-text').on('change', function() {
        var id = $(this).attr('id');
        var day = $('#id_day').val() || 0;
        var hour = $('#id_hour').val() || 0;
        var minute = $('#id_minute').val() || 0;
        var rDigits = /^\d*$/;
        var $startDate = $('#start-date');
        var startDate = $startDate.val();
        var $endDate = $('#end-date');
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
        //         $endDate.siblings('span').removeClass('ph').text(endDate);
        //     } else if (endDate) {
        //         startDate = getOppositeDate(endDate, -day, -hour, -minute);
        //         $startDate.val(startDate);
        //         $startDate.siblings('span').removeClass('ph').text(startDate);
        //     }
        // }
    });

    function getOppositeDate(date, day, hour, minute) {
        return moment.max(moment(date, FORMAT)
            .add(day, 'day')
            .add(hour, 'hour')
            .add(minute, 'minute'), moment()).format(FORMAT);
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

    $('#create-action-first').submit(function() {
        var name = $('#name').val();
        var host = $('#host').val();
        var prov_city = $('#prov_city').val();
        var prov = prov_city.split(' ')[0];
        var city = prov_city.split(' ')[1];
        var addr = $('#other-local-msg').val();
        var startDate = $('#start-date').val();
        var endDate = $('#end-date').val();
        var durationDay = $('#id_day').val();
        var durationHour = $('#id_hour').val();
        var durationMin = $('#id_minute').val();
        var maxAttendee = $('#id_max_attend').val();
        var bonus = $('#id_reward').val();
        var presentChecked = $('#id_reward').closest('li').hasClass('active');
        var present = $('#id_present').val();
        var desc = $('#desc').val();
        var actionType = $('#action-type').val();
        var poster = $('#poster').val();

        var $nextBtnW = $(this).find('.next-w');
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

                if (!prov_city) {
                    utils.warn('请选择省份和城市!');
                    return false;
                }

                if (!addr) {
                    utils.warn('请填写具体的地址!');
                    return false;
                }

                if (!startDate) {
                    utils.warn('请选择开始时间!');
                    return false;
                }

                if (!endDate) {
                    utils.warn('请选择结束时间!');
                    return false;
                }

                if (startDate > endDate) {
                    utils.warn('开始时间不能晚于结束时间!');
                    return false;
                }

                if (durationDay !== '' && +durationDay < 0) {
                    utils.warn('持续天数应该大于等于0天!');
                    return false;
                }

                if (durationHour === '') {
                    utils.warn('请填写持续小时数!');
                    return false;
                }

                if (+durationHour < 0 || +durationHour > 23) {
                    utils.warn('小时数应该大于等于0并且小于24!');
                    return false;
                }

                if (durationMin === '') {
                    utils.warn('请填写持续分钟数!');
                    return false;
                }

                if (+durationMin < 0 || +durationMin > 59) {
                    utils.warn('分钟数应该大于等于0并且小于60!');
                    return false;
                }

                if (maxAttendee === '') {
                    utils.warn('请填写参加人数!');
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
                console.error('擦了，创建活动提交失败~');
                $nextBtnW.removeClass('ing');
                $nextBtn.text('下一步');
            }
        });

        return false;
    })
});