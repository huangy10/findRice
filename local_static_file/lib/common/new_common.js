$(function(){
	foucsBorder($(".input-frame input"));
	login();
	register();
	findPwd();
})

function foucsBorder(obj){
	obj.on("focus",function(){
		$(this).parent().addClass("border4B");
	})
	obj.on("blur",function(){
		$(this).parent().removeClass("border4B");
	})
}

var numbers = 60,setInt = "";
function sendcode(current,mobile){
	var mobileValue=$(mobile).val().trim();
	var telReg  = !!mobileValue.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/);
	var csrfm = $("input[name='csrfmiddlewaretoken']").val();
	if(mobileValue == ""){
		alert("手机号不能为空！");
	}else{
		if(telReg == false){
			alert("手机号格式不正确！");
		}else{
			setInt = setInterval("countDown('"+current+"')",1000);
			$(current).val("重新发送(60)").addClass("sendCode").attr('disabled',true);
			$.ajax({
				type:"post",
				url:"/sendcode",
				data:{mobile:mobileValue,csrfmiddlewaretoken:csrfm},
				success:function(){
					
				}
			});
			
		}
	}
}






//定时器
function countDown(currents){
	numbers = --numbers;
	if(numbers == 0){
		numbers=60;
		clearInterval(setInt);
		$(currents).removeClass("sendCode").val("获取验证码").attr('disabled',false);
	}else{
		$(currents).val("重新发送("+numbers+")");
	}		
}


function  login(){

	$("#login-form").submit(function() {
		var username = $(".username").val().trim(),pwd = $(".pwd").val().trim();
            $(this).ajaxSubmit({
	            beforeSubmit: function() {
					var b = 0;
	            	if(username == ""){
	            		alert("手机号不能为空！");
	            	}else if(pwd == ""){
	            		alert("密码不能为空！");
	            	}else{
	            		b = 1;
	            	}
	            	if(b == 0){
	            		return false;
	            	}
	            },
	            dataType: "json",
	            success: function(t) {
	                var n = t && t.success,
	                e = t && t.data;
	                if (n) e.url && (location.href = e.url);
	                else {
	  					getReturn(e);
	                }
	            }
       		 })
    	return false;
	})





}

function  register(){
	
	$("#register-form").submit(function() {
		var mobile = $(".phone-type").val().trim()
			,authCode = $(".code-sytles").val().trim()
			,username = $(".username").val().trim()
			,pwd = $(".pwd").val().trim()
			,repeatPwd = $(".repeatPwd").val().trim()
			,birthdate = $("#birthdate").val().trim()
			,sexSecond = $(".sex-second").val().trim()
            ,telReg  =!!mobile.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/);
            $(this).ajaxSubmit({
	            beforeSubmit: function() {
					var b = 0;
	            	if(mobile == ""){
	            		alert("手机号不能为空！");
	            	}else if(telReg == false ){
	            		alert("手机号格式不正确！");
	            	}else if(authCode == ""){
	            		alert("验证码不能为空！");
	            	}else if(username == ""){
	            		alert("请输入真实姓名/企业名不能为空！");
	            	}else if(pwd == ""){
	            		alert("密码不能为空！");
	            	}else if(repeatPwd == ""){
	            		alert("重复密码不能为空！");
	            	}else if(pwd != repeatPwd ){
	            		alert("密码不一致！");
	            	}else if(birthdate == "" ){
	            		alert("请选择出生日期！");
	            	}else if(sexSecond == "请选择性别" ){
	            		alert("请选择性别！");
	            	}else{
	            		b = 1;
	            	}
	            	if(b == 0){
	            		return false;
	            	}
	            },
	            dataType: "json",
	            success: function(t) {
	                var n = t && t.success,
	                e = t && t.data;
	                if (n) e.url && (location.href = e.url);
	                else {
	  					getReturn(e);
	                }
	            }
       		 })
    	return false;
	})
	 
}



function  findPwd(){

	$("#findpwd-form").submit(function() {

		var mobile = $(".phone-type").val().trim()
			,authCode = $(".code-sytles").val().trim()
			,pwd = $(".pwd").val().trim()
			,repeatPwd = $(".repeatPwd").val().trim()
            ,telReg  =!!mobile.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/);
            $(this).ajaxSubmit({
	            beforeSubmit: function() {
					var b = 0;
	            	if(mobile == ""){
	            		alert("手机号不能为空！");
	            	}else if(telReg == false ){
	            		alert("手机号格式不正确！");
	            	}else if(authCode == ""){
	            		alert("验证码不能为空！");
	            	}else if(pwd == ""){
	            		alert("密码不能为空！");
	            	}else if(repeatPwd == ""){
	            		alert("重复密码不能为空！");
	            	}else if(pwd != repeatPwd ){
	            		alert("密码不一致！");
	            	}else{
	            		b = 1;
	            	}
	            	if(b == 0){
	            		return false;
	            	}
	            },
	            dataType: "json",
	            success: function(t) {
	                var n = t && t.success,
	                e = t && t.data;
	                if (n) e.url && (location.href = e.url);
	                else {
	  					getReturn(e);
	                }
	            }
       		 })
    	return false;
	})

}

//获取匹配后台json数据
function  getReturn(data){
	if(data.pwd){
		alert(data.pwd);
	}else if(data.pwd-confirm){
		alert(data.pwd-confirm);
	}else if(data.mobile){
       alert(data.mobile);
	}else if(data.verifycode){
   		alert(data.verifycode);
	}else if(data.unknown){
		alert(data.unknown);
	}else if(data.username){
		alert(data.username);
	}else if(data.phone_num){
       alert(data.phone_num);
	}else if(data.code){
   		alert(data.code);
	}else if(data.nickname){
		alert(data.nickname);
	}else if(data.password1){
		alert(data.password1);
	}else if(data.password2){
   		alert(data.password2);
	}else if(data.birthDate){
		alert(data.birthDate);
	}else if(data.gender){
		alert(data.gender);
	}
}

