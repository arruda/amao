# -*- coding: utf-8 -*-
import os
from decimal import Decimal
from django.conf import settings
from corretor_sem_prog import CorretorSemProg
from Corretor.base import Corretor, CompiladorException, ExecutorException,ComparadorException, LockException
from Corretor.utils import comparar_strings
from celery.decorators import task


class CorretorCPP(CorretorSemProg):
    """Um corretor padrao expecifico para a linguagem C++
    """
#    from Avaliacao.Questao.models import path_execs, path_execs_gabarito, path_automaticas, path_mkfiles_gabarito,path_mkfiles
    def compilar(self, **kwargs):
        """Metodo chamado quando se precisa compilar os arquivos
        """
        questao = kwargs.get('questao',None)
        if questao is None:
            raise CompiladorException

        path_mkfile= self.gerar_makefile(questao)

        #antes de compilar limpa antigos executaveis
        os.system("make clean_exec -f " + path_mkfile)
#        print "Compilando: %s"%questao
        #compila usando makefile dos fontes
        command = "make -f " + path_mkfile
        output = os.system(command)
        #depois de compilar limpa os arquivos .o gerados
        os.system("make clean -f " + path_mkfile)

        return output

    def pre_executar(self,**kwargs):
        """Metodo chamado antes de se executar.
        Verifica se o caminho para o executavel existe e está correto.
        """
        from Avaliacao.Questao.models import path_execs, path_execs_gabarito
        questao = kwargs.get('questao',None)
        if questao is None:
            raise ExecutorException

        if self._is_questao(questao):
            path_exec = path_execs_gabarito(questao,settings.MEDIA_ROOT)
        else:
            path_exec = path_execs(questao,settings.MEDIA_ROOT)


        if not os.path.exists(path_exec):
            raise ExecutorException(u"Executavel não existente.")

        return

    def executar(self, **kwargs):
        """Metodo chamado quando se precisa executar um programa.
        Pede um argumento path_exec que é o caminho para o executavel.
        Futuramente pode ser passado nivel de proteção na execução.
        """

        from Avaliacao.Questao.models import path_execs, path_saidas, path_execs_gabarito, path_saidas_gabarito
        questao = kwargs.get('questao',None)
        if questao is None:
            raise ExecutorException

        entrada_gabarito = kwargs.get('entrada_gabarito',None)
        if entrada_gabarito is None:
            raise ExecutorException

