import math
import csv
import random
from pathlib import Path


class SplitSteps:
    """Teilt TOTAL Steps auf 2 oder 3 KSampler (start/end-Verkettung) auf.

    Alle KSampler bekommen steps=TOTAL. Nur start_at/end_at werden gesplittet,
    dadurch geht bei Primzahlen (13, 17, 23) kein Step verloren.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "total_steps": ("INT", {"default": 12, "min": 1, "max": 10000, "step": 1}),
                "modus": (["2_sampler", "3_sampler"], {"default": "3_sampler"}),
                "rest_nach": (["ende_groesser", "mitte_groesser"], {"default": "ende_groesser"}),
                "anteil_erster": ("FLOAT", {"default": 0.6667, "min": 0.05, "max": 0.95, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT")
    RETURN_NAMES = ("total", "split1", "split2")
    FUNCTION = "split"
    CATEGORY = "steps/split"

    def split(self, total_steps, modus, rest_nach, anteil_erster):
        total = int(total_steps)
        if total < 1:
            total = 1

        if modus == "2_sampler":
            f = total * float(anteil_erster)
            if rest_nach == "ende_groesser":
                s1 = math.floor(f)   # Ende bekommt den Rest
            else:
                s1 = math.ceil(f)    # Anfang/Mitte bekommt den Rest
            s1 = max(1, min(s1, total - 1)) if total >= 2 else 1
            s2 = total  # in 2er-Modus ungenutzt, liegt auf TOTAL
            return (total, int(s1), int(s2))

        # 3_sampler: fest 1/3 und 2/3, nur Rundung entscheidet
        if rest_nach == "ende_groesser":
            s1 = math.floor(total / 3.0)
            s2 = math.floor(2.0 * total / 3.0)
        else:  # mitte_groesser
            s1 = math.floor(total / 3.0)
            s2 = math.ceil(2.0 * total / 3.0)

        if total >= 3:
            s1 = max(1, min(s1, total - 2))
            s2 = max(s1 + 1, min(s2, total - 1))
        elif total == 2:
            s1, s2 = 1, 2
        else:
            s1, s2 = 1, 1
        return (total, int(s1), int(s2))


class CsvSeedLoader:
    """Liest Seeds aus einer externen CSV-Datei (eine Seed-Sammlung).

    CSV-Format: entweder mit Spalte 'seed' oder einfach eine Zahl pro Zeile.
    Kopfzeilen, Leerzeilen und #-Kommentare werden ignoriert.
    Der Index wird per Modulo umgebrochen -> primzahlsicher, nie out-of-range.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"multiline": False, "default": "seeds.csv"}),
                "seed_index": ("INT", {"default": 0, "min": 0, "max": 999999, "step": 1}),
                "modus": (["index_(modulo)", "zufaellig"], {"default": "index_(modulo)"}),
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("seed", "info")
    FUNCTION = "load"
    CATEGORY = "steps/seed"

    def _read_seeds(self, csv_path):
        p = Path(csv_path.strip())
        if not p.is_file():
            # Fallback: relativ zum Repo-/Node-Ordner suchen
            here = Path(__file__).resolve().parent / p.name
            if here.is_file():
                p = here
        if not p.is_file():
            return [], str(p)

        seeds = []
        with open(p, "r", newline="", encoding="utf-8-sig") as f:
            # Sniffer fuer Trennzeichen, fallback Komma
            sample = f.read(4096)
            f.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;|\t") if sample.strip() else csv.excel
            except Exception:
                dialect = csv.excel
            reader = csv.DictReader(f, dialect=dialect)
            # DictReader-Fall: Spalte seed vorhanden?
            if reader.fieldnames and any(h and h.strip().lower() in ("seed", "seeds", "value") for h in reader.fieldnames):
                key = next(h for h in reader.fieldnames if h and h.strip().lower() in ("seed", "seeds", "value"))
                for row in reader:
                    seeds.extend(self._extract_ints(row.get(key)))
            else:
                f.seek(0)
                for row in csv.reader(f, dialect):
                    for cell in row:
                        seeds.extend(self._extract_ints(cell))
        return seeds, str(p)

    @staticmethod
    def _extract_ints(cell):
        if cell is None:
            return []
        s = str(cell).strip()
        if not s or s.startswith("#"):
            return []
        # Header-Woerter ohne Ziffern ueberspringen
        if not any(ch.isdigit() for ch in s):
            return []
        try:
            return [int(float(s))]
        except ValueError:
            return []

    def load(self, csv_path, seed_index, modus):
        seeds, resolved = self._read_seeds(csv_path)
        if not seeds:
            info = f"CSV leer/nicht gefunden: {resolved} -> fallback seed 0"
            print(f"[CsvSeedLoader] {info}")
            return (0, info)
        n = len(seeds)
        if modus == "zufaellig":
            pick = random.randint(0, n - 1)
        else:
            pick = int(seed_index) % n
        seed = int(seeds[pick])
        info = f"{resolved} | index {int(seed_index)} -> [{pick}/{n}] seed {seed}"
        return (seed, info)


NODE_CLASS_MAPPINGS = {
    "SplitSteps": SplitSteps,
    "CsvSeedLoader": CsvSeedLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SplitSteps": "Split Steps (2/3 KSampler)",
    "CsvSeedLoader": "CSV Seed Loader",
}
