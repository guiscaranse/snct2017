from functools import wraps
from app import app, gerencia
import random, string, sys
from flask import url_for, render_template, request, Response
'''
Routes
'''
@app.route('/', methods=['GET'])
def hello():
    teste = gerencia.Controle()
    print(teste.atividadesPorDia("26", "manha"), "\n")
    print(len(teste.atividadesPorDia("26", "manha")))
    return render_template("index.html",
                           manha_ter = teste.atividadesPorDia("24", "manha"),
                           manha_quar = teste.atividadesPorDia("25", "manha"),
                           manha_qui = teste.atividadesPorDia("26", "manha"),
                           manha_sex = teste.atividadesPorDia("27", "manha"))
