# -*- coding: utf-8 -*-

def database_lists_smartgrid():
    car_model_grid = SQLFORM.smartgrid(db.car_model)
    vendor_grid    = SQLFORM.smartgrid(db.vendor)
    accessory_grid = SQLFORM.smartgrid(db.accessory)
    sale_grid      = SQLFORM.smartgrid(db.sale)

    return locals()

def database_lists_grid():
    car_model_grid = SQLFORM.grid(db.car_model)
    vendor_grid    = SQLFORM.grid(db.vendor)
    accessory_grid = SQLFORM.grid(db.accessory)
    sale_grid      = SQLFORM.grid(db.sale)

    return locals()