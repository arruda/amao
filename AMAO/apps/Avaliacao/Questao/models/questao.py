# -*- coding: utf-8 -*-

from decimal import Decimal
from django.db import models
from django.conf import settings

from django_extensions.db.fields import AutoSlugField
from model_utils import Choices
from abs_models import Abs_titulado_slugfy
from Corretor.utils import get_corretor_choices, get_corretor_por_id
from Corretor.base import CorretorException
from Corretor.models import RetornoCorrecao
from Corretor.tasks import run_corretor_validar_gabarito
from tipo_questao import TipoQuestao
from lockable import Lockable



class Questao(Abs_titulado_slugfy,Lockable):
    """
    Representa uma Questao, isso é um problema que esta ligado a uma avaliacao que esta por sua vez ligada
    a um aluno.
    """

    CORRETORES = Choices(*get_corretor_choices())
#    CORRETORES = Choices((0,'base','Base'))

    enunciado = models.TextField(u"Enunciado")
    respostaDiscursiva = models.TextField(u"Resposta Discursiva",blank=True, null=True)
    #:Representa o percentual que a programacao tem nessa questao.
    percentNotaProgramacao = models.DecimalField(u"Percentual da Nota de Programação",max_digits=10, decimal_places=2,default=Decimal("100"))
    #:Representa o percentual que a multipla escolha tem nessa questao.
    percentNotaMultipla = models.DecimalField(u"Percentual da Nota das Multiplas Escolhas",max_digits=10, decimal_places=2,default=Decimal("0"))
    #:Representa o percentual que a discursiva tem nessa questao.
    percentNotaDiscursiva = models.DecimalField(u"Percentual da Nota da Discursiva",max_digits=10, decimal_places=2,default=Decimal("0"))

    #:indica se uma questão está pronta ou não para ser usada num template avaliacao.
    verificada = models.BooleanField(u"Verificada",default=False)

    #:o autor(usuario) dessa questao
    autor = models.ForeignKey('auth.User',blank=True,null=True, related_name='questoes_autor')


    id_corretor = models.SmallIntegerField(u"Corretor",choices=CORRETORES)#, default=CORRETORES.c)


    #tipo que da questao, usado para filtragem
    tipo = models.ManyToManyField(TipoQuestao, related_name="questoes")

    retorno_correcao = models.ForeignKey('Corretor.RetornoCorrecao',blank=True,null=True, on_delete=models.SET_NULL)
    @property
    def corretor(self):
        "recupera um corretor dado o id_corretor"
        return get_corretor_por_id(self.id_corretor)


    class Meta:
        verbose_name = u'Questão'
        app_label = 'Questao'

    def __unicode__(self):
        return self.slug

    def get_rand_entrada(self):
        "retorna uma entrada randomica"
        import random
        count = self.entradasGabarito.all().count()
        rand_entrada_num = 0
        if count >= 1:
            rand_entrada_num = random.randint(0,count -1)
            return self.entradasGabarito.all()[rand_entrada_num]
        else:
            return None
#        print rand_entrada_num

    def verificar_questao(self):
        """verifica se uma questão esta pronta para ser usada em uma avaliacao
            Ou seja, pode ser compilada e executada.
        """
        #se nao for uma questao com programacao nao faz essa verificacao
        if not self.percentNotaProgramacao > 0:
             self.verificada=True
             return

        corretor = self.corretor()

        retorno = self.get_retorno_or_create
        self.save(verificar=False)
        corretor_task = run_corretor_validar_gabarito.delay(corretor=corretor,questao=self)
        retorno = retorno.__class__.objects.get(pk=retorno.pk)
        retorno.task_id = corretor_task.task_id
        retorno.save()

    @property
    def is_programacao(self):
        "retorna true se essa for uma questao de programação"
        return self.percentNotaProgramacao > Decimal("0")


    @property
    def get_retorno_or_create(self):
        retorno = self.retorno_correcao
        if not self.retorno_correcao:
            retorno = RetornoCorrecao()
            retorno.save()
            self.retorno_correcao = retorno

        return retorno

    def save(self, *args, **kwargs):
        #Antes de salvar deve verificar se a questão é propria para ser usada em uma avaliacao
        #ou seja, da para compilar e executar sem erro.
        verificar = kwargs.get('verificar',True)
        if self.slug != "" and self.slug != None and verificar == True:
            self.verificar_questao()


        try:
            kwargs.pop('verificar')
        except KeyError:
            pass

        super(Questao, self).save(*args, **kwargs)



