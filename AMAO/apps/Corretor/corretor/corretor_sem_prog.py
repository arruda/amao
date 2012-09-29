# -*- coding: utf-8 -*-
import os
from django.conf import settings
from Corretor.base import Corretor, CompiladorException, ExecutorException,ComparadorException


class CorretorSemProg(Corretor):
    """Um corretor que apenas corrige a parte de questao discursiva e de multipla escolha.
    """

    def avaliar(self, **kwargs):
        """Metodo chamado quando se precisa fazer alguma avaliacao alem da comparacao
        no caso é feita uma verificacao na parte de discursiva e de multipla escolha da questao.
        """
        
        questao = kwargs.get('questao',None)
        if questao is None:
            raise CorretorException(msg="Não foi passado uma questao nos arqumentos.")

        gabarito = questao.questao
        
        #TODO:fazer uma formlua decente aki
        
        return 0
        

    def _is_questao(self,questao):
        if type(questao).__name__ is 'Questao':
            return True
        
        return False
    
    def corrigir(self, **kwargs):
        """Metodo chamado para fazer a correçao.
        Este metodo chama os outros metodos necessarios para fazer a mesma, e usam uma questao e uma questao de avaliacao como parametros principais.
        Passa-se uma questao de argumento(questao de avaliacao) e o resto é feito automaticamente.
        Ele retorna a nota final dessa questao, considerando já a nota da programacao e a nota de outros meios.
        """

        questao = kwargs.get('questao',None)
        if questao is None:
            raise CorretorException(msg="Não foi passado uma questao nos arqumentos.")

        gabarito = questao.questao
        #TODO:fazer algum criterio para seleção de entrada.
        import random
        rand_entrada_num = random.randint(0,gabarito.entradasGabarito.all().count()-1)
#        print rand_entrada_num
        entrada_gabarito=os.path.join(settings.MEDIA_ROOT,str(gabarito.entradasGabarito.all()[rand_entrada_num]))
#        saida_gabarito=os.path.join(settings.MEDIA_ROOT,str(questao.entradasGabarito.all()[0]))
        novo_dict = kwargs.copy()
        del novo_dict['questao']
        def res_incorreta(ret):
            for res in ret:
                if res != 0 and res != None:
                    return True
            return False

        ret_compilar_gabarito = self.compilar_completo(questao=gabarito,**novo_dict)
        ret_executar_gabarito = self.executar_completo(questao=gabarito,entrada_gabarito=entrada_gabarito,**novo_dict)   
        

        ret_compilar_questao = self.compilar_completo(questao=questao,**novo_dict)
        if res_incorreta(ret_compilar_questao):
            raise CompiladorException("Erro na compilação.")      
  
        ret_executar_questao = self.executar_completo(questao=questao,entrada_gabarito=entrada_gabarito,**novo_dict)
        if res_incorreta(ret_executar_questao):
            raise ExecutorException("Erro na execução.")

        ret_comparar = self.comparar_completo(questao=questao,gabarito=gabarito)
        if res_incorreta(ret_comparar):
            raise ComparadorException("Saída incorreta.")


        return True
