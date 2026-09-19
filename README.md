# ComfyUI SplitSteps + CSV-Seeder

Zwei ressourcenschonende Nodes fuer KSampler-Ketten (kein Step geht bei Primzahlen verloren).

## Nodes

### 1. Split Steps (2/3 KSampler)
Teilt `TOTAL` auf `start/end_at_step` auf. Alle KSampler bekommen `steps = total`.

Inputs:
- `total_steps` (INT), z.B. 12, 13, 17, 23
- `modus`: `2_sampler` oder `3_sampler` (Umschalter)
- `rest_nach`: `ende_groesser` oder `mitte_groesser` (wohin der Rest-Step bei Primzahlen faellt)
- `anteil_erster`: nur fuer `2_sampler`, Default `0.6667` (= 8+4 bei 12)

Outputs: `total`, `split1`, `split2`

Verdrahtung:
- 2er: `KS1: 0..split1`, `KS2: split1..total` (split2 = total, ignorieren)
- 3er: `KS1: 0..split1`, `KS2: split1..split2`, `KS3: split2..total`

Beispiele (`anteil_erster=0.6667`):
| TOTAL | 2er ende | 2er mitte | 3er ende (0-s1-s2-T) | 3er mitte |
|---|---|---|---|---|
| 12 | 8 (8+4) | 8 (8+4) | 4, 8 | 4, 8 |
| 13 | 8 (8+5) | 9 (9+4) | 4, 8 (4+4+5) | 4, 9 (4+5+4) |
| 17 | 11 (11+6) | 12 (12+5) | 5, 11 (5+6+6) | 5, 12 (5+7+5) |
| 23 | 15 (15+8) | 16 (16+7) | 7, 15 (7+8+8) | 7, 16 (7+9+7) |

### 2. CSV Seed Loader
Liest Seeds aus externer CSV (`seeds.csv`, eine Zahl pro Zeile oder Spalte `seed`).
Kopfzeilen, Leerzeilen, `#`-Kommentare werden ignoriert. Index per Modulo -> nie out-of-range.

Inputs: `csv_path`, `seed_index`, `modus` (`index_(modulo)` / `zufaellig`)
Outputs: `seed` (INT), `info` (STRING)

## Installation
Ordner nach `ComfyUI/custom_nodes/` kopieren (oder Repo dort clonen), ComfyUI neu starten.
Keine extra Abhaengigkeiten (nur Python-Standardlib).
