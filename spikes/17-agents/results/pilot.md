# Prova sul caso `tuning` (25 novembre 2026)

Una esecuzione per modo, lanciata come sotto-agente dalla sessione che ha costruito il banco. Sonnet (ultima versione), effort medio. Non entra nel punteggio.

## Cosa ha detto

1. **Un agente lanciato non può lanciarne altri**, in quell'ambiente: il coordinatore del modo B non aveva nessuno strumento per avviare agenti, l'ha scritto e si è fermato. Il modo B lì non si esegue.
2. **Un agente lanciato non scrive il suo report su file**: lo strumento di scrittura ha rifiutato («Subagents should return findings as text, not write report files»). Il report torna come testo alla sessione che ha lanciato, che deve ricopiarlo per darlo a `score.py`. Chi ricopia conosce la chiave.
3. **I token riportati non misurano il lavoro.** L'ambiente dà, per agente, token, chiamate a strumenti e durata; non il contesto massimo.

   | Agente | Token | Chiamate | Durata |
   |---|---|---|---|
   | Coordinatore B, fermo dopo aver letto 3 kB | 268 490 | 3 | 13 s |
   | Agente solo A, verifica completa di 84 kB | 286 994 | 12 | 469 s |

   Fra non fare niente e fare tutta la verifica c'è il 7%: il numero è quasi tutto costo fisso dell'ambiente. Le due soglie del criterio sui token e sul contesto lì non si possono valutare.
4. **L'effort medio basta** al modo A per un report completo, in tutte le sezioni.

## Punteggio del modo A

`score.py` sulla tabella FAIL ricopiata dal testo restituito:

- difetti noti trovati: **3 su 3** (U1, U2, U3), tutti per riga;
- righe FAIL: 21; senza difetto noto: 16, da giudicare;
- citazioni controllate: 20; alla riga indicata 12, riga sbagliata 3, non trovate 5. Diverse celle «Quote» descrivono invece di citare.

## Due difetti veri fuori dalla chiave

Riportati dall'agente e riprodotti sul repository vero (`main`, `cb75e4e`):

- `python3 scripts/check_facts.py --root .` fallisce su ogni file: con una radice relativa il percorso del file viene risolto due volte. Con una radice assoluta passa.
- `scripts/check.py` senza `.claude-plugin/plugin.json` termina con un traceback (`FileNotFoundError`) invece di un errore suo: i controlli dopo non girano.

Per questo le righe senza difetto noto non sono falsi positivi finché qualcuno non le giudica.

## Conseguenza

La serie che conta non si fa in quell'ambiente: il modo B non parte, i report vanno ricopiati a mano e token e contesto non si misurano. Si fa in locale con Claude Code, come scritto nella issue del progetto. Il modo F (`protocol/coordinator-flat.md`) resta scritto e non eseguito.
