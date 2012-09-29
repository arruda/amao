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

        ####MONTANDO ESTRUTURA             
        recorrenciaDeQuestoes = {}
        #prepara vetor que possui as questoes possiveis para cada filtro
        opcoesDeQuestoesDeFiltro = {}
        for fQuestao in self.filtrosQuestoes.all():
            opcoesDeQuestoesDeFiltro[fQuestao.pk]=fQuestao.filtrarQuestao()
            
        for idFiltro in opcoesDeQuestoesDeFiltro:
            for questao in opcoesDeQuestoesDeFiltro[idFiltro]:                
                if not recorrenciaDeQuestoes.has_key(questao.id):
                    recorrenciaDeQuestoes[questao.id] = []
                recorrenciaDeQuestoes[questao.id].append(idFiltro)
        ####TERMINANDO DE MONTAR ESTRUTURA
        numQuestoesNecessarias= self.filtrosQuestoes.all().count()

        while numQuestoesNecessarias < 0:      
            arrayDosMenores =[]
            menor=None
            #prepara o array com as questoes que tem menor numero de recorrencia
            #isso eh, menor numero de filtro de questoes que possui ela como opcao
            for key, value in recorrenciaDeQuestoes.items:
                if not menor:
                    arrayDosMenores.append(key)
                    menor=value.__len__()
                else:
                    if value.__len__() == menor:
                        arrayDosMenores.append(key)
                    elif value.__len__() <= menor:
                        arrayDosMenores = [key,]
                        
            #randomiza uma das questoes que tem menor recorrencia
            import random       
            rand = random.randint(0, arrayDosMenores.__len__()-1)
            idQuestaoEscolhida = arrayDosMenores[rand] 
            vetorDeFiltrosDaQuestaoEscolhida = recorrenciaDeQuestoes[idQuestaoEscolhida]
            
            arrayDosMenores =[]
            menor=None
            #prepara o array com os filtros de questao que possuem a questao escolhida 
            #que tem o menor numero de opcao de questao vinculadas a este
            for filtro in vetorDeFiltrosDaQuestaoEscolhida:
                if not menor:
                    arrayDosMenores.append(filtro)
                    menor=filtro.__len__()
                else:
                    if filtro.__len__() == menor:
                        arrayDosMenores.append(filtro)
                    elif filtro.__len__() <= menor:
                        arrayDosMenores = [filtro,]
           
            #randomiza o filtro dentro os que possuem o menor numero de questoes
            #do vetor de filtros da questao escolhidas            
            rand = random.randint(0, arrayDosMenores.__len__()-1)
            filtroDeQuestaoEscolhida = arrayDosMenores[rand]  
            
            #cria uma questao nessa avaliacao com o filtro escolhido
            novaAvaliacao.add_questao(questao,filtroDeQuestaoEscolhida)   
            #remove             

        #agora que é garantido que tds as questoes estao corretas
        #comeca a salvar cada uma delas na avaliacao           
        for questao,filtro in questoes:                 
            novaAvaliacao.add_questao(questao,filtro)      
#            from Avaliacao.Questao.models import QuestaoDeAvaliacao
#            #Cria uma instancia de QuestaoDeAvaliacao para essa questao e essa novaAvaliacao
#            questaoAvaliacao = QuestaoDeAvaliacao(avaliacao=novaAvaliacao,questao=questao)
#            #salva essa questaoAvaliacao
#            questaoAvaliacao.save()
               
               
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
