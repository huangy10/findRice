require('../../../common/pkgs/button/button');
require('../../../common/pkgs/progress/progress');
require('../css/create');

var header = require('../../header/js/header');
var zhaomi = require('../../../lib/common/common');
var utils = require('../../../common/utils');

var compileTpl = utils.compileTpl;

var RADIO = 'radio';
var CHECKBOX = 'checkbox';
var QUESTION = 'question';
var UPLOAD = 'upload';

$(function() {

    var $questions = $('#action-questions');
    // 以已存在的问题条目数作为初始化值，而不是0
    // 为了解决在编辑、复制问卷时，因页面已存在问题从而导致序号错误
    var seqNo = $('.action-item').length;

    // 增加问题
    $('#criteria-operation').on('click', 'ul li', function() {
        var qType = $(this).data('type'), ctx;
        seqNo++;
        ctx = {
            seqNo: seqNo
        }
        switch (qType) {
            case RADIO:
                $questions.append($(compileTpl(RADIO_TPL, ctx)));
                break;
            case CHECKBOX:
                $questions.append($(compileTpl(CHECKBOX_TPL, ctx)));
                break;
            case QUESTION:
                $questions.append($(compileTpl(QUESTION_TPL, ctx)));
                break;
            case UPLOAD:
                $questions.append($(compileTpl(UPLOAD_TPL, ctx)));
                break;
        }

        // placeholder polyfill
        $('input').placeholder();
    })

    $questions.on('mouseenter', '.criteria-q, ul li', function() {
        $(this).find('.criteria-del').addClass('show');
    }).on('mouseleave', '.criteria-q, ul li', function() {
        $(this).find('.criteria-del').removeClass('show');
    }).on('click', '.criteria-del', function() {
        // 删除问题
        if ($(this).parent('.criteria-q').length) {
            $(this).closest('.action-item').remove();
            seqNo--;
            updateSeqNo();
        } 
        // 删除问题的某个选项
        else {
            if ($(this).parents('.action-answers').find('.criteria-a-input').length < 3) {
                utils.warn('选项数不能少于2个！');
                return false;
            }
            $(this).closest('li').remove();
        }
    }).on('click', '.criteria-add', function() {
        var qType = $(this).closest('.action-item').data('type');
        if (qType === RADIO) {
            $(this).closest('li').before($(RADIO_OPT_TPL));
        } else if (qType === CHECKBOX) {
            $(this).closest('li').before($(CHECKBOX_OPT_TPL));
        }
    });

    $('#create-action-second').submit(function() {
        var data = collectData();

        $(this).ajaxSubmit({
            dataType: 'json',
            data: {
                criteria: JSON.stringify(data)
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
                        break;
                    }
                }
            }
        });

        return false;
    })

    // 更新问题序号
    function updateSeqNo() {
        var i = 1;
        $('.action-item').each(function(idx, elem) {
            $(elem).find('.criteria-seqno').text((i++) + '、');
        })
    }
