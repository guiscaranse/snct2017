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
    teste.geraArquivosCertificados()
    return render_template("index.html",
                            lista_ativ = sorted(teste.listaAtividades()),
                            nomes_certi = sorted(teste.buscaCertDisponiveisPorInscrito()))
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
@app.route('/lista/<cod>', methods=["GET"])
def lista(cod):
    ctrl = gerencia.Controle()
    return render_template("lista.html", cod = cod, nome = ctrl.getNome(cod), inscritos = ctrl.listaInscritos(cod))
@app.route('/lista', methods=["POST"])
def lista_uni():
    ctrl = gerencia.Controle()
    cod = request.form.get('atividades')[:4]
    return render_template("lista.html", cod = cod, nome = ctrl.getNome(cod), inscritos = ctrl.listaInscritos(cod))
@app.route('/certificados', methods=["POST"])
def certificados():
    ctrl = gerencia.Controle()
    nome = request.form.get('nome')
    return render_template("lista.html")
