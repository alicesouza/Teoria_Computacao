import re
import copy
from visual_automata.fa.nfa import VisualNFA
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def table(f):

    lines = f.readlines()
    ler = lines[0].split()
    nfa_enfa = {}
    inicio = None
    for line in lines[1:]:
        line = line.split()
        ehFinal = False
        if re.search(r"(\*)", line[0]):
            line[0] = line[0].replace("*", "")
            ehFinal = True

        if re.search(r"(\>)", line[0]):
            line[0] = line[0].replace(">", "")
            inicio = line[0]

        nfa_enfa[line[0]] = {}
        nfa_enfa[line[0]]["ehFinal"] = ehFinal
        nfa_enfa[line[0]]["estados"] = {}

        for i, l in enumerate(line[1:]):
            l = l.replace("{", "").replace("}", "")

            if "," in l:
                l = l.split(",")
                for state in l:
                    nfa_enfa[line[0]]["estados"][state] = []
            elif l != "":
                nfa_enfa[line[0]]["estados"][l] = []

        for i, l in enumerate(line[1:]):
            l = l.replace("{", "").replace("}", "")

            if "," in l:
                l = l.split(",")
                for state in l:
                    nfa_enfa[line[0]]["estados"][state].append(ler[i])
            elif l != "":
                nfa_enfa[line[0]]["estados"][l].append(ler[i])

    return inicio, nfa_enfa, ler

def search(nfa_enfa, estado, s, enfa):
    keys = nfa_enfa[estado]["estados"].keys()
    estados = []
    for key in keys:
        le = nfa_enfa[estado]["estados"][key]
        if enfa:
            if s in le or '&' in le:
                estados.append(key)
        else:
            if s in le:
                estados.append(key)

    return estados

def verifica(string, inicio, nfa_enfa, enfa = False):
    cont = 0
    caminhos = {}
    caminhos[cont] = {"caminho": [inicio],
                      "achou": True}

    for s in string:
        keys = caminhos.keys()
        for key in list(keys):
            if caminhos[key]["achou"]:
                estado = caminhos[key]["caminho"][-1]
                estados = search(nfa_enfa, estado, s, enfa)

                if len(estados) > 1:
                    caminho = copy.deepcopy(caminhos[key])
                    caminhos[key]["caminho"].append(estados[0])
                    for est in estados[1:]:
                        cont+=1
                        caminhos[cont] = caminho
                        caminhos[cont]["caminho"].append(est)

                elif len(estados) == 1:
                    caminhos[key]["caminho"].append(estados[0])
                elif estados == []:
                    caminhos[key]["achou"] = False

            # print("Caminhos: ", caminhos)

    keys = caminhos.keys()
    achou = False
    respostas = []
    for key in keys:
        estado = caminhos[key]["caminho"][-1]
        if caminhos[key]['achou'] and nfa_enfa[estado]["ehFinal"]:
            achou = True
            respostas.append(caminhos[key]["caminho"])

    if achou:
        return "aceita", respostas
    else:
        return "nao aceita"

def grafo(table, inicio, simbolos, title):
    estados = list(table.keys())
    estadosFinais = set([est for est in estados if table[est]['ehFinal']])
    estados = set(estados)
    simbolos = set(simbolos)
    transicoes = dict()

    for est in estados:
        transicoes[est] = {}
        estadosSeguintes = list(table[est]['estados'].keys())
        for seguinte in estadosSeguintes:
           symbles = table[est]['estados'][seguinte]
           for symble in symbles:
               try:
                   transicoes[est][symble].add(seguinte)
               except:
                   transicoes[est][symble] = {seguinte}

    dfa = VisualNFA(
        states=estados,
        input_symbols=simbolos,
        transitions=transicoes,
        initial_state=inicio,
        final_states=estadosFinais,
    )

    dfa.show_diagram(filename="./NFA/nfa")
    img = mpimg.imread('./NFA/nfa.png')
    imgplot = plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.show()


def mainNFA():
    print("\n--------NFA--------")
    #abre tabela nfa
    file = open("./NFA/tabelaTransicaoNFA.txt", "r")
    inicio, nfa_enfa, simbolos = table(file)
    # print(inicio)
    # print(nfa_enfa)
    grafo(nfa_enfa, inicio, simbolos, "Automato NFA")
    f = open("./NFA/stringsNFA.txt", "r")
    lines = f.readlines()
    for string in lines:
        string = string.strip()
        print("\n")
        print("entrada: ",string)
        print(verifica(string, inicio, nfa_enfa))


# mainNFA()

