#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Costruisce lo zip del plugin da caricare su claude.ai.

claude.ai accetta l'archivio solo se alla radice trova il manifest
.claude-plugin/plugin.json accanto a SKILL.md: una cartella che li contiene,
o uno zip senza manifest, vengono rifiutati. Questo script mette nello zip
solo i file che servono al plugin, sempre nello stesso ordine.

    python extras/crea_zip_plugin.py [--out FILE]

Senza --out lo zip finisce nella cartella che contiene la repo, con il nome
italiano-scrittura-anti-ai-<versione>.zip. Usa la sola libreria standard.
"""

import argparse
import json
import pathlib
import sys
import zipfile

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONTENUTO = [".claude-plugin/plugin.json", "SKILL.md", "LICENSE",
             "commands", "references", "scripts"]


def file_da_includere():
    for voce in CONTENUTO:
        percorso = RADICE / voce
        if percorso.is_file():
            yield percorso
        elif percorso.is_dir():
            yield from sorted(
                f for f in percorso.rglob("*")
                if f.is_file() and "__pycache__" not in f.parts
            )
        else:
            sys.exit(f"Manca {voce}: lo zip non sarebbe valido.")


def main():
    manifest = json.loads(
        (RADICE / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    versione = manifest["version"]
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out", type=pathlib.Path,
        default=RADICE.parent / f"italiano-scrittura-anti-ai-{versione}.zip",
    )
    uscita = parser.parse_args().out

    nomi = []
    with zipfile.ZipFile(uscita, "w", zipfile.ZIP_DEFLATED) as archivio:
        for f in file_da_includere():
            nome = f.relative_to(RADICE).as_posix()
            archivio.write(f, nome)
            nomi.append(nome)

    print(f"{uscita}: {len(nomi)} file, versione {versione}")


if __name__ == "__main__":
    main()
