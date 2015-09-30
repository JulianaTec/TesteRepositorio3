#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Para rodar os testes:
# - no shell entre na pasta: tests/
# - execute: python run_tests.py
# Assim este arquivo de encarregará de rodar os testes na pasta tests/
#


# Salva os caminhos das pastas que serão testadas no sys.path
import sys
import os
# Pasta onde fica localizado o web2py
W2P_PATH = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-3])
#W2P_PATH = "/home/rodrigo/Arquivos/web2py" #o comando acima pegara este caminho
# sys.path.append(os.path.abspath(W2P_PATH))
# sys.path.append(os.path.abspath(W2P_PATH+'/gluon'))
# sys.path.append(os.path.abspath(W2P_PATH+'/site-packages'))
# Pasta anterior a pasta atual (raiz projeto)
PROJECT_PATH = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
# Pasta atual, onde o run_tests.py está
ROOT_PATH = os.path.dirname(__file__)
#adiciona no sys.path os diretorios que contém arquivos ou módulos a serem testados
mods=['controllers','modules']
APP = os.path.sep.join(ROOT_PATH.split(os.path.sep)[:-1])
for m in mods:
    sys.path.append(os.path.abspath(APP+'/'+m))

# Roda os testes da pasta test/
from unittest import TestLoader, TextTestRunner
if __name__ == '__main__':
    # Pega todos os arquivos da pasta corrente que sejam .py
    tests = TestLoader().discover(ROOT_PATH, "*.py")
    # Roda os testes
    # verbosity=2 aumenta o nível de detalhe da saida
    #result = TextTestRunner(verbosity=2).run(tests)
    result = TextTestRunner().run(tests)
    # Se houver algum problema nos testes, fecha o programa
    if not result.wasSuccessful():
        sys.exit(1)
