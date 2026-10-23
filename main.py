"""
MiniC didático — pipeline das três fases de análise.

  fonte  →  tokens  →  AST  →  tabela de símbolos
           (léxico)  (sintático)   (semântico)

Uso:
  python main.py exemplos/media.minic
"""

import sys
from lexer import lex
from parser import analisar as parse, mostrar_arvore
from semantico import analisar as check, mostrar_tabela


def compilar(fonte):
    print("=" * 50)
    print("FASE 1 - Analise lexica  (AFD / Tipo 3)")
    print("=" * 50)
    tokens = lex(fonte)
    for tipo, lexema in tokens:
        if tipo == "EOF":
            print(f"  ({tipo})")
        else:
            print(f"  ({tipo}, '{lexema}')")

    print()
    print("=" * 50)
    print("FASE 2 - Analise sintatica  (GLC / LL(1) / Tipo 2)")
    print("=" * 50)
    ast = parse(tokens)
    print(mostrar_arvore(ast))

    print()
    print("=" * 50)
    print("FASE 3 - Analise semantica  (tabela / Tipo 1)")
    print("=" * 50)
    tabela = check(ast)
    print(mostrar_tabela(tabela))


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "exemplos/media.minic"
    with open(caminho, encoding="utf-8") as f:
        fonte = f.read()
    print(f"Arquivo: {caminho}\n")
    print("--- fonte ---")
    print(fonte.rstrip())
    print()
    compilar(fonte)
