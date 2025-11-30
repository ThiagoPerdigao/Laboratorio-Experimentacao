import csv
import time
import os
from rest_query import rest_request
from graphql_query import graphql_request

# Configurações
GRAPHQL_ENDPOINT = "https://api.github.com/graphql"
TOKEN = "TOKEN"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Cache-Control": "no-cache"
}

# Caminho correto para a pasta queries dentro de /code
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUERIES_DIR = os.path.join(BASE_DIR, "queries")

print(f"Buscando queries em: {QUERIES_DIR}")

# Verificação para evitar erros silenciosos
if not os.path.exists(QUERIES_DIR):
    raise FileNotFoundError(f"ERRO: A pasta 'queries' não foi encontrada em {QUERIES_DIR}")

# Carregar queries
graphql_simple = open(os.path.join(QUERIES_DIR, "graphql_simple.gql"), encoding="utf-8").read()
graphql_complex = open(os.path.join(QUERIES_DIR, "graphql_complex.gql"), encoding="utf-8").read()
rest_simple = open(os.path.join(QUERIES_DIR, "rest_simple.txt"), encoding="utf-8").read().strip()
rest_complex = open(os.path.join(QUERIES_DIR, "rest_complex.txt"), encoding="utf-8").read().strip()

def measure(api_type, scenario, function, *args):
    duration, size, status = function(*args)
    return {
        "api": api_type,
        "scenario": scenario,
        "duration_ms": duration,
        "size_bytes": size,
        "status": status,
        "timestamp": time.time()
    }

def run_experiment():
    results = []
    os.makedirs("results", exist_ok=True)

    for i in range(30):
        print(f"Rodando repetição {i+1}/30...")

        results.append(measure("REST", "simple", rest_request, rest_simple, HEADERS))
        results.append(measure("REST", "complex", rest_request, rest_complex, HEADERS))
        results.append(measure("GraphQL", "simple", graphql_request, GRAPHQL_ENDPOINT, graphql_simple, HEADERS))
        results.append(measure("GraphQL", "complex", graphql_request, GRAPHQL_ENDPOINT, graphql_complex, HEADERS))

    with open("results/measurements.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("Experimento finalizado!")

if __name__ == "__main__":
    run_experiment()
