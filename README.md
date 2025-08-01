<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/5f8df403-76ce-44d1-b1ca-441a51dd657a" />

# BigaoDB

Este repositório contém duas versões de um banco de dados ultra-simples **BigaoDB**:

* **v1**: append-only em arquivo texto, lookup O(N).
* **v2**: versão com índice em memória persistido em RAM-disk, lookup O(1) após carga inicial.

---

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [BigaoDB v1](#bigaodb-v1)

   * [Uso v1](#uso-v1)
   * [Sample com poucos dados](#sample-pequeno)
4. [BigaoDB v2 (RAM-disk)](#bigaodb-v2-ram-disk)

   * [Montar RAM-disk](#montar-ram-disk)
   * [Uso v2](#uso-v2)
   * [Sample com 50 milhões de registros](#sample-grande)
5. [Teste de performance](#teste-de-performance)

---

## Pré-requisitos

* Python 3.6+
* Linux com suporte a tmpfs
* `seq`, `awk` (para geração em shell) ou Python para scripts alternativos

---

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/bigaodb.git
   cd bigaodb
   ```
2. Dê permissão de execução aos scripts:

   ```bash
   chmod +x bigaodb_v1.py bigaodb_v3.py
   ```

---

## BigaoDB v1

Versão básica que grava cada par `key,value` em append-only e faz lookup varrendo o arquivo.

### Uso v1

```bash
# Armazenar dados
./bigaodb_v1.py set nome Big
# Recuperar último valor de uma chave
echo "$(./bigaodb_v1.py get nome)"
```

### Sample pequeno

Para criar um arquivo de testes com poucas linhas:

```bash
# 100 linhas, 10 chaves distintas
seq 100 | awk '{print "key"($1%10)",value"$1}' > bigaodb.db
```

Este arquivo tem 100 registros e 10 chaves distintas.

---

## BigaoDB v2 (RAM-disk)

Versão avançada que constrói um índice em memória, serializa em disco **em RAM** e faz lookup O(1) nas execuções subsequentes.

### Montar RAM-disk

```bash
sudo mkdir -p /mnt/ramdisk
sudo mount -t tmpfs -o size=512M tmpfs /mnt/ramdisk
export BIGAO_RAMDISK=/mnt/ramdisk
```

> **Obs.**: ajuste `size=` conforme a memória disponível.

### Uso v2

```bash
# Primeira execução: build + dump em RAM
time ./bigaodb_v2.py get qualquerChave
# Chamadas seguintes: lookup via RAM-disk
time ./bigaodb_v2.py get qualquerChave
```

O arquivo de índice ficará em `/mnt/ramdisk/bigaodb.db.idx`.

### Sample grande (50 milhões)

Para gerar um arquivo `bigaodb.db` com 50M de registros:

```bash
# Usando seq + awk (muito rápido)
seq 50000000 | awk '{print "key"$1",value"$1}' > bigaodb.db
```

Ou, em Python (pode demorar alguns minutos):

```python
DB = "bigaodb.db"
with open(DB, "w") as f:
    for i in range(1, 50000001):
        f.write(f"key{i},value{i}\n")
```

Este arquivo ocupa \~1 GB e serve para demonstrar a diferença de performance entre v1 e v2.

---

*BigaoDB — simples, didático e direto.*
