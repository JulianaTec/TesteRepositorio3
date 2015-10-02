# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'jjp@j.com>'
response.meta.description = 'descrevendo'
response.meta.keywords = 'palavra,chave'
response.meta.generator = 'Web2py Web Framework - juliana'

#response.title = request.application
response.title = 'nome do site'
response.subtitle = 'subtitulo'


## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('teste'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        #(T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('Menu_1'), False, URL('admin', 'default', 'site')),
          #(T('This App'), False, '#', [
          (T('Menu_2'), False, '#', [
             # (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
             (T('sub menu 1'), False, URL('admin', 'default', 'design/%s' % app)),
              LI(_class="divider"),
              (T('Controller'), False,URL('admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
              LI(_class="divider"),
              (T('View'), False,URL('admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
              (T('DB Model'), False,URL('admin', 'default', 'edit/%s/models/db.py' % app)),
              (T('Menu Model'), False,URL('admin', 'default', 'edit/%s/models/menu.py' % app)),
              (T('Config.ini'), False,URL('admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
              (T('Layout'), False,URL('admin', 'default', 'edit/%s/views/layout.html' % app)),
              (T('Stylesheet'), False,URL('admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
              (T('Database'), False, URL(app, 'appadmin', 'index')),
              (T('Errors'), False, URL('admin', 'default', 'errors/' + app)),
              (T('About'), False, URL('admin', 'default', 'about/' + app)),
              ]),
          ('Menu 3', False, '#', [
             (T('Download'), False,'http://www.web2py.com/examples/default/download'),
             (T('Support'), False,'http://www.web2py.com/examples/default/support'),
             (T('Demo'), False, 'http://web2py.com/demo_admin'),
             (T('Quick Examples'), False,'http://web2py.com/examples/default/examples'),
             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
             (T('Videos'), False,'http://www.web2py.com/examples/default/videos/'),
             (T('Free Applications'),False, 'http://web2py.com/appliances'),
             (T('Plugins'), False, 'http://web2py.com/plugins'),
             (T('Recipes'), False, 'http://web2pyslices.com/'),
             ]),
          (T('Documentation'), False, '#', [
             (T('Online book'), False, 'http://www.web2py.com/book'),
             LI(_class="divider"),
             (T('Preface'), False,'http://www.web2py.com/book/default/chapter/00'),
             (T('Introduction'), False,'http://www.web2py.com/book/default/chapter/01'),
             (T('Python'), False,'http://www.web2py.com/book/default/chapter/02'),
             (T('Overview'), False,'http://www.web2py.com/book/default/chapter/03'),
             (T('The Core'), False,'http://www.web2py.com/book/default/chapter/04'),
             (T('The Views'), False,'http://www.web2py.com/book/default/chapter/05'),
             (T('Database'), False,'http://www.web2py.com/book/default/chapter/06'),
             (T('Forms and Validators'), False,'http://www.web2py.com/book/default/chapter/07'),
             (T('Email and SMS'), False,'http://www.web2py.com/book/default/chapter/08'),
             (T('Access Control'), False,'http://www.web2py.com/book/default/chapter/09'),
             (T('Services'), False,'http://www.web2py.com/book/default/chapter/10'),
             (T('Ajax Recipes'), False,'http://www.web2py.com/book/default/chapter/11'),
             (T('Components and Plugins'), False,'http://www.web2py.com/book/default/chapter/12'),
             (T('Deployment Recipes'), False,'http://www.web2py.com/book/default/chapter/13'),
             (T('Other Recipes'), False,'http://www.web2py.com/book/default/chapter/14'),
             (T('Helping web2py'), False,'http://www.web2py.com/book/default/chapter/15'),
             (T("Buy web2py's book"), False,'http://stores.lulu.com/web2py'),
             ]),
          (T('Community'), False, None, [
             (T('Groups'), False,'http://www.web2py.com/examples/default/usergroups'),
              (T('Twitter'), False, 'http://twitter.com/web2py'),
              (T('Live Chat'), False,'http://webchat.freenode.net/?channels=web2py'),
              ]),
          (T('menu da ju'), False, None, [
              (T('pagina 1'), False,'http://127.0.0.1:8000/site_one/default/second'),
              (T('pagina 2'), False,'http://127.0.0.1:8000/site_one/default/second'),
              (T('pagina wiki'), False,'http://127.0.0.1:8000/site_one/default/wiki'),
              (T('pagina wikidemo'), False,'http://127.0.0.1:8000/site_one/default/wikidemo'),
              (T('return all local var'), False,URL("default","all_locals_var")),
              (T('teste2'), False,URL("default","teste2")),
              (T('return dic'), False,'http://127.0.0.1:8000/site_one/default/dic_return'),
              (T('return helper'), False,'http://127.0.0.1:8000/site_one/default/helper_return'),
              (T('return http'), False,'http://127.0.0.1:8000/site_one/default/http_return'),
              (T('return redirect'), False,'http://127.0.0.1:8000/site_one/default/redirect'),
              (T('return string'), False,'http://127.0.0.1:8000/site_one/default/string_return'),
              (T('teste de view'), False,'http://127.0.0.1:8000/site_one/default/test_view'),
              (T('teste de layout'), False,'http://127.0.0.1:8000/site_one/default/test_layout'),
              (T('teste de layout2'), False,'http://127.0.0.1:8000/site_one/default/view_teste2'),
              (T('teste de Banco de Dados'), False,'http://127.0.0.1:8000/site_one/default/bancoDados'),
              (T('teste de form'), False,'http://127.0.0.1:8000/site_one/default/TestForm'),
              (T('sql form'), False,'http://127.0.0.1:8000/site_one/default/sqlform'),
              (T('two forms'), False,'http://127.0.0.1:8000/site_one/default/two_forms'),
              (T('display forms'), False,'http://127.0.0.1:8000/site_one/default/display_form'),
              (T('display forms2'), False,'http://127.0.0.1:8000/site_one/default/display_form2'),
              (T('display forms3'), False,'http://127.0.0.1:8000/site_one/default/display_form3'),
              (T('data teste'), False,'http://127.0.0.1:8000/site_one/default/data_teste'),

              LI(_class="divider"),
              (T('retorna'), False,'http://127.0.0.1:8000/site_one/default/index'),
          ])
        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
