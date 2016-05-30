$(function() {
	//单选
	radio($(".dan-radio .round"),1);
    //多选
    radio($(".more-radio .round"),2);
    //点击答题区域判断是否登录
	$("#wrap_apply").on("click",function(){
		var $id = $("#dataId").attr("data-value");
		var $url=$(".btn-shade-bm").prop("href");
		if($id == 0){
			window.location.href=$url;
		}
	})
	//上传图片
	$('#fifth_file').change(function(){
		var picturName = $(this).val().split("\\");
		$(".file-btn").next(".hint-info").text(picturName[picturName.length-1]);
	}) 
	//表单提交验证
	$("#J_formDetail").submit(function(){
			  if ($("#J_apply").hasClass('no-selected')) {
	            return false;
	        }
			var firstRadio=$("#first_radio").find(".color-round").attr("data-value")
				,secondCheckbox=$("#second_checkbox").find(".color-round")
				,thirdId = $("#third_id").val()
				,fourActivity =$("#four_activity").val()
				,textDeatil = $(".text-detail")
				,nmb=0
				,dataList = []
				,secondCheckboxList = [];
				for(i=0;i<secondCheckbox.length;i++){
					secondCheckboxList[i]= $(secondCheckbox[i]).attr("data-value");
				}
				dataList = [
							{result: firstRadio,type:'radio'},
							{result: secondCheckboxList,type:'checkbox'},
							{result: thirdId,type:'question'},
							{result: fourActivity,type:'question'},
							{name: $("#fifth_file").attr("name"),result: 'whatever',type: 'upload'}
						];
						
			$(this).ajaxSubmit({
	            beforeSubmit: function() {
	    			textDeatil.each(function(){
						if($(this).val().trim() == ""){
							alert("有题目未做答！");
							nmb=1;
							return false;
						}
					})
	    			if(nmb == 1){
	    				return false;
	    			}
	    			//判断上传图片
	    			if($('#fifth_file').val() == ""){
	    				alert("请选择图片");
	    				return false;
	    			}
	    			$("#J_apply").addClass('no-selected').val('报名中...');
	            },
	            type:"post",
//	            url: "http://59.66.201.97/action/1/apply",
//	            dataType: 'json',
	            data: {
	                answer: JSON.stringify(dataList)
	            },
	            success: function(res) {
	                var success = res && res.success;
	                var data = res && res.data;
	                
	                if (success) {
	                    if (data.url) {
	                        location.href = data.url;  
	                    } 
	                } else {
	                   alert(res.data.id);
	                   $("#J_apply").remove('no-selected').val('报名');
	                }
	            }
	        })
			return false;
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