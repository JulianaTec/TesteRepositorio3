# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():

    # contador para identificar quantas vezes entrou na session
    if not session.counter:
        session.counter = 1
    else:
        session.counter += 1

    # tag que aparece no começo da página
    response.flash = T("Bem vindo ao Site One")

    # banco de dados da imagem
    #images = db().select(db.image.ALL, orderby=db.image.title)

    #return dict(images=images, message=T('Pagina 1'), counter=session.counter)
    return dict(message=T('Pagina 1'), counter=session.counter)

def test_view():
    return dict(i=0)

def test_layout():
    return dict(i=0)

def teste2():
    return dict(i=0)

def view_teste2():
    return dict(i=0)

def bancoDados():

    try:
        pessoas_form = bancoDados_form()
        pessoas_sqlform = bancoDados_sqlform()

        myfield_form = bancoDados_form2()
        myfield_sqlform2 = bancoDados_sqlform2()

        if pessoas_sqlform.process().accepted:
            response.flash = 'Ok'
        elif pessoas_sqlform.errors:
            response.flash = 'Error'

    except:
        db.rollback()
        response.flash = 'Error for all'
    else:
        db.commit()
        response.flash = 'Ok for all'

    return locals()

def TestForm():
    return locals()



def TesteFormHelpers():
    form=FORM('Your name:', INPUT(_name='name'), INPUT(_type='submit'))

    form2=FORM('Your name:',
              INPUT(_name='name', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))

    if form2.accepts(request,session):
        response.flash = 'form accepted'
    elif form2.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'

    db.purchase.coupon_code.show_if = (db.purchase.have_coupon==True)
    form3 = SQLFORM(db.purchase).process()

    return locals()

def bancoDados_sqlform2():
    sqlform2 = SQLFORM(db.mytable)
    return sqlform2

def bancoDados_form2():
    return FORM(LABEL('myfield:'),INPUT(_name='myfield'),INPUT(_type='submit'))

def bancoDados_form():
    return FORM(LABEL('Your name:'), INPUT(_name='name'), INPUT(_type='submit'))

def bancoDados_sqlform():
    sqlform = SQLFORM(db.person)
    return sqlform


# requisição com senha de adm
@auth.requires_membership('adm')
def manage():
    grid = SQLFORM.smartgrid(db.image,linked_tables=['post'])
    return dict(grid=grid)

# requisição de login
@auth.requires_login()
def show():
    image = db.image(request.args(0,cast=int)) or redirect(URL('index'))
    db.post.image_id.default = image.id
    form = SQLFORM(db.post)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = db(db.post.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

# pagina um
def first():

    # contador para identificar quantas vezes entrou na session
    if not session.counter2:
        session.counter2 = 1
    else:
        session.counter2 += 1

    # tag que aparece no começo da página
    response.flash = T("pagina 1")

    form = SQLFORM.factory(Field('visitor_name',
                                 label='Qual seu nome?',
                                 requires=IS_NOT_EMPTY()))

    if form.process().accepted:
        session.visitor_name = form.vars.visitor_name
        redirect(URL('second'))

    return dict(message=T('Pagina 1'), counter2=session.counter2, form=form)

def second():
      # contador para identificar quantas vezes entrou na session
    if not session.counter3:
        session.counter3 = 1
    else:
        session.counter3 += 1

    if not request.function == 'first' and not session.visitor_name:
        redirect(URL('first'))

  # banco de dados da imagem
    images = db().select(db.image.ALL, orderby=db.image.title)

    return dict(images=images, session3=session.counter3)

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

def wiki():
     """ this controller returns a dictionary rendered by the view
         it lists all wiki pages
     >>> wiki().has_key('wiki')
     True
     """
     pages = db().select(db.page.id,db.page.title,orderby=db.page.title)

     return dict(pages=pages)

def show_wiki():
     """shows a wiki page"""
     this_page = db.page(request.args(0,cast=int)) or redirect(URL('wiki'))
     db.post2.page_id.default = this_page.id
     form = SQLFORM(db.post2).process() if auth.user else None
     pagecomments = db(db.post2.page_id==this_page.id).select()
     return dict(page=this_page, comments=pagecomments, form=form)

@auth.requires_login()
def edit():
     """edit an existing wiki page"""
     this_page = db.page(request.args(0,cast=int)) or redirect(URL('wiki'))
     form = SQLFORM(db.page, this_page).process(
         next = URL('show_wiki',args=request.args))
     return dict(form=form)

def search():
     """an ajax wiki search page"""
     return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
              _onkeyup="ajax('callback', ['keyword'], 'target');")),
              target_div=DIV(_id='target'))

