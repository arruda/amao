#coding: utf-8

import subprocess

class ChamadaSistema(object):
    """
    Representa uma chamada ao sistema, e deixa encapsulado tudo o necessário para realiza-la
    """

    def __init__(self,cmd):
        self.cmd = cmd
        self.output = ""
        self.returncode = 0


    def executar(self):
        """
        Executa o comando e seta os dados de output e returncode para os do comando executados.
        Retorna esses dados tambem, caso necessario.
        """

        #por defaul o codigo de retorno é 0, que significa que rodou com exito
        #caso de algum erro, o retorno será alterado para o que o comando retornou
        returncode = 0
        output = ""
        try:

            output = subprocess.check_output(
                self.cmd.split(' '),
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError, e:
            output = e.output
            returncode= e.returncode

        self.output = output
        self.returncode = returncode

        return returncode, output

    def __unicode__(self):
        return self.cmd + " | " + self.returncode

    def __str__(self):
        return self.cmd + " | " + self.returncode
