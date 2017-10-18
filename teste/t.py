import os,csv
def buscaInscritos(cod):
    dados = os.path.dirname(os.path.realpath(__file__)) + "/inscritos.csv"
    manha = os.path.dirname(os.path.realpath(__file__)) + "/manha.csv"
    noite = os.path.dirname(os.path.realpath(__file__)) + "/noite.csv"
    relacao = []
    with open(manha, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                codigo = row['Código']
                vaga = row['Vagas']
                relacao.append([codigo, vaga])
    with open(noite, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                codigo = row['Código']
                vaga = row['Vagas']
                relacao.append([codigo, vaga])
    with open(dados, encoding="utf8") as csvfile:
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
                        if len(ins) < vagas_disp:
                            ins.append([row['Nome'], row['Email\\n']])
                        else:
                            esgotou = True
                print(ins)
                print("ESGOTOU?", esgotou)
buscaInscritos("MC08")
