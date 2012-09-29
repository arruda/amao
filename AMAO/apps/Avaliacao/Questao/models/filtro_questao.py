# -*- coding: utf-8 -*-

from django.db import models    
from tipo_questao import TipoQuestao
from questao import Questao
#from libs.uniqifiers_benchmark import f11 as uniqifier

class FiltroQuestao(models.Model):
    """
    Classe que ira gerar uma questao(QuestaoDeAvaliacao) com base em alguns criterios/filtros(TipoQuestao).
    """
    
    #vou fazer que um filtro de questao pode ser usado apenas num template de Avaliacao por vez, acho q fica mais
    #logico a ideia.
    templateAvaliacao = models.ForeignKey('Avaliacao.TemplateAvaliacao', related_name='filtrosQuestoes')   
    
    #representa a nota que o aluno receberá se conseguir 100% da questão
    notaBase = models.DecimalField(u"Nota Base",max_digits=10, decimal_places=2,default="0.00")
    #representa o limite inferior que a nota dessa questao pode chegar.
    notaLimMinimo = models.DecimalField(u"Limite Mínimo da Nota",max_digits=10, decimal_places=2,default="0.00")
    #representa o limite superior que a nota dessa questao pode chegar.
    notaLimMaximo = models.DecimalField(u"Limite Máximo da Nota",max_digits=10, decimal_places=2,default="0.00")
    
    #tipo que da questao, usado para filtragem
    tipo = models.ManyToManyField(TipoQuestao, related_name="filtrosQuestoes")        
    
    #caso seja de uma questao expecifica.
    questaoExata = models.ForeignKey(Questao, related_name='filtrosQuestoes', blank=True, null=True,limit_choices_to = {'verificada':True})   
    
    class Meta:
        verbose_name = u'Filtro de Questão'
        app_label = 'Questao'
    
    def verifica_autor(self,autor):
        "verifica se um dado autor(usuario) corresponde ao autor do templateAvaliacao desse filtro"
        return self.templateAvaliacao.autor.pk == autor.pk
    
    def filtrarQuestao(self):
        """
        Retorna uma questao utilizando criterios de busca baseado no campo 'tipo', ou retorna questaoExata se esta for != None
        Passando como parametro uma lista de questoes previamente selecionadas, para evitar a selecao de uma destas.
        se for uma questão exata e simulado=True então nao pega a propria questão mas uma qualquer que seja do mesmo tipo que esta.
        """
                     
        ######################
        #: se tiver questão exata, retorna a mesma, caso contrario, tenta recuperar uma questão aleatoria
        if self.questaoExata:
            print "(EXATA) " + self.questaoExata.slug
            return self.questaoExata
        
        #prepara os tipos requeridos, juntando n elementos de num_descendentes cada um dos tipos
        tiposRequeridos = []
        for tipoFiltro in self.tipo.all():            
            listaTiposFilho = tipoFiltro.get_descendants(include_self=True)
            tiposRequeridos.append(listaTiposFilho)   
        print "===================================="
        print ">>>tiposFiltro:"
        print self.tipo.all()
        print ">>>tiposRequeridos:"
        print tiposRequeridos
        print ">>>>>>>>>>>>>>>>>>>"
        #recupera todas as questoes
        tdsQuestoes = Questao.objects.filter(verificada=True)
        if questoesAnteriores != []:
            tdsQuestoes = tdsQuestoes.exclude(questoesAnteriores)

        questoesSelecionadas = []

        for questaoATestar in tdsQuestoes:
            numTiposRequeridos = tiposRequeridos.__len__()
            for tipoQuestao in questaoATestar.tipo.all():
                for grupoDeTiposRequeridos in tiposRequeridos:
                    if tipoQuestao in grupoDeTiposRequeridos:
                        numTiposRequeridos-=1
                        break
                if numTiposRequeridos == 0:
                    questoesSelecionadas.append(questaoATestar)
                    break
        
        print ">>>questoesSelecionadas:"
        for q in questoesSelecionadas:
            print "%s - [%s]" %(q,q.tipo.all())
        print ">>>>>>>>>>>>>>>>>>>"
                       
        if questoesSelecionadas == []:
            raise Exception("Nenhuma questao encontrada para os seguintes filtro:%s"%str(self.pk))
#        #randamiza uma dessas questoes para ser a resposta.
#        import random       
#        rand = random.randint(0, questoesSelecionadas.__len__()-1)
#        questao = questoesSelecionadas[rand]
#        print str(rand) + " " + questao.slug
 
        return questoesSelecionadas
        
        



   #Ver qual o unicode que vou por para esse model 
   # def __unicode__(self):
   #     return self.arquivo.name
