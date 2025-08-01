<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/5f8df403-76ce-44d1-b1ca-441a51dd657a" />

# BigaoDB

Este repositório contém duas versões de um banco de dados ultra-simples **BigaoDB**:

* **v1**: append-only em arquivo texto, lookup O(N).
* **v2**: daemon em Python com índice em memória, lookup O(1) em execução contínua.

---

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [BigaoDB v1](#bigaodb-v1)

   * [Uso v1](#uso-v1)
   * [Sample com poucos dados](#sample-pequeno)
4. [BigaoDB v2 (Daemon)](#bigaodb-v2-daemon)

   * [Iniciar o daemon](#iniciar-o-daemon)
   * [Cliente CLI](#cliente-cli)
   * [Sample com 50 milhões de registros](#sample-grande)
5. [Teste de performance](#teste-de-performance)

---

## Pré-requisitos

* Python 3.6+
* Linux (para socket Unix)
* `nc` (netcat) instalado para o cliente CLI
* `seq`, `awk` (para gerar samples em shell)

---

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/bigaodb.git
   cd bigaodb
   ```
2. Dê permissão de execução aos scripts:

   ```bash
   chmod +x bigaodb_v1.py bigaoDB_v2.py bigaodb_cli.sh
   ```

---

## BigaoDB v1

Versão básica que grava cada par `key,value` em append-only e faz lookup varrendo o arquivo.

### Uso v1

```bash
# Armazenar dados
./bigaodb_v1.py set nome Big
# Recuperar último valor de uma chave
./bigaodb_v1.py get nome
```

### Sample pequeno

Para criar um arquivo de testes com poucas linhas:

```bash
# 100 linhas, 10 chaves distintas
seq 100 | awk '{print "key"($1%10)",value"$1}' > bigaodb.db
```

Este arquivo tem 100 registros e 10 chaves distintas.

---

## BigaoDB v2 (Daemon)

Versão que mantém um índice em memória vivo, exposto via Unix socket, eliminando reloads e garantindo lookup O(1).

### Iniciar o daemon

```bash
# Inicia o daemon escutando em /tmp/bigaodb.sock
python3 bigaoDB_v2.py --db bigaodb.db --sock /tmp/bigaodb.sock
```

### Cliente CLI

Use o script cliente para enviar comandos ao daemon:

```bash
# No shell, sem necessidade de export
./bigaodb_cli.sh set usuario alice
./bigaodb_cli.sh get usuario     # → alice
```

O cliente usa por padrão `/tmp/bigaodb.sock`; para mudar, defina a variável `BIGAO_SOCK` antes:

```bash
export BIGAO_SOCK=/caminho/outro.sock
./bigaodb_cli.sh get usuario
```

### Sample grande (50 milhões)

Para gerar um arquivo `bigaodb.db` com 50M de registros:

```bash
# Usando seq + awk (rápido)
seq 50000000 | awk '{print "key"$1",value"$1}' > bigaodb.db
```

Ou, em Python:

```python
#!/usr/bin/env python3
DB = "bigaodb.db"
with open(DB, "w") as f:
    for i in range(1, 50000001):
        f.write(f"key{i},value{i}\n")
```

---

## Teste de performance

1. **Sample pequeno** (100 linhas):

   ```bash
   time ./bigaodb_v1.py get key5
   time ./bigaodb_cli.sh get key5
   ```
2. **Sample grande** (50 M linhas):

   ```bash
   time ./bigaodb_v1.py get key49999999  # vários segundos
   time ./bigaodb_cli.sh get key49999999 # milissegundos, sem reload
   ```

Compare os tempos para ilustrar o ganho de manter o daemon vivo com índice em RAM.

---

*BigaoDB — simples, didático e direto.*
