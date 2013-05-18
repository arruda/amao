# -*- coding: utf-8 -*-

from django import forms

from django.contrib.auth.models import User
from model_utils import Choices

from Avaliacao.Questao.models import TipoQuestao, Questao

class FiltroQuestaoForm(forms.Form):
    "filtro de parametros para questoes"

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(FiltroQuestaoForm, self).__init__(*args, **kwargs)

        self.fields['tipos'] = forms.ModelMultipleChoiceField(
                                                       label=u'Tipos de Questão',
                                                       queryset=TipoQuestao.objects.all(),
                                                       required=False)


    def _get_questoes_tipo(self,questoes,tipos_requridos):
        "retorna questoes que batem com os tipos requeridos"
        tdsQuestoes = questoes
        questoesSelecionadas = []
        for questaoATestar in tdsQuestoes:

            questao_valida = True
            for grupoDeTiposRequeridos in tipos_requridos:

                tipo_valido = False
                for tipoQuestao_da_questaoATestar in questaoATestar.tipo.all():

                    if tipoQuestao_da_questaoATestar in grupoDeTiposRequeridos:
                        tipo_valido=True
                        break

                if not tipo_valido:
                    questao_valida = False
                    break

            if questao_valida:
                questoesSelecionadas.append(questaoATestar)
        return questoesSelecionadas

    def get_questoes(self):
        "retorna as questoes com base nos filtros desse formulario"

        questoes = Questao.objects.all()

        # author = self.cleaned_data.get('author',None)
        # if author:
        #     books = books.filter(author=author)

        tipos = self.cleaned_data.get('tipos',None)
        tipos_requeridos = []
        for tipo in tipos:
            listaTiposFilho_e_proprio = tipo.get_descendants(include_self=True)
            tipos_requeridos.append(listaTiposFilho_e_proprio)

        if tipos:
            questoes = self._get_questoes_tipo(questoes,tipos_requeridos)

        # search = self.cleaned_data.get('search', None)
        # if search:
        #     books = books.filter(name__icontains=search)
        return questoes
