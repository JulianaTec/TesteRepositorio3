__author__ = 'TecSUS-3'


from gluon.tools import Auth

auth2 = Auth(db2,controller='veiculo', function = 'Inicio',url_index = URL('veiculo','Inicio'),propagate_extension = URL('default','index'))

#adiciona campo
auth2.settings.extra_fields['auth_user'] = [
                                            Field('sexo'),
                                            ]



auth2.define_tables(username=True,signature=False)

#pede aprovação após registro
auth2.settings.registration_requires_approval = True  #blocked pending nada

# criamos um validador pré definido
notempty = IS_NOT_EMPTY(error_message=e_m['empty'])

db2.define_table('vendedor',
                 Field('nome', unique=True, notnull=True),format='%(nome)s')

# definição da tabela de marcas
db2.define_table('marca',
                Field('nome', unique=True, notnull=True),format='%(nome)s')

# validadores da tabela de marcas
db2.marca.nome.requires=[notempty, IS_NOT_IN_DB(db2, 'marca.nome',error_message=e_m['in_db'])]

# definição da tabela de carros
db2.define_table('carro',
                Field('marca', db2.marca, notnull=True),
                Field('modelo', notnull=True),
                Field('ano', 'integer', notnull=True),
                Field('cor', notnull=True),
                Field('valor', 'double'),
                Field('itens', 'list:string'),
                Field('estado', notnull=True),
                Field('desc', 'text'),
                Field('foto', 'upload'),format='%(modelo)s - %(ano)s - %(estado)s'
                )

# validação da tabela carro
db2.carro.marca.requires=IS_IN_DB(db2, 'marca.id','marca.nome',error_message=e_m['not_in_db'])
db2.carro.modelo.requires=notempty
db2.carro.ano.requires=[notempty, IS_INT_IN_RANGE(request.now.year-20,request.now.year+2,error_message=e_m['not_in_range'])]
db2.carro.cor.requires=IS_IN_SET(cores)
db2.carro.itens.requires=IS_IN_SET(('Alarme','Trava','Som', 'Ar'),multiple=True,error_message=e_m['not_in_set'])
db2.carro.estado.requires=IS_IN_SET(estados,error_message=e_m['not_in_set'])
db2.carro.foto.requires=IS_EMPTY_OR(IS_IMAGE(extensions=('jpeg', 'png', '.gif'),error_message=e_m['image']))

# definição da tabela de compradores
db2.define_table('comprador',
                Field('nome'),
                Field('email'),
                Field('telefone'),
                )

# validação da tabela de compradores
db2.comprador.nome.requires=notempty
db2.comprador.email.requires=IS_EMAIL(error_message=e_m['email'])
db2.comprador.telefone.requires=notempty

db2.comprador.nome.label = 'Nome completo'
db2.comprador.email.label = 'Seu email'
db2.comprador.telefone.label = 'Seu telefone'

id_doc = db2.define_table('venda',
                 Field('modelo',db2.carro,notnull=True),
                 Field('nome_vendedor',db2.vendedor,notnull=True),
                 Field('desconto'),
                 Field('forma_pagamento','list:string'),
                 Field('data', 'datetime', default=request.now),
                 )

# validação da tabela venda
db2.venda.modelo.requires=IS_IN_DB(db2, 'carro.id','carro.modelo',error_message=e_m['not_in_db'])
db2.venda.nome_vendedor.requires=IS_IN_DB(db2, 'vendedor.id','vendedor.nome',error_message=e_m['not_in_db'])
db2.venda.forma_pagamento.requires=IS_IN_SET(('A vista','Parcelas','Financiamento', 'Troca'),multiple=False,error_message=e_m['not_in_set'])
db2.venda.data.writable = False
db2.venda.data.readable = False

db2.venda.modelo.widget = SQLFORM.widgets.autocomplete(request, db2.carro.modelo, limitby=(0,5), min_length=1)


###########################################
#Configuração do servidor
##########################################
## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

from gluon.tools import Mail
mails = auth2.settings.mailer
mails.settings.server = myconf.take('smtp.server')
mails.settings.sender = myconf.take('smtp.sender')
mails.settings.login = myconf.take('smtp.login')


