import random
from enum import Enum
from anytree import Node, RenderTree
import math
import argparse

class Difficulty(Enum):
    FACILE = 1
    NORMALE = 2
    DISCRETA = 3
    AVANZATA = 4
def roll3D6():
    return random.randint(1,6)+random.randint(1,6)+random.randint(1,6)

def getDv(difficolta):
    match difficolta:
        case Difficulty.FACILE:
            return {"DV6", 2, "n/a"}
        case Difficulty.NORMALE:
            return {"DV8", 4, "<=2"}
        case Difficulty.DISCRETA:
            return {"DV10", 6, "<=4"}
        case Difficulty.AVANZATA:
           return {"DV12", 8, "<=6"}
# Roll 3d6. This is the total number of floors the Architecture will have.
def numeroPiani():
   return roll3D6()

def numeroDiramazioni():
    diramazioni = 0

    while(random.randint(1,10) >= 7):
        diramazioni += 1

    return diramazioni
idbranch = ["A", "B", "C", "D", "E", "F"]
def generaPiani(numPiani=1,  diff=Difficulty.NORMALE, numDiramazioni=0, root=None, idpiano=1):
    Radice = root
    padre = Radice
    i = idpiano
    if(root == None):
        # caso base, crea radice
        # crea i due piani lobby
        Radice = Node(generaPiano(1, diff))
        padre = Node(generaPiano(2, diff), Radice)
        numPiani-=2
        i=2
    # ora genero i piani partendo da padre
    if(numPiani > 0):
        i+=1
        # se ho ancora piani da generare:
        # genero un piano chiamando ricorsivamente la funzione.
        # in caso di diramazione suddivido il numero di piani in modo che siano pari o quasi e stesso
        if (numDiramazioni > 0) and ((random.randint(1,10)) < (float(numDiramazioni)/float(numPiani))*10):
            # diramo albero utilizzando come nodo padre "padre"
            padresx = Node(generaPiano(i, diff, idBranch=idbranch[0]), padre)
            padredx = Node(generaPiano(i, diff, idBranch=idbranch[1]), padre)

            numPianiSx = math.ceil((numPiani-2)/2)
            generaPiani(numPianiSx, diff, numDiramazioni-1, padresx, idpiano=i)
            generaPiani(numPiani-numPianiSx, diff, numDiramazioni-1, padredx, idpiano=i)
        else:
            padrenew = Node(generaPiano(i, diff), padre)

            generaPiani(numPiani-1, diff,  root=padrenew, idpiano=i)
    return Radice

def generaPiano(piano, diff=Difficulty.NORMALE, idBranch=""):
# lobby:
# 1 File DV6
# 2 Password DV6
# 3 Password DV8
# 4 Skunk
# 5 Wisp
# 6 Killer
    lobby = ["File DV6","Password DV6", "Password DV8", "Skunk", "Wisp", "Killer"]
    basici = [
        "_PARTE DA 3_"
        "_PARTE DA 3_"
        "padding"
        "Sabertooth",
        "Raven x2",
        "Hellhound",
        "Wisp",
        "Raven",
        "Password DV6",
        "File DV6",
        "Control Node",
        "Password DV6",
        "Skunk",
        "Asp",
        "Scorpion",
        "Killer, Skunk",
        "Wisp x3",
        "Liche",
        ]
    normale = [
        "_PARTE DA 3_",
        "_PARTE DA 3_",
        "Hellhound x2",
        "Hellhound, Killer",
        "Skunk x2",
        "Sabertooth",
        "Scorpion",
        "Hellhound",
        "Password DV8",
        "File DV8",
        "Control Node DV8",
        "Password DV8",
        "Asp",
        "Killer",
        "Liche",
        "Asp",
        "Raven x3",
        "Liche, Raven"
    ]

    discreti = [
        "_parte da 3_",
        "_parte da 3_",
    "Kraken",
    "Hellhound, Scorpion",
    "Hellhound, Killer",
    "Raven x2",
    "Sabertooth",
    "Hellhound",
    "Password DV10",
    "File DV10",
    "Control Node DV10",
    "Password DV10",
    "Killer",
    "Liche",
    "Dragon",
    "Asp, Raven",
    "Dragon, Wisp",
    "Giant"
    ]
    avanzati = [
              "_parte da 3_",
        "_parte da 3_",
    "Hellhound x3",
    "Asp x2",
    "Hellhound, Liche",
    "Wisp x3",
    "Hellhound, Sabertooth",
    "Kraken",
    "Password DV12",
    "File DV12",
    "Control Node DV12",
    "Password DV12",
    "Giant",
    "Dragon",
    "Killer, Scorpion",
    "Kraken",
    "Raven, Wisp, Hellhound",
    "Dragon x2"

    ]

    incontroPiano = ""
    if piano <= 2:
        incontroPiano= lobby[random.randint(1,6)-1]
    else:
        # lancio 3d6
        lancio = roll3D6()-1
        match diff:
            case Difficulty.FACILE:
                incontroPiano=  basici[lancio]
            case Difficulty.NORMALE:
                incontroPiano=  normale[lancio]
            case Difficulty.DISCRETA:
                incontroPiano=  discreti[lancio]
            case Difficulty.AVANZATA:
                incontroPiano=  avanzati[lancio]
    return str(piano)+idBranch+ " " + incontroPiano

if __name__ =="__main__":
    # prendo gli argomenti da linea di comando
    parser = argparse.ArgumentParser("nethelper")
    parser.add_argument("piani", help="numero naturale che rappresenta quanti piani generare", type=int)
    parser.add_argument("diramazioni", help="numero naturale che rappresenta quante diramazioni massime inserire", type=int)
    # parsing degli argomenti
    args = parser.parse_args()

    root = generaPiani(args.piani, numDiramazioni=args.diramazioni)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))