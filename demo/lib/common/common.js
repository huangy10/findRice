module.exports = {
    postData: function(url, data, successCallback, errorCallback) {

        var csrfToken = $('#csrf_token').val();
        $.ajax({
            url: url,
            type: 'post',
            data: $.extend(data, {csrfToken: csrfToken}), 
            success: successCallback,
            error: errorCallback
        })
    }
}