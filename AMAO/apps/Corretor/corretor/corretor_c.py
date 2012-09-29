# -*- coding: utf-8 -*-
import os
from Corretor.base import Corretor, CompiladorException
from Questao.models import Questao, QuestaoDeAvaliacao
from Questao.models import path_execs,path_execs_gabarito, path_automaticas, path_mkfiles_gabarito,path_mkfiles

class CorretorCPP(Corretor):
    """Um corretor padrao expecifico para a linguagem CPP
    """

    def compilar(self, **kwargs):
        """Metodo chamado quando se precisa compilar os arquivos
        """
        questao = kwargs.get('questao',None)
        if questao is None:
            raise CompiladorException

        path_mkfile= self.gerar_makefile(questao)
        
        
        #compila usando makefile dos fontes
        command = "make -f " + path_mkfile
        output = os.system(command)    
        #depois de compilar limpa os arquivos .o gerados
        os.system("make clean -f " + path_mkfile)
        
        return output

    def comparar(self, **kwargs):
        """Metodo chamado quando se precisa comparar o resultado com um gabarito
        """
        return

    def avaliar(self, **kwargs):
        """Metodo chamado quando se precisa fazer alguma avaliacao alem da comparacao
        """
        return

    def _criar_texto_mkfile(self,questao):
        """
        Gera o conteudo do makefile para utilizar todos os .cpp necessarios
        """
        avaliacao = None
        aluno=None
        path_execs= ""
        if type(questao) is QuestaoDeAvaliacao:
            fontes = questao.fontes.all()
            avaliacao = questao.avaliacao
            aluno = avaliacao.aluno
            questao=questao.questao
            path_execs= path_execs(questao)
        elif type(questao) is Questao:
            fontes = questao.fontesGabarito.all()
            path_execs= path_execs_gabarito(questao)

        conteudo = "CC=g++\nCFLAGS=-c -Wall\nLDFLAGS=\nSOURCES="
        #se for questão de avaliacao faz percorre os fontes e usa as paths dos mesmos 
        for fonte in fontes:
            conteudo += joinPath(settings.MEDIA_ROOT, fonte.__str__()) + " "
        conteudo += "\nOBJECTS=$(SOURCES:.cpp=.o)\nEXECUTABLE="
        conteudo += path_execs
        conteudo += "\nall: $(SOURCES) $(EXECUTABLE)\n$(EXECUTABLE): $(OBJECTS)\n\t$(CC) $(LDFLAGS) $(OBJECTS) -o $@"
        conteudo += "\n.cpp.o:\n\t$(CC) $(CFLAGS) $< -o $@\nclean:\n\trm -rf "
        conteudo += path_automaticas({'tipo':'fontes','aluno':aluno,'avaliacao':avaliacao,'questao':questao,'filename':"*.o"})
            
            
        return conteudo


    def gerar_makefile(self,questao):
        """
        Gera um makefile para os fontes necessarios e retorna o path para o arquivo gerado.
        """
        #se for a questao de um aluno
        if type(questao) is QuestaoDeAvaliacao:
            filepath = path_mkfiles(questao)
        #se for questao gera makefile no gabarito
        elif type(questao) is Questao:
            filepath = path_mkfiles_gabarito(questao)
                    
        #abre o arquivo no caminho posto acima, escreve no arquivo e da close
        mkfile = open(filepath,'w')                   
        mkfile.write(self._criar_texto_mkfile(questao))        
        mkfile.close()        
        
        return filepath
