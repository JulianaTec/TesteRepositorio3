__author__ = 'TecSUS-3'

####################################### IMPORTS #######################################
from gluon import A, INPUT, IS_NOT_EMPTY, SQLFORM, URL, TR, TABLE, FORM, IS_LIST_OF, IS_IN_DB, redirect
from gluon import Field
from gluon.tools import Crud

####################################### GLOBALS #######################################
global request, session, response
crud = Crud(db2)

'''
# ## critical --- make a copy of the environment

global_env = copy.copy(globals())
global_env['datetime'] = datetime

http_host = request.env.http_host.split(':')[0]
remote_addr = request.env.remote_addr
try:
    hosts = (http_host, socket.gethostname(),
             socket.gethostbyname(http_host),
             '::1','127.0.0.1','::ffff:127.0.0.1')
except:
    hosts = (http_host, )

if request.env.http_x_forwarded_for or request.env.wsgi_url_scheme\
     in ['https', 'HTTPS']:
    session.secure()
elif (remote_addr not in hosts) and (remote_addr != "127.0.0.1"):
    raise HTTP(200, T('appadmin is disabled because insecure channel'))
if not gluon.fileutils.check_credentials(request):
    redirect(URL(a='admin', c='default', f='index'))

ignore_rw = True
response.view = 'appadmin.html'
response.menu = [[T('design'), False, URL('admin', 'default', 'design',
                 args=[request.application])], [T('db'), False,
                 URL(r=request, f='index')], [T('state'), False,
                 URL(r=request, f='state')], [T('cache'), False,
                 URL(r=request, f='ccache')]]

'''

###teste de classe########################################
class MyClass(object):
        z = 2
        def __init__(self, a, b):
            self.x = a
            self.y = b
        def add(self):
            return self.x + self.y + self.z


class MyList(object):
        def __init__(self, *a): self.a = list(a)
        def __len__(self): return len(self.a)
        def __getitem__(self, i): return self.a[i]
        def __setitem__(self, i, j): self.a[i] = j

TiposCarros = ['Novo','Usado']

def meu_user():

    title = 'Login'

    form = auth2()

    order = db2.carro.marca
    #selecionar apenas os que possuem fotos
    registros = db2(db2.carro.foto!=None).select(orderby=order)

    form_teste = FORM(registros)

    form_carro = detalhes_geral(db2.carro, 2)

    (form_crud,table_crud) = pesquisa_geral(db2.carro)

    #meu_grupo('grupo_teste', 'teste de grupo')
    #meu_membros('2','4')
    #permissao_id = db2.permissoes.insert(nome = 'Leitura')
    #minha_permissao('2','read',permissao_id)
    #print auth2.has_permission('read',permissao_id,1,3)
    #print 'aqui'

    return locals()

def minha_permissao(id_grupo,descricao,leitura):

    auth2.add_permission(id_grupo,descricao,leitura)

    return locals()

def meu_grupo(nome_grupo,descricao):

    auth2.add_group(nome_grupo,descricao)

    return locals()

def meu_membros(grupo_id,user_id):

    auth2.add_membership(grupo_id,user_id)

    return locals()

def fecha_venda(formulario):

    file = open('venda'+str(formulario.id)+'.txt', 'w')
    file.write('venda realizada!')
    modelo = db2.carro[formulario.modelo].modelo
    nome = db2.vendedor[formulario.nome_vendedor].nome
    print modelo+'  este aqui'
    file.write(str(formulario.id)+' - '+modelo+' - '+nome+' - '+str(formulario.desconto)+' - '+str(formulario.forma_pagamento)+' - '+str(formulario.data))
   #file.close()
    #file = open('a', 'r')
    #print file.read()
    #file.close()

    return locals();

def Inicio():

    session.flashed = False

    #####classes#################
    myinstance = MyClass(3, 4)
    print myinstance.add()

    b = MyList(3, 4, 5)
    print b[1]
    b.a[1] = 7
    print b.a
    ##############################

    if not session.flashed:
        response.flash = T('Bem vindo a loja de carros!')

    #response.write('Venha conhecer nossos carros!!!')
    ###############################
    agora = request.now

    #lista todos os carros na tela
    #car_smartgrid  = SQLFORM.smartgrid(db2.carro)

    #lista todos os carros na tela
    car_grid = SQLFORM.grid(db2.carro)

    #contador de sessão
    session.counter = (session.counter or 0) + 1
    counter = session.counter

    #mostrar o nome do usuário na tela
    if auth2.user:
       visitor_name = auth2.user.first_name
    else:
       visitor_name = 'nenhum'

    table_hora = []
    table_hora.append(TR('Hora Atual:',agora))
    table_hora.append(TR('Visitante:',visitor_name))
    table_hora.append(TR('Número de visitas:',counter))
    table = TABLE(table_hora)
    form_hora = FORM(table)

    order = db2.carro.marca
    #selecionar apenas os que possuem fotos
    registros = db2(db2.carro.foto!=None).select(orderby=order)

    form_teste = FORM(registros)

    form_carro = detalhes_geral(db2.carro, 2)

    (form_crud,table_crud) = pesquisa_geral(db2.carro)

    title = "Loja de Carros"

