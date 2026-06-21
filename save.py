def writeFile(texto):
    try:
        with open("save.txt", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        conteudo = ""

    if texto not in conteudo:
        with open("save.txt", "a", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            if texto not in linhas:
                arquivo.write(f"{texto}\n")


def pocaoLista():
    try:
        with open("save.txt", "r", encoding="utf-8") as arquivo:
            pocao_vec = arquivo.readlines()

            return pocao_vec

    except FileNotFoundError:
        # Caso o arquivo ainda não exista, retorna uma lista vazia
        return []
