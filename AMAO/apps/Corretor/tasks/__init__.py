#coding: utf-8

import os
from celery.decorators import task
from django.conf import settings

from Corretor.base import CorretorException

from Corretor.base import CompiladorException
from Corretor.chamada_sistema import ChamadaSistema

@task
def run_corretor(*args,**kwargs):
    """roda o corretor usando uma task do celery

        Isso tem que ser feito, já que colocando o metodo 'corrigir' decorado como uma @task não adianta.
        O problema é que ao chamar corretor.corrigir(...) ele pede pela instancia(o 'self'), que de alguma forma fica perdido quando se marca
        com esse decorator. Assim teria que chamar: corretor.corrigir(corretor,...) o que é um tanto quanto estranho, e pode causar mais problemas
        para frente.
        Sendo assim acho que o mais adeguado é fazer essa funcao que deixa isso encapsulado e pode ser executado sem problemas.
    """
    corretor = kwargs['corretor']
    ret = None
    ret = corretor.corrigir(*args,**kwargs)
    return ret


@task
def run_corretor_validar_gabarito(*args,**kwargs):
    """roda o corretor usando uma task do celery para validar uma questao gabarito

    Este método verifica se a questao gabarito passada no parametro é valida para o corretor, isto é:
    - É capaz de compilar
    - Possui entrada
    - Executa sem problema com a entrada.

    Caso o gabarito seja valido ele retorna True.
    """
    # print ">>>run_corretor_validar_gabarito"

    def res_incorreta(ret):
        for res in ret:
            if isinstance(res,ChamadaSistema):
                res = res.returncode

            if res != 0 and res != None:
                return True
        return False

    corretor = kwargs['corretor']
    gabarito = kwargs['questao']

    verificada = False
    erroException = None
    try:
        ret_compilar_gabarito = corretor.compilar_completo(questao=gabarito)
        #se houver erro na compilação ja para aqui e levanta exception explicando qual foi o problema.
        if res_incorreta(ret_compilar_gabarito):
            raise CompiladorException("Erro na compilação: %s" % ret_compilar_gabarito[1].output)

        entrada_gabarito=os.path.join(settings.MEDIA_ROOT,str(gabarito.get_rand_entrada()))
        ret_executar_gabarito = corretor.executar_completo(questao=gabarito,entrada_gabarito=entrada_gabarito)

        if not res_incorreta(ret_executar_gabarito):
            verificada = True

    except CorretorException,e:
        # self.verificada = False
        erroException=e
        # print ">>>CorretorException"

    finally:
        # print ">>>fim"
        gabarito_new = gabarito.__class__.objects.get(pk=gabarito.pk)
        gabarito_new.verificada= verificada
        # print ">>>f1"
        retorno_correcao = gabarito_new.get_retorno_or_create
        # print ">>>retorno_correcao",retorno_correcao
        # print ">>>retorno_correcao.pk",retorno_correcao.pk
        retorno_correcao.altera_dados(sucesso=verificada,erroException=erroException)
        retorno_correcao.save()
        gabarito_new.save(verificar=False)



class MyException(Exception):
    pass


class Teste(object):

    @task()
    def add(self,x, y):
        if x == y:
            raise MyException("FUUUU")
        return x + y

    @task()
    def add2(self,**kwargs):
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        if x == y:
            raise MyException("FUUUU")
        return x + y
