import csv, os, shutil, random, string
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
    def buscaAtividades(self, cpf):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        resposta = []
        with open(dados) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if cpf in str(row['CPF']):
                    resposta.append(row['Atividade'])
        return resposta
    def deletaAtividades(self, cpf):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        out = os.path.dirname(os.path.realpath(__file__)) + "/static/" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + ".csv"
        f = open(dados,"r+")
        d = f.readlines()
        f.seek(0)
        for i in d:
            print(i)
            if str(cpf) not in i:
                f.write(i)
        f.truncate()
        f.close()
