# Esito dello spike #17 (26 novembre 2026)

**Non fare.** Il modo B, cioè un coordinatore con i suoi agenti, ha più falsi positivi del modo A, l'agente solo: 68 contro 13. Questo basta, da solo, a far scattare il «non fare» del criterio. Oltre a questo, B sta fuori anche dalle soglie su costo e contesto.

## Come sono state fatte le esecuzioni

- **Dove:** in locale con Claude Code 2.1.89, il 25 novembre 2026 dalle 21:16 alle 00:16, solo S-A-1 alle 11:56. Una esecuzione alla volta, alternando A e B.
- **Modello:** `claude-sonnet-5-5` a effort medio per ogni agente, sotto-agenti compresi. La skill è al commit `cb75e4e`.
- **Protocollo:** quello di B è `protocol/coordinator.md` al commit f502dd2, fermo dopo la messa a punto sul caso `tuning`.
- **Misure e punteggio:** le misure vengono da `measure.py`, i punteggi da `score.py`. Le righe FAIL senza un difetto noto le ha giudicate un agente per caso, alla cieca, come dice launcher.md al punto 7.
- **Esiti:** le 18 esecuzioni sono finite tutte con exit 0 e senza errori della sessione.

I dati sono in:
- `runs.csv`: una riga per esecuzione;
- `reports/<esecuzione>/`: report, punteggio, misure e, per B, il log del coordinatore;
- `judge/<caso>/`: le righe date al giudice, i suoi verdetti e la mappa da riga a esecuzione, che il giudice non ha visto.

## I numeri, per caso e per modo

Somme sulle tre esecuzioni. Contesto e tempo sono medie.

| Caso | Modo | Difetti noti trovati | Costo USD | Contesto max | Tempo (s) | Citazioni controllate | Riga sbagliata | Non verificabili | FAIL senza difetto noto | di cui veri | falsi positivi | non si può dire |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S | A | 12/12 | 2,84 | 111k | 345 | 50 | 5 | 8 | 21 | 15 | 4 | 2 |
| S | B | 8/12 | 9,55 | 114k | 690 | 134 | 0 | 4 | 74 | 41 | 31 | 2 |
| M | A | 24/24 | 3,81 | 136k | 472 | 92 | 10 | 3 | 47 | 36 | 8 | 3 |
| M | B | 24/24 | 12,12 | 138k | 852 | 148 | 0 | 3 | 98 | 74 | 19 | 5 |
| L | A | 34/36 | 3,66 | 152k | 376 | 82 | 2 | 16 | 28 | 27 | 1 | 0 |
| L | B | 36/36 | 16,86 | 161k | 915 | 199 | 1 | 4 | 104 | 83 | 18 | 3 |
| **Tutti** | **A** | **70/72** | **10,32** | | | 224 | 17 | **27** | 96 | 78 | **13** | 5 |
| **Tutti** | **B** | **68/72** | **38,53** | | | 481 | 1 | **11** | 276 | 198 | **68** | 10 |

## Il criterio del README, una condizione alla volta

**Fare**, se valgono tutte e quattro:

1. **B trova almeno tanti difetti quanti A.** B ne trova 68, A 70: non vale. I quattro difetti che mancano a B sono tutti di S-B-1 (vedi sotto).
2. **Sul caso `L` il contesto massimo del coordinatore è al più il 70% di quello dell'agente solo.** In media è 161 152 contro 151 595 token, cioè il **106%**: non vale.
3. **B costa al più 2,5 volte A.** B costa 38,53 USD, A 10,32 USD, cioè **3,73 volte**: non vale.
4. **Citazioni non verificabili e falsi positivi di B non superano quelli di A.** Le citazioni sono 11 contro 27, quindi su queste vale. I falsi positivi sono 68 contro 13: non vale.

**Non fare**, se B trova meno difetti di A per più della differenza fra la migliore e la peggiore esecuzione di A, *oppure* ha più falsi positivi. La seconda condizione vale: 68 contro 13. **Esito: non fare.**

