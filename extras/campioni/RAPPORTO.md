# Tic rimasti nell'output con la skill attiva

Campione: 21 testi, 7 per registro (blog divulgativo, marketing, professionale), 7.898 parole. Li hanno scritti tre agenti separati con la versione 1.5.0 del fork, senza sapere che i testi sarebbero stati analizzati. Lo script di misura è `extras/misura_campione.py`.

## Quello che la skill ha già risolto

Zero em-dash, zero *non è X, è Y*, zero incipit e chiusure formulaici, parole spia quasi assenti (7 in tutto il campione), frasi di lunghezza variabile (coefficiente di variazione tra 0,32 e 0,74). La qualità generale è alta.

## Tic rimasti, dal più grave

### 1. La virgola prima di *e* resiste

Il 34% delle *e* ha la virgola davanti (75 su 221), 9,5 ogni 1000 parole. Molte non rientrano nei tre casi ammessi: *Il fenomeno si chiama retrogradazione, e spiega perché…*, *Il fornaio cuoce pezzature grandi, e una pagnotta da un chilo…*.

**Causa probabile:** la regola sta in `grammatica-italiana.md` §8, che chi scrive non sempre apre. Le regole del SKILL.md, che valgono sempre, non la contengono.

**Proposta:** promuoverla a regola non negoziabile numero 17, come era successo al *non è X, è Y*.

### 2. Esperienze personali inventate

Nei blog quattro testi su sette si aprono o si chiudono con un aneddoto in prima persona che il modello non può aver vissuto: *Ho cominciato a correre a quarantatré anni*, *ho comprato la mia attuale bici da città per novanta euro*, *La prima volta che ho sfornato una pagnotta decente*. Nei testi professionali compaiono confessioni costruite, come *Ho anche commesso errori, e uno mi ha insegnato parecchio*.

**Causa probabile:** `personalita-e-anima.md` consiglia la prima persona e l'ammissione di complessità. Il modello le applica inventando un vissuto. È il finto umano di plastica da cui la skill stessa mette in guardia, ma con un problema in più, perché è falso: spacciare per vere esperienze mai vissute danneggia chi pubblica.

**Proposta:** una regola esplicita. La prima persona si usa solo con fatti forniti dall'utente; altrimenti la voce si costruisce con posizioni e giudizi, senza biografia inventata. Dove serve un aneddoto, va chiesto all'utente oppure segnalato come esempio.

### 3. L'incipit scenico diventa uno schema

Tutti e sette i blog si aprono con una scena o un dettaglio concreto (*Sono le due e venti.*, *Il tabellone segna dieci minuti di ritardo, poi quindici, poi venticinque.*). Presa da sola, ognuna di queste aperture funziona. Ripetuta sempre uguale, la scena è diventata il nuovo *Nel mondo di oggi*. Quattro blog su sette si chiudono anche con un consiglio in prima persona (*Io consiglierei…*, *Il mio consiglio, da pendolare…*).

**Proposta:** nella guida agli incipit, alternare i tipi di apertura (il fatto nudo, la tesi, il dato, una domanda vera) invece di usarne sempre uno. Lo stesso vale per le chiusure.

### 4. La suspense del «è un altro»

Cinque casi: *la strada più frequente è un'altra.* (e il paragrafo dopo comincia con *È quella civile.*), *Il risultato di cui vado più fiero è un altro.*, *Il motivo preciso è questo.*, *Il risultato è questo:*. È la stessa famiglia di *qui sta il punto*, già in `leak-conversazionale.md`, in una variante che il catalogo non nomina.

**Proposta:** aggiungere la variante al catalogo e alle stringhe da cercare: `è un altro.`, `è un'altra.`, `è questo.`, `è questa:`.

### 5. Gerundi in fila

*Ci sono arrivato passando molte ore in reparto, ascoltando chi guida i carrelli, cambiando i turni…, formando tre capisquadra…*: quattro gerundi in fila. Nel campione ci sono 9 gerundi in coda, concentrati nei testi professionali.

**Proposta:** nella sezione 2 di `pattern-strutturali.md`, segnalare la catena di gerundi come variante del gerundio parassita.

### 6. Il punto e virgola quasi assente

0,9 ogni 1000 parole, sette in tutto, tutti nei testi professionali. La skill dice di usarlo, ma è un'indicazione morbida. Per questo tic serve prima un riferimento umano (PAISÀ, Wikipedia) per sapere quale sarebbe la frequenza normale.

