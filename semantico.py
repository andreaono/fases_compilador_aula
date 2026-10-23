"""
Fase 3 — Análise semântica
Teoria: sensível ao contexto (Chomsky Tipo 1) · tabela de símbolos · atributos

Entrada: árvore sintática
Saída:   árvore anotada com tipos + tabela de símbolos

A GLC sozinha não garante que o nome usado seja o mesmo declarado
(linguagem { w c w }). O compilador resolve isso com dados extras:
atributos na árvore e uma tabela de símbolos.
"""


def analisar(ast):
    """Percorre a AST, monta a tabela e anota o atributo 'tipo' nas expressões."""
    tabela = {}  # nome -> tipo ("int" ou "float")

    def tipo_de(no):
        # Atributo sintetizado: o tipo sobe das folhas para a raiz.
        if no[0] == "Num":
            # ("Num", lexema, eh_float)
            return "float" if no[2] else "int"

        if no[0] == "Var":
            return tabela[no[1]]

        if no[0] == "Bin":
            ta = tipo_de(no[2])
            tb = tipo_de(no[3])
            # int + float → float (promoção)
            return "float" if "float" in (ta, tb) else "int"

    for cmd in ast[1]:
        if cmd[0] == "Decl":
            _, vtype, nome, init = cmd
            if init is not None:
                tipo_de(init)
            tabela[nome] = vtype

        elif cmd[0] == "Assign":
            _, nome, e = cmd
            tipo_de(e)
            tabela[nome]  # uso exige declaração prévia (contexto)

        elif cmd[0] == "Read":
            tabela[cmd[1]]  # idem

        elif cmd[0] == "Print":
            tipo_de(cmd[1])

    return tabela


def mostrar_tabela(tabela):
    if not tabela:
        return "(vazia)"
    largura = max(len(n) for n in tabela)
    linhas = [f"{'nome'.ljust(largura)}  tipo"]
    linhas.append("-" * (largura + 6))
    for nome, tipo in tabela.items():
        linhas.append(f"{nome.ljust(largura)}  {tipo}")
    return "\n".join(linhas)
