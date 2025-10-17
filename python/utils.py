#!/home/alves/edutech/venv/bin/python

import csv
import os
import sys

def obter_quantidade(nome_entidade, padrao):
    LIMITE_CATEGORIAS = 10 
    
    while True:
        try:
            if sys.stdin.isatty():
                prompt_limite = ""
                if nome_entidade == "categorias":
                    prompt_limite = f" (Máx: {LIMITE_CATEGORIAS})"
                entrada = input(f"Quantos {nome_entidade} deseja gerar (Padrão: {padrao}){prompt_limite}? ")
            else:
                return padrao 
            if not entrada:
                return padrao
            quantidade = int(entrada)
            if quantidade < 0:
                print("ERRO: A quantidade deve ser positiva. Usando o padrão.")
                return padrao
            if nome_entidade == "categorias" and quantidade > LIMITE_CATEGORIAS:
                print(f"ERRO: O catálogo só permite no máximo {LIMITE_CATEGORIAS} categorias. Usando {LIMITE_CATEGORIAS}.")
                return LIMITE_CATEGORIAS
            return quantidade
        except ValueError:
            print("ERRO: Entrada inválida. Por favor, digite um número inteiro.")
            continue

def exportar_para_csv(data, nome_arquivo):
    if not data:
        print(f"Alerta: Não há dados para exportar em {nome_arquivo}.")
        return
    fieldnames = list(data[0].keys())
    caminho_arquivo = f'./data/{nome_arquivo}.csv'
    try:
        with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"  -> Exportado: {len(data)} registros para {caminho_arquivo}")
    except Exception as e:
        print(f"ERRO ao exportar {nome_arquivo}: {e}")
