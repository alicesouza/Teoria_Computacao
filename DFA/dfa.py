import re
from visual_automata.fa.dfa import VisualDFA
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def table():
    f = open("./DFA/tabelaTransicaoDFA.txt", "r")
    lines = f.readlines()
    ler = lines[0].split()
    dfa = {}
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

        dfa[line[0]] = {}
        dfa[line[0]]["ehFinal"] = ehFinal
        dfa[line[0]]["estados"] = {}

        for i, l in enumerate(line[1:]):
            dfa[line[0]]["estados"][l] = []
        for i, l in enumerate(line[1:]):
            dfa[line[0]]["estados"][l].append(ler[i])

    return inicio, dfa, ler

def verifica(string, inicio, dfa):
    estado = inicio
    caminho = []
    caminho.append(estado)
    for s in string:
        keys = dfa[estado]["estados"].keys()
        for key in keys:
            achou = False
            le = dfa[estado]["estados"][key]
            if s in le:
                achou = True
                estado2 = key
            if achou:
                estado = estado2
                caminho.append(estado)
                break

        if not achou:
            return "não aceita"


    if dfa[estado]["ehFinal"]:
        return "aceita", caminho
    else:
        return "não aceita"

def grafo(table, inicio, simbolos):
    estados = list(table.keys())
    estadosFinais = set([est for est in estados if table[est]['ehFinal']])
    estados = set(estados)
    simbolos = set(simbolos)
    transicoes = dict()

    for est in estados:
        transicoes[est] = {}
        estadosSeguintes = list(table[est]['estados'].keys())
        for seguinte in estadosSeguintes:
            transicoes[est][table[est]['estados'][seguinte][0]] = seguinte

    dfa = VisualDFA(
        states=estados,
        input_symbols=simbolos,
        transitions=transicoes,
        initial_state=inicio,
        final_states=estadosFinais,
    )

    dfa.show_diagram(filename="./DFA/dfa")
    img = mpimg.imread('./DFA/dfa.png')
    imgplot = plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.title("Automato DFA")
    plt.show()

def mainDFA():
    print("\n--------DFA--------")
    f = open("./DFA/stringsDFA.txt", "r")
    lines = f.readlines()
    inicio, dfa, simbolos = table()
    # print(dfa)
    # print(inicio)
    grafo(dfa, inicio, simbolos)
    for string in lines:
        string = string.strip()
        print("\n")
        print("entrada: ",string)
        print(verifica(string, inicio, dfa))



# mainDFA()




