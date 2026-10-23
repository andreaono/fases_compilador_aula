# MiniC didático

Material de sala para **Linguagens Formais e Autômatos**.  
Complementa *Anatomia de um Compilador*: o aluno **vê as três fases**, lê o código mínimo e liga cada fase à hierarquia de Chomsky.

Não há recuperação de erros, otimização nem geração de máquina.

| Fase | Chomsky | Ferramenta | Código |
|------|---------|------------|--------|
| Léxica | Tipo 3 · Regular | AFD + maior casamento | `lexer.py` |
| Sintática | Tipo 2 · Livre de contexto | GLC · LL(1) | `parser.py` |
| Semântica | Tipo 1 · Sensível ao contexto | Tabela + atributos | `semantico.py` |

---

## Comece por aqui 

Abra **`laboratorio.html`** no navegador (duplo clique — sem servidor, sem Python).

1. Escolha uma das **5 fontes**
2. (Opcional) edite o código
3. Clique em **Executar fases**

A página mostra, com explicação em cada painel:

- **Fase 1** → tokens  
- **Fase 2** → árvore sintática (AST)  
- **Fase 3** → tabela de símbolos  

### As 5 fontes do laboratório

| # | Fonte | O que destacar na aula |
|---|--------|-------------------------|
| 1 | Média | Fluxo completo: `read`, parênteses, `float` |
| 2 | Precedência | Na AST, `3*4` fica **abaixo** do `+` |
| 3 | Tipos | `NUM_REAL` e promoção int/float |
| 4 | Parênteses | `(2+3)*4` inverte a árvore em relação à fonte 2 |
| 5 | Declaração | Programa mínimo — contar tokens à mão |

A lógica embutida no HTML é a mesma de `lexer.py`, `parser.py` e `semantico.py`.

---

## Arquitetura

```
fonte MiniC
      │
      ▼
   léxico      →  tokens           (Tipo 3)
      │
      ▼
   sintático   →  AST              (Tipo 2)
      │
      ▼
   semântico   →  tabela + tipos  (Tipo 1)
```

```
minic_didatico/
├── README.md            ← este guia
├── laboratorio.html     ← interface principal (5 fontes + explicações)
├── main.py              ← mesmo pipeline no terminal
├── lexer.py             ← fase 1
├── parser.py            ← fase 2
├── semantico.py         ← fase 3
└── exemplos/            ← fontes para o terminal
    ├── media.minic
    ├── expressao.minic
    └── tipos.minic
```

- **Projetor / aluno:** `laboratorio.html`  
- **Ler o código:** os três `.py`  
- **Terminal (opcional):** `main.py`

---

## A linguagem MiniC

```
programa -> comando*
comando  -> ('int'|'float') ID ('=' expr)? ';'
          | ID '=' expr ';'
          | 'print' '(' expr ')' ';'
          | 'read'  '(' ID ')'  ';'
expr     -> termo  (('+'|'-') termo)*
termo    -> fator  (('*'|'/') fator)*
fator    -> NUM | ID | '(' expr ')'
```

Comentários: `//` até o fim da linha.

```
int a = 2;
int b = 3;
print(a + b * 4);
```

---

## Rodar no terminal (opcional)

Python 3, sem dependências.

```bash
cd minic_didatico
python main.py exemplos/media.minic
python main.py exemplos/expressao.minic
python main.py exemplos/tipos.minic
```

Saída: tokens → AST → tabela (ex.: `a:int`, `b:int`, `media:float`).

---

## Roteiro

### 1. Por que fases? 

No diagrama de *Anatomia de um Compilador*: cada fase usa a **classe de linguagem mais simples** que resolve o problema.

### 2. Laboratório no navegador 

Abra `laboratorio.html` com a turma.

| Fonte | Pergunta para a turma |
|-------|------------------------|
| 5. Declaração | Quantos tokens? Por que `int` é `PALAVRA`? |
| 2. Precedência | Onde está o `*` na árvore? |
| 4. Parênteses | Em que a AST muda em relação à fonte 2? |
| 3. Tipos | Como `10.5` vira `NUM_REAL`? O que a tabela guarda? |
| 1. Média | Percorra as três fases do programa completo |

### 3. Código-fonte das fases 

Com o laboratório ainda aberto, abra os `.py`:

**`lexer.py`** — `DELTA` (transição), `FINAIS`, maior casamento, tabela de reservadas.

**`parser.py`** — uma função por não-terminal (LL(1)); `while` no lugar da recursão à esquerda; precedência pela gramática.

**`semantico.py`** — tabela nome→tipo; `tipo_de` como atributo sintetizado; uso exige declaração (contexto).

### 4. Fechamento 

| Se o problema for… | Quem detecta? |
|--------------------|---------------|
| caractere `@` | léxico (AFD sem transição) |
| `print a;` sem `()` | sintático |
| `x` sem `int x;` | semântico (tabela) |

---

## O que este material **não** faz (de propósito)

- Mensagens de erro elaboradas / modo pânico  
- Código intermediário, otimização, assembly  
- Escopos aninhados, funções, vetores  

Isso aparece nas fases 4–6 de *Anatomia de um Compilador - aula.html*. Aqui o objetivo é **entender o arquivo inteiro** em uma leitura.

---

## Exercícios

1. **Léxico.** Inclua o token `%`. O que muda em `SIMBOLOS` e no parser?
2. **AFD.** Por que `3.` não é `NUM_REAL`? (estado `DOT` não é final.)
3. **Sintático.** Compare as ASTs das fontes 2 e 4 no laboratório. Desenhe a derivação de `a * (b + 2)`.
4. **Semântico.** Na fonte Média, apague `float media;` e execute. O que quebra e por quê?
5. **Chomsky.** Em uma frase: tokens = Tipo 3; forma do programa = Tipo 2; “declarou = usou” = Tipo 1.

---

## Ligação com a aula interativa

| Neste projeto | Em *Anatomia de um Compilador* |
|---------------|-------------------------------|
| `laboratorio.html` | Laboratórios ao vivo das fases 1–3 |
| `lexer.py` | Fase 1 · AFD e tokens |
| `parser.py` | Fase 2 · pilha / AST |
| `semantico.py` | Fase 3 · tabela e tipos |

Use a aula HTML para **ver o autômato**; use este projeto para **executar as fases** (`laboratorio.html`) e **ler o código** (`.py`).
