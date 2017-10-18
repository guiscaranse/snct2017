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
    error = [False, ""]
    try:
        for a in atividades:
            ctrl.verificaCadastro(cpf, a[:4])
        ctrl.cadastra(name, email, cpf, atividades)
    except Exception as e:
        error[0], error[1] = True, str(e)
    return render_template("subscribe.html", error = error)

@app.route('/find', methods=["POST"])
def find():
    ctrl = gerencia.Controle()
    cpf = request.form.get('cpf')
    aprovadas = []
    ativs = ctrl.buscaAtividades(cpf)
    for a in ativs:
        if(ctrl.checaCadastro(a[:4], cpf)):
            aprovadas.append(a[:4])
    return render_template("find.html", busca = ctrl.buscaAtividades(cpf), cpf = cpf, aprovadas = aprovadas)
@app.route('/deleta/<cpf>/<cod>', methods=["GET"])
def deleta(cpf, cod):
    ctrl = gerencia.Controle()
    ctrl.deletaAtividades(cpf, cod)
    return render_template("deleta.html", cod = cod)
@app.route('/deleta/duplicatas', methods=["GET"])
def deleta_dupli():
    ctrl = gerencia.Controle()
    ctrl.removeDuplicatas()
    return render_template("deleta.html", cod = "DUPLICATAS")
