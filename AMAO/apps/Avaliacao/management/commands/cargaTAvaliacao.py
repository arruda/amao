from django.core.management.base import BaseCommand, CommandError
from Avaliacao.models import *
from Avaliacao.Questao.models import TipoQuestao, Questao, FiltroQuestao
import random       

def criarFiltroQuestao(templAv,rangeFiltro,rangeTipo):
    tiposQuestoe = TipoQuestao.objects.all()
    questoes = Questao.objects.all()
    #vai criar de 1-rgq filtros.
    #isso eh de 1-rgq questoes aleatorias nesse templAv
    for i in range(rangeFiltro):        
        fq = FiltroQuestao(templateAvaliacao=templAv)
        fq.save()
        #utiliza uma questao randomica como base para a questao que sera gerada por esse filtro.
        randQuestao = questoes[random.randint(0, questoes.__len__()-1)]
        
        #1/3 de chance de ser uma questao expecifica
        if random.randint(1,3) == 3 :                
            fq.questaoExata = randQuestao
            fq.save()            
        #caso nao seja uma questao expecifica, cria filtros para gerar ao menos a questao randomica.o    
        else:                   
            for tipo in randQuestao.tipo.all():
                fq.tipo.add(tipo)
                
            fq.save()
            

def cargaTesteTemplateAvaliacao(rangeTemplate=6,rangeFiltro=10,rangeTipo=4): 
    #inclui templateAvaliacao de rg1-rg2.
    for i in range(rangeTemplate):
        ta = TemplateAvaliacao(titulo="Template de Avaliacao %d" %i)
        
        ta.save()
        criarFiltroQuestao(ta,rangeFiltro,rangeTipo)
                     
        

class Command(BaseCommand):
    args = '<rangeTemplate rangeFiltro rangeTipo>'
    help = 'Inicia o bd com dados relativos ao aplicativo de Avaliacao(Teste)'

    def handle(self, *args, **options):
        self.stdout.write('Carga de Teste da App(Avaliacao) iniciada.\n')
        
        try:
            x = args[2]
            cargaTesteTemplateAvaliacao(int(args[0]),int(args[1]), int(args[2]))
        except IndexError:
            self.stderr.write('Usando valores padroes\n')
            cargaTesteTemplateAvaliacao()
        
            
        self.stdout.write('Dados de teste da App Avaliacao carregados com sucesso\n')
        
