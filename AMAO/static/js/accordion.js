$(document).ready(function(){
	$('h3.accordion').click(function(){
		$(this).parent().find('div.accordion').slideToggle("slow");
	});
});