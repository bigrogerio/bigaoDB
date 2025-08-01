import argparse
import os
import pickle

DB_FILE = "bigaodb.db"

"""
Faça ISSO ANTES meus amigos:

Monte o ramdisk: 

    sudo mount -t tmpfs -o size=512M tmpfs /mnt/ramdisk

Exporte (se quiser)

    export BIGAO_RAMDISK=/mnt/ramdisk
"""

RAMDISK_DIR = os.environ.get("BIGAO_RAMDISK", "/mnt/ramdisk")
IDX_FILE = os.path.join(RAMDISK_DIR, os.path.basename(DB_FILE) + ".idx")

class BigaoDB:
    def __init__(self, path: str):
        self.path    = path
        self.idxpath = IDX_FILE
        self.index   = {}
        os.makedirs(os.path.dirname(self.idxpath), exist_ok=True)

        if self._is_index_fresh():
            self._load_index_from_disk()
        else:
            self._build_index()
            self._dump_index_to_disk()

    def _is_index_fresh(self) -> bool:
        try:
            return os.path.getmtime(self.idxpath) >= os.path.getmtime(self.path)
        except OSError:
            return False

    def _build_index(self):
        self.index.clear()
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                key, val = line.rstrip("\n").split(",", 1)
                self.index[key] = val

    def _dump_index_to_disk(self):
        with open(self.idxpath, "wb") as f:
            pickle.dump(self.index, f, protocol=pickle.HIGHEST_PROTOCOL)

    def _load_index_from_disk(self):
        with open(self.idxpath, "rb") as f:
            self.index = pickle.load(f)

    def set(self, key: str, value: str) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"{key},{value}\n")
        self.index[key] = value
        self._dump_index_to_disk()

    def get(self, key: str) -> str:
        return self.index.get(key, "")

def main():
    parser = argparse.ArgumentParser(
        prog="bigaodb",
        description="BigaoDB v3: índice em memória persistido em RAM-disk"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_set = sub.add_parser("set", help="armazena uma chave e valor")
    p_set.add_argument("key",   help="chave única")
    p_set.add_argument("value", help="valor a armazenar")

    p_get = sub.add_parser("get", help="recupera valor de uma chave")
    p_get.add_argument("key", help="chave a buscar")

    args = parser.parse_args()

    db = BigaoDB(DB_FILE)

    if args.cmd == "set":
        db.set(args.key, args.value)
    else:  
        print(db.get(args.key) + f"\n", end="")

if __name__ == "__main__":
    main()
