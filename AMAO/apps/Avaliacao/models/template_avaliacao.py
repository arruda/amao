# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from abs_models import Abs_titulado
#from Materia.models import Materia

#from avaliacao import Avaliacao

class TemplateAvaliacaoQuerySet(QuerySet):
    """Query set for TemplateAvaliacao
    """
    def list_templatesAvaliacao_aluno(self,aluno):   
        """Retorna uma lista de templates de avaliacao para esse aluno que ainda nao foram comecadas
        """
        template_avaliacoes_comecadas = (av.templateAvaliacao_id for av in aluno.avaliacoes.all().exclude(simulado=True))
#        print template_avaliacoes_comecadas
#        print aluno.turmas.all()
        return self.filter(turma__pk__in=aluno.turmas.all(),ativa=True).exclude(id__in=template_avaliacoes_comecadas)
        
    def list_templatesAvaliacaoFuturas_aluno(self,aluno):   
        """Retorna uma lista de templates de avaliacao que ainda estão para acontecer para esse aluno
        """
        template_avaliacoes_comecadas = (av.templateAvaliacao_id for av in aluno.avaliacoes.all().exclude(simulado=True))
#        print template_avaliacoes_comecadas
#        print aluno.turmas.all()
        return self.filter(turma__pk__in=aluno.turmas.all(),data_inicio__gt=datetime.datetime.now()).exclude(id__in=template_avaliacoes_comecadas)


class TemplateAvaliacao(Abs_titulado):
    """
    Classe responsavel por gerar uma avaliacao com base em determinados filtros e atributos.
    """
    turma = models.ForeignKey('Turma.Turma', related_name="templateAvaliacoes")
    ativa = models.BooleanField(u"Ativa",default=False)
    data_inicio = models.DateTimeField(u"Data de Inicio")
    data_termino = models.DateTimeField(u"Data de Termino")
    
    #:o autor(usuario) dessa questao
    autor = models.ForeignKey('auth.User',blank=True,null=True, related_name='templateAvaliacoes_autor')
    
    permite_simulado = models.BooleanField(u"Permitir Simulado?")
    
        
    def gerarAvaliacao(self,aluno,simulado=False):
        """
        Essa funcao gera uma avaliação automaticamente para um aluno em particular, populando a avaliacao
        com questoes aleatorias(seguindo certas regras) ou questoes expecificas(se assim forem definidas no filtroQuestao).
        é o mesmo método usado para gerar uma simulação, mas nesse caso as questões especificas são trocadas, e no lugar delas é pego
        qualquer outra questão que tenha os mesmos tipos de questão que elas.
        """
        from Avaliacao.Questao.models import FiltroQuestao
        #cria uma avaliacao/simulado para esse aluno ligada a esse templateAvaliacao
        data_inicio = self.data_inicio
        data_termino=self.data_termino
        if simulado:
            data_inicio = datetime.datetime.now()
            tempo_duracao = self.data_termino - self.data_inicio
            data_termino =  data_inicio + tempo_duracao
            #se a data de termino do simulado for posterior a data de termino desse template, 
            #entao coloca a data de termino como sendo a data de inicio do template
            data_termino = data_termino if data_termino < self.data_inicio else self.data_inicio
            
          
        novaAvaliacao =\
        self.avaliacoes.create(titulo=self.titulo,aluno=aluno,simulado=simulado,data_inicio=data_inicio,data_termino=data_termino)

        ####RETIRANDO AS QUESTOES QUE SAO EXATAS
        filtros_questoes_exatas = self.filtrosQuestoes.exclude(questaoExata=None)
        
        questoes_exatas = [f.filtrarQuestao()[0] for f in filtros_questoes_exatas ]
        
        ####SALVANDO logo as questoes exatas
        for i in xrange(0,filtros_questoes_exatas.count()):
            novaAvaliacao.add_questao(questoes_exatas[i],filtros_questoes_exatas[i].pk)  
        
        ###### FAZENDO O RESTO DAS QUESTOES ALEATORIAS
        filtros_restantes = self.filtrosQuestoes.filter(questaoExata=None)
        
        ####MONTANDO ESTRUTURA             
        recorrenciaDeQuestoes = {}
        #prepara vetor que possui as questoes possiveis para cada filtro
        opcoesDeQuestoesDeFiltro = {}
        for fQuestao in filtros_restantes.all():
            opcoes_para_filtro = fQuestao.filtrarQuestao()
            #removendo questoes exatas
            for questao_exata in questoes_exatas:
                try:
                    opcoes_para_filtro.remove(questao_exata)
                except ValueError:
                    pass
            
            opcoesDeQuestoesDeFiltro[fQuestao.pk]=opcoes_para_filtro
            
        for idFiltro in opcoesDeQuestoesDeFiltro:
            for questao in opcoesDeQuestoesDeFiltro[idFiltro]:                
                if not recorrenciaDeQuestoes.has_key(questao.id):
                    recorrenciaDeQuestoes[questao.id] = []
                recorrenciaDeQuestoes[questao.id].append(idFiltro)
        ####TERMINANDO DE MONTAR ESTRUTURA
        numQuestoesNecessarias= filtros_restantes.all().count()
        
        print "\n\n\n\n\n==================================================\n\n\n\n\n"
        print "numQuestoesNecessarias>>>%s" % str(numQuestoesNecessarias)
        while numQuestoesNecessarias > 0:      
            print "====\nNova questao"
            #array das questões que tem o menor_num_filtros numero de filtros em que ela se encaixa
            arrayDosMenores =[]
            
            #quantidade de filtros da questão que possui a menor_num_filtros quantidade de filtros
            menor_num_filtros=None
            
            #prepara o array com as questoes que tem menor_num_filtros numero de recorrencia
            #isso eh, menor_num_filtros numero de filtro de questoes que possui ela como opcao
            for idQuestao, listIdFiltro in recorrenciaDeQuestoes.items():
                quantidade_filtros = listIdFiltro.__len__()
                
