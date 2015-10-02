# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
#essas 2 linhas serão o titulo e subtitulo na view
response.title = T('My Blog')
response.subtitle = T('My blog is Python powered')

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()

    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))
    """
    #enviamos uma mensagem de boas vindas
    response.flash = T('Welcome to my BLOG')

    #retornando todos os posts ordenados descendentemente
    #aqui fazemos um Inner join entre as tabelas de posts e categories
    posts = db(db.categories.id==db.posts.post_category).select(db.posts.ALL,db.categories.ALL,orderby=~db.posts.post_time)

    # aqui retornamos as categorias e a contagem de posts de cada uma
    # Existem outras formas de fazer isso, mas preferi mostrar as diferentes possibilidades de retorno e iteração
    cats = db().select(db.categories.ALL)
    categories = []
    for cat in cats:
        count = len(db(
                   db.posts.post_category == cat.id
                   ).select(db.posts.ALL))
        categorie = {'id':cat.id,'name':cat.category_name,'posts':str(count)}
        categories.append(categorie)

    #aqui retornamos os dois objetos populados
    return dict(posts=posts,categories=categories)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


