def writeFile(texto):
    try:
        with open("save.txt", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        conteudo = ""

    if texto not in conteudo:
        with open("save.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{texto}\n")


def pocaoLista():
    try:
        with open("save.txt", "r", encoding="utf-8") as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        return []