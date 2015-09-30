# -*- coding: utf-8 -*-

####################################### IMPORTS #######################################
from gluon import A, INPUT, IS_NOT_EMPTY, SQLFORM, URL, TR, TABLE, FORM, IS_LIST_OF, IS_IN_DB, redirect
from gluon import Field


####################################### GLOBALS #######################################
global request, session, db, response


####################################### ACTIONS #######################################
def car_model_form():
    """
    Creates a form using web2py helpers.

    This is the most manual method of creating a form. It allows
    the specification of every aspect of the resulting html
    elements.

    Some notes:
        Validators must be specified during the INPUT fields creation.
        form.accepts() must be called to process the form.
        Database insertion must be handled manually.
    """

    # Must repeat the field validators declared in the db.py
    car_model_input=INPUT(_name='car_model', requires=IS_NOT_EMPTY())
    base_price_input=INPUT(_name='base_price', requires=IS_NOT_EMPTY())

    # Manual creation of the html table
    table_rows = []
    table_rows.append(TR('Car Model:', car_model_input))
    table_rows.append(TR('Base Price:', base_price_input))
    # Fields starting with _ are passed to the html as attribute elements
    table_rows.append(TR(TD(INPUT(_type='submit'), _colspan='2', _align='center')))
    table = TABLE(table_rows)

    form = FORM(table)

    # Processing the form submition
    if form.accepts(request,session):
        # Retriving the form fields
        form_car_model = form.vars.car_model
        form_base_price = form.vars.base_price
        # Inserting in the database
        db.car_model.insert(car_model=form_car_model, car_base_price=form_base_price)
        # Tell the user about the insertion
        response.flash = 'New car: ' + form_car_model
    elif form.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill the form'

    return dict(car_model_form=form)


def vendor_sqlform():
    """
    Create a simple form using the SQLFORM function of web2py.

    Some notes:
        The accepts function validates each field and write the results to de database.
    """

    vendor_sqlform = SQLFORM(db.vendor)

    if vendor_sqlform.accepts(request,session):
        response.flash = 'Form accepted'
    elif vendor_sqlform.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill the form'

    return locals()


def accessory_crud():
    """ Create a simple form using the CRUD function of web2py. """

    from gluon.tools import Crud
    crud = Crud(db)
    accessory_crud = crud.create(db.accessory)
    return locals()


def sale_sqlform_factory():
    """
    Create a custom form using SQLFORM.factory and custom widgets.

    This action creates a form based on the sale table but it also includes a
    wrapper field which can hold one of the following:
        A link to a grid that allows the user to select accessories to include in the sale.
        A grid holding the selected accessories.

    The ids of the selected accessories are passed in the request.
    """

    accessory_wrapper_field = Field('IncludedAccessories',widget=custom_accessory_widget, type='boolean')
    sale_sqlform_factory    = SQLFORM.factory(db.sale, accessory_wrapper_field)

    if sale_sqlform_factory.process().accepted:
        sale_id = db.sale.insert(**db.sale._filter_fields(sale_sqlform_factory.vars))
        insert_accessories(sale_id, request.vars.id)
	#TODO request.clear()
        response.flash = 'Record inserted'

    return locals()


####################################### FUNCTIONS #######################################

### Grid Functions ###
def build_accessories_grid(query, extra_parameters):
    default_parameters = {
        'fields':     [db.accessory.accessory_name, db.accessory.accessory_price],
        'csv':        False,
        'details':    False,
        'searchable': False
    }

    parameters = merge_dicts(default_parameters, extra_parameters)

    grid = SQLFORM.grid(query, **parameters)
    remove_grid_counter(grid)

    return grid


def accessories_grid_selectable():
    query  = db.accessory
    params = {
        'selectable_submit_button': 'Include',
        'selectable': lambda ids : redirect(URL('forms', 'sale_sqlform_factory', vars=dict(id=ids)))
    }

    accessories_grid_selectable = build_accessories_grid(query, params)

    return locals()


def accessories_grid_from_ids(accessories_ids):
    query  = db.accessory.id.belongs(accessories_ids)
    params = {}

    grid   = build_accessories_grid(query, params)
    link   = change_accessories_link()

    grid.append(link)

    return grid

### Auxiliary Functions ###
def fetch_id_list():
    id_list = request.vars.id
    if isinstance(id_list,str):
            id_list = [id_list]
    return id_list


def remove_grid_counter(grid):
    del grid[0][0]


def merge_dicts(dict1, dict2):
    resulting_dict = dict1.copy()
    resulting_dict.update(dict2)

    return resulting_dict


### Html Helper Functions ###
def accessory_bt():
    return A('Add Accessories', _href='accessories_grid_selectable')


def change_accessories_link():
    return A('Change Accessories', _href='accessories_grid_selectable')


### Custom Widgets ###
def custom_accessory_widget(field,value):
    accessories_ids=fetch_id_list()

    if accessories_ids:
        return accessories_grid_from_ids(accessories_ids)
    else:
        return accessory_bt()


### Database Functions ###
def insert_accessories(sale_id, accessories_ids):
    if not accessories_ids:
        return

    if isinstance(accessories_ids,str):
        accessories_ids = [accessories_ids]

    for accessory_id in accessories_ids:
        db.accessory_list.insert(sale_id=sale_id, accessory_id=accessory_id)

    return
