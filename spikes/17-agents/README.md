# Spike #17: un agente solo o un coordinatore con agenti?

Banco usa e getta per la issue #17. Non fa parte della skill e non va unito a `main`: resta sul ramo `spike-17-bench`.

## Domanda

Dividere una verifica grande fra agenti con contesto proprio la rende migliore o più efficiente, e a che costo?

Una sola domanda. Il banco non dice quale protocollo multi-agente sia il migliore: confronta un agente solo con un protocollo, quello di `protocol/coordinator.md`.

## Cosa c'è

| File | Cosa fa |
|---|---|
| `defects.py` | I 15 difetti inseriti: file, testo di prima e di dopo, dominio, categoria. **È la chiave delle risposte: un verificatore non lo vede mai.** |
| `witnesses.py` | Un testimone per difetto: codice che dice se il difetto si osserva in un albero. |
| `build.py` | Costruisce gli alberi dei casi dal commit di base e rifiuta ogni difetto che il suo testimone non dimostra. |
| `score.py`, `test_score.py` | Punteggio meccanico di un report contro la chiave, con i suoi test. |
| `protocol/single.md`, `protocol/coordinator.md` | I due modi, con i prompt. |
| `results/runs.csv` | Una riga per esecuzione. |

## I casi

Il repository è questo, al commit `cb75e4e` (`main` dopo la PR #31), senza la cartella `spikes/`. Il testo della skill non è mai nel perimetro: è lo strumento, non l'oggetto.

| Caso | Perimetro | Dimensione | Difetti |
|---|---|---|---|
| `S` | `scripts/check.py` | 22,9 kB | S1-S4 |
| `M` | `scripts/` | 57,2 kB | S1-S4, M1-M4 |
| `L` | `scripts/`, README, CHANGELOG, `plugin.json`, `evals/` | 177,7 kB | S1-S4, M1-M4, L1-L4 |
| `tuning` | `scripts/`, README | 83,8 kB | U1-U3 |

- I casi sono annidati: gli stessi quattro difetti di `S` stanno anche in `M` e in `L`. Quanti di quei quattro si trovano al crescere del perimetro è la misura dell'effetto della dimensione.
- `tuning` serve a mettere a punto il protocollo del coordinatore e non entra mai nel punteggio. I suoi tre difetti non stanno in nessun altro caso.
- Domini: Code (7), Tests (3), Documentation (3), Data (2).

## Come si sa che un difetto è un difetto

Ogni difetto ha un testimone eseguibile. `build.py` pretende che sia:

- falso sul commit di base;
- vero sulla base più quel solo difetto;
- vero in ogni caso che lo contiene e falso negli altri.

Se una di queste non vale, la costruzione si ferma. Le prime due versioni del banco sono state rifiutate così: un testimone cercava «private term» e lo trovava nella riga di riepilogo; i test dell'albero, lanciati con `-I`, non si importavano e risultavano rossi per ogni difetto; un difetto ne nascondeva un altro nel caso `L`.

Con `--profile` la chiave dice anche quali difetti sono già presi dai controlli del repository. Oggi: 6 su 15 (S1, S2, S3, M3, L4, U1). Gli altri 9 si trovano solo leggendo.

## I due modi

- **A, agente solo** (`protocol/single.md`): una sessione, la skill com'è.
- **B, coordinatore con agenti** (`protocol/coordinator.md`): agenti per dominio, verificatore indipendente sui 5 claim a rischio più alto, giro sulle categorie di errore, citazioni cercate nel file.

Uguali nei due modi: skill al commit di base, modello, effort, strumenti, profondità standard, solo ragionamento, formato del report.

### Modello ed effort (decisione dell'utente del 25 novembre 2026)

- **Modello:** Sonnet, ultima versione, per ogni agente lanciato: l'agente solo del modo A, il coordinatore e i suoi agenti nel modo B. In `runs.csv` va l'identificativo completo del modello che l'ambiente riporta, non il nome breve.
- **Effort:** medio. «Alto se necessario» non si decide esecuzione per esecuzione, perché il confronto fra i modi non reggerebbe: si decide una volta, sul caso `tuning`. Se lì un modo non arriva a un report completo nel formato della skill, l'effort sale ad alto per **tutti e due** i modi, prima delle esecuzioni che contano, e lo si scrive qui.
- **Un altro modello** è una serie di esecuzioni nuova, mai una riga in mezzo a questa.
- **Chi lancia non coordina.** La sessione che ha costruito il banco conosce la chiave delle risposte: lancia gli agenti e calcola il punteggio, ma il coordinatore del modo B è un agente lanciato, che della chiave non sa niente.

## Misure

| Misura | Da dove |
|---|---|
| Difetti noti trovati, solo ipotizzati, mancati | `score.py` |
| Citazioni non verificabili e con la riga sbagliata | `score.py` |
| Righe FAIL che non corrispondono a un difetto noto | `score.py` le elenca; una persona che non sa il modo le giudica |
| Token totali, contesto massimo del coordinatore (in A: dell'agente), tempo | l'ambiente che lancia le sessioni |
| Categorie di errore trovate rispetto a quelle della chiave | lettura del report, a mano |

`score.py` non decide i falsi positivi: il repository di base può avere difetti veri che la chiave non conosce.

## Criterio di decisione

Fissato prima della prima esecuzione che conta: N e le tre soglie sono confermati dall'utente il 25 novembre 2026. Da qui non si cambiano.

- **N = 3** esecuzioni per caso e per modo: 18 esecuzioni sui casi `S`, `M`, `L`.
- **Fare**, se valgono tutte:
  - B trova, sommando casi ed esecuzioni, almeno tanti difetti quanti A;
  - sul caso `L` il contesto massimo del coordinatore è al più il **70%** di quello dell'agente solo;
  - i token totali di B sono al più **2,5 volte** quelli di A;
  - citazioni non verificabili e falsi positivi di B non superano quelli di A.
- **Non fare**, se B trova meno difetti di A per più della differenza fra la migliore e la peggiore esecuzione di A, oppure ha più falsi positivi.
- **Rimandare** in ogni altro caso. Si riapre con più casi o più esecuzioni.

### Chi giudica le righe senza difetto noto

Un agente (decisione dell'utente del 25 novembre 2026), stesso modello ed effort degli altri. Riceve l'albero del caso e le righe FAIL che `score.py` non ha abbinato, mescolate fra i due modi e senza dire da quale vengono; non riceve la chiave. Per ogni riga risponde: difetto vero, non è un difetto, non si può dire, con la riga del file che lo mostra. Falso positivo è solo «non è un difetto».

## Limiti

- **Un solo repository, piccolo, in Python e Markdown.** Niente si può dire di altri linguaggi o di progetti grandi.
- **Il caso grande non è grande.** 178 kB possono non bastare a saturare un contesto: l'effetto della dimensione ha tre punti soli.
- **12 difetti nel punteggio, 3 esecuzioni.** Si leggono solo differenze nette.
- **Difetti inseriti a mano da chi ha scritto anche il banco**, quasi tutti di una riga. Nessun difetto di architettura; quelli fra più file sono i tre di documentazione e M2.
- **Alcuni commenti ora contraddicono il codice** (S2, M1, M4): aiutano chi verifica, in tutti e due i modi.
- **Gli alberi non hanno storia né diff.** Si misura la verifica di un perimetro, non di una modifica.
- **L'isolamento di un agente è un'istruzione, non una barriera.** Ogni agente lavora in una cartella sua e gli si dice di non leggere fuori; l'ambiente non lo impedisce, e sullo stesso disco c'è la chiave.
- **Le eval di `evals.json` non sono nel banco.** La #17 le chiede; vanno valutate alla cieca e sono un lavoro a parte.

## Come si lancia

Servono git, python3, rustc e node.

```bash
python3 spikes/17-agents/build.py --out /tmp/bench --profile   # alberi e chiavi; si ferma se un testimone non regge
python3 -m unittest discover -s spikes/17-agents -p 'test_score.py'
python3 spikes/17-agents/score.py --tree /tmp/bench/L --key /tmp/bench/keys/L.json report.md
```

Chi verifica riceve `/tmp/bench/<caso>` e la cartella della skill di `/tmp/bench/base`. Mai `/tmp/bench/keys`, mai questa cartella.

## Cosa manca per partire

1. Una prova sul caso `tuning`, nei due modi, per sapere tre cose che oggi non si sanno: se in questo ambiente un agente lanciato può lanciarne altri (serve al coordinatore), che cosa riporta l'ambiente su token e contesto di ogni agente, e se l'effort medio basta.
2. Mettere a punto il protocollo B sul caso `tuning` finché regge, poi non toccarlo più.
3. Le 18 esecuzioni che contano, poi il giudizio alla cieca.
