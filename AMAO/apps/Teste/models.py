# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User

from os.path import join as joinPath, basename

from django.conf import settings
        
    
def criar_texto_mkfile(questao):
    """Gera o conteudo do makefile para utilizar todos os .cpp necessarios
    """
    conteudo = "CC=g++\nCFLAGS=-c -Wall\nLDFLAGS=\nSOURCES="
    for fonte in questao.fontes.all():
        conteudo += settings.MEDIA_ROOT +str(fonte.__str__()) + " "
    conteudo += "\nOBJECTS=$(SOURCES:.cpp=.o)\nEXECUTABLE="
    conteudo += settings.MEDIA_ROOT + "execs/"+questao.user.username+"/"+questao.titulo
    conteudo += "\nall: $(SOURCES) $(EXECUTABLE)\n$(EXECUTABLE): $(OBJECTS)\n\t$(CC) $(LDFLAGS) $(OBJECTS) -o $@"
    conteudo += "\n.cpp.o:\n\t$(CC) $(CFLAGS) $< -o $@\nclean:\n\trm -rf "
    conteudo += joinPath(settings.MEDIA_ROOT,"fontes",str(questao.user.username),"*.o") 
    
    return conteudo
    
class TesteQuestao(models.Model):

    user = models.ForeignKey(User)    


    titulo = models.CharField(u"Titulo", max_length=250)    
    enunciado = models.TextField(u"Enunciado da Questao")
    #fonte = models.FileField(u"Fonte",upload_to=get_upload_path)
    entrada = models.FileField(u"Entrada",upload_to='entrada',null=True, blank=True)
    saidaRef = models.FileField(u"Saida de Referencia",upload_to='saidaRef',null=True, blank=True)
    saida = models.FileField(u"Saida",upload_to='saida',null=True, blank=True)
    
    def gerar_makefile(self):
        """Gera um makefile para os fontes necessarios e retorna o path para o arquivo gerado.
        """
        filePath = joinPath(settings.MEDIA_ROOT,"fontes",str(self.user.username),"makefile")
        
        #abre o arquivo no caminho posto acima, escreve no arquivo e da close
        mkfile = open(filePath,'w')                   
        mkfile.write(criar_texto_mkfile(self))        
        mkfile.close()        
        
        return filePath
        
    def save(self, *args, **kwargs):
        super(TesteQuestao, self).save(*args, **kwargs)
        #self.gerar_makefile()
        
    def __unicode__(self):
        return self.titulo

def get_upload_path_fontes(instance, filename):
    return joinPath("fontes",str(instance.questao.user.username), filename)

class Fontes(models.Model):
    questao = models.ForeignKey(TesteQuestao, related_name='fontes')    
    
    fonte = models.FileField(u"Fonte",upload_to=get_upload_path_fontes)
    
    def filename(self):
        return basename(self.fonte.name)

    def __unicode__(self):
        return self.fonte.name
        
    def save(self, *args, **kwargs):
        super(Fontes, self).save(*args, **kwargs)
        self.questao.gerar_makefile()
        
        
        
class Contatos(models.Model):
    nome = models.CharField('Nome', max_length=40)
    telefone = models.CharField('Telefone', max_length=15, blank=True)
    celular = models.CharField('Celular', max_length=15, blank=True)
    email = models.CharField('E-mail', max_length=40, blank=True)

    class Meta:
        db_table = 'contatos' #define o nome da tabela no banco

    def __unicode__(self):
        return self.nome
    
