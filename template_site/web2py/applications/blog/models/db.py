# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

import datetime

if auth.is_logged_in():
    user_id = auth.user.id
else:
    user_id = None

db.define_table(
        'categories',
        Field('category_name', required=True)
        )

db.define_table(
         'posts',
         Field('post_title',notnull=True,required=True,
               requires=[IS_NOT_EMPTY(error_message=T('Fill the field!')),
               IS_NOT_IN_DB(db, 'posts.post_title')]),
         Field('post_text', 'text'),
         Field('post_time', 'datetime', default=datetime.datetime.today()),
         Field('post_category',db.categories, required=True,
               requires = IS_IN_DB(db, 'categories.id', 'categories.category_name')),
         Field('author', db.auth_user, default=user_id)
)
db.define_table(
        'comments',
         Field('post_id', db.posts, required=True),
         Field('comment_author'),
         Field('comment_author_email', required=True),
         Field('comment_author_website'),
         Field('comment_text', 'text', required=True),
         Field('comment_time', 'datetime', required=True,
              default=datetime.datetime.today()),
         Field('approved','boolean')
               )

db.define_table(
        'documents',
        Field('post_id', db.posts, required=True),
        Field('name'),
        Field('file_doc', 'upload'),
        Field('created_on', 'datetime', default=request.now),
        Field('created_by', db.auth_user, default=user_id)
        )

db.posts.post_text.requires = IS_NOT_EMPTY()
db.posts.author.readable = False
db.posts.author.writable = False

db.comments.post_id.requires = IS_IN_DB(db, 'posts.id', '')
db.comments.comment_text.requires = IS_NOT_EMPTY()
db.comments.comment_author_email.requires = IS_EMAIL()
db.comments.comment_author_website.requires = IS_URL()
db.comments.post_id.readable = False
db.comments.post_id.writable = False

db.documents.post_id.requires = IS_IN_DB(db, 'posts.id', '')
db.documents.name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'documents.name')]
db.documents.post_id.readable = False
db.documents.post_id.writable = False
db.documents.created_by.readable = False
db.documents.created_by.writable = False
db.documents.created_on.readable = False
db.documents.created_on.writable = False