#        path_entrada = questao.entradasGabarito.all()[0]
        if self._is_questao(questao):
            path_exec = path_execs_gabarito(questao,settings.MEDIA_ROOT)
            path_saida= path_saidas_gabarito(questao,settings.MEDIA_ROOT)
        else:
            path_exec = path_execs(questao,settings.MEDIA_ROOT)
            path_saida = path_saidas(questao,settings.MEDIA_ROOT)

        max_file_size = 1024 #1Mb

        safeexec_path = settings.SAFEEXEC_PATH

        #para rodar p executavel e por sua saida no local correto.
        #chama o executavel, passando uma entrada, e redirecionando a saida para um arquivo.
        command = "%(SAFEEXEC)s --fsize %(FILE_SIZE)s --exec %(EXEC)s < %(INPUT)s > %(OUTPUT)s"
        cmd_infos = {
                     'SAFEEXEC' : safeexec_path,
                     'FILE_SIZE': max_file_size,
                     'EXEC' : path_exec,
                     'INPUT':entrada_gabarito,
                     'OUTPUT': path_saida
                     }
        command = command % cmd_infos
        print "command", command


        output = os.system(command)


        return output

    def comparar(self, **kwargs):
        """Metodo chamado quando se precisa comparar o resultado com um gabarito
        """
        from Avaliacao.Questao.models import  path_saidas, path_saidas_gabarito

        questao = kwargs.get('questao',None)
        gabarito = kwargs.get('gabarito',None)
        if questao is None or gabarito is None:
            raise ComparadorException

        saida_gabarito= path_saidas_gabarito(gabarito,settings.MEDIA_ROOT)
        saida_questao= path_saidas(questao,settings.MEDIA_ROOT)

        #TODO:Alterar para usar o difflib
        command = "diff %s %s"%(saida_questao,saida_gabarito)
        #output = """"""+settings.MEDIA_ROOT
        #output = commands.getoutput(command)

        output = os.system(command)


        return output

    def avaliar(self, **kwargs):
        """Metodo chamado quando se precisa fazer alguma avaliacao alem da comparacao, no caso chama o metodo
        da classe pai que avalia outras coisas alem da programacao
        """
        return super(CorretorCPP, self).avaliar(**kwargs)


    def _criar_texto_mkfile(self,questao):
        """
        Gera o conteudo do makefile para utilizar todos os .cpp necessarios
        """

        from Avaliacao.Questao.models import path_execs, path_execs_gabarito, path_automaticas
        avaliacao = None
        aluno=None
        path_exec= ""
        print ">>>>type questao = %s"%(type(questao).__name__)
        if type(questao).__name__ is 'QuestaoDeAvaliacao':
            print ">>>>eh questao de avaliacao"
            fontes = [f for f in questao.fontes.all()]
            #depois de add os arquivos fontes da quetao de avaliacao
            #percorrer os fontes da questao e ver qual deles tem q ser usado tmb.
            for fontegabarito in questao.questao.fontesGabarito.filter(usarNaResolucao=True):
                fonte_temp = fontegabarito.copiar_para_questaoDeAvaliacao(questao)
                fontes.append(fonte_temp)
                print "fonte de gabarito>>> %s" % str(fontegabarito)
                print "fonte copiada>>> %s" % str(fonte_temp)
            avaliacao = questao.avaliacao
            aluno = avaliacao.aluno
            path_exec= path_execs(questao,settings.MEDIA_ROOT)
            questao=questao.questao
        elif type(questao).__name__ is 'Questao':
            fontes = questao.fontesGabarito.all()
            path_exec= path_execs_gabarito(questao,settings.MEDIA_ROOT)

        conteudo = "CC=g++\nCFLAGS=-c -Wall\nLDFLAGS=\nSOURCES="
        for fonte in fontes:
            conteudo += os.path.join(settings.MEDIA_ROOT, fonte.__str__()) + " "
        conteudo += "\nOBJECTS=$(SOURCES:.cpp=.o)\nEXECUTABLE="
        conteudo += path_exec
        conteudo += "\nall: $(SOURCES) $(EXECUTABLE)\n$(EXECUTABLE): $(OBJECTS)\n\t$(CC) $(LDFLAGS) $(OBJECTS) -o $@"
        conteudo += "\n.cpp.o:\n\t$(CC) $(CFLAGS) $< -o $@\nclean:\n\trm -rf "
        conteudo += path_automaticas(**{'tipo':'fontes','aluno':aluno,'avaliacao':avaliacao,'questao':questao,'filename':"*.o",'header':settings.MEDIA_ROOT})
        conteudo += "\nclean_exec:\n\trm -rf " + path_exec



        return conteudo

    def _is_questao(self,questao):
        if type(questao).__name__ is 'Questao':
            return True

        return False

    def gerar_makefile(self,questao):
        """
        Gera um makefile para os fontes necessarios e retorna o path para o arquivo gerado.
        """

        from Avaliacao.Questao.models import path_mkfiles_gabarito,path_mkfiles
        #se for a questao de um aluno
        if type(questao).__name__ is 'QuestaoDeAvaliacao':
            filepath = path_mkfiles(questao,settings.MEDIA_ROOT)
        #se for questao gera makefile no gabarito
        elif type(questao).__name__ is 'Questao':
            filepath = path_mkfiles_gabarito(questao,settings.MEDIA_ROOT)

        #abre o arquivo no caminho posto acima, escreve no arquivo e da close
        mkfile = open(filepath,'w')
        mkfile.write(self._criar_texto_mkfile(questao))
        mkfile.close()

        return filepath


    def _res_incorreta(self, ret):
        for res in ret:
            if res != 0 and res != None:
                return True
        return False
    def _corrigir_programacao(self,**kwargs):
        """Corrige apenas a parte de programação
        retorna a nota do aluno nessa parte.
        """

        questao = kwargs.get('questao',None)
        if questao is None:
            raise CorretorException(u"Não foi passado uma questao nos arqumentos.")

        gabarito = questao.questao


        #TODO:fazer algum criterio para seleção de entrada.
        import random
        rand_entrada_num = random.randint(0,gabarito.entradasGabarito.all().count()-1)
#        print rand_entrada_num
        entrada_gabarito=os.path.join(settings.MEDIA_ROOT,str(gabarito.entradasGabarito.all()[rand_entrada_num]))
