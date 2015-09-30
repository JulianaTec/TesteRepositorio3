__author__ = 'TecSUS-3'

def NovaManual():
    '''
    Teste de como fazer um menu de opções
    '''
    response.menu=[['Inicial  - true',True,'http://127.0.0.1:8000/site_two_alterado/'],
                   ['Exemplos Simples',False,URL('ExemplosSimples')],
                   ['Session Examples',False,URL('SessionExamples')],
                   ['Template Examples',False,URL('TemplateExamples')],
                   ['form',False,URL('form')],
                   ['db test',False,URL('db_teste')],
                   ['cache',False,URL('cache_teste')],
                   ['ajax',False,URL('ajax_teste')],
                   ['testing',False,URL('testing')],
                   ['form validators',False,URL('FormValidators')],
                   ['valida antes de submeter',False,URL('insert_numbers')],
                   ['verifica mudança antes de submeter',False,URL('edit_dog')],
                   ['sqlform',False,URL('display_form')],
                   ['1 form 2 tables',False,URL('register')],
                   ['geral',False,URL('formsGeral')],
                   ['CRUDE',False,URL('formCrude')],
                  ]
    response.flash='Nova Manual'
    return dict(message=T("Nova Manual return"))

def formCrude():
    '''
    Teste de como fazer um menu de opções
    '''
    response.menu=[
                   ['Exemplos Simples',False,URL('crudeGeral')],
                   ['Exemplos de seleção',False,URL('people')],
                   ['Exemplos de crude',False,URL('manage')],
                   ['Completa automaticamente',False,URL('autocomplet')],

                  ]
    response.flash='Nova Manual'
    return dict(message=T("Nova Manual return"))


def ExemplosSimples():
    '''
    Teste de como fazer um menu de opções
    '''
    response.menu=[['Nova Manual  - true',True,URL('NovaManual')],
                   ['teste 2  - false',False,URL('database_lists_grid')],
                   ['hello 4 -  Retorna com menu',False,URL('hello4')],
                   ['hello 5 - Retorna vermelho',False,URL('hello5')],
                   ['status - toolbar',False,URL('status')],
                   ['json',False,URL('makejson')],
                   ['make rtf',False,URL('makertf')],
                   ['rss',False,URL('rss_aggregator')],
                   ['markmin ajax',False,URL('ajaxwiki')],
                   ]
    response.flash='Exemplos Simples'
    return dict(message=T("ExemplosSimples"))

def SessionExamples():
    '''
    Teste de como fazer um menu de opções
    '''
    response.menu=[['Nova Manual',True,URL('NovaManual')],
                   ['counter',False,URL('counter')],
                   ]
    response.flash='Exemplos Simples'
    return dict(message=T("ExemplosSimples"))

def TemplateExamples():

    response.menu=[['Nova Manual  - true',True,URL('NovaManual')],
                   ['variables',False,URL('variables')],
                   ['test_for',False,URL('test_for')],
                   ['hello 5 - Retorna vermelho',False,URL('hello5')],
                   ['status - toolbar',False,URL('status')],
                   ['json',False,URL('makejson')],
                   ['make rtf',False,URL('makertf')],
                   ['rss',False,URL('rss_aggregator')],
                   ['markmin ajax',False,URL('ajaxwiki')],
                   ]
    return dict(globals())

def cache_teste():
    return globals()

def ajax_teste():
    return globals()

def data_view():
    return dict()

###################################################################
#Exemplo Simples
###################################################################

'''
Teste que cria um flash, muda de página e escreve hello world
'''
def hello4():
    response.view='http://127.0.0.1:8000/site_two_alterado/'
    response.flash=T("Hello World in a flash!")
    return dict(message=T("Hello World"))

'''
Teste que retorna uma mensagem em vermelho
'''
def hello5():
    return HTML(BODY(H1(T('Hello World'),_style="color: red;"))).xml() # .xml to serialize