La prima condizione dipende da come si legge «la migliore e la peggiore esecuzione di A»:
- **Sullo stesso caso:** la differenza è 2, su `L` (12 contro 10). B ne trova 2 in meno, quindi non è «più della differenza».
- **Fra casi diversi:** la differenza è 12 contro 4. Anche così B non sta sotto A di più di quella differenza.

In nessuna delle due letture questa condizione decide. L'esito viene dai falsi positivi.

## S-B-1

- **Cosa è successo:** il coordinatore ha scritto le tabelle FAIL senza la colonna `Fix` del formato della skill.
- **Come conta `score.py`:** riconosce una tabella FAIL da quella colonna, quindi in S-B-1 non legge nessuna riga FAIL. Trova solo S2 come comportamento nascosto e dà 0 difetti trovati su 4.
- **Cosa dice il report:** cita alcune delle righe dei difetti, per esempio `scripts/check.py:223` e la giunzione `SEP`.
- **Come è stata contata:** il README chiede lo stesso formato di report nei due modi. L'esecuzione resta col suo punteggio, per decisione dell'utente del 26 novembre 2026.
- **Effetto sull'esito:** nessuno. Anche contando S-B-1 come 4 su 4, B troverebbe 72 difetti contro i 70 di A, ma resterebbero fuori soglia il contesto, il costo e i falsi positivi.

## Cosa si vede oltre al criterio

Sono osservazioni, non entrano nell'esito.

- **B segnala molto di più:** 276 righe FAIL senza difetto noto contro 96. Il giudice ne considera vere 198 contro 78, e false 68 contro 13. B trova più difetti veri fuori dalla chiave, ma con una precisione più bassa: 72% delle righe giudicate vere contro 81%.
- **B cita meglio:** 1 riga sbagliata su 481 citazioni controllate, contro 17 su 224 per A. Le non verificabili sono 11 contro 27. È l'effetto della ricerca delle citazioni nel file che il coordinatore fa.
- **Il coordinatore non risparmia contesto.** Legge i ritorni degli agenti e cerca le citazioni nei file, e arriva allo stesso contesto dell'agente solo, anche un po' più su. A 177,7 kB il caso `L` non basta a riempire il contesto dell'agente solo: A trova 34 difetti noti su 36.
- **Tempo:** B impiega da 1,8 a 2,4 volte il tempo di A.
- **Difformità dichiarate dai coordinatori nel `log.md`:** i rinvii delle righe scartate sono andati ad agenti nuovi, perché un agente finito non si può riprendere. In S-B-1 le citazioni sono state cercate su una lettura del file fatta prima, non con una ricerca per ogni riga.

## Limiti del banco

- **Effetto soffitto:** l'agente solo trova già 70 difetti noti su 72. Sui difetti noti il banco non può mostrare che B ne trova di più. Il vantaggio di dividere il lavoro dovrebbe vedersi su perimetri più grandi di quelli che il banco ha.
- **Casi annidati:** S1-S4 stanno in tutti e tre i casi, quindi le 9 esecuzioni per modo non sono 9 prove indipendenti.
- **Un solo giudice per caso**, dello stesso modello degli agenti. Ha giudicato solo le righe senza difetto noto, e una per una: «non si può dire» ha preso 5 righe di A e 10 di B. Nessuna persona ha ricontrollato i verdetti.
- **Un solo protocollo multi-agente**, quello di `coordinator.md`. L'esito dice che questo protocollo non conviene, non che nessun protocollo multi-agente possa convenire.
- **Un solo modello e un solo effort.** Un altro modello sarebbe una serie nuova.
- **Il repository di base può avere difetti veri** che la chiave non conosce. Per questo il giudizio alla cieca ha contato solo i falsi positivi, non i difetti mancati fuori dalla chiave.
- **Costo della serie:** 48,85 USD per le 18 esecuzioni e 1,73 USD per i tre giudici, come lo riporta la sessione. Gira sull'abbonamento dell'utente.