def callback():
     """an ajax callback that returns a <ul> of links to wiki pages"""
     query = db.page.title.contains(request.vars.keyword)
     pages = db(query).select(orderby=db.page.title)
     links = [A(p.title, _href=URL('show_wiki)',args=p.id)) for p in pages]
     return UL(*links)

@auth.requires_login()
def create():
     """creates a new empty wiki page"""
     form = SQLFORM(db.page).process(next=URL('wiki'))
     return dict(form=form)

@auth.requires_login()
def documents():
     """browser, edit all documents attached to a certain page"""
     page = db.page(request.args(0,cast=int)) or redirect(URL('wiki'))
     db.document.page_id.default = page.id
     db.document.page_id.writable = False
     grid = SQLFORM.grid(db.document.page_id==page.id,args=[page.id])
     return dict(page=page, grid=grid)

def news():
    """generates rss feed from the wiki pages"""
    response.generic_patterns = ['.rss']
    pages = db().select(db.page.ALL, orderby=db.page.title)
    return dict(
       title = 'mywiki rss feed',
       link = 'http://127.0.0.1:8000/mywiki/default/index',
       description = 'mywiki news',
       created_on = request.now,
       items = [
          dict(title = row.title,
               link = URL('show_wiki', args=row.id, scheme=True,
	                  host=True, extension=False),
               description = MARKMIN(row.body).xml(),
               created_on = row.created_on
               ) for row in pages])


service = Service()

@service.xmlrpc
def find_by(keyword):
     """finds pages that contain keyword for XML-RPC"""
     return db(db.page.title.contains(keyword)).select().as_list()

def call():
    """exposes all registered services, including XML-RPC"""
    return service()

def wikidemo(): return auth.wiki()

def string_return():
    return 'dado'

def dic_return():
    return dict(key='value')

def all_locals_var():
    return locals()

def http_return():
    raise HTTP(404)

def helper_return():
    return FORM(INPUT(_name='test'))

def my_form_processing(form):
    c = form.vars.a * form.vars.b
    if c < 0:
       form.errors.b = 'a*b cannot be negative'
    else:
       form.vars.c = c


def sqlform():
   form = SQLFORM(db.numbers)
   if form.process(onvalidation=my_form_processing).accepted:
       session.flash = 'record inserted'
       redirect(URL('teste2'))
   return dict(form=form)

form15 = FORM('Your name:',
              INPUT(_name='name', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
form15.add_button('Back', URL('index'))

def teste2():

    if form15.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('TestForm'))
    elif form15.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form15)


def two_forms():
    form1 = form15
    form2 = FORM(INPUT(_name='name', requires=IS_NOT_EMPTY()),
               INPUT(_type='submit'))
    if form1.process(formname='form_one').accepted:
        response.flash = 'form one accepted'
    if form2.process(formname='form_two').accepted:
        response.flash = 'form two accepted'
    return dict(form1=form1, form2=form2)


def display_form():
   form = SQLFORM(db.person3)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def display_form2():
   record = db.person3(request.args(0))
   form = SQLFORM(db.person3, record)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   return dict(form=form)

def display_form3():
   record = db.person3(request.args(0))
   form = SQLFORM(db.person3, record, deletable=True,
                  upload=URL('download'))
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   return dict(form=form)

def download():
    return response.download(request, db)

def data_teste():
    return dict(form1=crud())

