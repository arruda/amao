#coding: utf-8

import os
from celery.decorators import task
from django.conf import settings

from Corretor.base import CorretorException

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
    return corretor.corrigir(*args,**kwargs)


@task
def run_corretor_validar_gabarito(*args,**kwargs):
    """roda o corretor usando uma task do celery para validar uma questao gabarito

    Este método verifica se a questao gabarito passada no parametro é valida para o corretor, isto é:
    - É capaz de compilar
    - Possui entrada
    - Executa sem problema com a entrada.

    Caso o gabarito seja valido ele retorna True.
    """

    def res_incorreta(ret):
        for res in ret:
            if res != 0 and res != None:
                return True
        return False
    corretor = kwargs['corretor']
    gabarito = kwargs['questao']
    verificada = False
    try:
        ret_compilar_gabarito = corretor.compilar_completo(questao=gabarito)
        entrada_gabarito=os.path.join(settings.MEDIA_ROOT,str(gabarito.get_rand_entrada()))
        ret_executar_gabarito = corretor.executar_completo(questao=gabarito,entrada_gabarito=entrada_gabarito)
        if not res_incorreta(ret_compilar_gabarito) and not res_incorreta(ret_executar_gabarito):
            verificada = True

    except CorretorException:
        # self.verificada = False
        pass

    finally:
        gabarito_new = gabarito.__class__.objects.get(pk=gabarito.pk)
        gabarito_new.verificada= verificada
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
