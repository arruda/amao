# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response

from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.conf import settings

from Teste.models import TesteQuestao, Fontes

#-----------------------AJAX----------------------
from django.core import serializers
from django.http import HttpResponse
#from django.shortcuts import render_to_response
#from DjangoAjax.contatos.models import Contatos
from Teste.models import Contatos
#-----------------------AJAX----------------------

def index(request):
    return render_to_response('Teste/testeAjax.html',)

def get_contatos(request):
    contatos = Contatos.objects.all()
    retorno = serializers.serialize("json",  contatos)
    return HttpResponse(retorno, mimetype="text/javascript")



def xhr_test(request):
    if request.is_ajax():
        message = "Hello AJAX"
    else:
        message = "Hello"
    return HttpResponse(message)



#import commands
import os

def compilar(questao,user):
    #verifica se existe a pasta, se nao existe ele cria
    if not os.path.exists(settings.MEDIA_ROOT + """execs/"""+user.username):
        os.makedirs (settings.MEDIA_ROOT + """execs/"""+user.username)
        
    #caminho pro arquivo makefile gerado dinamicamente
    pathMkFile = os.path.join(settings.MEDIA_ROOT,"fontes",str(questao.user.username),"makefile")   
    
    #gera o makefile dos fontes
    #questao.gerar_makefile()
    
    #compila usando makefile dos fontes
    command = "make -f " + pathMkFile
    
    #output = commands.getoutput(command)

    output = os.system(command)    
    #depois de compilar limpa os arquivos .o gerados
    os.system("make clean -f " + pathMkFile)
    
    return output


@login_required     
def testeCompilacao(request,questao_id):
    user = request.user
    questao = get_object_or_404(TesteQuestao,pk=questao_id)
      
    ret = compilar(questao,user)


    return render_to_response('Teste/testeCompilacao.html', locals(),context_instance=RequestContext(request))


def rodar(questao,user):
    #verifica se existe a pasta de usuario em execs, se nao existe ele cria
    if not os.path.exists(settings.MEDIA_ROOT + """execs/"""+user.username):
        os.makedirs (settings.MEDIA_ROOT + """execs/"""+user.username)

    #verifica se existe a pasta de usuario em saida, se nao existe ele cria
    if not os.path.exists(settings.MEDIA_ROOT + """saida/"""+user.username):
        os.makedirs (settings.MEDIA_ROOT + """saida/"""+user.username)
                        
    command = settings.MEDIA_ROOT + """execs/"""+user.username+"""/"""+ questao.titulo 
    command += " < "+ settings.MEDIA_ROOT + questao.entrada.__str__() +""" > """ + settings.MEDIA_ROOT + """saida/"""+user.username+"""/"""+questao.titulo
    #output = """"""+settings.MEDIA_ROOT
    #output = commands.getoutput(command)

    output = os.system(command)

    return output

@login_required     
def testeRodar(request, questao_id):
    user = request.user
    questao = get_object_or_404(TesteQuestao,pk=questao_id)
      
    ret = rodar(questao,user)


    return render_to_response('Teste/testeRodar.html', locals(),context_instance=RequestContext(request))


def comparar(questao,user):

    #verifica se existe a pasta de usuario em saida, se nao existe ele cria
    if not os.path.exists(settings.MEDIA_ROOT + """saida/"""+user.username):
        os.makedirs (settings.MEDIA_ROOT + """saida/"""+user.username)
        
    command ="""diff """ + settings.MEDIA_ROOT + """saida/"""+user.username+"""/"""+ questao.titulo +""" """ + settings.MEDIA_ROOT + """saidaRef/"""+questao.titulo
    #output = """"""+settings.MEDIA_ROOT
    #output = commands.getoutput(command)

    output = os.system(command)

    return output    

@login_required     
def testeComparacao(request, questao_id):
    user = request.user
    questao = get_object_or_404(TesteQuestao,pk=questao_id)
      
    ret = comparar(questao,user)


    return render_to_response('Teste/testeRodar.html', locals(),context_instance=RequestContext(request))


def removerTudoQuestao(user,questao):
    
    pathExec = settings.MEDIA_ROOT + """execs/"""+user.username+"/"
    execFilePath =  pathExec + questao.titulo
        
    pathSaida = settings.MEDIA_ROOT + """saida/"""+user.username+"/"
    saidaFilePath =  pathSaida + questao.titulo
        
    
    for fonte in questao.fontes.all():            
        pathFontes = settings.MEDIA_ROOT + """fonte/"""+user.username
        sourceFilePath =  settings.MEDIA_ROOT + fonte.fonte.__str__()
        mkFilePath = os.path.join(pathFontes,"makefile")   
        #remove os fontes
        if os.path.exists(pathFontes):
            os.remove(sourceFilePath)
            #remover makefile?
            #os.remove(mkFilePath)
            
        
    #remove o exetucavel
    if os.path.exists(pathExec):
        os.remove(execFilePath)
                        
    #remove o saida
    if os.path.exists(pathSaida):
        os.remove(saidaFilePath)
        
    return True

@login_required     
def testeTudo(request,questao_id):
    user = request.user

    questao = get_object_or_404(TesteQuestao,pk=questao_id)
    
    ret1 = compilar(questao,user)
    ret2 = rodar(questao,user)        
    ret3 = comparar(questao,user)
    
    ret =str(ret1)+"\n\n"+str(ret2)+"\n\n"+str(ret3)+"\n\n"
        
    removerTudoQuestao(user,questao)        
    
    return render_to_response('Teste/testeRodar.html', locals(),context_instance=RequestContext(request))

