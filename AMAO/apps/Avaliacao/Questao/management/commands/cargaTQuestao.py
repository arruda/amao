from django.core.management.base import BaseCommand, CommandError
from Avaliacao.Questao.models import *
import random       

def cargaTesteTipoQuestao(rg1=4,rg2=2,rrg=10):
    #inclui tipo questoes rg1-rg2.
    for i in range(rg1):
        tq = TipoQuestao(tipo="Tipo %d" %i)
        tq.save()
            
        for j in range(rg2):
            tq2 = TipoQuestao(tipo=("Tipo %d " %i)+str(j), tipoPai=tq)
            tq2.save()
    
    
    #inclui tipo questoes com pais aleatorios (rrg)
    tiposQuestoe = TipoQuestao.objects.all()
    for i in range(rrg):
        randTipoQuestao = random.randint(0, tiposQuestoe.__len__()-1)
        tq = tiposQuestoe[randTipoQuestao]    
        tq2 = TipoQuestao(tipo=("Tipo (rand) %d - " %i )+str(tq.id), tipoPai=tq)
        tq2.save()
        
    
def cargaTesteQuestao(rg=150,rrg=3):
    tiposQuestoe = TipoQuestao.objects.all()
    
    for i in range(rg):         
        q = Questao(titulo="Questao com titulo %d" % i)
        q.enunciado = "Enunciado da Questao %d" % i        
        q.save()        
        #cada questao tem de 1 a 5 tipos de questao.
        randnumTQs = random.randint(1, rrg)
        for j in range(randnumTQs):            
            randTipoQuestao = random.randint(0, tiposQuestoe.__len__()-1)
            tq = tiposQuestoe[randTipoQuestao]                     
            q.tipo.add(tq)
        q.save()
            #print "questao "+str(i) + "/ tp "+tq.tipo
            
        

class Command(BaseCommand):
    args = '<TQRange1 TQRange2 TQRRange QRange QRRange>'
    help = 'Inicia o bd com dados relativos ao aplicativo de Questao(Teste)'

    def handle(self, *args, **options):
        
        self.stdout.write('Carga de Teste da App(Questao) iniciada.\n')
        try:
            x = args[4]
            cargaTesteTipoQuestao(int(args[0]),int(args[1]), int(args[2]))
            cargaTesteQuestao(int(args[3]),int(args[4]))
        except IndexError:
            self.stderr.write('Usando valores padroes\n')
            cargaTesteTipoQuestao()
            cargaTesteQuestao()
        
            
        self.stdout.write('Dados de teste da App Questao carregados com sucesso\n')
        
