"""
Fase 1 — Análise léxica
Teoria: linguagens regulares (Chomsky Tipo 3) · AFD · maior casamento

Entrada: cadeia de caracteres
Saída:   lista de tokens
"""

# Palavras que casam com a ER de ID, mas são palavras reservadas.
PALAVRAS_RESERVADAS = {"int", "float", "print", "read"}

# Símbolos de um caractere (não passam pelo AFD).
SIMBOLOS = {
    "+": "OP_SOMA",
    "-": "OP_SUB",
    "*": "OP_MULT",
    "/": "OP_DIV",
    "=": "ATRIB",
    "(": "ABRE_PAR",
    ")": "FECHA_PAR",
    ";": "PONTO_VIRG",
}

# Função de transição δ do AFD: (estado, classe) → próximo estado
# Classes: letra | digito | ponto
DELTA = {
    "q0":  {"letra": "ID",  "digito": "INT"},
    "ID":  {"letra": "ID",  "digito": "ID"},
    "INT": {"digito": "INT", "ponto": "DOT"},
    "DOT": {"digito": "FLT"},
    "FLT": {"digito": "FLT"},
}

# Estados finais: qual tipo de token cada um reconhece
FINAIS = {"ID": "ID", "INT": "NUM_INT", "FLT": "NUM_REAL"}


def classe(c):
    if c.isalpha() or c == "_":
        return "letra"
    if c.isdigit():
        return "digito"
    if c == ".":
        return "ponto"
    return "outro"


def passo(estado, c):
    return DELTA.get(estado, {}).get(classe(c))


def lex(fonte):
    """Varre a fonte e devolve a lista de tokens (maior casamento)."""
    tokens = []
    i = 0
    n = len(fonte)

    while i < n:
        c = fonte[i]

        # Espaços e comentários // ... são descartados (não viram token).
        if c.isspace():
            i += 1
            continue
        if c == "/" and i + 1 < n and fonte[i + 1] == "/":
            while i < n and fonte[i] != "\n":
                i += 1
            continue

        # Símbolos de um caractere.
        if c in SIMBOLOS:
            tokens.append((SIMBOLOS[c], c))
            i += 1
            continue

        # Maior casamento: anda no AFD enquanto houver transição,
        # guarda o último estado final visitado e emite o token dali.
        estado = "q0"
        j = i
        ultimo_final = None
        fim_final = i
        while j < n:
            prox = passo(estado, fonte[j])
            if prox is None:
                break
            estado = prox
            j += 1
            if estado in FINAIS:
                ultimo_final = estado
                fim_final = j

        lexema = fonte[i:fim_final]
        tipo = FINAIS[ultimo_final]
        if tipo == "ID" and lexema in PALAVRAS_RESERVADAS:
            tipo = "PALAVRA"
        tokens.append((tipo, lexema))
        i = fim_final

    tokens.append(("EOF", ""))
    return tokens
