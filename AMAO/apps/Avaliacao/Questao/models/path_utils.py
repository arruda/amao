# -*- coding: utf-8 -*-

from django.db import models    
import os
    
#def get_upload_path_saidaRef(instance, filename):
#    """
#    Retorna o caminho para o arquivo de saidaRef de uma questao
#    saidaRef/questaoID/filename
#    """    
#    return joinPath("saidaRef",str(instance.slug),filename)
#    
#def get_upload_path_entradaRef(instance, filename):
#    """
#    Retorna o caminho para o arquivo de entradaRef de uma questao
#    entradasRef/questaoID/filename
#    """
#    #verificar se ja existe a questao nesse momento.
#    return joinPath("entradaRef",str(instance.slug), filename)


#def get_upload_path_fontes(instance, filename):
#    """
#    Retorna o caminho para o arquivo fonte de uma QuestaoAvaliacao
#    fontes/ALUNO.SLUG/AVALIACAO.SLUG/QUESTAO.SLUG/filename
#    """
#    #verificar se ja existe id para avaliacao e para questao nesse momento, pois isso é crucial
#    return joinPath("fontes",str(instance.questao.avaliacao.aluno.slug),str(instance.questao.avaliacao.slug),str(instance.questao.questao.slug), filename)


#def get_upload_path_fonteGabarito(instance, filename):
#    """
#    Retorna o caminho para o arquivo fonte
#    fontes/QUESTAO.SLUG/GABARITO/FONTES/filename
#    """
#    #verificar se ja existe id para avaliacao e para questao nesse momento, pois isso é crucial
#    return joinPath("fontes",str(instance.questao.slug),"FONTES","GABARITO", filename)

#def get_upload_path_entradaGabarito(instance, filename):
#    """
#    Retorna o caminho para o arquivo fonte
#    entradas/QUESTAO.SLUG/GABARITO/ENTRADAS/filename
#    """
#    #verificar se ja existe id para avaliacao e para questao nesse momento, pois isso é crucial
#    return joinPath("entradas",str(instance.questao.slug),"ENTRADAS","GABARITO", filename)





#refazendo as paths do sistema

def exist_or_create_path(path):
    """Verifica se um caminho existe, se não existir cria ele com todas as estruturas de diretorio necessarias.
    """

    if not os.path.exists(path):
        os.makedirs(path)
    

def path_base(questao,aluno=None,avaliacao=None):
    """Retorna o caminho basico para upload de arquivos.
       se avaliacao for diferente de None ele considera que é para um aluno.
        se for None ele faz como sendo um gabarito.

    GABARITO_BASE = gabarito/QUESTAO 
    ALUNO_BASE = ALUNO/AVALIACAO/QUESTAO
    BASE= ALUNO_BASE ou GABARITO_BASE
    """
    
    if avaliacao != None and aluno != None:
        base = os.path.join(aluno.slug,avaliacao.slug)
    else:
        base = "gabarito"

    base = os.path.join(base,questao.slug)
    return base



def path_helper(tipo,**kwargs):
    """tipo = pasta a ser criada depois do basico.
        questao
        avaliacao -> 
        aluno ->se for para um aluno
        criar -> se é para tentar criar o diretorio
    """
    questao= kwargs.get('questao',None)
    aluno = kwargs.get('aluno',None)
    avaliacao = kwargs.get('avaliacao',None)
    criar = kwargs.get('criar',False)
    base = path_base(questao,aluno,avaliacao)  
    path = os.path.join(base,tipo)
    
    header = kwargs.get('header',None)
    if header != None:
        path = os.path.join(header,path)
    if criar:
        exist_or_create_path(path)

    return path

def _dict_questao_aluno(questao):
    "Retorna um dicionario com informacoes da questao, avaliacao e aluno de uma questao de avaliacao"
    dct = {'questao':questao.questao,
            'avaliacao':questao.avaliacao,
            'aluno':questao.avaliacao.aluno}
    return dct
    

#automaticas
def path_automaticas(**kwargs):
    """Informar questao(questao ou uma questao de avaliacao)
        se for uma questao de avaliacao, informar tambem:
        aluno e avaliacao.
    """
    tipo = kwargs.get('tipo',None)
    novo_dict = kwargs.copy()
    novo_dict['criar']=True
    if tipo != None:
        del novo_dict['tipo']
    filename = kwargs.get('filename',None)
    if tipo is None or filename is None:
        return None
    
    return os.path.join(path_helper(tipo,**novo_dict),filename)

def path_execs_gabarito(questao,header=None):
    "Retorna o caminho no formato: GABARITO/QUESTAO/EXECS/QUESTAO"
    dct = {'tipo':'execs','questao':questao,'filename':questao.slug}    
    dct['header'] = header
    return path_automaticas(**dct)

def path_mkfiles_gabarito(questao,header=None):
    "Retorna o caminho no formato: GABARITO/QUESTAO/MKFILES/QUESTAO"
#    avaliacao = questao.avaliacao
#    aluno = avaliacao.aluno
    dct = {'tipo':'mkfiles','questao':questao,'filename':questao.slug}    
    dct['header'] = header
    return path_automaticas(**dct)

def path_saidas_gabarito(questao,header=None):
    "Retorna o caminho no formato: GABARITO/QUESTAO/SAIDAS/QUESTAO"
#    avaliacao = questao.avaliacao
#    aluno = avaliacao.aluno
    dct = {'tipo':'saidas','questao':questao,'filename':questao.slug}    
    dct['header'] = header
    return path_automaticas(**dct)

def path_execs(questao,header=None):
    "Retorna o caminho no formato: ALUNO/AVALIACAO/QUESTAO/EXECS/QUESTAO"
    avaliacao = questao.avaliacao
    aluno = avaliacao.aluno
    dct = {'tipo':'execs','aluno':aluno,'avaliacao':avaliacao,'questao':questao.questao,'filename':questao.questao.slug}    
    dct['header'] = header
    return path_automaticas(**dct)


def path_mkfiles(questao,header=None):
    "Retorna o caminho no formato: ALUNO/AVALIACAO/QUESTAO/MKFILES/QUESTAO"
    avaliacao = questao.avaliacao
    aluno = avaliacao.aluno
    dct = {'tipo':'mkfiles','aluno':aluno,'avaliacao':avaliacao,'questao':questao.questao,'filename':questao.questao.slug}
    dct['header'] = header    
    return path_automaticas(**dct)

def path_saidas(questao,header=None):
    "Retorna o caminho no formato: ALUNO/AVALIACAO/QUESTAO/SAIDAS/QUESTAO"
    avaliacao = questao.avaliacao
    aluno = avaliacao.aluno
    dct = {'tipo':'saidas','aluno':aluno,'avaliacao':avaliacao,'questao':questao.questao,'filename':questao.questao.slug}  
    dct['header'] = header  
    return path_automaticas(**dct)

#uploads
def path_fontes_gabarito_upload(instance,filename):
    questao = instance.questao

    return os.path.join(path_helper('fontes',questao=questao),filename)

def path_fontes_upload(instance,filename):
    dct = _dict_questao_aluno(instance.questao)
    return os.path.join(path_helper('fontes',**dct),filename)

def path_entradas_gabarito_upload(instance,filename):
    questao = instance.questao
    return os.path.join(path_helper('entradas',questao=questao),filename)

