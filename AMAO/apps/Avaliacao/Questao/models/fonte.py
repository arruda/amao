# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_delete, pre_save 

from os.path import basename

#from path_utils import get_upload_path_entradaGabarito, get_upload_path_fonteGabarito, get_upload_path_fontes
from path_utils import path_entradas_gabarito_upload, path_fontes_gabarito_upload, path_fontes_upload, path_helper
        
from questao_avaliacao import QuestaoDeAvaliacao
from questao import Questao

class EntradaGabarito(models.Model):
    """
    Classe que representa um arquivo de entrada(gabarito) de uma questao.
    """   
    questao = models.ForeignKey(Questao, related_name='entradasGabarito')    
    
    arquivo = models.FileField(u"Arquivo", upload_to=path_entradas_gabarito_upload)
    
    class Meta:
        verbose_name = u'Entrada Gabarito'
        app_label = 'Questao'

    def filename(self):
        return basename(self.arquivo.name)

    def __unicode__(self):
        return self.arquivo.name   

class AbsFonte(models.Model):
    
    def filename(self):
        return basename(self.arquivo.name)
    
    def get_content(self):
        try:
            content = self.arquivo.read()
        except IOError:
            content ="No Content"
        return content

    def __unicode__(self):
        return self.arquivo.name   
    
    def save(self, *args, **kwargs):
        if self.pk != None:
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            print old.arquivo.name
            rm_fisica_arquivos(None,instance=old)
                
        super(AbsFonte, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        app_label = 'Questao'

def rm_fisica_arquivos(sender,**kwargs):
    "faz uma remoção fisica dos arquivos caso haja alguma alteracao em um arquivo fonte"
    fonte = kwargs['instance']
    from os import remove
    from os.path import join
    from django.conf import settings
    if fonte.arquivo == None or fonte.arquivo == "":
        return
    
    remove(join(settings.MEDIA_ROOT,str(fonte)))
    print join(settings.MEDIA_ROOT,str(fonte))
    

class FonteGabarito(AbsFonte):
    """
    Classe que representa um arquivo fonte de um gabarito de uma questao.
    """
    questao = models.ForeignKey(Questao, related_name='fontesGabarito')    
    
    arquivo = models.FileField(u"Arquivo", upload_to=path_fontes_gabarito_upload)
    
    usarNaResolucao = models.BooleanField(u"UsarNaResolucao",default=False)
    
    
    class Meta:
        verbose_name = u'Fonte Gabarito'
        app_label = 'Questao'

    def copiar_para_questaoDeAvaliacao(self,questaoAvaliacao):
        """
        copia esse arquivo fonte para a pasta de fontes do aluno
        cria um Fonte, sem salvar
        e retorna este, com as informacoes de arquivo e etc...
        """
        from os.path import join
        from shutil import copyfile
        from django.conf import settings
        fonte = Fonte(questao=questaoAvaliacao)
        path_src = join(settings.MEDIA_ROOT,str(self.arquivo))
        print "path_src %s" % path_src
        path_rel = path_fontes_upload(fonte,self.filename())
        fonte.arquivo = path_rel
        
        dct = {'questao':questaoAvaliacao.questao,
                'avaliacao':questaoAvaliacao.avaliacao,
                'aluno':questaoAvaliacao.avaliacao.aluno}
        dct['criar']=True
        dct['header']=settings.MEDIA_ROOT
        path_dest = join(path_helper('fontes',**dct),self.filename())
        print "path_src %s" % path_src
        print "path_dest %s" % path_dest
        copyfile(path_src,path_dest)
        return fonte
        
class Fonte(AbsFonte):
    """
    Classe que representa um arquivo fonte de uma questao de um aluno.
    """
    questao = models.ForeignKey(QuestaoDeAvaliacao, related_name='fontes')    
    
    arquivo = models.FileField(u"Arquivo",upload_to=path_fontes_upload)
    
    class Meta:
        verbose_name = u'Fonte'
        app_label = 'Questao'

#pre_save.connect(rm_fisica_arquivos, sender=Fonte)
#pre_save.connect(rm_fisica_arquivos, sender=FonteGabarito)
pre_delete.connect(rm_fisica_arquivos, sender=Fonte)
pre_delete.connect(rm_fisica_arquivos, sender=FonteGabarito)
        
    #Ver questao de signals em django    
    #para fazer isso da forma correta!
    #def save(self, *args, **kwargs):
    #    super(Fontes, self).save(*args, **kwargs)
    #    self.questao.gerar_makefile()
    

