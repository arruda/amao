#coding: utf-8

from celery.decorators import task

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