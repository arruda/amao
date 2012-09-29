var elemento=new Array()

function prepara(nome,agrup,val){
    var num=document.getElementsByClassName(nome).length-1;
    elemento[nome]=new Array()
    elemento[nome]['html']=document.getElementsByClassName(nome)[num].innerHTML;  
    elemento[nome]['class']=document.getElementsByClassName(nome)[num].className;  
    elemento[nome]['hiddenId']='id_'+val+'-TOTAL_FORMS';  
    elemento[nome]['agrupador']=agrup;  
    elemento[nome]['num_inputs']=document.getElementsByClassName(nome)[0].getElementsByTagName("span").length; 
} 

function adicionar(nome){
    var novoEle=document.createElement('div');
    novoEle.innerHTML=elemento[nome]['html'];  
    novoEle.className=elemento[nome]['class'];
    document.getElementById(elemento[nome]['agrupador']).appendChild(novoEle);
}

function remover(ele){
    ele.parentNode.parentNode.parentNode.removeChild(ele.parentNode.parentNode);
}

function salvar(ele){ 
    for(var nome in elemento){
        var imputs=document.getElementById(elemento[nome]['agrupador']).getElementsByTagName("span");
        for(var i=0;i<imputs.length;i++){
            var imp=imputs[i].lastChild;
            var nameForm=imp.name.split("-")
            imp.name=nameForm[0]+"-"+Math.floor(i/elemento[nome]['num_inputs'])+"-"+nameForm[2];
        }
        document.getElementById(elemento[nome]['hiddenId']).value=Math.floor(i/elemento[nome]['num_inputs']);
    }
   ele.form.submit();
}

