// http://www.jiathis.com/help/html/share-with-jiathis-api
// http://www.jiathis.com/help/html/support-media-website
module.exports = function share(options) {
    options = options || {};
    if (!options.webid || !options.url) {
        return;
    }

    var title = options.title || '找米分享';

    // $("#share-dialog").dialog({
    //     resizable: false,
    //     width: 500,
    //     title: '通过链接分享：'
    // });
    window.open('http://www.jiathis.com/send/?webid=' +
        options.webid + '&url=' + 
        options.url + '&title=' +
        title);
}