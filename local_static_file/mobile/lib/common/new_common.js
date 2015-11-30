$(function(){
	foucsBorder($(".input-frame input"));	
})

function foucsBorder(obj){
	obj.on("focus",function(){
		$(this).parent().addClass("border4B");
	})
	obj.on("blur",function(){
		$(this).parent().removeClass("border4B");
	})
}
