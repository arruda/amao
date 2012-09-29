function fecharDiv(ele){
	var alvo=ele.parentNode;
	if(alvo.getAttribute('data-lock')!='true'){
		var classes=alvo.className.split(" ");
		if(classes[classes.length-1]=='closed'){		
			resizeTo(alvo,parseInt(alvo.getAttribute('data-height')),"ele.className=ele.getAttribute('data-class')");
			ele.innerHTML='F';
			return;
		}
		alvo.setAttribute('data-class',alvo.className);
		alvo.setAttribute('data-height',alvo.offsetHeight);
		resizeTo(alvo,40,'');	
		alvo.className+=' closed';
		ele.innerHTML='A';
	}
}
function resizeTo(ele,nHeight,callback){
	ele.setAttribute('data-lock','true');
	var atualHeight=ele.offsetHeight;
	var dif=nHeight-atualHeight;
	var base=dif/Math.abs(dif)*10;
	if(Math.abs(dif)<=Math.abs(base)){
		ele.setAttribute('data-lock','false');
		eval(callback);
	}else{
		ele.style.height=(atualHeight+base)+"px";
		setTimeout(function(){ resizeTo(ele,nHeight,callback); },30);
	}
}