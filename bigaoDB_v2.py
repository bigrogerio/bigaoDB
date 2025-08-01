import os
import socket
import threading
import argparse

DB_FILE   = "bigaodb.db"
SOCK_PATH = "/tmp/bigaodb.sock"

class BigaoDBServer:
    def __init__(self, db_file, sock_path):
        self.db_file   = db_file
        self.sock_path = sock_path
        self.index     = {}
        self._load_index()

    def _load_index(self):
        if not os.path.exists(self.db_file):
            return
        with open(self.db_file, "r", encoding="utf-8") as f:
            for line in f:
                key, val = line.rstrip("\n").split(",", 1)
                self.index[key] = val
        print(f"[daemon] Índice carregado: {len(self.index)} chaves")

    def _handle(self, conn):
        try:
            data = conn.recv(1024).decode().strip().split()
            cmd, *args = data
            if cmd.upper() == "SET" and len(args) == 2:
                key, val = args
                with open(self.db_file, "a", encoding="utf-8") as f:
                    f.write(f"{key},{val}\n")
                self.index[key] = val
                conn.send(b"OK")
            elif cmd.upper() == "GET" and len(args) == 1:
                val = self.index.get(args[0], "")
                conn.send(val.encode())
            else:
                conn.send(b"ERR")
        except Exception as e:
            conn.send(f"ERR {e}".encode())
        finally:
            conn.close()

    def serve_forever(self):
        if os.path.exists(self.sock_path):
            os.remove(self.sock_path)
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(self.sock_path)
        os.chmod(self.sock_path, 0o666)
        srv.listen()
        print(f"[daemon] Escutando em {self.sock_path}")
        try:
            while True:
                conn, _ = srv.accept()
                threading.Thread(target=self._handle, args=(conn,), daemon=True).start()
        finally:
            srv.close()
            os.remove(self.sock_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="bigaodb-daemon")
    parser.add_argument("--db",   default=DB_FILE,   help="arquivo de dados")
    parser.add_argument("--sock", default=SOCK_PATH, help="Unix socket path")
    args = parser.parse_args()

    daemon = BigaoDBServer(args.db, args.sock)
    daemon.serve_forever()
