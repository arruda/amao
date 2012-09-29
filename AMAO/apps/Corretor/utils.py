#coding: utf-8

from django.conf import settings
import difflib

def verify_corretores():
    "Retorna true se todos os corretoes estiverem oks, e joga exceção caso contrario"    
    for nome, desc, classe in settings.CORRETORES:
        try:
            _get_class(classe)
        except:
            #raise
            return False

def _get_class(path):
    "Retorna uma classe dado um caminho para ela, usando reflections"
    class_name = path.split('.')[-1]
    mod_name = path[:-1*(class_name.__len__()+1)]
    mod =  __import__(mod_name, fromlist=[class_name])
    return getattr(mod, class_name)

def get_corretor(path):
    """Retorna um corretor dado o seu caminho.
    """
    return _get_class(path)

def get_corretores():
    """Retorna todos os corretores do settings.
    """
    corretores = [[i,n,d,get_corretor(c)] for i,n,d,c in settings.CORRETORES]
    return corretores

def get_corretor_por_id(id_corretor):
    for corretor in get_corretores():
        if corretor[0] == id_corretor:
            return corretor[3]

    return None


def get_corretor_choices():
    choices = ()
    for corretor in get_corretores():
        choices = ((corretor[0],corretor[1],corretor[3].__name__),) + choices
    return choices

def comparar_strings(txt1,txt2,isjunk=None):
    "compara duas strings dando o grau de similaridade delas"
    if not txt1 or not txt2:
        return 0
    return difflib.SequenceMatcher(isjunk,txt1,txt2).ratio()


#( 0, 'aguardando',  u'Aguardando Pagamento'),
#        ( 1, 'pago',        u'Pago'),
#        ( 2, 'produzindo',  u'Aguardando Produção'),
#        ( 3, 'enviando',    u'Aguardando Envio'),    
#        ( 4, 'enviado',     u'Enviado'),

#CORRETORES = (
##    ('nome','app.corretor.classe'),
#    ('C','Corretor.corretor.CorretorC'),
#)