#    showcase = SHOWCASE(registros)

    return locals()

def consultar_compradores(carro_id):
    carro_muda = db2(db2.carro.id == carro_id).select()
    form_consulta = SQLFORM(carro_muda)
    return locals()

@auth2.requires_membership('Master')
def venda():

     if not session.flashed:
        response.flash = T('Bem vindo a tela de vendas!')

     title = "Venda"

     ####SQL####################################################
     #######################################################
     #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
     #mas não mostra a mensagem de falha ou aceitação sozinho
     venda_sqlform = SQLFORM(db2.venda)

     if venda_sqlform.accepts(request,session):
        response.flash = 'Form accepted'
        formulario = db2().select(db2.venda.ALL).last()
        fecha_venda(formulario)
     elif venda_sqlform.errors:
        response.flash = 'Form has errors'
     else:
        response.flash = 'Please fill the form'

     form_venda = detalhes_geral(db2.venda, 2)

     (form_crud,table_crud) = pesquisa_geral(db2.venda)

     return locals()

def download():
    import os
    #db2 = get_database(request)
    return response.download(request, db2)

@auth2.requires_membership('Master')
def comprador():


    title = 'Cliente'

    #lista todos os carros na tela
    comprador_grid = SQLFORM.smartgrid(db2.comprador)

    #CRUD
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    comprador_crud = crud.create(db2.comprador)

    ####SQL####################################################
    #######################################################
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mas não mostra a mensagem de falha ou aceitação sozinho
    comprador_sqlform = SQLFORM(db2.comprador)

    if comprador_sqlform.accepts(request,session):
        response.flash = 'Form accepted'
    elif comprador_sqlform.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill the form'

    form_geral = detalhes_geral(db2.comprador, 1)

    (form_crud,table_crud) = pesquisa_geral(db2.comprador)

    return locals()


def detalhes_geral(tabela, tb_id):

    registro_geral = tabela(tb_id) or redirect(URL('Inicio'))

    form_geral =SQLFORM(tabela,registro_geral,deletable=True,upload=URL('veiculo','download'))

    if form_geral.accepts(request.vars,session):
        response.flash = 'Sucesso'
    elif form_geral.errors:
        response.flash = 'Erro'

    return form_geral

def pesquisa_geral(tabela):

    form_crud,table_crud = crud.search(tabela)

    return form_crud,table_crud

@auth2.requires_membership('Master')
def marca():

    title = "Cadastro de Marcas"

    #lista todos os carros na tela
    marca_grid  = SQLFORM.smartgrid(db2.marca)

    #CRUD
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    marca_crud = crud.create(db2.marca)

    ####SQL####################################################
    #######################################################
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mas não mostra a mensagem de falha ou aceitação sozinho
    marca_sqlform = SQLFORM(db2.marca)

    if marca_sqlform.accepts(request,session):
        response.flash = 'Form accepted'
    elif marca_sqlform.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill the form'

    form_marca = detalhes_geral(db2.marca, 2)

    (form_crud,table_crud) = pesquisa_geral(db2.marca)

    return locals()

@auth2.requires_membership('Master')
def carro():

    title = "Cadastro de Carros"

    if not session.flashed:
        response.flash = T('Bem vindo a loja de carros!')

    #lista todos os carros na tela
    car_grid = SQLFORM.smartgrid(db2.carro)

    #CRUD
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    carro_crud = crud.create(db2.carro)

    #######################################################
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mas não mostra a mensagem de falha ou aceitação sozinho
    carro_sqlform = SQLFORM(db2.carro)

    if carro_sqlform.accepts(request,session):
        response.flash = 'Form accepted'
    elif carro_sqlform.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill the form'

    excluir_carro(1)

    alterar_carro(2)

    #######################################################
     # Must repeat the field validators declared in the db.py
    marca_input=INPUT(_name='marca_input', requires=IS_IN_DB(db2, 'marca.id','marca.nome',error_message=e_m['not_in_db']))
    modelo_input=INPUT(_name='modelo_input')
    y1 = request.now.year-20
    y2 = request.now.year+2
    ano_input=INPUT(_name='ano_input', requires=IS_INT_IN_RANGE(y1,y2,error_message=e_m['not_in_range']))
    cor_input=INPUT(_name='cor_input', requires=IS_IN_SET(cores))
    valor_input=INPUT(_name='valor_input')
    itens_input=INPUT(_name='itens_input',requires=IS_IN_SET(('Alarme','Trava','Som', 'Ar'),multiple=True,error_message=e_m['not_in_set']))
    estado_input=INPUT(_name='estado_input',requires=IS_IN_SET(estados,error_message=e_m['not_in_set']))
    desc_input=INPUT(_name='desc_input')
    foto_input=INPUT(_name='foto_input',requires=IS_IMAGE(IS_IMAGE(extensions=('jpeg', 'png', '.gif'),error_message=e_m['image'])))

    #neste ponto define a posição dos dados dentro de uma tabela
    # Manual creation of the html table
    table_rows = []
    table_rows.append(TR('Marca:', marca_input))
    table_rows.append(TR('Modelo:', modelo_input))
    table_rows.append(TR('Ano:', ano_input))
    table_rows.append(TR('Cor:', cor_input))
    table_rows.append(TR('Valor:', valor_input))
    table_rows.append(TR('Itens:', itens_input))
    table_rows.append(TR('Estado:', estado_input))
    table_rows.append(TR('Descrição:', desc_input))
    table_rows.append(TR('Foto:', foto_input))
    # Fields starting with _ are passed to the html as attribute elements
    table_rows.append(TR(TD(INPUT(_type='submit'), _colspan='2', _align='center')))
    table = TABLE(table_rows)

    form = FORM(table)

    #momento em que realmente o dado é colocado dentro do banco de dados
    # Processing the form submition
    if form.accepts(request,session):
        # Retriving the form fields
        form_marca_input = form.vars.marca
        form_modelo_input = form.vars.modelo
        form_ano_input = form.vars.ano
        form_cor_input = form.vars.cor
        form_valor_input = form.vars.valor
        form_itens_input = form.vars.itens
        form_estado_input = form.vars.estado
        form_desc_input = form.vars.desc
        form_foto_input = form.vars.foto
        # Inserting in the database
        db.car_model.insert(marca=form_marca_input, modelo = form_modelo_input,ano = form_ano_input, cor = form_cor_input, valor = form_valor_input, itens = form_itens_input, estado = form_estado_input, desc = form_desc_input, foto = form_foto_input)
        # Tell the user about the insertion
        response.flash = 'New car: ' + form_modelo_input
    elif form.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill the form'

    #######################################################
    form_carro = detalhes_geral(db2.carro,2)

    (form_crud,table_crud) = pesquisa_geral(db2.carro)

    return locals()

