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
    return render_template("index.html",
                           manha_ter = teste.atividadesPorDia("24", "manha"),
                           manha_quar = teste.atividadesPorDia("25", "manha"),
                           manha_qui = teste.atividadesPorDia("26", "manha"),
                           manha_sex = teste.atividadesPorDia("27", "manha"),
                           noite_seg = teste.atividadesPorDia("23", "noite"),
                           noite_ter = teste.atividadesPorDia("24", "noite"),
                           noite_quar = teste.atividadesPorDia("25", "noite"),
                           lista_ativ = sorted(teste.listaAtividades()))
@app.route('/subscribe', methods=["POST"])
def subscribe():
    ctrl = gerencia.Controle()
    email = request.form.get('email')
    name = request.form.get('name')
    atividades = request.form.getlist('atividades')
    cpf = request.form.get('cpf')
    ctrl.cadastra(name, email, cpf, atividades)
    return render_template("subscribe.html")

@app.route('/find', methods=["POST"])
def find():
    ctrl = gerencia.Controle()
    cpf = request.form.get('cpf')
    return render_template("find.html", busca = ctrl.buscaAtividades(cpf), cpf = cpf)
@app.route('/deleta/<int:cpf>', methods=["GET"])
def deleta(cpf):
    ctrl = gerencia.Controle()
    ctrl.deletaAtividades(cpf)
    return render_template("deleta.html")
