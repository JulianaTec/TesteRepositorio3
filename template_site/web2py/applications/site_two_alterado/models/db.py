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
db.define_table('car_model',
                Field('car_model', type='string', label='Car Model', requires=IS_NOT_EMPTY()),
                Field('car_base_price', type='double', label='Base Price', requires=IS_NOT_EMPTY()))


db.define_table('vendor',
                Field('vendor_name', type='string', label='Name', requires=IS_NOT_EMPTY()),
                Field('vendor_birthday',type='date', label='Birthday', requires=IS_DATE()),
                Field('vendor_cpf', type='string', label='CPF'))

db.define_table('accessory',
                Field('accessory_name',  type='string', label='Accessory', requires=IS_NOT_EMPTY()),
                Field('accessory_price', type='double', label='Base Price', requires=IS_FLOAT_IN_RANGE(0,1000000)),
                Field('accessory_image_file', type='upload'))

db.define_table('sale',
                Field('car_id', 'reference car_model', label='Sale Car'),
                Field('vendor_id','reference vendor', label='Sale Vendor'),
                Field('sale_date', type='date', label='Date',requires=IS_DATE()),
                Field('sale_discount', type='integer', label='Discount', requires=IS_INT_IN_RANGE(0,100)),
                Field('sale_total_price', type='double', label='Total Price', requires=IS_NOT_EMPTY()))

db.sale.car_id.widget    = SQLFORM.widgets.autocomplete(request, db.car_model.car_model, id_field=db.car_model.id)
db.sale.vendor_id.widget = SQLFORM.widgets.autocomplete(request, db.vendor.vendor_name, id_field=db.vendor.id)

db.define_table('accessory_list',
                Field('sale_id','reference sale'),
                Field('accessory_id','reference accessory'))


db.define_table(
    'person',
    Field('name'),
    Field('email'),
    format = '%(name)s')

# ONE (person) TO MANY (products)

db.define_table(
    'product',
    Field('seller_id',db.person),
    Field('name'),
    Field('description', 'text'),
    Field('picture', 'upload', default=''),
    format = '%(name)s')

# MANY (persons) TO MANY (purchased)

db.define_table(
    'purchased',
    Field('buyer_id', db.person),
    Field('product_id', db.product),
    Field('quantity', 'integer'),
    format = '%(quantity)s %(product_id)s -> %(buyer_id)s')

purchased = (db.person.id==db.purchased.buyer_id)&(db.product.id==db.purchased.product_id)

db.person.name.requires = IS_NOT_EMPTY()
db.person.email.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'person.email')]
db.product.name.requires = IS_NOT_EMPTY()
db.purchased.quantity.requires = IS_INT_IN_RANGE(0, 10)

#brincando com uma tabela com o exemplo da aposti

db.define_table('minhatabela',
                Field('meucampo','string')
                )

db.minhatabela.notnull=True
db.minhatabela.required=True
db.minhatabela.meucampo.requires=IS_NOT_EMPTY()
db.minhatabela.defaul='Olá mundo'

db.minhatabela.meucampo.widget = SQLFORM.widgets.autocomplete(request,db.minhatabela.meucampo, id_field=db.minhatabela.meucampo)

db.define_table('numbers',
    Field('asa', 'integer'),
    Field('b', 'integer'),
    Field('casa', 'integer', readable=False, writable=False))

db.define_table('dog',Field('name'))

db.define_table('person4',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('married', 'boolean'),
    Field('gender', requires=IS_IN_SET(['Male', 'Female', 'Other'])),
    Field('profile', 'text'),
    Field('image_filename'),
    Field('image', 'upload',autodelete=True))

db.define_table('client',
     Field('name'))

db.define_table('address',
    Field('client','reference client',
          writable=False,readable=False),
    Field('street'),Field('city'))

db.define_table('category',Field('name'))
db.define_table('product2',Field('name'),Field('category'))
db.product2.category.widget = SQLFORM.widgets.autocomplete(request, db.category.name, limitby=(0,10), min_length=2)