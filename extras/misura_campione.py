#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Misura i tic ricorrenti in una cartella di testi generati.

Serve a verificare sul campo l'effetto delle regole della skill: si generano
gli stessi testi con due versioni diverse e si confrontano le misure. Legge
tutti i file .md della cartella, salta la prima riga (il titolo) e ignora
l'elenco «Da completare» che la regola 18 chiede in fondo al testo.

    python extras/misura_campione.py CARTELLA [CARTELLA ...]

Con più cartelle stampa una tabella di confronto, una colonna per cartella.
Le misure sono euristiche, pensate per confrontare campioni fra loro e non
per giudicare un testo singolo. Usa la sola libreria standard.
"""

import pathlib
import re
import statistics
import sys

LETTERA = r"A-Za-zÀ-ÿ'"

MISURE = {
    "virgola prima di e": rf",\s+e(?![{LETTERA}])",
    "due punti": r":",
    "punto e virgola": r";",
    "em-dash": r"—",
    "gerundio in coda": r", [a-zàèéìòù]+(?:ando|endo)\b",
    "non è X, è Y": r"\bnon è\b[^.;]{1,60}[,:;] è\b",
    "non solo X ma Y": r"\bnon solo\b[^.]{0,80}\bma\b",
    "suspense «è un altro»": r"\bè (?:un altro|un'altra|questo|questa)[.:]",
    "riga di elenco": r"(?m)^\s*[-*] ",
    "segnaposto [..]": r"\[[^\]\n]{1,40}\]",
    "grassetto": r"\*\*[^*]+\*\*",
}

PRIMA_PERSONA = r"\b(?:ho|avevo) (?:[a-zàèéìòù]+ )?[a-zàèéìòù]+(?:ato|uto|ito)\b"


def corpo(testo):
    righe = testo.splitlines()[1:]
    for i, riga in enumerate(righe):
        if re.match(r"^\W*da completare", riga, re.IGNORECASE):
            righe = righe[:i]
            break
    return "\n".join(righe)


def misura(cartella):
    file = sorted(pathlib.Path(cartella).glob("*.md"))
    file = [f for f in file if f.name.upper() != "RAPPORTO.MD"]
    conteggi = dict.fromkeys(MISURE, 0)
    parole = e_tot = 0
    con_da_completare = 0
    blog_prima_persona = 0
    cv = []
    for f in file:
        testo = f.read_text(encoding="utf-8")
        if re.search(r"(?im)^\W*da completare", testo):
            con_da_completare += 1
        c = corpo(testo)
        parole += len(re.findall(rf"[{LETTERA}]+", c))
        e_tot += len(re.findall(rf"(?<![{LETTERA}])e(?![{LETTERA}])", c))
        for nome, rx in MISURE.items():
            conteggi[nome] += len(re.findall(rx, c))
        if f.name.startswith("blog") and re.search(PRIMA_PERSONA, c):
            blog_prima_persona += 1
        frasi = [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", " ".join(c.split()))
                 if len(s.split()) > 2]
        if frasi:
            cv.append(statistics.pstdev(frasi) / statistics.mean(frasi))
    return {
        "testi": len(file),
        "parole": parole,
        "e precedute da virgola (%)": round(100 * conteggi["virgola prima di e"] / e_tot, 1) if e_tot else 0,
        **{f"{k} (ogni 1000 parole)": round(1000 * v / parole, 2) if parole else 0
           for k, v in conteggi.items()},
        "blog con passato prossimo in 1a persona": blog_prima_persona,
        "testi con elenco Da completare": con_da_completare,
        "variazione lunghezza frasi (CV medio)": round(statistics.mean(cv), 2) if cv else 0,
    }


def main():
    cartelle = sys.argv[1:]
    if not cartelle:
        sys.exit(__doc__)
    risultati = [misura(c) for c in cartelle]
    nomi = [pathlib.Path(c).name for c in cartelle]
    larghezza = max(len(k) for k in risultati[0])
    print(" " * larghezza + "  " + "  ".join(f"{n:>10}" for n in nomi))
    for chiave in risultati[0]:
        print(f"{chiave:<{larghezza}}  " + "  ".join(f"{r[chiave]:>10}" for r in risultati))


if __name__ == "__main__":
    main()