## Ordine consigliato

1 e 2 subito: il primo è misurabile e già normato, il secondo riguarda l'onestà del testo. Poi 4 e 5, che sono aggiunte piccole al catalogo. Il 3 richiede di riscrivere una parte della guida. Il 6 aspetta i corpora.

---

# Secondo campione: versione 1.6.0

Stesse 21 richieste, tre agenti nuovi, versione 1.6.0 con le regole 17 e 18. 7.652 parole.

| Misura | 1.5.0 | 1.6.0 |
|---|---|---|
| *e* precedute da virgola | 34% (75 su 221) | 17% (38 su 220) |
| Aneddoti personali inventati nei blog | 4 testi su 7 | 0 |
| Segnaposto tipo `[prezzo]` | 0 | 41, in 8 testi |
| Righe di elenco puntato | 5 | 30 |
| Due punti ogni 1000 parole | 6,1 | 10,3 |
| Punto e virgola ogni 1000 parole | 0,9 | 2,1 |
| Gerundi in coda | 9 | 11 |

**Regola 17:** la virgola davanti a *e* si è dimezzata, ma un'occorrenza su due fra quelle rimaste resta ingiustificata, compresa una virgola di Oxford (*sono lente, costose, e lasciano*).

**Regola 18:** gli aneddoti inventati sono spariti. L'effetto però è andato oltre il bersaglio. Tutti i testi di marketing e la lettera di candidatura ora hanno segnaposto anche per dati aziendali (prezzi, telefoni, date, nomi), che nella 1.5.0 venivano inventati. La lettera ne ha 13 e così non si usa senza riscriverla. Non inventare un prezzo è giusto, ma sette testi su sette pieni di parentesi sono troppi per una bozza.

**Effetti collaterali:** i testi sono più strutturati, con più elenchi e più due punti. Alcune chiusure dei blog si sono appiattite in riassunti (*in sostanza, è un problema di rete e di investimenti*) o in avvertenze generiche (*è bene sentire un avvocato*). Le aperture sono più varie: tre blog su sette partono da un fatto invece che da una scena.

**Limite:** un solo campione per versione, e i modelli variano da un'esecuzione all'altra. Le differenze grandi (aneddoti, segnaposto, virgola) sono affidabili. Quelle piccole (gerundi, singole parole spia) no.

---

# Terzo campione: versione 1.7.0

Stesse richieste, tre agenti nuovi, regole 17 e 18 corrette. 7.207 parole. Misure prodotte con `python extras/misura_campione.py extras/campioni/v1.5.0 extras/campioni/v1.6.0 extras/campioni/v1.7.0`.

| Misura | 1.5.0 | 1.6.0 | 1.7.0 |
|---|---|---|---|
| *e* precedute da virgola | 33,9% | 17,3% | 10,6% |
| Virgole prima di *e* ogni 1000 parole | 9,5 | 5,0 | 2,8 |
| Aneddoti personali inventati nei blog | 4 su 7 | 0 | 0 |
| Segnaposto ogni 1000 parole | 0 | 5,0 | 1,4 |
| Testi con elenco *Da completare* | 0 | 0 | 13 |
| Suspense *è un altro* ogni 1000 parole | 0,51 | 0,26 | 0 |
| Gerundi in coda ogni 1000 parole | 1,14 | 1,44 | 0,56 |
| Righe di elenco ogni 1000 parole | 0,6 | 3,9 | 3,5 |
| Variazione della lunghezza delle frasi | 0,54 | 0,55 | 0,59 |

**Regola 17:** la virgola prima di *e* è scesa a un terzo del valore iniziale. Delle 20 occorrenze rimaste quasi tutte segnano un cambio di soggetto (*resta una bici rubata, e il mercato dell'usato ne è pieno*). Ne restano poche ingiustificate, come *non posso disporre il rimborso, e preferisco dirglielo subito*, dove il soggetto è lo stesso.

**Regola 18:** niente vissuto inventato, segnaposto scesi da 41 a 14. In 13 testi i dati mancanti stanno ora nell'elenco *Da completare*, e il testo si legge senza parentesi. Un solo testo supera il limite di tre segnaposto: la lettera di candidatura, con quattro.

**Da tenere d'occhio:** gli elenchi puntati sono rimasti più frequenti che nella 1.5.0. Per un verbale o una circolare possono servire, ma vanno controllati nei prossimi campioni.
