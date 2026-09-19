# _PROJEKT-SplitSampler

Dein fester Platz fuer die 2er/3er-KSampler-Experimente. Nichts geht mehr verloren.

## Struktur
- `00_AKTUELL/` — nur die 1 Workflow-Datei, mit der du gerade arbeitest.
  Aktuell: `3 KSampler STUFE V.json`
- `01_TESTS/` — jede neue Idee als Kopie hier ablegen, nie das Original ueberschreiben.
- `02_ARCHIV/` — was laeuft, kommt hierher mit Datum im Namen, z.B. `2026-09-19_3KSampler-12steps-gut.json`.
- `seeds/seeds.csv` — deine Seed-Sammlung fuer den CSV Seed Loader.
- `NOTIZEN.md` — Ideen- und Aenderungs-Log (unten).

Gleiche Ordner gibt es auch unter `input/_PROJEKT-SplitSampler/` (Quellbilder)
und `output/_PROJEKT-SplitSampler/` (Ergebnisse).

## Regel (gegen Chaos)
1. Neue Idee? Workflow in `01_TESTS/` kopieren, dort aendern.
2. Ergebnis gut? Datei nach `02_ARCHIV/` mit Datum, `00_AKTUELL/` aktualisieren.
3. Jede Aenderung in 1 Zeile in NOTIZEN.md eintragen: Datum, was, Seed, Steps, Ergebnis.

## SplitNode-Verkabelung (Merkzettel)
- Alle KSampler: `steps = total` (Get TOTAL)
- 2er: `KS1: 0..split1`, `KS2: split1..total`
- 3er: `KS1: 0..split1`, `KS2: split1..split2`, `KS3: split2..total`
- `rest_nach`: `ende_groesser` (Rest ans Ende) oder `mitte_groesser` (Rest in die Mitte)
