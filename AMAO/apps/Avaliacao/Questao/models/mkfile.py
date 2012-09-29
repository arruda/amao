# -*- coding: utf-8 -*-

from django.db import models    

from os.path import join as joinPath, exists as existisPath , basename

from django.conf import settings
        
        

def criar_texto_mkfile(questao):
    """
    Gera o conteudo do makefile para utilizar todos os .cpp necessarios
    """
    conteudo = "CC=g++\nCFLAGS=-c -Wall\nLDFLAGS=\nSOURCES="
    for fonte in questao.fontes.all():
        conteudo += joinPath(settings.MEDIA_ROOT, fonte.__str__()) + " "
    conteudo += "\nOBJECTS=$(SOURCES:.cpp=.o)\nEXECUTABLE="
    conteudo += joinPath(settings.MEDIA_ROOT,"execs",questao.avaliacao.aluno.slug,questao.avaliacao.slug,questao.slug,questao.questao.slug)
    conteudo += "\nall: $(SOURCES) $(EXECUTABLE)\n$(EXECUTABLE): $(OBJECTS)\n\t$(CC) $(LDFLAGS) $(OBJECTS) -o $@"
    conteudo += "\n.cpp.o:\n\t$(CC) $(CFLAGS) $< -o $@\nclean:\n\trm -rf "
    conteudo += joinPath(settings.MEDIA_ROOT,"fontes",str(questao.avaliacao.aluno.slug),str(questao.avaliacao.slug),str(questao.slug),"*.o") 
        
    return conteudo
    

#def gerar_makefile(self):
#    """
#    Gera um makefile para os fontes necessarios e retorna o path para o arquivo gerado.
#    """
#    #se diretorio nao existir cria eles
#    dirPath = joinPath(settings.MEDIA_ROOT,"fontes",str(self.avaliacao.aluno.slug),str(self.avaliacao.slug),str(self.questao.slug))
#    if not existisPath(filePath):
#        from os import makedirs
#        os.makedirs(dirPath)
#        
#    filePath = joinPath(dirPath, "makefile")            
#    #abre o arquivo no caminho posto acima, escreve no arquivo e da close
#    mkfile = open(filePath,'w')                   
#    mkfile.write(criar_texto_mkfile(self))        
#    mkfile.close()        
#    
#    return filePath
