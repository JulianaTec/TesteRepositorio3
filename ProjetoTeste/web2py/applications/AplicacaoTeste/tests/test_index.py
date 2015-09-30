from unittest import TestCase

# Importa o controlador que sera testado

import os,sys

print '>>>>',os.path.dirname(__file__)
print '>>>>',sys.path

print os.path.dirname(__file__)

import os,sys

print '>>>>',os.path.dirname(__file__)
print '>>>>',sys.path


import default

class TestIndex(TestCase):
    def test_index(self):
        self.assertEqual(default.index()['nome'],'blai')
      
