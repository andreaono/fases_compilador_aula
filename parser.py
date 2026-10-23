"""
Fase 2 — Análise sintática
Teoria: linguagens livres de contexto (Chomsky Tipo 2) · GLC · LL(1)

Entrada: lista de tokens
Saída:   árvore sintática (AST)

Gramática (já sem recursão à esquerda — pronta para descida recursiva):

  programa -> comando*
  comando  -> ('int'|'float') ID ('=' expr)? ';'
            | ID '=' expr ';'
            | 'print' '(' expr ')' ';'
            | 'read'  '(' ID ')'  ';'
  expr     -> termo  (('+'|'-') termo)*
  termo    -> fator  (('*'|'/') fator)*
  fator    -> NUM | ID | '(' expr ')'
"""


def analisar(tokens):
    """Descida recursiva LL(1): uma função por não-terminal."""
    pos = 0

    def olha():
        return tokens[pos]

    def avanca():
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return t

    def fator():
        tipo, lexema = olha()
        if tipo in ("NUM_INT", "NUM_REAL"):
            avanca()
            return ("Num", lexema, tipo == "NUM_REAL")
        if tipo == "ID":
            avanca()
            return ("Var", lexema)
        if tipo == "ABRE_PAR":
            avanca()
            e = expr()
            avanca()  # FECHA_PAR
            return e

    def termo():
        # termo -> fator (('*'|'/') fator)*
        esq = fator()
        while olha()[0] in ("OP_MULT", "OP_DIV"):
            op = avanca()[1]
            esq = ("Bin", op, esq, fator())
        return esq

    def expr():
        # expr -> termo (('+'|'-') termo)*
        # A precedência nasce da gramática: * / ficam mais "fundo" que + -
        esq = termo()
        while olha()[0] in ("OP_SOMA", "OP_SUB"):
            op = avanca()[1]
            esq = ("Bin", op, esq, termo())
        return esq

    def comando():
        tipo, lexema = olha()

        if tipo == "PALAVRA" and lexema in ("int", "float"):
            avanca()
            nome = avanca()[1]  # ID
            init = None
            if olha()[0] == "ATRIB":
                avanca()
                init = expr()
            avanca()  # ;
            return ("Decl", lexema, nome, init)

        if tipo == "PALAVRA" and lexema == "print":
            avanca()
            avanca()  # (
            e = expr()
            avanca()  # )
            avanca()  # ;
            return ("Print", e)

        if tipo == "PALAVRA" and lexema == "read":
            avanca()
            avanca()  # (
            nome = avanca()[1]
            avanca()  # )
            avanca()  # ;
            return ("Read", nome)

        if tipo == "ID":
            nome = avanca()[1]
            avanca()  # =
            e = expr()
            avanca()  # ;
            return ("Assign", nome, e)

    corpo = []
    while olha()[0] != "EOF":
        corpo.append(comando())
    return ("Program", corpo)


def _linhas(no):
    """Devolve lista de linhas da impressão da árvore."""
    kind = no[0]

    if kind == "Program":
        out = ["Program"]
        cmds = no[1]
        for i, cmd in enumerate(cmds):
            ultimo = i == len(cmds) - 1
            _anexa(out, _linhas(cmd), ultimo)
        return out

    if kind == "Decl":
        _, tipo, nome, init = no
        out = [f"Decl {tipo} {nome}"]
        if init is not None:
            _anexa(out, _linhas(init), True)
        return out

    if kind == "Assign":
        out = [f"Assign {no[1]}"]
        _anexa(out, _linhas(no[2]), True)
        return out

    if kind == "Print":
        out = ["Print"]
        _anexa(out, _linhas(no[1]), True)
        return out

    if kind == "Read":
        return [f"Read {no[1]}"]

    if kind == "Num":
        return [f"Num {no[1]}"]

    if kind == "Var":
        return [f"Var {no[1]}"]

    if kind == "Bin":
        out = [f"Bin {no[1]}"]
        _anexa(out, _linhas(no[2]), False)
        _anexa(out, _linhas(no[3]), True)
        return out

    return [str(no)]


def _anexa(destino, filhos, ultimo):
    ramo = "`-- " if ultimo else "|-- "
    cont = "    " if ultimo else "|   "
    destino.append(ramo + filhos[0])
    for linha in filhos[1:]:
        destino.append(cont + linha)


def mostrar_arvore(no):
    return "\n".join(_linhas(no))
