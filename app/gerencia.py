import csv, os, shutil, random, string
from flask import jsonify
class Controle(object):
    dados = os.path.dirname(os.path.realpath(__file__)) + "/static/manha.csv"
    manha = os.path.dirname(os.path.realpath(__file__)) + "/static/manha.csv"
    noite = os.path.dirname(os.path.realpath(__file__)) + "/static/noite.csv"
    inscritos = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
    def atividadesPorDia(self, dia, turno):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/"+ turno +".csv"
        resposta = []
        with open(self.dados, encoding="utf8") as csvfile:
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
        with open(dadosManha, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    nome = row['Nome']
                    if row['Nome'] == "":
                        nome = row['Código']
                    if "AP" not in row['Código']:
                        resposta.append([row['Código'], nome, row['Data'] + " (" + row['Horário'] + ")"])
        with open(dadosNoite, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    nome = row['Nome']
                    if row['Nome'] == "":
                        nome = row['Código']
                    if "AP" not in row['Código']:
                        resposta.append([row['Código'], nome, row['Data'] + " (" + row['Horário'] + ")"])
        return resposta
    def cadastra(self, nome, email, cpf, ativs):
        with open(self.inscritos, 'a', newline='', encoding="utf8") as f:
            erros = []
            writer = csv.writer(f)
            if(len(ativs) > 0):
                for x in ativs:
                    if not self.checaVagas(x[:4]):
                        fields=[x, nome, cpf, email]
                        writer.writerow(fields)
                    else:
                        erros.append(x[:4])
            else:
                fields=["SEM ATIVIDADES", nome, cpf, email]
                writer.writerow(fields)
            if(len(erros) > 0):
                raise Exception("As seguintes atividades estão com vagas esgotadas: " + str(erros))
    def buscaAtividades(self, cpf):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        resposta = []
        with open(dados, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if cpf in str(row['CPF']):
                    resposta.append(row['Atividade'])
        return resposta
    def deletaAtividades(self, cpf, cod):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        out = os.path.dirname(os.path.realpath(__file__)) + "/static/" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + ".csv"
        f = open(dados,"r+", encoding="utf8")
        d = f.readlines()
        f.seek(0)
        for i in d:
            print(i)
            if str(cpf) not in i and str(cod) not in i:
                f.write(i)
        f.truncate()
        f.close()
    def checaVagas(self, cod):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        relacao = []
        with open(self.manha, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    codigo = row['Código']
                    vaga = row['Vagas']
                    relacao.append([codigo, vaga])
        with open(self.noite, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    codigo = row['Código']
                    vaga = row['Vagas']
                    relacao.append([codigo, vaga])
        with open(self.dados, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for ativ in relacao:
                if str(ativ[0]) == str(cod):
                    print(ativ)
                    print(ativ[1])
                    vagas_disp = int(ativ[1])
                    ins = []
                    esgotou = False
                    for row in reader:
                        if ativ[0] in row['Atividade']:
                            if len(ins)+1 < vagas_disp:
                                ins.append([row['Nome'], row['Email\\n']])
                            else:
                                esgotou = True
            return esgotou
    def removeDuplicatas(self):
        lines_seen = set()
        nova = os.path.dirname(os.path.realpath(__file__)) + "/nova.csv"
        outfile = open(nova, "w", encoding="utf8")
        for line in open(self.inscritos, "r", encoding="utf8"):
            if line not in lines_seen:
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        shutil.move(nova, self.dados)