// window.xxx = collectData;
    function collectData() {
        var data = {
            radio: [],
            checkbox: [],
            question: [],
            upload: []
        };

        $('.action-item').each(function(idx, elem) {
            var q, type, opts = [];
            var $actionItem = $(elem);
            var singleQuestion;

            type = $actionItem.data('type');
            q = $actionItem.find('.criteria-q-input').val();

            singleQuestion = {
                q: q,
                type: type
            }
            
            if (type === RADIO || type === CHECKBOX) {
                opts = $actionItem.find('.action-answers ul li')
                    .map(function(idx, elem) {
                        return $(elem).find('.criteria-a-input').val();
                    })
                    .filter(function(idx, val) {
                        return val !== '';
                    })
                opts = $.makeArray(opts);
                singleQuestion['a'] = opts;
            }
            
            // if (lastIndexOfType[type])
            data[type].push(singleQuestion);
        })

        return data.radio.concat(data.checkbox)
                .concat(data.question).concat(data.upload);
    }

    var RADIO_TPL = '<div class="action-item" data-type="radio">' +
                        '<div class="criteria-q fn-clr">' +
                            '<span class="criteria-seqno">{seqNo}、</span>' +
                            '<input class="criteria-q-input" placeholder="在这里填写你的单选问题~"></input>' +
                            '<span class="criteria-del"></span>' +
                        '</div>' +
                        '<div class="action-answers">' +
                            '<ul class="fn-clr">' +
                                '<li>' +
                                    '<span class="z-radio"></span>' +
                                    '<input class="criteria-a-input" placeholder="选项"></input>' +
                                    '<span class="criteria-del"></span>' +
                                '</li>' +
                                '<li>' +
                                    '<span class="z-radio"></span>' +
                                    '<input class="criteria-a-input" placeholder="选项"></input>' +
                                    '<span class="criteria-del"></span>' +
                                '</li>' +
                                '<li>' +
                                    '<span class="z-radio"></span>' +
                                    '<input class="criteria-a-input" placeholder="选项"></input>' +
                                    '<span class="criteria-del"></span>' +
                                '</li>' +
                                '<li>' +
                                    '<span class="criteria-add"></span>' +
                                '</li>' +
                            '</ul>' +
                        '</div>' +
                    '</div>';
    var RADIO_OPT_TPL = '<li>' +
                            '<span class="z-radio"></span>' +
                            '<input class="criteria-a-input" placeholder="选项"></input>' +
                            '<span class="criteria-del"></span>' +
                        '</li>';

    var CHECKBOX_TPL = '<div class="action-item" data-type="checkbox">' +
                            '<div class="criteria-q fn-clr">' +
                                '<span class="criteria-seqno">{seqNo}、</span>' +
                                '<input class="criteria-q-input" placeholder="在这里填写你的多选问题~"></input>' +
                                '<span class="criteria-del"></span>' +
                            '</div>' +
                            '<div class="action-answers">' +
                                '<ul class="fn-clr">' +
                                    '<li>' +
                                        '<span class="z-checkbox"></span>' +
                                        '<input class="criteria-a-input" placeholder="选项"></input>' +
                                        '<span class="criteria-del"></span>' +
                                    '</li>' +
                                    '<li>' +
                                        '<span class="z-checkbox"></span>' +
                                        '<input class="criteria-a-input" placeholder="选项"></input>' +
                                        '<span class="criteria-del"></span>' +
                                    '</li>' +
                                    '<li>' +
                                        '<span class="z-checkbox"></span>' +
                                        '<input class="criteria-a-input" placeholder="选项"></input>' +
                                        '<span class="criteria-del"></span>' +
                                    '</li>' +
                                    '<li>' +
                                        '<span class="criteria-add"></span>' +
                                    '</li>' +
                                '</ul>' +
                            '</div>' + 
                        '</div>';
    var CHECKBOX_OPT_TPL = '<li>' +
                            '<span class="z-checkbox"></span>' +
                            '<input class="criteria-a-input" placeholder="选项"></input>' +
                            '<span class="criteria-del"></span>' +
                        '</li>';

    var QUESTION_TPL = '<div class="action-item" data-type="question">' +
                            '<div class="criteria-q fn-clr">' +
                                '<span class="criteria-seqno">{seqNo}、</span>' +
                                '<input class="criteria-q-input" placeholder="请在这里填写你要问的问答题~"></input>' +
                                '<span class="criteria-del"></span>' +
                            '</div>' +
                            '<textarea></textarea>' +
                        '</div>';

    var UPLOAD_TPL = '<div class="action-item" data-type="upload">' +
                        '<div class="criteria-q fn-clr">' +
                            '<span class="criteria-seqno">{seqNo}、</span>' +
                            '<input class="criteria-q-input" placeholder="请在这里填写你要求上传的文件~"></input>' +
                            '<span class="criteria-del"></span>' +
                        '</div>' +
                        '<input type="file"/>' +
                    '</div>';
});