def excluir_carro(carro_id):
    carro_muda = db2(db2.carro.id == carro_id).delete()
    return locals()


#######################################################
#não funciona
#######################################################
def alterar_carro(carro_id):
    carro_muda = db2(db2.carro.id == carro_id).select()
    for i in carro_muda:
        i.update(modelo = 'outro')

    return locals()

@auth2.requires_membership('Master')
def vendedor():

    title = "Cadastro de Vendedores"

    #lista todos os carros na tela
    vendedor_grid  = SQLFORM.smartgrid(db2.vendedor)

    #CRUD
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mostra a mensagem de falha sozinho
    vendedor_crud = crud.create(db2.vendedor)

    ####SQL####################################################
    #######################################################
    #aqui ele formata tudo sozinho e ainda envia para o banco sozinho também
    #mas não mostra a mensagem de falha ou aceitação sozinho
    vendedor_sqlform = SQLFORM(db2.vendedor)

    if vendedor_sqlform.accepts(request,session):
        response.flash = 'Form accepted'
    elif vendedor_sqlform.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill the form'

    form_vendedor = detalhes_geral(db2.vendedor, 1)

    (form_crud,table_crud) = pesquisa_geral(db2.vendedor)

    return locals()


@auth2.requires_login()
def admin():

    args = request.args

    title = 'administration'

    if not args:
        link = UL(*[LI(A(tab,_href=URL(args=tab))) for tab in db.tables])
        return dict(items=link,title=title)

    if not args(1):
        i = 0
    else:
        i =1

    for tab in db.tables:
        if tab==args(i):
            tb = db[tab]

    crud = Crud(db)

    if args(0)=='edit':
        form = crud.update(tb, args(2),next=URL(f='admin',args=args(1)))
        items = None
        title = 'Edit %s ' % args(i)
    else:
        form = crud.create(tb)
        rows = db().select(tb.ALL)
        items = SQLTABLE(rows,linkto='edit')
        title = 'Insert %s ' % args(i)


    return dict(form=form,items=items,title=title)

@auth2.requires_login()
def send_email():

    title = 'Contato'

    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY()),
        Field('email', requires =[ IS_EMAIL(error_message='invalid email!'), IS_NOT_EMPTY() ]),
        Field('subject', requires=IS_NOT_EMPTY()),
        Field('message', requires=IS_NOT_EMPTY(), type='text')
    )
    if form.process().accepted:
        session.name = form.vars.name
        session.email = form.vars.email
        session.subject = form.vars.subject
        session.message = form.vars.message

        x = mails.send(to=['juliana.padilha@gmail.com'],
            subject='loja de carros',
            message= "Olá esse é um email de teste da lja de carros.\nName:"+ session.name+" \nEmail : " + session.email +"\nSubject : "+session.subject +"\nMessage : "+session.message+ ".\n "
        )

        if x == True:
            response.flash = 'email sent sucessfully.'
        else:
            response.flash = 'fail to send email sorry!'

        #response.flash = 'form accepted.'
    elif form.errors:
        response.flash='form has errors.'

    form_carro = detalhes_geral(db2.carro, 2)

    (form_crud,table_crud) = pesquisa_geral(db2.carro)

    return locals()