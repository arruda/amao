#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django import template
register = template.Library()

@register.simple_tag
def get_nota_multipla(questaoAvaliacao, opcao):
    """"Retorna a nota que uma opcao multipla escolha tem em uma determinada questao de avaliacao
    """
    return opcao.get_nota(questaoAvaliacao.nota)