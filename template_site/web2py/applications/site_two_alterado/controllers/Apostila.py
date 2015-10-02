__author__ = 'TecSUS-3'
####################################### IMPORTS #######################################
from gluon import A, INPUT, IS_NOT_EMPTY, SQLFORM, URL, TR, TABLE, FORM, IS_LIST_OF, IS_IN_DB, redirect
from gluon import Field

def Apostila():

    ###########Basicos e calculos###############
    print"Teste de print!!!!!"

    form12 = (5+2)*9
    form2 = 50+50
    form3 = 7/2
    form4 = 7.0/2
    form5 = "Brasil "*4

    objeto = 234 #Criamos uma variavel(objeto) e atribuimos o valor inteiro 234
    objeto.__hex__() #O método __hex__() da classe **int** converte para hexadecimal

    form6= 'estamos no ano de ' + str(2010)
    form7= 'estamos no ano de %s ' % (2010)
    form8= 'estamos no ano de %(ano)s ' % dict(ano=2010) # recomendado

    form9 = 'Desenvolvimento web com {0} e {1}'.format('Python','web2py')

    form10 = 'Desenvolvimento web com {linguagem} e {framework}'.format(framework='web2py',linguagem='Python')

    ###############Listas####################

    #criando a lista
    linguagens = ['Python','PHP','Ruby','Java','Lua']

    #adicionando item a lista
    linguagens.append('VB')

    for linguagem in linguagens:
        print linguagem

    #ultimo elemento da lista
    linguagens[-1]

    #primeiro elemento da lista
    linguagens[0]
    #tudo do 3 item em diante
    linguagens[2:]
    #do terceiro ao quinto
    linguagens[2:5]
    #remove
    linguagens.remove('VB')
    #ordenando
    linguagens.sort()
    #listando
    linguagens

###########tuplas
    minhatupla=tuple(linguagens)
    minhatupla=list(linguagens)

    minhalista = [1,2]
    minhatupla = (minhalista,4,[1,2],'Python')
    minhatupla

    minhatupla[0].append(3)

#######empacotar valores
    a = 2,3,'hello'
    x,y,z = a
    print x
    print z

#####################dicionários
    pessoa_dic = {'nome':'João','idade':35,'altura':1.69}


    pessoas_dic={}
    pessoas_dic['bruno']={'idade':23,'cidade':'cotia'}
    pessoas_dic['claudia']={'idade':20,'cidade':'cotia'}
    pessoas_dic['claudia1']={'idade':20,'cidade':'cotia'}

    pessoas_dic['claudia']['idade']

    for pessoa_dic2 in pessoas_dic:
        print pessoa_dic2 +' '+pessoas_dic[pessoa_dic2]['cidade']+' '+str(pessoas_dic[pessoa_dic2]['idade'])

    pessoas_dic.keys()
    pessoas_dic.values()
    pessoas_dic.items()

    for item in pessoas_dic.items():
        print item

    del pessoas_dic['bruno']


    #####identação

    i=0
    while i<3:
        print i
        i=i+1

    for i in xrange(3,6):
        print i

    for i in range(3):
        print i

    for i in [1, 2, 3]:
        print i
        break

    for i in [1, 2, 3]:
        print i
        if i==2:
            continue
        print 'test'

    while i < 10:
        i = i + 1


    return dict(i=i, pessoas_dic= pessoas_dic,minhatupla= minhatupla,linguagens=linguagens,form12=form12,form10=form10,form2=form2,form3=form3,form4=form4,form5=form5,form6=form6,form7=form7,form8=form8,form9=form9, form11=objeto)

def services_testes():

    return locals()

def feed():
    return dict(title="my feed",
                link="http://feed.example.com",
                description="my first feed",
                entries=[
                  dict(title="my feed",
                  link="http://feed.example.com",
                  description="my first feed")
                ])