'''
Não funciona, acho que deveria mudar a posição do menu
'''
def status():
    return dict(toobar=response.toolbar())

'''
não entendi pra que serve
'''
def makejson():
   return response.json(['foo', {'bar': ('baz', None, 1.0, 2)}])

'''
Escreve em documento
'''
def makertf():
    import gluon.contrib.pyrtf as q
    doc=q.Document()
    section=q.Section()
    doc.Sections.append(section)
    section.append('Este é um teste de txt')
    section.append('Muito doido. '*100)
    response.headers['Content-Type']='text/rtf'
    return q.dumps(doc)

'''
Não funciona, mas tb não entendi pra que serve
'''
def rss_aggregator():
    import datetime
    import gluon.contrib.rss2 as rss2
    import gluon.contrib.feedparser as feedparser
    d = feedparser.parse("http://rss.slashdot.org/Slashdot/slashdot/to")

    rss = rss2.RSS2(title=d.channel.title,
    link = d.channel.link,
    description = d.channel.description,
    lastBuildDate = datetime.datetime.now(),
    items = [
       rss2.RSSItem(
         title = entry.title,
         link = entry.link,
         description = entry.description,
         # guid = rss2.Guid('unkown'),
         pubDate = datetime.datetime.now()) for entry in d.entries]
       )
    response.headers['Content-Type']='application/rss+xml'
    return rss2.dumps(rss)

'''
Esses dois últimos não funcionaram corretamente
'''
def ajaxwiki():
    form=FORM(TEXTAREA(_id='text',_name='text'),INPUT(_type='button',_value='markmin',_onclick="ajax('ajaxwiki_onclick',['text'],'html')"))
    return dict(form=form,html=DIV(_id='html'))

def ajaxwiki_onclick():
   return MARKMIN(request.vars.text).xml()

   '''
    Teste de como fazer um menu de opções
    '''

###################################################################
#Sessions
###################################################################

'''
conta quantas vezes a pessoa entrou na página
'''
def counter():
    session.counter = (session.counter or 0) + 1
    return dict(counter=session.counter)


###################################################################
#Templates
###################################################################


'''
Loop não funcionou e as demais também
'''
def variables():
    return dict(a=10, b=20)

def test_for():
    return dict()
########

