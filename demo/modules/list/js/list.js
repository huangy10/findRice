require('../../../common/pkgs/button/button');
require('../css/list');

console.log(1)
var header = require('../../header/js/header');
var share = require('../../../common/pkgs/share/share');

$(function() {
    $('#banner').unslider({
        speed: 600,
        delay: 3000, 
        dots: true
    });

    $('.share').click(function() {
        share({
            webid: 'cqq',
            url: 'http://www.baidu.com',
            title: '测试share功能'
        })
    });

    $('.action-card').click(function() {
        window.open('/demo/detail.html', '_blank');
    })
});