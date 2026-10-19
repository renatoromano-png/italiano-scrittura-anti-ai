#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Segnala riga per riga i punti sospetti di un testo italiano.

Fa parte della skill italiano-scrittura-anti-ai. Cerca nel testo le stringhe
e le strutture che le regole della skill vietano o chiedono di giustificare,
e per ciascuna stampa riga, colonna, regola e un estratto. Non corregge
niente: ogni segnalazione va guardata da chi rivede, perché alcune (la
virgola prima di «e», il gerundio in coda) sono legittime in certi casi.

    python controlla_testo.py FILE [FILE ...]
    python controlla_testo.py -          (legge il testo da stdin)
    python controlla_testo.py --prova    (lancia le autoprove)

Esce con codice 1 se trova almeno una violazione certa, 0 altrimenti.
Non usa librerie esterne, non accede alla rete e non scrive nessun file.
"""

import re
import sys

# Ogni controllo: (nome, livello, regola, espressione, nota).
# «certo» indica una violazione da correggere sempre; «verifica» un punto
# che può essere legittimo e va giustificato da chi rivede.
LETTERA = r"A-Za-zÀ-ÿ'"
CONTROLLI = [
    ("em-dash", "certo", "regola 1", r"—", "sostituire con virgole, parentesi o due punti"),
    ("virgolette inglesi", "certo", "regola 3", r"[\"“”]", "usare le caporali « »"),
    ("incipit formulaico", "certo", "regola 4",
     r"(?i)\b(?:nel mondo di oggi|nel panorama attuale|nell'era digitale|ti sei mai chiesto|"
     r"hai mai pensato|immagina un mondo|scopri il potere)", "aprire con un fatto o una tesi"),
    ("chiusura formulaica", "certo", "regola 5",
     r"(?i)\b(?:in conclusione|in definitiva|per tirare le somme|spero che questo articolo)",
     "chiudere con una conseguenza o un'immagine"),
    ("meta-annuncio", "certo", "regola 6",
     r"(?i)\b(?:è importante sottolineare|vale la pena notare|non si può non menzionare|degno di nota)",
     "dire la cosa invece di annunciarla"),
    ("lessico AI", "certo", "regola 7",
     r"(?i)\b(?:delinea\w*|approfondi\w*|navigare il panorama|esplorare insieme)", "parola semplice e contestuale"),
    ("non solo… ma anche", "certo", "regola 8", r"(?i)\bnon solo\b[^.]{0,80}\bma\b", "congiunzione semplice"),
    ("errore ortografico", "certo", "regola 9",
     r"(?i)\b(?:un'altro|qual'è|un pò|perchè|nè)(?![{L}])".format(L=LETTERA), "forma corretta: un altro, qual è, un po', perché, né"),
    ("piuttosto che", "verifica", "regola 10", r"(?i)\bpiuttosto che\b", "ammesso solo in senso comparativo, mai per «oppure»"),
    ("artefatto da chatbot", "certo", "regola 11",
     r"(?i)(?:\bcerto!|ottima domanda|ecco un articolo|spero che ti sia utile|fammi sapere se)", "eliminare"),
    ("knowledge cutoff", "certo", "regola 12",
     r"(?i)\b(?:sulla base delle informazioni disponibili|fino al mio ultimo aggiornamento)", "verificare o attribuire la fonte"),
    ("contrasto fittizio", "certo", "regola 16",
     r"(?i)\bnon (?:è|si tratta di)\b[^.;]{1,60}[,:;] (?:è|ma di)\b", "affermare direttamente il positivo"),
    ("virgola di Oxford", "certo", "regola 17",
     r"(?<![{L}])[{L}]+, [{L}]+, e (?=[{L}])".format(L=LETTERA), "in un elenco mai la virgola prima di «e»"),
    ("virgola prima di e", "verifica", "regola 17", r",\s+e(?![{L}])".format(L=LETTERA),
     "ammessa solo per cambio di soggetto ambiguo, stacco ritmico o «e» avversativa"),
    ("gerundio in coda", "verifica", "pattern 2 e 21", r", [a-zàèéìòù]+(?:ando|endo)\b",
     "controllare che non sia parassita o irrelato"),
    ("suspense", "verifica", "leak conversazionale",
     r"(?i)\b(?:qui sta il punto|ecco la cosa|la verità è che|il fatto è che|è (?:un altro|un'altra|questo|questa)[.:])",
     "dire subito la cosa"),
]
MAX_SEGNAPOSTO = 3


def controlla(testo):
    """Restituisce l'elenco delle segnalazioni come tuple (riga, colonna, nome, livello, regola, estratto, nota)."""
    trovati = []
    righe = testo.splitlines()
    for numero, riga in enumerate(righe, 1):
        if re.match(r"^\W*da completare", riga, re.IGNORECASE):
            break
        for nome, livello, regola, rx, nota in CONTROLLI:
            for m in re.finditer(rx, riga):
                inizio = max(0, m.start() - 25)
                estratto = riga[inizio:m.end() + 25].strip()
                trovati.append((numero, m.start() + 1, nome, livello, regola, estratto, nota))
    # la virgola di Oxford è anche una virgola prima di «e»: si tiene solo la più grave
    oxford = {(r, c + m) for r, c, n, *_ in trovati if n == "virgola di Oxford"
              for m in range(0, 80)}
    trovati = [t for t in trovati if not (t[2] == "virgola prima di e" and (t[0], t[1]) in oxford)]
    segnaposto = re.findall(r"\[[^\]\n]{1,40}\]", testo.split("Da completare")[0])
    if len(segnaposto) > MAX_SEGNAPOSTO:
        trovati.append((0, 0, "troppi segnaposto", "certo", "regola 18",
                        f"{len(segnaposto)} segnaposto",
                        f"al massimo {MAX_SEGNAPOSTO}: gli altri dati vanno nell'elenco «Da completare»"))
    return sorted(trovati)


