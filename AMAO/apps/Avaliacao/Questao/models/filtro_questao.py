# -*- coding: utf-8 -*-

from django.db import models    
from tipo_questao import TipoQuestao
from questao import Questao
from libs.uniqifiers_benchmark import f11 as uniqifier

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
    
    def gerarQuestao(self, questoesAnteriores,simulado):
        """
        Retorna uma questao utilizando criterios de busca baseado no campo 'tipo', ou retorna questaoExata se esta for != None
        Passando como parametro uma lista de questoes previamente selecionadas, para evitar a selecao de uma destas.
        se for uma questão exata e simulado=True então nao pega a propria questão mas uma qualquer que seja do mesmo tipo que esta.
        """
        from django.db.models import Q
        #: se não for um simulado, e se tiver questão exata, retorna a mesma, caso contrario, tenta recuperar uma questão aleatoria
        if self.questaoExata and not simulado:
            print "(EXATA) " + self.questaoExata.slug
            return self.questaoExata
             
        #: se tiver uma questão exata quer e está aqui quer dizer q esse é um simulado, e os tipos devem ser iguais aos tipos
        #: da questão exata.
        if self.questaoExata:
            tipos = self.questaoExata.tipo.all()
        else:            
            #recupera queryset de questoes que tem TipoQuestao pertencendo a lista de TipoQuestao desse filtrosQuestoes.?
            tipos = self.tipo.all()
            
        #utiliza apenas questoes verificadas
        query = Questao.objects.filter(verificada=True)
        
        for tipo in tipos:
#                print tipo.id
            #inclui tmb os tipos filho, isso para o caso em
            #que o filtro tem um tipo A(pai de B), isso é, uma generalizacao
            #sendo assim Qualquer questao com A ou B devem poder ser buscadas.
#            for tipoFilho in tipo.get_descendants():
#                pass
                
            query = query.filter(tipo = tipo)
            
           
#        tipos = uniqifier(tipos)
        questoes = []
        for questao in query.select_related('tipo').distinct():
            ok = True
            if questoesAnteriores != None:
                for q_anterior, f_anterior in questoesAnteriores:
                    if questao == q_anterior or self == f_anterior:
                        ok = False
               
            for tipo in questao.tipo.all():
                if tipo not in tipos:
                    #fazer recursao
                    ok = False
                    break
            if ok:
                questoes.append(questao)

        #se nao tiver nenhuma questao na lista entao retorna None
        if questoes.__len__() == 0:
        
            return None
           
        #randamiza uma dessas questoes para ser a resposta.
        import random       
        rand = random.randint(0, questoes.__len__()-1)
        questao = questoes[rand]
        print str(rand) + " " + questao.slug

        return questao
        



   #Ver qual o unicode que vou por para esse model 
   # def __unicode__(self):
   #     return self.arquivo.name
