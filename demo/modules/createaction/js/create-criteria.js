require('../../../common/pkgs/button/button');
require('../../../common/pkgs/progress/progress');
require('../css/create');

var header = require('../../header/js/header');
var utils = require('../../../lib/common/common');

var RADIO = 'radio';
var CHECKBOX = 'checkbox';
var QUESTION = 'question';
var UPLOAD = 'upload';

$(function() {

    var $questions = $('#action-questions');
    var seqNo = 0;

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
    })

    $questions.on('mouseenter', '.criteria-q, ul li', function() {
        $(this).find('.criteria-del').show();
    }).on('mouseleave', '.criteria-q, ul li', function() {
        $(this).find('.criteria-del').hide();
    }).on('click', '.criteria-del', function() {
        // 删除问题
        if ($(this).parent('.criteria-q').length) {
            $(this).closest('.action-item').remove();
            seqNo--;
            updateSeqNo();
        } 
        // 删除问题的某个选项
        else {
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

    $('#action-criteria-btns').click(function() {
        var data = collectData();
console.log(data)
        // utils.post('url', data);
    })

    // 更新问题序号
    function updateSeqNo() {
        var i = 1;
        $('.action-item').each(function(idx, elem) {
            $(elem).find('.criteria-seqno').text((i++) + '、');
        })
    }

    function compileTpl(tpl, data) {
        return tpl.replace(/\{(\w+)\}/g, function(all, param) {
            return data[param] || '';
        })
    }

    function collectData() {
        var data = [];

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
                opts = $.makeArray(opts);
                singleQuestion['a'] = opts;
            }
            
            data.push(singleQuestion);
        })

        return data;
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
                                '<input class="criteria-q-input" placeholder="在这里填写你的单选问题~"></input>' +
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