#        saida_gabarito=os.path.join(settings.MEDIA_ROOT,str(questao.entradasGabarito.all()[0]))
        novo_dict = kwargs.copy()
        del novo_dict['questao']

        ret_compilar_gabarito = self.compilar_completo(questao=gabarito,**novo_dict)
        ret_executar_gabarito = self.executar_completo(questao=gabarito,entrada_gabarito=entrada_gabarito,**novo_dict)

        ret_compilar_questao = self.compilar_completo(questao=questao,**novo_dict)
        if self._res_incorreta(ret_compilar_questao):
            raise CompiladorException("Erro na compilação.")

        ret_executar_questao = self.executar_completo(questao=questao,entrada_gabarito=entrada_gabarito,**novo_dict)
        if self._res_incorreta(ret_executar_questao):
            raise ExecutorException("Erro na execução.")

        ret_comparar = self.comparar_completo(questao=questao,gabarito=gabarito)
        if self._res_incorreta(ret_comparar):
            raise ComparadorException("Saída incorreta.")


        return 1

    def _corrigir_multipla(self,**kwargs):
        "corrige apenas a parte de multipla escolha de uma questao"

        questao = kwargs.get('questao',None)
        if questao is None:
            raise CorretorException(u"Não foi passado uma questao nos arqumentos.")

        gabarito = questao.questao

        res_multipla = Decimal("0.0")
        for opcao in questao.opcoesMultiplaEscolha.all():
            res_multipla += opcao.correta/100

        #anula os acertos para um expecifico caso tenha marcado alguma opcao de anular
        #no caso pega apenas a que tem o menor valor caso exista
        anulada = questao.get_opcao_anuladora
        res_multipla= res_multipla if anulada == None else anulada.correta


        return res_multipla

    def _corrigir_discursiva(self,**kwargs):
        "corrige apenas a parte de discursiva de uma questao"

        questao = kwargs.get('questao',None)
        if questao is None:
            raise CorretorException(u"Não foi passado uma questao nos arqumentos.")

        gabarito = questao.questao

        res_disc = Decimal(comparar_strings(questao.respostaDiscursiva,gabarito.respostaDiscursiva))

        return res_disc

    def corrigir(self, **kwargs):
        """Metodo chamado para fazer a correçao.
        Este metodo chama os outros metodos necessarios para fazer a mesma, e usam uma questao e uma questao de avaliacao como parametros principais.
        Passasse uma questao de argumento(questao de avaliacao) e o resto é feito automaticamente.
        Se for passado o parametro limitar, o corretor corrige apenas o que o limitar(lista de strs) permite.
        O limitar pode ser:
                  - prog : Apenas a programação é corrigida.
                  - mult : Apenas resposta multipla escolha são corrigidas
                  - disc : Apenas resposta discursiva é corrigida.
                  por default se não passar o limite, considera tudo.
        """


        questao = kwargs.get('questao',None)
        if questao is None:
            raise CorretorException(u"Não foi passado uma questao nos arqumentos.")


        print "corrigir1>>>questao.retorno_correcao: %s" % questao.retorno_correcao
        gabarito = questao.questao

        #limite de o que deve ser corrigido
        limitar = kwargs.get('limitar',["prog","mult","disc"])

        #se o gabarito nao de programacao, entao n tenta corrigir isso.
        if not gabarito.is_programacao:
            try:
                limitar.remove("prog")
            except ValueError:
                pass
        nota = questao.nota
        prog_erro= None
        perc_prog=0
        perc_mult=0
        perc_disc=0

        if limitar.count('prog'):
            #lock de questao
            if questao.is_locked:
                raise LockException(u"Questão está sendo compilada.")
            else:
                questao.lock()

            try:
                perc_prog = self._corrigir_programacao(**kwargs)
            except Exception as e:
                prog_erro = e

        #verifica se é para corrigir as multiplas escolhas
        if limitar.count('mult'):
            perc_mult = self._corrigir_multipla(**kwargs)

        #verifica se é para corrigir a discursiva
        if limitar.count('disc'):
            perc_disc = self._corrigir_discursiva(**kwargs)

        nota = self.nota(questao=questao,prog=perc_prog,mult=perc_mult,disc=perc_disc)

        #tira a lock da questao, caso tenha sido posto anteriormente.
        questao.unlock()

        #levantar erro de programacao
        if prog_erro:
            raise prog_erro

        print "corrigir2>>>questao.retorno_correcao: %s" % questao.retorno_correcao
        return nota

    def nota(self,**kwargs):
        "salva e retorna uma nota(total) baseado no resultado da avaliacao."

        questao = kwargs.get('questao',None)
        if questao is None:
            raise CorretorException(msg="Não foi passado uma questao nos arqumentos.")
        #porcentagem dos acertos nas diversas areas: prog, mult, disc
        programacao = kwargs.get('prog',0)
        multipla = kwargs.get('mult',0)
        discursiva = kwargs.get('disc',0)

        nota_base = questao.filtro.notaBase
        nota_min = questao.filtro.notaLimMinimo
        nota_max = questao.filtro.notaLimMaximo

        perc_prog = questao.questao.percentNotaProgramacao
        perc_mult = questao.questao.percentNotaMultipla
        perc_disc = questao.questao.percentNotaDiscursiva

        nota_questao = 0

        nota_prog_base = nota_base * perc_prog/100
        #nota do aluno na parte de programacao
        nota_prog = nota_prog_base * programacao
        nota_questao+=nota_prog

        nota_mult_base = nota_base * perc_mult/100
        #nota do aluno na parte de multiplaescolha
        nota_mult = nota_mult_base * multipla
        nota_questao+=nota_mult

        nota_disc_base = nota_base * perc_disc/100
        #nota do aluno na parte de discursiva
        nota_disc = nota_disc_base * discursiva
        nota_questao+=nota_disc

        #aplica filtro de minimo e maximo.
        nota_questao = nota_min if nota_questao < nota_min else nota_questao
        nota_questao = nota_max if nota_questao > nota_max else nota_questao
        questao.nota=nota_questao
        questao.perc_prog=programacao
        questao.perc_mult=multipla
        questao.perc_disc=discursiva
        questao.save()

        return nota_questao
