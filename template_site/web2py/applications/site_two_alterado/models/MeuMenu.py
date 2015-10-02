__author__ = 'TecSUS-3'

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################


'''
Template para criar um  menu lateral independente do código padrão cheio de lixo do
web2py
'''

response.MeuMenu = [
    (T('Principal'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/Inicio'),
    (T('Cadastro de Comprador'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/comprador'),
    (T('Cadastro de Carro'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/carro'),
    (T('Cadastro de Vendedor'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/vendedor'),
    (T('Cadastro de Marca'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/marca'),
    (T('Admin'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/admin'),
    (T('Venda'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/venda'),
    (T('Contato'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/send_email'),
    (T('Login'), False, 'http://127.0.0.1:8000/site_two_alterado/Veiculo/meu_user')

    ]