#                print ">> idQuestao>>>%s" % str(idQuestao) 
#                print ">> listIdFiltro>>>%s" % str(listIdFiltro)     
                if not menor_num_filtros:
                    arrayDosMenores.append(idQuestao)
                    menor_num_filtros= quantidade_filtros
                else:
                    if quantidade_filtros == menor_num_filtros:
                        arrayDosMenores.append(idQuestao)
                    elif quantidade_filtros < menor_num_filtros:
                        arrayDosMenores = [idQuestao,]
                        menor_num_filtros = quantidade_filtros
                        
            print "arrayDosMenores>>>%s" % str(arrayDosMenores)            
            #randomiza uma das questoes que tem menor_num_filtros recorrencia
            import random       
            rand_id_questao = random.randint(0, arrayDosMenores.__len__()-1)
            idQuestaoEscolhida = arrayDosMenores[rand_id_questao] 
            vetorDeIdFiltrosDaQuestaoEscolhida = recorrenciaDeQuestoes[idQuestaoEscolhida]
            print "idQuestaoEscolhida>>>%s" % str(idQuestaoEscolhida)         
            
            arrayDosMenoresIdFiltrosDaQuestaoEscolhida =[]
            menor_num_questoes_do_filtro=None
            #prepara o array com os filtros de questao que possuem a questao escolhida 
            #que tem o menor_num_filtros numero de opcao de questao vinculadas a este
            for idFiltro in vetorDeIdFiltrosDaQuestaoEscolhida:
                num_questoes = opcoesDeQuestoesDeFiltro[idFiltro].__len__()
#                num_questoes = filtro.__len__()
                
                if not menor_num_questoes_do_filtro:
                    arrayDosMenoresIdFiltrosDaQuestaoEscolhida.append(idFiltro)
                    menor_num_questoes_do_filtro=num_questoes
                    
                else:
                    if num_questoes == menor_num_questoes_do_filtro:
                        arrayDosMenoresIdFiltrosDaQuestaoEscolhida.append(idFiltro)
                    elif num_questoes < menor_num_questoes_do_filtro:
                        arrayDosMenoresIdFiltrosDaQuestaoEscolhida = [idFiltro,]
                        menor_num_questoes_do_filtro = num_questoes
                        
            print "arrayDosMenoresIdFiltrosDaQuestaoEscolhida>>>%s" % str(arrayDosMenoresIdFiltrosDaQuestaoEscolhida)         
            
            #randomiza o filtro dentro os que possuem o 'menor_num_questoes_do_filtro' 
            #do vetor de filtros da questao escolhidas            
            rand_id_filtro = random.randint(0, arrayDosMenoresIdFiltrosDaQuestaoEscolhida.__len__()-1)
            idFiltroDeQuestaoEscolhida = arrayDosMenoresIdFiltrosDaQuestaoEscolhida[rand_id_filtro]  
            
            #cria uma questao nessa avaliacao com o filtro escolhido
            novaAvaliacao.add_questao(idQuestaoEscolhida,idFiltroDeQuestaoEscolhida)   
            recorrenciaDeQuestoes.pop(idQuestaoEscolhida)
            #menos uma questão para criar
            numQuestoesNecessarias = numQuestoesNecessarias -1

               
        return novaAvaliacao        
        
    def verifica_aluno(self,aluno):
        "verifica se o aluno em questao pode fazer essa avaliacao"
#        print aluno.turmas.all()
#        print "a"
#        print self.turma
#        print "b"
        return (self.turma in aluno.turmas.all() and self.ativa==True) 
    
    def verifica_simulado_aluno(self,aluno):
        "verifica se o aluno em questao pode fazer um simulado dessa avaliacao"
        return self.permite_simulado and self.data_inicio > datetime.datetime.now() and self.turma in aluno.turmas.all()
       
    def verifica_professor(self,professor):
        "verifica se o professor em questao pode ter acesso a essa avaliacao"
        return self.turma.professor.pk == professor.pk    
    
    def verifica_monitor(self,monitor):
        "verifica se o monitor em questao pode ter acesso a essa avaliacao"
        return self.turma.materia == monitor.materia   
    
    
    objects = PassThroughManager(TemplateAvaliacaoQuerySet)

    class Meta:
        verbose_name = u'Avaliação de Turma'
        app_label = 'Avaliacao'

    
    @property
    def terminada(self):
        """retorna true se a mesma ja tiver passado do tempo para ser feita a questao,
        false caso contrario"""
        return self.data_termino < datetime.datetime.now()
    
    @property
    def get_nota_minima(self):
        """retorna a nota minima que pode ser tirada nessa avaliacao,
        percorrendo os filtros e somando os limites de notas minimas"""
        
        min = 0
        for filtro in self.filtrosQuestoes.all():
            min += filtro.notaLimMinimo
        return min
    
    @property
    def get_nota_maxima(self):
        """retorna a nota maxima que pode ser tirada nessa avaliacao,
        percorrendo os filtros e somando os limites de notas maximas"""
        
        max = 0
        for filtro in self.filtrosQuestoes.all():
            max += filtro.notaLimMaximo
        return max
    
    def terminar(self):
        """termina uma avaliacao, consequentemente terminando todas as avaliacoes
            ligadas a ela.
        """
            
        self.ativa=False
        self.save()
        for avaliacao in self.avaliacoes.filter(ativa=True):
            avaliacao.terminar()
    
    @property
    def simulados(self):
        "retorna todos os simulados desse templateAvaliacao" 
        from Avaliacao.models import Simulado
        return Simulado.objects.filter(templateAvaliacao=self)
