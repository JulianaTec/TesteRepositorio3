#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Cria os falsos objetos de: request, response, session, cache e T,
# pois são os objetos globais principais do web2py.

# TODO: colocar os demais objetos globais aqui.

# importa o Mock, para a criação dos objetos falsos.
from mock import Mock

# objeto fake do T
def foo(f):
	return f
# Quando T() for chamado, será retornado o valor que entrar, porque não é necessário
# testar a funcionalidade do T(), pois é uma função do sistema, não do desenvolvedor.
T = Mock(side_effect = foo)

# objeto fake do cache
cache = Mock()

# objeto fake do request
request = Mock()

# objeto fake do session
session = Mock()

# objeto fake do session
session = Mock()

# #
# #
# # Alguns imports globais do web2py
#     import gluon.languages.translator as T
#     from gluon.cache import Cache
#     from gluon.contrib.gql import GQLDB
#     from gluon.globals import Request
#     from gluon.globals import Response
#     from gluon.globals import Session
#     from gluon.html import *
#     from gluon.http import HTTP
#     from gluon.http import redirect
#     from gluon.sql import DAL
#     from gluon.sql import Field
#     from gluon.sql import SQLDB
#     from gluon.sqlhtml import SQLFORM
#     from gluon.validators import *
#     cache = Cache()
#     request = Request()
#     response = Response()
#     session = Session()
# #
# #
