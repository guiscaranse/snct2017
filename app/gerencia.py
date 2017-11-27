import csv, os, shutil, random, string, hashlib
import pdfkit


class Controle(object):
    dados = os.path.dirname(os.path.realpath(__file__)) + "/static/manha.csv"
    manha = os.path.dirname(os.path.realpath(__file__)) + "/static/manha.csv"
    noite = os.path.dirname(os.path.realpath(__file__)) + "/static/noite.csv"
    inscritos = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
    def verificaCadastro(self, cpf, cod):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        with open(self.dados, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if cod in row['Atividade'] and cpf in row['CPF']:
                    raise Exception("já está cadastrado em " + row['Atividade'])
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
            if cpf in i:
                if cod not in i:
                    f.write(i)
            else:
                f.write(i)
        f.truncate()
        f.close()
    def deletaTodasAtividades(self, cpf):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        out = os.path.dirname(os.path.realpath(__file__)) + "/static/" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + ".csv"
        f = open(dados,"r+", encoding="utf8")
        d = f.readlines()
        f.seek(0)
        for i in d:
            print(i)
            if str(cpf) not in i:
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
                    if str(ativ[1]) == "":
                        vagas_disp = 999999999999999
                    else:
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
        shutil.move(nova, self.inscritos)
    def checaCadastro(self, cod, cpf):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        relacao = []
        ins = []
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
                    if str(ativ[1]) == "":
                        vagas_disp = 999999999999999
                    else:
                        vagas_disp = int(ativ[1])
                    esgotou = False
                    for row in reader:
                        if ativ[0] in row['Atividade']:
                            if len(ins)+1 < vagas_disp:
                                ins.append(row['CPF'])
        if(cpf in ins):
            return True
        else:
            return False
    def listaInscritos(self, cod):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        relacao = []
        ins = []
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
                    if str(ativ[1]) == "":
                        vagas_disp = 999999999999999
                    else:
                        vagas_disp = int(ativ[1])
                    esgotou = False
                    for row in reader:
                        if ativ[0] in row['Atividade']:
                            if len(ins)+1 < vagas_disp + 3:
                                ins.append([row['Nome'], row['Email\\n']])
            return ins

    def getNome(self, cod):
        self.dados = os.path.dirname(os.path.realpath(__file__)) + "/static/inscritos.csv"
        relacao = []
        nome = ""
        with open(self.manha, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    codigo = row['Código']
                    vaga = row['Vagas']
                    nome = row['Nome']
                    relacao.append([codigo, vaga, nome])
        with open(self.noite, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                    codigo = row['Código']
                    nome = row['Nome']
                    relacao.append([codigo, vaga, nome])
        for ativ in relacao:
            if str(ativ[0]) == str(cod):
                nome = ativ[2]
        return nome
    def buscaCertDisponiveisPorInscrito(self):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/certificados.csv"
        resposta = []
        with open(dados, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if str(row['Nome']) not in resposta:
                    resposta.append(row['Nome'])
        return resposta
    def buscaCertDisponiveisPorNome(self, nome):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/certificados.csv"
        resposta = []
        with open(dados, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if nome in str(row['Nome']):
                    print()
                    resposta.append([row['Atividade'], hashlib.sha224(bytes(row['Nome']+row['Atividade'], encoding='utf-8')).hexdigest()])
        return resposta
    def geraArquivosCertificados(self):
        dados = os.path.dirname(os.path.realpath(__file__)) + "/static/certificados.csv"
        cert_folder = os.path.dirname(os.path.realpath(__file__)) + "/static/vendor/certificados/"
        cert_model = os.path.dirname(os.path.realpath(__file__)) + "/static/modelo.svg"
        cert_model_html = os.path.dirname(os.path.realpath(__file__)) + "/static/modelo.html"
        with open(dados, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                h = hashlib.sha224(bytes(row['Nome']+row['Atividade'], encoding='utf-8')).hexdigest()
                shutil.copyfile(cert_model, os.path.join(cert_folder, h + ".svg"))
                shutil.copyfile(cert_model_html, os.path.join(cert_folder, h + ".html"))
                replacements = {'[TIPO]':str(row['Tipo']), '[NOME]':str(row['Nome']), '[ATIVIDADE]':str(row['Atividade']), '[CH]':str(row['Carga Horaria'])}
                lines = []
                with open(os.path.join(cert_folder, h + ".svg"), encoding='utf8') as infile:
                    for line in infile:
                        for src, target in replacements.items():
                            line = line.replace(src, target)
                        lines.append(line)
                with open(os.path.join(cert_folder, h + ".svg"), 'w', encoding='utf8') as outfile:
                    for line in lines:
                        outfile.write(line)
                lines = []
                with open(os.path.join(cert_folder, h + ".html"), encoding='utf8') as infile:
                    for line in infile:
                        line = line.replace("modelo.svg", h + ".svg")
                        lines.append(line)
                with open(os.path.join(cert_folder, h + ".html"), 'w', encoding='utf8') as outfile:
                    for line in lines:
                        outfile.write(line)
        print("Gerado certificados")
