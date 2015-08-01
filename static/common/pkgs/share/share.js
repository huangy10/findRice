// http://www.jiathis.com/help/html/share-with-jiathis-api
// http://www.jiathis.com/help/html/support-media-website
module.exports = function share(options) {
    options = options || {};
    if (!options.webid || !options.url) {
        return;
    }

    window.open('http://www.jiathis.com/send/?webid=' +
        options.webid + '&url=' + 
        options.url + '&title=' +
        options.title);
}