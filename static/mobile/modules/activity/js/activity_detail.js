$(function() {
	//单选
	radio($(".dan-radio .round"),1);
    //多选
    radio($(".more-radio .round"),2);
    //点击答题区域判断是否登录
	$("#wrap_apply").on("click",function(){
		var $id = $("#dataId").attr("data-value");
		if($id == 0){
			window.location.href="new_logo.html";
		}
	})
});


function radio(elements,num){
	elements.on("click",function(){
		var $current=$(this);
		if(num==1){
			if(!$current.find("div").hasClass("color-round")){
				elements.find("div").removeClass("color-round");
				$current.find("div").addClass("color-round");
			}
		}else if(num == 2){
			if(!$current.find("div").hasClass("color-round")){
				$current.find("div").addClass("color-round");
			}else{
				$current.find("div").removeClass("color-round");
			}
		}else{
			return;
		}
	})
}
