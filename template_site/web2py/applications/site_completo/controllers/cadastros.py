__author__ = 'TecSUS-3'

####################################### IMPORTS #######################################
from gluon import A, INPUT, IS_NOT_EMPTY, SQLFORM, URL, TR, TABLE, FORM, IS_LIST_OF, IS_IN_DB, redirect
from gluon import Field

####################################### GLOBALS #######################################
global request, session, db, response

#######################################################################################

def endereco_crud():
    """ Create a simple form using the CRUD function of web2py. """

    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    from gluon.tools import Crud
    crud = Crud(db)

    endereco_crud = crud.create(db.Endereco)
    return locals()

def pessoa_crud():
    """ Create a simple form using the CRUD function of web2py. """

    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    from gluon.tools import Crud
    crud = Crud(db)
    pessoa_crud = crud.create(db.Pessoa)
    return locals()

def tipo_usuario_crud():
    """ Create a simple form using the CRUD function of web2py. """

    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    from gluon.tools import Crud
    crud = Crud(db)
    tipo_usuario_crud = crud.create(db.Tipo_Usuario)
    return locals()

def post_crud():
    """ Create a simple form using the CRUD function of web2py. """

    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    from gluon.tools import Crud
    crud = Crud(db)
    post_crud = crud.create(db.Post)
    return locals()

def view_posts():
    """ Shows all users and posts"""
    #users = db(db.auth_user.id > 0).select()
    users = db(db.Pessoa.id>0).select()
    posts = db(db.Post.id > 0).select()
    return dict(users=users, posts=posts)