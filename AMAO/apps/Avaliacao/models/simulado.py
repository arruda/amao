# -*- coding: utf-8 -*-
"""
    apps.Avaliacao.models.simulado
    ~~~~~~~~~~~~~~

   models referentes a um simulado.

    :copyright: (c)  02/05/2012  by arruda.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

# -*- coding: utf-8 -*-
import datetime
from django.db import models
from avaliacao import Avaliacao


class SimuladoManager(models.Manager):
    """
    Um Manager que retorna basicamente as avaliacoes que tem o campo simulado=True como sendo um simulado
    """
    def get_query_set(self):
        return super(SimuladoManager, self).get_query_set().filter(simulado=True)
    
class Simulado(Avaliacao):
    """
    Representa um simulado de um aluno.
    lembrando que um aluno pode ter mais de um simulado para o mesmo templateAvaliacao,
    o que nao pode é ter mais de um simulado desses ativos(ocorrendo ao mesmo tempo).
    Pode também ter mais de um simulado para diferentes templatesAvaliacao.
    """
    #:alterando o manager default de simulado para recuperar apenas simulados
    objects = SimuladoManager()
    
    def __init__(self, *args, **kwargs):        
        "todo simulado tem a informacao de simulado = True"
        super(Simulado, self).__init__(*args, **kwargs)        
        self.simulado = True
        
    class Meta:
        proxy = True
        verbose_name = u'Simulado'
        app_label = 'Avaliacao'
        
    @classmethod
    def get_or_create(cls,templateAvaliacao,aluno):
        """recupera um simulado se ja houver(evitando ter mais de um simulado ao mesmo tempo
            para o mesmo templateAvaliacao para o mesmo aluno que esteja ativo, se nao houver então cria e retorna o mesmo.
        """
        #verifica se ja existe um simulado para esse aluno nesse template que ainda esteja ativo.
        try:
            #se existir pega a mesma
            avaliacao = cls.objects.get(templateAvaliacao=templateAvaliacao,aluno=aluno,simulado=True,ativa=True)
        except cls.DoesNotExist:
            #caso nao exista cria uma 
            avaliacao = templateAvaliacao.gerarAvaliacao(aluno,simulado=True)

        return avaliacao