def BD_Apostila():

    #############seleciona os registros com informações
    print 'lendo antes de inserir'
    registros = db(db.minhatabela.meucampo!=None).select()
    for registro in registros:
        print registro.meucampo

    ############seleciona os registros com a palavra teste, porém só mostra no terminal
    minhaquery = (db.minhatabela.meucampo == 'pepino')
    # definir o conjunto de registros ' SELECT * FROM minhatabela where meucampo = 'Teste'
    conjunto = db(minhaquery)
    # executar o select acima e popula o objeto registros
    registros = conjunto.select()
    # alterar os registros 'UPDATE minhatabela set meucampo = 'Teste2' where meucampo = 'Teste'
    conjunto.update(meucampo='arroz')
    ##########################################################################
    print 'lendo depois de trocar'
    registros = db(db.minhatabela.meucampo!=None).select()
    for registro in registros:
        print registro.meucampo
    ############seleciona os registros com a palavra arroz, porém só mostra no terminal
    minhaquery2 = (db.minhatabela.meucampo == 'verde')
    # definir o conjunto de registros ' SELECT * FROM minhatabela where meucampo = 'Teste'
    conjunto2 = db(minhaquery2)
    # executar o select acima e popula o objeto registros
    registros2 = conjunto2.select()
    # deletar os registros 'DELETE FROM minhatabela where meucampo = 'Teste'
    conjunto2.delete()
    ##########################################################################
    print 'lendo depois de deletar'
    registros = db(db.minhatabela.meucampo!=None).select()
    for registro in registros:
        print registro.meucampo
    ##########################################################################

    ##################
    print 'lendo na minhaordem'
    minhaordem = db.minhatabela.meucampo.upper() | db.minhatabela.id
    registro = db().select(db.minhatabela.ALL, orderby=minhaordem)
    for registro in registros:
        print registro.meucampo
    ###########Adicionando um elemento no form/db############################
    meucampo_input=INPUT(_name='meucampo', requires=IS_NOT_EMPTY(error_message='você deve informar algo'))
    table_rows = []
    table_rows.append(TR('Meu campo:',meucampo_input))
    table_rows.append(TR(TD(INPUT(_type='submit'),colspan='2',align='center')))
    table=TABLE(table_rows)

    form_db = FORM(table)

    if form_db.accepts(request,session):
        form_meucampo = form_db.vars.meucampo
        db.minhatabela.insert(meucampo=form_meucampo)
        response.flash = 'tabela:'+ form_meucampo
    elif form_db.errors:
        response.flash = 'form errors'
    else:
        response.flash = 'please fill the form'

    ##########################adicionando um elemento SQLFORM/db
    form99=SQLFORM(db.minhatabela)
    ##########################################################################

    print 'lendo depois de inserir'
    registros = db(db.minhatabela.meucampo!=None).select()
    for registro in registros:
        print registro.meucampo
    ##########################################################################

    print 'Inserindo mais dados'
    db.minhatabela.insert(meucampo = 'verde')
    print 'lendo depois de inserir'
    registros = db(db.minhatabela.meucampo!=None).select()
    for registro in registros:
        print registro.meucampo

    print 'Inserindo muitos dados'
    maisdados = [{'meucampo':'azul'},
                 {'meucampo':'amarelo'},
                 {'meucampo':'pepino'}
                ]

    #############falta o código

    query = db.minhatabela.meucampo != 'verde'

    conjunto = db(query)
    registros = conjunto.select()

    print 'lendo query'

    for registro in registros:
        print registro.meucampo

    meuregistro = db.minhatabela(10)
    print meuregistro

    meuregistro = db.minhatabela(db.minhatabela.id == 10 )
    print meuregistro

    meuregistro = db.minhatabela(10,meucampo='laranja')
    print meuregistro

    print 'Orderby'
    for registro in db().select(db.minhatabela.ALL, orderby=db.minhatabela.meucampo):
        print registro.meucampo

    print 'query multipla'
    for registro in db((db.minhatabela.meucampo=='laranja')|(db.minhatabela.meucampo=='verde')).select():
        print registro.meucampo

    print db(db.minhatabela.id>0).count()

    print 'alterar campo'
    teste = db.minhatabela(10)
    print teste.meucampo
    teste.meucampo = 'rosa'
    print teste.meucampo

    print 'alterando todos'
    teste = db().select(db.minhatabela.ALL)
    for test in teste:
        test.update(meucampo='estragou')

    for registro in teste:
        print registro.meucampo

    return dict(form_db_table=form_db, registros=registros, form99=form99)


