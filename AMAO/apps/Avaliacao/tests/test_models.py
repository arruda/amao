# -*- coding: utf-8 -*-
"""
    Avaliacao.test_models
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao modelo.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""
import datetime
from django.test import TestCase
from model_mommy import mommy
from Avaliacao.models import Avaliacao, TemplateAvaliacao
from Materia.Turma.models import Turma
from Avaliacao.Questao.models import TipoQuestao, FiltroQuestao

from Aluno.models import Aluno

class AvaliacaoTest(TestCase):


    def setUp(self):
        self.avaliacao = mommy.make_one(Avaliacao)


    def test_avaliacao_save(self):
        " verifica se consegue salvar um avaliacao "
        self.avaliacao.save()

        self.assertEqual(self.avaliacao.id, 1)

class TemplateAvaliacaoTest(TestCase):

    fixtures = ['test_alunos']

    def setUp(self):
        self.aluno = Aluno.objects.get(pk=1)
        self.turma = mommy.make_one(Turma,nome="Teste",sigla="tst")
        self.gerar_tipoQuestao()
        self.gerar_Questoes()

    def gerar_tipoQuestao(self):
        "gera tipos de questao que sao denominados tipo1-10"
        from Avaliacao.Questao.models import TipoQuestao
        for i in xrange(1,11):
            tipo = TipoQuestao(tipo="tipo%s"%str(i))
            tipo.save()
#            print "tipo %s"%str(tipo.id)

    def gerar_Questoes(self):
        """gera questões mocked com tipo variando
        """
        from Avaliacao.Questao.models import Questao
        for i in xrange(1,21):
            #:basicamente quando i=1 -> mod = 1; i = 10 -> mod = 10; i = 11 -> mod = 1; i=20 -> mod = 10
            mod = i%10 if i != 10 and i != 20 else 10
            #:retorna basicamente tipos de questao que tem PK < i(nunca ultrapassando 10)
            tipos = TipoQuestao.objects.filter(pk__lte=mod)
            questao = mommy.make_one(Questao,tipo=tipos,titulo="questao%s"%str(i))
            #forcando verificada, ja que estas questoes sao mocks e nao seriam verificadas automaticamente.
            #por que se fossem iriam dar erro no arquivo fonte.
            questao.verificada=True
            questao.save(verificar=False)
            print "q=%s i=%s mod=%s"%(questao.id,i,mod)
#            questao.save()

    def test_fixtures(self):
        "testar as fixtures carregaram corretamente"
        self.assertEquals(Aluno.objects.get(pk=1).slug,'123456')


    def gerarFiltroQuestao(self,num_tipos,template):
        """gera filtros de questao para um determinado template,
        considerando que vai pegar todos os tipos que tem pk <= num_tipos"""
        tipos = TipoQuestao.objects.filter(pk__lte=num_tipos)
        filtro = mommy.make_one(FiltroQuestao,templateAvaliacao=template,questaoExata=None,tipo=tipos)
        return filtro
#        for tipo in filtro.tipo.all():
#            print "tipo %s"%str(tipo.id)
#        print "="

    # def test_gerarAvaliacao_templateAvaliacao(self):
    #     " verifica se consegue gerarAvaliacao por templateAvaliacao "
    #     self.templateAvaliacao = TemplateAvaliacao(titulo="Avaliacao Teste",turma=self.turma,ativa=True)
    #     self.templateAvaliacao.data_inicio = datetime.datetime.now()
    #     self.templateAvaliacao.data_termino = datetime.datetime.now() + datetime.timedelta(hours=2)
    #     self.templateAvaliacao.save()
    #     for i in xrange(1,11):
    #         self.gerarFiltroQuestao(i,self.templateAvaliacao)
    #     avaliacao = self.templateAvaliacao.gerarAvaliacao(self.aluno)
    #     self.assertEqual(avaliacao.titulo,self.templateAvaliacao.titulo)
    #     import pdb; pdb.set_trace()

    #     for i in xrange(0,10):
    #         questao = avaliacao.questoes.all()[i]
    #         self.assertIn(questao.questao.id,[i+1,i+11])

    def test_list_templatesAvaliacao_aluno(self):
        " verifica se o metodo list_templatesAvaliacao_aluno retorna todos os templates corretamente "

        templates_list_espected= []
        for turma_num in xrange(1,3):
            turma = mommy.make_one(Turma,nome="Teste%s"%str(turma_num),sigla="tst%s"%str(turma_num))
            if turma_num == 1:
                turma.alunos.add(self.aluno)

            for template_num in xrange(1,3):
                templateAvaliacao = TemplateAvaliacao(titulo="Avaliacao Teste %s"%str(template_num),turma=turma,ativa=True)
                templateAvaliacao.data_inicio = datetime.datetime.now()
                templateAvaliacao.data_termino = datetime.datetime.now() + datetime.timedelta(hours=2)
                templateAvaliacao.save()
                for filtro in xrange(1,11):
                    self.gerarFiltroQuestao(filtro,templateAvaliacao)

                if turma_num == 1 and template_num != 1:
                    templates_list_espected.append(templateAvaliacao)

                if template_num == 1:
                    templateAvaliacao.gerarAvaliacao(self.aluno)

        templates_list = TemplateAvaliacao.objects.list_templatesAvaliacao_aluno(self.aluno)
        print "lista"
        print templates_list
        for template in templates_list:
            self.assertIn(template,templates_list_espected)

        for template in templates_list_espected:
            self.assertIn(template,templates_list)

    # def test_gerar_simulado(self):
    #     " verifica se ao gerar um avaliacão para um aluno ele faz corretamente, como filtros,  questoes exatas e etc..."
    #     from Avaliacao.Questao.models import Questao
    #     #prepara a avaliacao
    #     self.templateAvaliacao = TemplateAvaliacao(titulo="Avaliacao Teste Criacao",turma=self.turma,ativa=False)
    #     self.templateAvaliacao.data_inicio = datetime.datetime.now() + datetime.timedelta(hours=3)
    #     self.templateAvaliacao.data_termino = datetime.datetime.now() + datetime.timedelta(hours=5)
    #     self.templateAvaliacao.save()
    #     #prepara os filtros
    #     for i in xrange(1,11):
    #         filtro = self.gerarFiltroQuestao(i,self.templateAvaliacao)
    #         #se for o 5 filtro prepara para testar o caso da questao exata
    #         if i == 5:
    #             #coloca o filtro 5 como sendo a questao de id 4
    #             filtro.questaoExata = Questao.objects.get(pk=4)
    #             filtro.save()
    #             print "filtro %s" %(filtro.questaoExata)

    #     print ">>gerar simulado"
    #     #gera a avaliacao pra um aluno(nesse caso um simulado)
    #     avaliacao = self.templateAvaliacao.gerarAvaliacao(self.aluno,True)
    #     #verifica se a avaliacao tem o mesmo titulo que o templateAvaliacao
    #     self.assertEqual(avaliacao.titulo,self.templateAvaliacao.titulo)
    #     #verifica se as questões foram selecionadas corretamente

    #     #sendo que se a 4º questao for a questao de id =4, então obrigatoriamente a 5º questão(a que era exata) devera ser "randomizada" como sendo
    #     #a unica que falta, a questão de id 14, se ela nao for a 4 então deve ser exatamente o oposto, e se nao for isso entao é um erro!
    #     quarta_questao = avaliacao.questoes.all()[3].questao
    #     quinta_questao = avaliacao.questoes.all()[4].questao
    #     msg_erro="a questao exata nao foi gerada corretamente no simulador %d - %d"

    #     self.assertFalse(quarta_questao.id==quinta_questao.id,"%d -%d"%(quarta_questao.id,quinta_questao.id))
    #     if quarta_questao.id == 4:
    #         self.assertEqual(quinta_questao.id,14,msg_erro%(quinta_questao.id,14))
    #     elif quarta_questao.id == 14:
    #         self.assertEqual(quinta_questao.id,4,msg_erro%(quinta_questao.id,4))
    #     else:
    #         self.fail(u"a quarta questao não foi nem 4 nem 14, e isso ta errado.")


    # def test_gerar_avaliacao(self):
    #     " verifica se ao gerar um simulado para um aluno ele faz corretamente, trocando questoes exatas e etc..."
    #     from Avaliacao.Questao.models import Questao
    #     #prepara a avaliacao
    #     self.templateAvaliacao = TemplateAvaliacao(titulo="Avaliacao Teste simulado",turma=self.turma,ativa=False)
    #     self.templateAvaliacao.data_inicio = datetime.datetime.now() + datetime.timedelta(hours=3)
    #     self.templateAvaliacao.data_termino = datetime.datetime.now() + datetime.timedelta(hours=5)
    #     self.templateAvaliacao.save()
    #     #prepara os filtros
    #     for i in xrange(1,11):
    #         filtro = self.gerarFiltroQuestao(i,self.templateAvaliacao)
    #         #se for o 5 filtro prepara para testar o caso da questao exata
    #         if i == 5:
    #             #coloca o filtro 5 como sendo a questao de id 4
    #             filtro.questaoExata = Questao.objects.get(pk=4)
    #             filtro.save()
    #             print "filtro %s" %(filtro.questaoExata)

    #     print ">>gerar simulado"
    #     #gera a avaliacao pra um aluno(nesse caso um simulado)
    #     avaliacao = self.templateAvaliacao.gerarAvaliacao(self.aluno,True)
    #     #verifica se a avaliacao tem o mesmo titulo que o templateAvaliacao
    #     self.assertEqual(avaliacao.titulo,self.templateAvaliacao.titulo)
    #     #verifica se as questões foram selecionadas corretamente

    #     #sendo que se a 4º questao for a questao de id =4, então obrigatoriamente a 5º questão(a que era exata) devera ser "randomizada" como sendo
    #     #a unica que falta, a questão de id 14, se ela nao for a 4 então deve ser exatamente o oposto, e se nao for isso entao é um erro!
    #     quarta_questao = avaliacao.questoes.all()[3].questao
    #     quinta_questao = avaliacao.questoes.all()[4].questao
    #     msg_erro="a questao exata nao foi gerada corretamente no simulador %d - %d"

    #     self.assertFalse(quarta_questao.id==quinta_questao.id,"%d -%d"%(quarta_questao.id,quinta_questao.id))
    #     if quarta_questao.id == 4:
    #         self.assertEqual(quinta_questao.id,14,msg_erro%(quinta_questao.id,14))
    #     elif quarta_questao.id == 14:
    #         self.assertEqual(quinta_questao.id,4,msg_erro%(quinta_questao.id,4))
    #     else:
    #         self.fail(u"a quarta questao não foi nem 4 nem 14, e isso ta errado.")

class GerarAvaliacaoTest(TestCase):

    fixtures = ['test_alunos']

    def setUp(self):
        self.aluno = Aluno.objects.get(pk=1)
        self.turma = mommy.make_one(Turma,nome="Teste",sigla="tst")
        self.gerar_tipoQuestao()
        self.gerar_Questoes()
        self.gerarTemplate()

    def gerar_tipoQuestao(self):
        "gera tipos de questao que sao denominados tipo1-10, com 3 filhos cada(nomeados tipoX-1-tipoX-3)"
        from Avaliacao.Questao.models import TipoQuestao
        for i in xrange(1,11):
            tipo = TipoQuestao(tipo="tipo%s"%str(i))
            tipo.save()
            for j in xrange(1,4):
                tipo_filho = TipoQuestao(tipo="tipo%s-%s" % (i,j), tipoPai=tipo)
                tipo_filho.save()
#            print "tipo %s"%str(tipo.id)

    def gerar_Questoes(self):
        """gera questoes mocked com tipo variando
        """
        import random

        from Avaliacao.Questao.models import Questao
        for i in xrange(1,31):
            #:basicamente quando i=1 -> mod = 1; i = 10 -> mod = 10; i = 11 -> mod = 1; i=20 -> mod = 10
            mod =  i%10
            if mod == 0:
                mod = 10

            #:retorna basicamente tipos de questao que tem PK < i(nunca ultrapassando 10)

            tipos_pai = TipoQuestao.objects.filter( tipo__in = ["tipo%s"%str(j) for j in xrange(1,mod+1)] )
            tipos_escolhidos = []
            for tipo_pai in tipos_pai:
                tipos_filho_e_proprio=tipo_pai.get_descendants(include_self=True)
                rand_tipo = random.randint(0, tipos_filho_e_proprio.__len__()-1)
                tipos_escolhidos.append( tipos_filho_e_proprio[rand_tipo] )

            questao = mommy.make_one(Questao,tipo=tipos_escolhidos,titulo="questao%s"%str(i))
            #forcando verificada, ja que estas questoes sao mocks e nao seriam verificadas automaticamente.
            #por que se fossem iriam dar erro no arquivo fonte.
            questao.verificada=True
            questao.save(verificar=False)
            print "q=%s i=%s mod=%s"%(questao.id,i,mod)
#            questao.save()


    def gerarFiltroQuestaoParaTemplate(self,num_tipos,template):
        """gera filtros de questao para um determinado template,
        considerando que vai pegar todos os tipos que tem pk <= num_tipos"""
        tipos_pai = TipoQuestao.objects.filter( tipo__in = ["tipo%s"%str(j) for j in xrange(1,num_tipos+1)] )
        #tipos = TipoQuestao.objects.filter(pk__lte=num_tipos)
        filtro = mommy.make_one(FiltroQuestao,templateAvaliacao=template,questaoExata=None,tipo=tipos_pai)
        return filtro

    def gerarTemplate(self):
        "gera um template com filtro coerentes"
        from Avaliacao.Questao.models import Questao
        #prepara a avaliacao
        self.templateAvaliacao = TemplateAvaliacao(titulo="Avaliacao Teste Filtros",turma=self.turma,ativa=True)
        self.templateAvaliacao.data_inicio = datetime.datetime.now() - datetime.timedelta(hours=3)
        self.templateAvaliacao.data_termino = datetime.datetime.now() + datetime.timedelta(hours=5)
        self.templateAvaliacao.save()
        #prepara os filtros
        #são 10 questões na avaliação
        for num_tipos in xrange(1,11):
            filtro = self.gerarFiltroQuestaoParaTemplate(num_tipos,self.templateAvaliacao)
            #se for o 5 filtro prepara para testar o caso da questao exata
            if num_tipos == 5:
                #coloca o filtro 5 como sendo a questao de id 4
                filtro.questaoExata = Questao.objects.get(pk=1)
                filtro.save()
                print "filtro %s" %(filtro.questaoExata)

    def test_fixtures(self):
        "testar as fixtures carregaram corretamente"
        self.assertEquals(Aluno.objects.get(pk=1).slug,'123456')

    def test_filtrarQuestao(self):
        "testar se um filtroQuestao(pk=6) retorna corretamente as questoes possiveis"

        for num_id in xrange(1,11):
            filtro = FiltroQuestao.objects.get(pk=num_id)
            lista_ids_questoes=[]
            for i in xrange(num_id,11):
                lista_ids_questoes.append(i)
                lista_ids_questoes.append(i+10)
                lista_ids_questoes.append(i+20)

            if num_id == 5:
                lista_ids_questoes= [1]

            print "lista_ids_questoes>> %s" % str(lista_ids_questoes)

            questoes_selecionadas = filtro.filtrarQuestao()
            msg_erro="Questao de pk:%s nao esta dentro da lista que questoes possiveis do filtro de pk:%s"
            for questao in questoes_selecionadas:
                self.assertIn(questao.pk, lista_ids_questoes, msg_erro%(questao.pk,num_id))

    def test_gerarAvaliacao(self):
        "testa se a avaliacao foi gerada corretamente"
        avaliacao = self.templateAvaliacao.gerarAvaliacao(self.aluno)

        #verifica se a avaliacao tem o mesmo titulo que o templateAvaliacao
        self.assertEqual(avaliacao.titulo,self.templateAvaliacao.titulo)
        msg_error="Questao de Avaliacao: %s nao esta presente na lista de questoes possiveis para o filtro:%s"
        questoes_selecionadas = []
        #verifica se as questões foram selecionadas corretamente
        for i in xrange(0,10):
            questaoAvaliacao = avaliacao.questoes.all()[i]
            filtroCorrespondente = questaoAvaliacao.filtro
            print ">>>> I :%d" % i
            self.assertNotIn(questaoAvaliacao.questao, questoes_selecionadas)
            self.assertIn(questaoAvaliacao.questao,filtroCorrespondente.filtrarQuestao())

            questoes_selecionadas.append(questaoAvaliacao.questao)




class GerarAvaliacaoCasoA1Test(TestCase):
    """
    fazendo isso basado no caso A1 descrito na documentacao
    Basicamente:
    q1 -> C, Facil
    q2 -> C, Facil
    q3 -> C.malloc, Facil
    q4 -> C++, Facil
    q5 -> C,C++, c.malloc, Facil



    Avaliação ->
    1 -> q1
    2 -> C, Facil
    3 -> Facil, C.Malloc


    Resultado esperado ->
    1 -> q1
    2 -> C, Facil (q2, q5)
    3 -> Facil, C.Malloc (q3, q5)


    Resultado ->
    1 -> Facil, C.Malloc
    2 -> C, Facil
    3 -> q5 ou q1(aleatoriamente)
    """
    fixtures = ['test_alunos']

    def setUp(self):
        self.aluno = Aluno.objects.get(pk=1)
        self.turma = mommy.make_one(Turma,nome="Teste",sigla="tst")
        self.gerar_tipoQuestao()
        self.gerar_Questoes()
        self.gerarTemplate()

    def gerar_tipoQuestao(self):
        "gera tipos de questao que sao denominados tipo1-10, com 3 filhos cada(nomeados tipoX-1-tipoX-3)"
        from Avaliacao.Questao.models import TipoQuestao

        tipo_C = TipoQuestao(tipo="C")
        tipo_C.save()

        tipo_C_Malloc = TipoQuestao(tipo="Malloc", tipoPai=tipo_C)
        tipo_C_Malloc.save()

        tipo_CPP = TipoQuestao(tipo="CPP")
        tipo_CPP.save()

        tipo_Facil = TipoQuestao(tipo="Facil")
        tipo_Facil.save()


    def gerar_Questoes(self):
        """gera questoes mocked com tipo variando
        """
        import random


        from Avaliacao.Questao.models import Questao
        tipos=[]
        #q1 -> C, Facil
        tipos = TipoQuestao.objects.filter(tipo__in = ["C", "Facil"] )
        q1 = mommy.make_one(Questao,tipo=tipos,titulo="questao1")
        q1.verificada=True
        q1.save(verificar=False)

        #q2 -> C, Facil
        tipos = TipoQuestao.objects.filter(tipo__in = ["C", "Facil"] )
        q2 = mommy.make_one(Questao,tipo=tipos,titulo="questao2")
        q2.verificada=True
        q2.save(verificar=False)

        #q3 -> C.malloc, Facil
        tipos = TipoQuestao.objects.filter(tipo__in = ["Malloc", "Facil"] )
        q3 = mommy.make_one(Questao,tipo=tipos,titulo="questao3")
        q3.verificada=True
        q3.save(verificar=False)

        #q4 -> C++, Facil
        tipos = TipoQuestao.objects.filter(tipo__in = ["CPP", "Facil"] )
        q4 = mommy.make_one(Questao,tipo=tipos,titulo="questao4")
        q4.verificada=True
        q4.save(verificar=False)

        #q5 -> C,C++, c.malloc, Facil
        tipos = TipoQuestao.objects.filter(tipo__in = ["C","Malloc","CPP", "Facil"] )
        q5 = mommy.make_one(Questao,tipo=tipos,titulo="questao5")
        q5.verificada=True
        q5.save(verificar=False)



    def gerarTemplate(self):
        "gera um template com filtro coerentes"
        from Avaliacao.Questao.models import Questao

#    Avaliação ->
#    1 -> q1
#    2 -> C, Facil
#    3 -> Facil, C.Malloc
        #prepara a avaliacao
        self.templateAvaliacao = TemplateAvaliacao(titulo="Avaliacao Teste Filtros",turma=self.turma,ativa=True)
        self.templateAvaliacao.data_inicio = datetime.datetime.now() - datetime.timedelta(hours=3)
        self.templateAvaliacao.data_termino = datetime.datetime.now() + datetime.timedelta(hours=5)
        self.templateAvaliacao.save()
        #prepara os filtros
        #são 3 questoes na avaliacao

        tipos = TipoQuestao.objects.filter(tipo__in = ["C", "Facil"] )
        fq1 = mommy.make_one(FiltroQuestao,templateAvaliacao=self.templateAvaliacao,questaoExata=Questao.objects.get(pk=1),tipo=tipos)
        fq1.save()

        tipos = TipoQuestao.objects.filter(tipo__in = ["C", "Facil"] )
        fq2 = mommy.make_one(FiltroQuestao,templateAvaliacao=self.templateAvaliacao,questaoExata=None,tipo=tipos)
        fq2.save()

        tipos = TipoQuestao.objects.filter(tipo__in = ["Facil","Malloc"] )
        fq3 = mommy.make_one(FiltroQuestao,templateAvaliacao=self.templateAvaliacao,questaoExata=None,tipo=tipos)
        fq3.save()


    def test_fixtures(self):
        "testar as fixtures carregaram corretamente"
        self.assertEquals(Aluno.objects.get(pk=1).slug,'123456')

    def test_filtrarQuestao(self):
        "testar se um filtroQuestao(pk=6) retorna corretamente as questoes possiveis"
        msg_erro="Questao de pk:%s nao esta dentro da lista que questoes possiveis do filtro de pk:%s"

        fq1 = FiltroQuestao.objects.get(pk=1)
        questoes_selecionadas1 = fq1.filtrarQuestao()

        for questao in questoes_selecionadas1:
            self.assertEquals([questao.pk,], [1,], msg_erro%(questao.pk,fq1.pk))

        fq2 = FiltroQuestao.objects.get(pk=2)
        questoes_selecionadas2 = fq2.filtrarQuestao()
        num_questoes = questoes_selecionadas2.__len__()
        self.assertEquals(num_questoes , 4, "filtro 2 nao teve numero correto de questoes. Esperava: %s mas veio %s" % (4, num_questoes))
        for questao in questoes_selecionadas2:
            questoes_ids = [1,2,3,5]
            self.assertIn(questao.pk, questoes_ids , msg_erro%(questao.pk,fq2.pk))

        fq3 = FiltroQuestao.objects.get(pk=3)
        questoes_selecionadas3 = fq3.filtrarQuestao()

        num_questoes = questoes_selecionadas3.__len__()
        self.assertEquals(num_questoes , 2, "filtro 3 nao teve numero correto de questoes. Esperava: %s mas veio %s" % (2, num_questoes))
        for questao in questoes_selecionadas3:
            questoes_ids = [3,5]
            self.assertIn(questao.pk, questoes_ids , msg_erro%(questao.pk,fq3.pk))





    def test_gerarAvaliacao(self):
        "testa se a avaliacao foi gerada corretamente"

#    Resultado esperado ->
#    1 -> q1
#    2 -> C, Facil (q2, q5)
#    3 -> Facil, C.Malloc (q3, q5)
#
        avaliacao = self.templateAvaliacao.gerarAvaliacao(self.aluno)

        #verifica se a avaliacao tem o mesmo titulo que o templateAvaliacao
        self.assertEqual(avaliacao.titulo,self.templateAvaliacao.titulo)
        msg_error="Questao de Avaliacao: %s nao esta presente na lista de questoes possiveis para o filtro:%s"

        possiveis_q1 = [1,]
        possiveis_q2 = [2,3,5]
        possiveis_q3 = [3,5]

        q1 = avaliacao.questoes.all()[0]
        self.assertIn(q1.questao.pk, possiveis_q1, msg_error % (q1, 1 ))

        q2 = avaliacao.questoes.all()[1]
        self.assertIn(q2.questao.pk, possiveis_q2, msg_error % (q2, 2 ))

        q3 = avaliacao.questoes.all()[2]
        self.assertIn(q3.questao.pk, possiveis_q3, msg_error % (q3, 3 ))

        self.assertFalse(q1.questao.pk == q2.questao.pk)
        self.assertFalse(q2.questao.pk == q3.questao.pk)
        self.assertFalse(q1.questao.pk == q3.questao.pk)
        print "q1: %s" % (q1,)
        print "q2: %s" % (q2,)
        print "q3: %s" % (q3,)












