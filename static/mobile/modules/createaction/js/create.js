require('../../../common/pkgs/button/button');
require('../css/create');
var common = require('../../../lib/common/common.js');
var utils = common;

$(function() {

  var $form = $('#create-action-final');

  var $container = $(this).parents('.main');
  var isVerified = $container.data('verified') === 'yes';
  var verifiedAction = $container.data('verifiedaction');

  $('#publish').click(function(e) {

      $form.ajaxForm({
          dataType: 'json',
          success: function(res) {
              var success = res && res.success;
              var data = res && res.data;
              
              if (success) {
                  if (data.url) {
                      var modal = common.modal({
                         tipText: '发布成功',
                         sureBtnText: '确定',
                         verifiedAction: verifiedAction,
                         sureCallback: function() {
                            location.href = data.url;        
                         },
                         isSimpleModal: isVerified
                      });
                      modal.show();
                  } 
              } else {
                  for (var key in data) {
                      // $('#' + key).removeClass('focus').addClass('err');
                      utils.warn(data[key]);
                      break;
                  }
              }
          }
      })

      $form.submit();
  });

  $('#save').click(function() {
      var actionUrl = $(this).data('action');
      var $container = $(this).parents('.main');
      var isVerified = $container.data('verified') === 'yes';
      var verifiedAction = $container.data('verifiedaction');

      $form.ajaxForm({
          url: actionUrl,
          dataType: 'json',
          success: function(res) {
              var success = res && res.success;
              var data = res && res.data;
              
              if (success) {
                  if (data.url) {
                      var modal = common.modal({
                         tipText: '保存成功',
                         sureBtnText: '确定',
                         verifiedAction: verifiedAction,
                         sureCallback: function() {
                            location.href = data.url;        
                         },
                         isSimpleModal: isVerified
                      });
                      modal.show(); 
                  } 
              } else {
                  for (var key in data) {
                      // $('#' + key).removeClass('focus').addClass('err');
                      utils.warn(data[key]);
                      break;
                  }
              }
          }
      })

      $form.submit();
  });
})