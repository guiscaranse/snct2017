import csv, os
from flask import jsonify
class Controle(object):
    dados = os.path.dirname(os.path.realpath(__file__)) + "/static/manha.csv"
    inscritos = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
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
        dadosManha = os.path.dirname(os.path.realpath(__file__)) + "/static/manha.csv"
        dadosNoite = os.path.dirname(os.path.realpath(__file__)) + "/static/noite.csv"
        resposta = []
        with open(dadosManha) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    nome = row['Nome']
                    if row['Nome'] == "":
                        nome = row['Código']
                    if "AP" not in row['Código']:
                        resposta.append([row['Código'], nome, row['Data'] + " (" + row['Horário'] + ")"])
        with open(dadosNoite) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    nome = row['Nome']
                    if row['Nome'] == "":
                        nome = row['Código']
                    if "AP" not in row['Código']:
                        resposta.append([row['Código'], nome, row['Data'] + " (" + row['Horário'] + ")"])
        return resposta
    def cadastra(self, nome, email, cpf, ativs):
        with open(self.inscritos, 'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            if(len(ativs) > 0):
                for x in ativs:
                    fields=[x, nome, cpf, email]
            else:
                fields=["SEM ATIVIDADES", nome, cpf, email]        
            writer.writerow(fields)
