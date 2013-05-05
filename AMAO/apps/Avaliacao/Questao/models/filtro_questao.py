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
    def _prepara_tipos_requeridos(self):
        """
        Metodo usado por filtrarQuestao.

        prepara os tipos requeridos, juntando n elementos de num_descendentes cada um dos tipos

        retorna um vetor com um vetor de listas de todos os tipos e seus descententes

        Ex:

        Tipos:
            * C -> Ponteiro -> Malloc
            * Facil
            * Estruturas de Dados -> Pilha

        Isso resultaria no seguinte vetor:

            [[C,Ponteiro,Malloc], [Facil,], [Estruturas de Dados, Pilha]]


        """
        tiposRequeridos = []
        for tipoFiltro in self.tipo.all():
            listaTiposFilho_e_proprio = tipoFiltro.get_descendants(include_self=True)
            tiposRequeridos.append(listaTiposFilho_e_proprio)
        return tiposRequeridos

    def _questoes_selecionadas(self,tiposRequeridos):
        """
        Recupera todas as questoes selecionadas usando os filtros(sem serem exatas)
        dos tiposRequeridos.



        """
        #recupera todas as questoes
        tdsQuestoes = Questao.objects.filter(verificada=True)
        questoesSelecionadas = []

        for questaoATestar in tdsQuestoes:

            questao_valida = True
            for grupoDeTiposRequeridos in tiposRequeridos:

                tipo_valido = False
                for tipoQuestao_da_questaoATestar in questaoATestar.tipo.all():

                    if tipoQuestao_da_questaoATestar in grupoDeTiposRequeridos:
                        tipo_valido=True
                        break

                if not tipo_valido:
                    questao_valida = False
                    break

            if questao_valida:
                questoesSelecionadas.append(questaoATestar)
        return questoesSelecionadas

    def filtrarQuestao(self):
        """
        Retorna uma questao utilizando criterios de busca baseado no campo 'tipo', ou retorna questaoExata se esta for != None
        Passando como parametro uma lista de questoes previamente selecionadas, para evitar a selecao de uma destas.
        se for uma questão exata e simulado=True então nao pega a propria questão mas uma qualquer que seja do mesmo tipo que esta.
        """

        ######################
        #: se tiver questão exata, retorna a mesma(uma lista com apenas ela)
        #caso contrario, tenta recuperar uma questão aleatoria, seguindo os tipos do filtro
        if self.questaoExata:
#            print "(EXATA) " + self.questaoExata.slug
            return [self.questaoExata,]

        #prepara os tipos requeridos, juntando n elementos de num_descendentes cada um dos tipos
        tiposRequeridos = self._prepara_tipos_requeridos()
#        print "===================================="
#        print ">>>tiposFiltro:"
#        print self.tipo.all()
#        print ">>>tiposRequeridos:"
#        print tiposRequeridos
#        print ">>>>>>>>>>>>>>>>>>>"
        questoesSelecionadas = self._questoes_selecionadas(tiposRequeridos)


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
