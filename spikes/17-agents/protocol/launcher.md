# Chi lancia le esecuzioni

Istruzioni per la sessione di Claude Code che esegue lo spike #17 in locale. Si avvia nel repository, sul ramo `spike-17-bench`.

## Il tuo ruolo

Lanci, misuri e conti. Non verifichi.

Stando nel repository puoi leggere la chiave delle risposte (`defects.py`, le cartelle `keys`). Per questo:

- non leggi i report per giudicarli, non li correggi, non li riscrivi;
- non dai nessun suggerimento alle sessioni che lanci: ricevono il loro prompt così com'è;
- ogni decisione sul contenuto la prendono gli script (`score.py`, `judge_input.py`) o una sessione che non conosce la chiave.

Domanda, misure, criterio e limiti sono in `spikes/17-agents/README.md`. Il criterio è fissato e non si cambia.

## 0. Prima di tutto

1. Controlla `claude --version`, `python --version` (3.8 o più) e `git --version`.
2. Leggi `claude --help` e trova come si fa, nella versione installata, a: lanciare una sessione non interattiva con un prompt; fissare il modello; fissare l'effort; avere l'output come flusso di eventi JSON con l'uso dei token; fissare i permessi.
3. Ogni sessione lanciata usa il modello **Sonnet, ultima versione**, a **effort medio**. Se per una sessione non interattiva non si possono fissare tutti e due, fermati e dillo all'utente.

## 1. Cartelle, fuori dal repository

Due cartelle in due posti diversi, mai dentro il repository:

- `BENCH`: alberi dei casi e chiavi. Per esempio nella cartella temporanea dell'utente.
- `RUNS`: una cartella per esecuzione. Per esempio `spike17-runs` accanto al repository.

Le sessioni lanciate lavorano in `RUNS` e non devono poter trovare `BENCH` per caso.

## 2. Costruzione

```bash
python spikes/17-agents/build.py --out BENCH
python -m unittest discover -s spikes/17-agents -p test_score.py
```

`build.py` deve finire con «every witness holds». Se si ferma, riporta il messaggio e fermati: non si toccano `defects.py` né `witnesses.py`.

## 3. Il comando di lancio

Scrivi il comando che lancia una sessione non interattiva nella cartella di una esecuzione, con il prompt letto da un file, Sonnet, effort medio e il flusso di eventi salvato in `out/session.jsonl`.

Permessi: il minimo che permetta di leggere e cercare file, scrivere nella propria cartella e, per il modo B, lanciare agenti. Mai la modalità che salta tutti i controlli.

**Prima di lanciare la prima sessione mostra all'utente il comando esatto e aspetta il suo sì.**

## 4. Taratura (non entra nel punteggio)

```bash
python spikes/17-agents/prepare.py --bench BENCH --case tuning --mode B --run 1 --runs RUNS --relative
python spikes/17-agents/prepare.py --bench BENCH --case tuning --mode A --run 1 --runs RUNS --relative
```

Ogni sessione parte nella sua cartella (`RUNS/tuning-B-1`, `RUNS/tuning-A-1`). Il prompt è `prompt-prompt-of-the-coordinator.txt` per il modo B e `prompt-prompt.txt` per il modo A.

Il modo B regge se: gli agenti sono partiti, `out/briefs` e `out/returns` non sono vuoti, `out/report.md` e `out/log.md` esistono, non c'è `out/CANNOT_LAUNCH.txt`.

Se non regge puoi cambiare `protocol/coordinator.md`, ma solo perché funzioni (agenti che partono, ritorni nel formato, report completo), mai per trovare più difetti. Ogni cambio è un commit sul ramo con il motivo. Poi una nuova esecuzione (`--run 2`, `--run 3`). Dopo tre tentativi falliti, fermati.

Quando regge, il protocollo non si tocca più.

**Poi fermati e riporta all'utente**: il comando usato, le misure delle due esecuzioni (punto 6), il punteggio sul caso `tuning`, i cambi fatti al protocollo. Le 18 esecuzioni partono solo con il suo via.

## 5. Le 18 esecuzioni

Casi `S`, `M`, `L`; modi `A` e `B`; esecuzioni 1, 2, 3.

```bash
python spikes/17-agents/prepare.py --bench BENCH --case L --mode A --run 1 --runs RUNS --relative
```

- Una alla volta, mai in parallelo, alternando A e B.
- Se una sessione cade per un motivo dell'ambiente (rete, limite d'uso), rinomina la sua cartella in `<nome>.failed`, rilanciala con lo stesso numero e annotalo. Non si rilancia mai una esecuzione perché il report non convince.
- Il report deve essere in `out/report.md`. Se manca, l'esecuzione conta con zero difetti trovati e lo si annota.

## 6. Misure di ogni esecuzione

Dal flusso `out/session.jsonl`:

- **Costo totale** riportato a fine sessione. È la misura che si confronta con la soglia «al più 2,5 volte»: secondo la documentazione comprende i sotto-agenti, mentre il conteggio dei token copre solo la sessione principale. Stesso modello nei due modi, quindi il rapporto dei costi sta per il rapporto dei token. Annota anche i token riportati.
- **Contesto massimo della sessione principale** (in B è il coordinatore): il massimo, sui messaggi dell'assistente della sessione principale e non dei sotto-agenti, di token in ingresso più token letti dalla cache più token scritti nella cache.
- **Durata**, **numero di agenti lanciati** (modo B), **righe scartate dal coordinatore** (da `out/log.md`).

Scrivi uno script `spikes/17-agents/measure.py` che calcola queste misure dal flusso, con un test su un flusso vero, e mostralo all'utente con le misure della taratura. Se il flusso non riporta l'uso per messaggio, fermati e dillo: il contesto massimo non si può stimare a occhio.

Punteggio:

```bash
python spikes/17-agents/score.py --json --tree RUNS/L-A-1/tree --key BENCH/keys/L.json RUNS/L-A-1/out/report.md > RUNS/L-A-1/out/score.json
```

Una riga per esecuzione in `spikes/17-agents/results/runs.csv`.

## 7. Giudizio alla cieca

Per ogni caso:

```bash
python spikes/17-agents/judge_input.py --case L --key BENCH/keys/L.json --runs RUNS --out RUNS/judge-L/rows.md
```

Il file `rows.md.map.json` resta a te e non va nella cartella del giudice: spostalo fuori prima di lanciare. Nella cartella `RUNS/judge-L` metti una copia dell'albero del caso (`BENCH/L`) come `tree`. Poi una sessione nuova, Sonnet a effort medio, con questo prompt:

```
The file ./rows.md lists findings that some verifier reported about the project in ./tree.
For each numbered row decide, by reading the project's files: is it a real defect, not a
defect, or can you not tell? Read nothing outside this folder and run nothing.

Write ./verdicts.md with one line per row:
<number>: real defect | not a defect | cannot tell - <path:line that shows it> - <one sentence>
```

Poi conti con la mappa: i falsi positivi di una esecuzione sono le sue righe giudicate «not a defect».

## 8. Esito

Applica il criterio del README alla lettera e scrivi `spikes/17-agents/results/outcome.md`: i numeri per caso e per modo, l'esito (fare, non fare, rimandare) e, accanto, i limiti del banco.

Commit sul ramo `spike-17-bench`: `runs.csv`, `measure.py`, `outcome.md`, i `score.json` e i report in `results/reports/`. Push solo se l'utente lo chiede. Niente PR, niente merge su `main`, niente commenti sulle issue senza che l'utente lo chieda.