def stampa(nome_file, trovati):
    certi = sum(1 for t in trovati if t[3] == "certo")
    print(f"== {nome_file}: {certi} da correggere, {len(trovati) - certi} da verificare")
    for riga, col, nome, livello, regola, estratto, nota in trovati:
        dove = f"{riga}:{col}" if riga else "testo"
        segno = "!!" if livello == "certo" else "??"
        print(f"  {segno} {dove:>7}  {nome} ({regola}): …{estratto}…")
        print(f"             {nota}")
    return certi


def prova():
    casi = [
        ("Il fenomeno si chiama retrogradazione, e spiega tutto.", "virgola prima di e", True),
        ("Il fenomeno si chiama retrogradazione e spiega tutto.", "virgola prima di e", False),
        ("Sono lente, costose, e lasciano strascichi.", "virgola di Oxford", True),
        ("Sono lente, costose, e lasciano strascichi.", "virgola prima di e", False),
        ("La soluzione — che pareva impossibile — funziona.", "em-dash", True),
        ("Non è un problema tecnico, è un problema di soldi.", "contrasto fittizio", True),
        ("Non solo veloce ma anche economico.", "non solo… ma anche", True),
        ("Qual'è il punto?", "errore ortografico", True),
        ("Perché no?", "errore ortografico", False),
        ("La strada più frequente è un'altra.", "suspense", True),
        ("Ha firmato il decreto, confermando la linea.", "gerundio in coda", True),
        ("Prezzo [prezzo], data [data], ora [ora], luogo [luogo].", "troppi segnaposto", True),
        ("Prezzo [prezzo].\n\nDa completare\n- [a] [b] [c] [d]", "troppi segnaposto", False),
        ("Ho scritto \"ciao\".", "virgolette inglesi", True),
        ("Ho scritto «ciao».", "virgolette inglesi", False),
    ]
    falliti = 0
    for testo, nome, atteso in casi:
        trovato = any(t[2] == nome for t in controlla(testo))
        if trovato != atteso:
            falliti += 1
            print(f"FALLITA: {nome!r} su {testo!r}: atteso {atteso}, trovato {trovato}")
    print(f"{len(casi)} casi, {falliti} falliti.")
    return 1 if falliti else 0


def main(argomenti):
    if not argomenti:
        sys.exit(__doc__)
    if argomenti == ["--prova"]:
        sys.exit(prova())
    totale_certi = 0
    for nome in argomenti:
        if nome == "-":
            testo = sys.stdin.read()
        else:
            with open(nome, encoding="utf-8") as f:
                testo = f.read()
        totale_certi += stampa(nome, controlla(testo))
    sys.exit(1 if totale_certi else 0)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
