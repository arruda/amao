# -*- coding: utf-8 -*-

from os.path import join as joinPath, exists as existisPath , basename
from os import remove
from django.db import models    
from django.conf import settings
from path_utils import path_helper

class Lockable(models.Model):
    """Um modelo abstrato que possui informações sobre como lidar com locks para a correção
    """
    
    class Meta:
        abstract = True
        
    @property
    def is_locked(self):
        """retorna True se houver um arquivo .lock dentro da pasta fontes da questao
        Se nao houver a pasta da questao, ou se dentro dela nao tiver o arquivo então retorna False
        """
        return existisPath(self.get_lock_path)
    
    @property
    def get_lock_path(self):
        "retorna a path para o arquivo de lock dessa questao"
        if hasattr(self,'avaliacao'):
            dct = {'questao':self.questao,
                    'avaliacao':self.avaliacao,
                    'aluno':self.avaliacao.aluno,
                    }
        else:
            dct = {'questao':self}
        #obriga a criar o diretorio caso esse nao exista.
        dct['criar']=True
        dct['header']=settings.MEDIA_ROOT
            
        return joinPath(path_helper('fontes',**dct),".lock")
    
    def lock(self):
        "faz com que essa questao fique locked"
        lock = open(self.get_lock_path,'w')
        lock.close()
        
    def unlock(self):
        "faz com que essa questao fique sem ser locked"
        if existisPath(self.get_lock_path):
            remove(self.get_lock_path)