def form():
    form=FORM(TABLE(TR("Your name:",INPUT(_type="text",_name="name",requires=IS_NOT_EMPTY())),
                    TR("Your email:",INPUT(_type="text",_name="email",requires=IS_EMAIL())),
                    TR("Admin",INPUT(_type="checkbox",_name="admin")),
                    TR("Sure?",SELECT('yes','no',_name="sure",requires=IS_IN_SET(['yes','no']))),
                    TR("Profile",TEXTAREA(_name="profile",value="write something here")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request,session):
        response.flash="form accepted"
    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"
    return dict(form=form,vars=form.vars)

###################################################################
#db
###################################################################

def RegisterPerson():
    # create an insert form from the table
    form = SQLFORM(db.person).process()
    form.add_button('Back', URL('db_teste'))

    # if form correct perform the insert
    if form.accepted:
        response.flash = 'new record inserted'

    # and get a list of all persons
    records = SQLTABLE(db().select(db.person.ALL),headers='fieldname:capitalize')

    return dict(form=form, records=records)

def RegisterProduct():
    # create an insert form from the table
    form = SQLFORM(db.product).process()
    form.add_button('Back', URL('db_teste'))

    if form.accepted:
        response.flash = 'new record inserted'

    records = SQLTABLE(db().select(db.product.ALL),
                      upload = URL('download'), # allows pics preview
                      headers='fieldname:capitalize')

    return dict(form=form, records=records)

def buy():

     form = SQLFORM.factory(
        Field('buyer_id',requires=IS_IN_DB(db,db.person.id,'%(name)s')),
        Field('product_id',requires=IS_IN_DB(db,db.product.id,'%(name)s')),
        Field('quantity','integer',requires=IS_INT_IN_RANGE(1,100))).process()

     form.add_button('Back', URL('db_teste'))

     if form.accepted:
        # get previous purchese for same product
        purchase = db((db.purchase.buyer_id == form.vars.buyer_id)&
            (db.purchase.product_id==form.vars.product_id)).select().first()

        if purchase:
            # if list contains a record, update that record
            purchase.update_record(
                quantity = purchase.quantity+form.vars.quantity)
        else:
            # self insert a new record in table
            db.purchase.insert(buyer_id=form.vars.buyer_id,
                               product_id=form.vars.product_id,
                               quantity=form.vars.quantity)
        response.flash = 'product purchased!'
     elif form.errors:
        response.flash = 'invalid values in form!'

     # now get a list of all purchases
     records = SQLTABLE(db(purchased).select(),headers='fieldname:capitalize')

     return dict(form=form, records=records)

def db_teste():
    return locals()

#def download():
#    return response.download(request,db)

def manage_transactions():
    grid = SQLFORM.smartgrid(db.person,linked_tables=['product','purchase'],
                             user_signature=False)
    return dict(grid=grid)

###################################################################
#Cache
###################################################################

def cache_in_ram():
    import time
    t=cache.ram('time',lambda:time.ctime(),time_expire=5)
    return dict(time=t,link=A('click to reload',_href=URL(r=request)))


###################################################################
#Ajax
###################################################################

'''
Este não funcionou também
'''
def data():
    if not session.m or len(session.m)==10: session.m=[]
    if request.vars.q: session.m.append(request.vars.q)
    session.m.sort()
    return TABLE(*[TR(v) for v in session.m]).xml()

def flash():
    response.flash='this text should appear!'
    return dict()

def fade():
    return dict()

###################################################################
#testing
###################################################################

def testing():
    '''
    This is a docstring. The following 3 lines are a doctest:
    >>> request.vars.name='Max'
    >>> index()
    {'name': 'Max'}
    '''
    return dict(name=request.vars.name)

######################################################################
#FormValidators
######################################################################
def FormValidators():

    form=FORM('Your name:',
          INPUT(_name='name', requires=IS_NOT_EMPTY()),
          INPUT(_type='submit'))

    form.add_button('Back', URL('NovaManual'))

    if form.accepts(request,session):
       response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'


    db.person.name.show_if = (db.person.email=='ju@ju.com')
    form2 = SQLFORM(db.person).process()

#este pedacinho que era pra mostrar uma mensagem de falha deu errado
    form3=FORM('Your name:',
          INPUT(_name='name', requires=IS_NOT_EMPTY()),
          INPUT(_type='submit'))

    if form3.accepts(request,session):
       response.flash = 'form accepted'
    elif form3.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'

    return dict(form=form, form2=form2, form3=form3)

#########################################################
#validando antes de submeter
########################################################
def my_form_processing(form):
    casa = form.vars.asa * form.vars.b
    if casa < 0:
       form.errors.b = 'asa*b cannot be negative'
    else:
       form.vars.casa = casa

def insert_numbers():
   form = SQLFORM(db.numbers)
   if form.process(onvalidation=my_form_processing).accepted:
       session.flash = 'record inserted'
       redirect(URL())

   form.add_button('Back', URL('NovaManual'))

   return dict(form=form)

#########################################################
#verifica se foi modificado antes de salvar  a alteração
########################################################
def edit_dog():
   # dog = db.dog(request.args(0)) or redirect(URL('FormValidators'))
    form=SQLFORM(db.dog)
    form.process(detect_record_change=True)
    if form.record_changed:
        msg = 'mudou'
    elif form.accepted:
        redirect(URL('NovaManual'))
    else:
        msg = 'erro'

    form.add_button('Back', URL('NovaManual'))

    return dict(form=form,msg=msg)

#########################################################
#testes com sqlform
########################################################
def display_form():

   form2 = SQLFORM(db.person4,deletable=True, labels={'name':'digite seu nome'},buttons = [TAG.button('Back',_type="button",_onClick = "parent.location='%s' " % URL('NovaManual')),TAG.button('Next',_type="submit")])

   Field('image', 'upload', uploadfolder='FormValidators')

   #form2 = SQLFORM(db.person4)
   my_extra_element = TR(LABEL('I agree to the terms and conditions'),INPUT(_name='agree',value=True,_type='checkbox'))
   form2[0].insert(-1,my_extra_element)

   if form2.process().accepted:
       response.flash = 'form accepted'
   elif form2.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'


   record = db.person4(request.args(0)) or redirect(URL('FormValidators'))
   url = URL('download')

   form = SQLFORM(db.person4, record, deletable=True,upload=url, fields=['name', 'image'])

   Field('image', 'upload', uploadfolder='FormValidators')

   if request.vars.image!=None:
        form.vars.image_filename = request.vars.image_filename
   if form.process().accepted:
        response.flash = 'form accepted'
   elif form.errors:
        response.flash = 'form has errors'

   return dict(form=form, form2=form2)

def download():
    return response.download(request, db)


#########################################################
#testes de form factory
########################################################

def form_from_factory():
    form = SQLFORM.factory(
        Field('your_name', requires=IS_NOT_EMPTY()),
        Field('your_image', 'upload'))

    Field('your_image', 'upload', uploadfolder='FormValidators')

    if form.process().accepted:
        response.flash = 'form accepted'
        session.your_name = form.vars.your_name
        session.your_image = form.vars.your_image
    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form)


#########################################################
#um form e duas tabelas
########################################################
def register():
    form=SQLFORM.factory(db.client,db.address)
    if form.process().accepted:
        id = db.client.insert(**db.client._filter_fields(form.vars))
        form.vars.client=id
        id = db.address.insert(**db.address._filter_fields(form.vars))
        response.flash='Thanks for filling the form'
    return dict(form=form)

#########################################################
#form de confirmação
########################################################
def formsGeral():

    form = FORM.confirm('Are you sure?')
    if form.accepted:register()

    form2 = FORM.confirm('Are you sure?',{'Back':URL('other_page')})
    if form2.accepted:register()

    return dict(form=form,form2=form2)


#########################################################
#CRUDE
########################################################
def crudeGeral():

    from gluon.tools import Crud
    crud = Crud(db)

    form = crud.create(db.client)

    id=1

    form2 = crud.read(db.client, id)

    form3 = crud.update(db.client, id)

    form4 = crud.search(db.client)

    #form5 = SQLFORM(db.client, myrecord).process(onsuccess=auth.archive)

    #form5 = crud.update(db.mytable, myrecord, onaccept=auth.archive)

    return dict(form=form,form2=form2,form3=form3,form4=form4)

def people():

    from gluon.tools import Crud
    crud = Crud(db)

    form = crud.create(db.client, next=URL('people'),message=T("record created"))
    persons = crud.select(db.client, fields=['name'],headers={'client.name': 'Name'})

    return dict(form=form, persons=persons)

def manage():

######
#não funcionou
#####
    table=db[request.args(0)]
    form = crud.update(table,request.args(1))
    table.id.represent = lambda id, row:        A('edit:',id,_href=URL(args=(request.args(0),id)))
    search, rows = crud.search(table)

    return dict(form=form,search=search,rows=rows)

#########################################################################
#autocomplet
#########################################################################
def autocomplet():

    from gluon.tools import Crud
    crud = Crud(db)

    form = crud.create(db.product2, next=URL('autocomplet'),message=T("record created"))
    persons = crud.select(db.product2, fields=['category'],headers={'product2.category': 'Tipo'})

    return dict(form=form, persons=persons)