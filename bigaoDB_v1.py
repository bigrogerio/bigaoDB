import argparse
import os

DB_FILE = "bigaodb.db"

def db_set(key: str, value: str) -> None:
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{key},{value}\n")

def db_get(key: str) -> None:
    if not os.path.exists(DB_FILE):
        print("", end="")
        return

    result = ""
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            k, v = line.rstrip("\n").split(",", 1)
            if k == key:
                result = v
    print(result + f"\n", end="")

def main():
    parser = argparse.ArgumentParser(prog="bigaodb",
        description="BigaoDB: banco key→value em arquivo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_set = sub.add_parser("set", help="armazena uma chave e valor")
    p_set.add_argument("key", help="chave única")
    p_set.add_argument("value", help="valor a armazenar")

    p_get = sub.add_parser("get", help="recupera valor de uma chave")
    p_get.add_argument("key", help="chave a buscar")

    args = parser.parse_args()

    if args.cmd == "set":
        db_set(args.key, args.value)
    elif args.cmd == "get":
        db_get(args.key)

if __name__ == "__main__":
    main()
