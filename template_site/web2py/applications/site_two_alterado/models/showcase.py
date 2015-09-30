__author__ = 'TecSUS-3'

# -*- coding: utf-8 -*-
def SHOWCASE(rows):
    """Creates a car showcase"""

    #Armazena a estrutura do HTML que será interpolado
    placeholder ="""
    <div class='vcarros' style='width:500px;border:1px solid gray;'>
        <div class='vcfoto' style='float:left;margin:10px;'>
            <a href='%(url)s'>

            </a>
        </div>
        <div class='vcdata' style='padding:10px;margin:10px;'>
            <span class='vcdtitle'>
                <strong>
                %(brand)s - %(model)s - %(year)s - %(status)s
                </strong>
            </span>
            <div style='padding: 10px 100px 1px;'>
            <ul class='vcdinfo'>
                <li>%(color)s</li>
                <li>%(status)s</li>
                <li>%(itens)s</li>
            <ul>
            <p class='vcdtext'>
                <blockquote>
                %(desc)s
                </blockquote>
            </p>
            <span class='vcdvalor'
                  style="float:right;color:blue;font-size:20px;">
                <strong>%(price)s</strong>
            </span>
        </div>
    </div>
    """

    #Caso existam registros em "rows" efetua a interpolação
    if rows:
        showcase = [placeholder % dict(url=URL('details', args=row.id),
                                    urlpict=URL('download',args=row.foto),
                                    brand=row.marca,
                                    model=row.modelo,
                                    year=row.ano,
                                    status=row.estado,
                                    color=row.cor,
                                    itens=' | '.join(row.itens),
                                    desc=row.desc,
                                    price=row.valor,
                                    ) for row in rows ]

    else:
        showcase = ["<h1 class='nothing'>No cars were found</h1>"]

    return showcase