import csv, os
from flask import jsonify
class Controle(object):
    dados = os.path.dirname(os.path.realpath(__file__)) + "/static/manha.csv"
    def atividadesPorDia(self, dia, turno):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/"+ turno +".csv"
        resposta = []
        with open(self.dados) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if dia in str(row['Data']):
                    nome = row['Nome']
                    if row['Nome'] == "":
                        nome = row['Código']
                    resposta.append([nome, row['Horário']])
        return resposta
    def listaAtividades(self):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/"+ turno +".csv"
        resposta = []
        with open(self.dados) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    nome = row['Nome']
                    if row['Nome'] == "":
                        nome = row['Código']
                    resposta.append([row['Código'], nome])
        return resposta
