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
db = DAL("sqlite://storage.sqlite")

db.define_table('image',
   Field('title', unique=True),
   Field('file', 'upload'),
   format = '%(title)s')

db.define_table('post',
   Field('image_id', 'reference image'),
   Field('author'),
   Field('email'),
   Field('body', 'text'))

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.post.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.post.author.requires = IS_NOT_EMPTY()
db.post.email.requires = IS_EMAIL()
db.post.body.requires = IS_NOT_EMPTY()

db.post.image_id.writable = db.post.image_id.readable = False

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)

from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('page',
    Field('title'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(title)s')

db.define_table('post2',
    Field('page_id', 'reference page'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id))

db.define_table('document',
    Field('page_id', 'reference page'),
    Field('name'),
    Field('file', 'upload'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(name)s')

db.page.title.requires = IS_NOT_IN_DB(db, 'page.title')
db.page.body.requires = IS_NOT_EMPTY()
db.page.created_by.readable = db.page.created_by.writable = False
db.page.created_on.readable = db.page.created_on.writable = False

db.post2.body.requires = IS_NOT_EMPTY()
db.post2.page_id.readable = db.post2.page_id.writable = False
db.post2.created_by.readable = db.post2.created_by.writable = False
db.post2.created_on.readable = db.post2.created_on.writable = False

db.document.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.document.page_id.readable = db.document.page_id.writable = False
db.document.created_by.readable = db.document.created_by.writable = False
db.document.created_on.readable = db.document.created_on.writable = False

db.define_table('mytable', Field('myfield'))
rows = db(db.mytable.myfield!=None).select()

for row in rows:
    print row.myfield

myquery = (db.mytable.myfield != None) | (db.mytable.myfield > 'A')

myset = db(myquery)
rows = myset.select()
myset.update(myfield='somevalue')
myset.delete()

myorder = db.mytable.myfield.upper() | db.mytable.id
db().select(db.mytable.ALL, orderby=myorder)

db.mytable.myfield.extra = {}

db.mytable._extra = {}

db.define_table('person',Field('name',default='',requires=IS_NOT_EMPTY()),format='%(name)s')
db.person._format = '%(name)s/%(id)s'
db.person.name.default = 'anonymous'
db.executesql('CREATE INDEX IF NOT EXISTS myidx ON person (name);')

db.person.insert(name="Alex")
db.person.insert(name="Bob")
db.person.truncate()
db.person.insert(name="Alex")
db.person.bulk_insert([{'name':'Alex'}, {'name':'John'}, {'name':'Tim'}])

db.person.insert(name="Bob")
db.rollback()

db.executesql('SELECT * FROM person;')

db.person.insert(name="Alex")
db.person.insert(name="Bob")
db.person.insert(name="Carl")


person = db.person

name = person.name

q = name=='Alex'
s = db(q)

rows = s.select()
for row in rows:
    print row.id, row.name

for row in db(db.person.name=='Alex').select():
    print row.name

for row in db().select(db.person.id, db.person.name):
    print row.name

for row in db().select(db.person.ALL):
    print row.name

for row in db(db.person.id > 0).select():
    print row.name


row.name
row['name']
row('person.name')

for row in db().select(db.person.ALL, orderby=db.person.name):
        print row.name

for row in db().select(db.person.ALL, orderby=db.person.name):
        print row.name

for row in db().select(
        db.person.ALL, orderby=~db.person.name):
        print row.name

for row in db().select(
        db.person.ALL, orderby='<random>'):
        print row.name

for row in db().select(db.person.ALL, limitby=(0, 2)):
        print row.name

rows = db((db.person.name=='Alex') & (db.person.id>3)).select()
for row in rows: print row.id, row.name

rows = db((db.person.name=='Alex') | (db.person.id>3)).select()
for row in rows: print row.id, row.name

rows = db(~(db.person.name=='Alex') | (db.person.id>3)).select()
for row in rows: print row.id, row.name

print db(db.person.id > 0).count()

print db(db.person.id > 0).isempty()

print db(db.person).isempty()

db(db.person.id > 3).delete()

db(db.person.id > 3).update(name='Ken')

rows = db().select(db.person.ALL)
print db._lastsql


db.define_table('myfile',Field('image', 'upload', uploadfield='image_file'),Field('image_file', 'blob'))

for row in db().select(db.person.ALL, orderby=db.person.name):
        print row.name

db.define_table('person2',Field('name'),Field('visits', 'integer', default=0))
db(db.person2.name == 'Massimo').update(visits = db.person2.visits + 1)

condition = db.person.name.startswith('M')
yes_or_no = condition.case('Yes','No')
for row in db().select(db.person.name, yes_or_no):
     print row.person.name,  row(yes_or_no)

db.define_table('log', Field('event'),Field('event_time', 'datetime'),Field('severity', 'integer'))

import datetime
now = datetime.datetime.now()
print db.log.insert(event='port scan', event_time=now, severity=1)
print db.log.insert(event='xss injection', event_time=now, severity=2)
print db.log.insert(event='unauthorized login', event_time=now, severity=3)

db.define_table('item',
Field('unit_price','double'),
Field('quantity','integer'),
Field('total_price',
compute=lambda r: r['unit_price']*r['quantity']))
r = db.item.insert(unit_price=1.99, quantity=5)
print r.total_price

db.define_table('product',Field('name'),  Field('colors','list:string'))
db.product.colors.requires=IS_IN_SET(('red','blue','green'))
db.product.insert(name='Toy Car',colors=['red','green'])
products = db(db.product.colors.contains('red')).select()
for item in products:
     print item.name, item.colors


db.define_table('sysuser',Field('username'),Field('fullname'))
db.sysuser.insert(username='max',fullname='Max Power')
db.sysuser.insert(username='tim',fullname=None)
print db(db.sysuser).select(db.sysuser.fullname.coalesce(db.sysuser.username))

db.define_table('sysuser2',Field('username'),Field('points'))
db.sysuser2.insert(username='max',points=10)
db.sysuser2.insert(username='tim',points=None)
print db(db.sysuser2).select(db.sysuser2.points.coalesce_zero().sum())

db = DAL('sqlite:memory:')
db.define_table('person',
    Field('name'),
    format='%(name)s')
db.define_table('thing',
    Field('owner_id', 'reference person'),
    Field('name'),
    format='%(name)s')

if not db(db.person).count():
    id = db.person.insert(name="Massimo")
    db.thing.insert(owner_id=id, name="Chair")

db.define_table('purchase', Field('have_coupon','boolean'),Field('coupon_code'))

db.define_table('numbers',
    Field('a', 'integer'),
    Field('b', 'integer'),
    Field('c', 'integer', readable=False, writable=False))

db.define_table('person3',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('married', 'boolean'),
    Field('gender', requires=IS_IN_SET(['Male', 'Female', 'Other'])),
    Field('profile', 'text'),
    Field('image', 'upload'))


from gluon.tools import Crud
crud = Crud(db)

