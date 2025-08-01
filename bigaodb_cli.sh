#!/usr/bin/env bash
SOCK=${BIGAO_SOCK:-/tmp/bigaodb.sock}

cmd="$(echo "$1" | tr '[:lower:]' '[:upper:]')"
case "$cmd" in
  SET)
    # uso: bigaodb_cli.sh set chave valor
    printf "SET %s %s" "$2" "$3" | nc -U "$SOCK" ;;
  GET)
    # uso: bigaodb_cli.sh get chave
    printf "GET %s" "$2" | nc -U "$SOCK" ;;
  *)
    echo "Uso: $0 {get chave|set chave valor}" ;;
esac
